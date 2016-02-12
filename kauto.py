#!/usr/bin/env python3

import sys
import time
import traceback
from datetime import datetime

import game
from api_server import api_server
from dfa import BaseDFA, BaseDFAStatus
from utils import Point, random_sleep, random_point, random_click


################################################################
#
#  Utils
#
################################################################


def port_has_damaged_ship(request):
    ''' Check whether there is damaged ship when returning to port.
    '''
    deck0 = request.body['api_deck_port'][0]['api_ship']
    ships = request.body['api_ship']
    for ship_id in deck0:
        if ship_id < 0:
            continue
        ship = None
        for shipd in ships:
            if shipd.get('api_id', -1) == ship_id:
                ship = shipd
                break
        if ship is None:
            raise Exception("Cannot find ship with id: %d" % ship_id)
        if any(['api_nowhp' not in ship,
                'api_maxhp' not in ship,
                4 * ship['api_nowhp'] <= ship['api_maxhp']
                ]):
            print("!! WARNING: Damaged ship found!")
            return True
    return False


################################################################
#
#  Automatic Script
#
################################################################

def auto_1_1_single():
    game.set_foremost()

    game.dock_back_to_port()

    game.port_open_panel_sortie()
    game.sortie_select(1, 1)
    game.sortie_confirm()

    game.combat_map_loading()
    game.combat_map_moving()
    game.combat_move_to_button_left()
    game.combat_result()

    game.combat_advance()
    game.combat_compass()
    game.combat_map_moving()
    game.combat_move_to_button_left()
    game.combat_result()

    api_server.wait("/kcsapi/api_get_member/useitem")
    random_sleep(1.6)
    game.port_open_panel_supply()
    game.supply_first_ship()


def auto_1_1():
    for i in range(1, 4):
        print("!! auto 1-1 (%d)" % i)
        auto_1_1_single()


def auto_3_2():
    game.set_foremost()

    while True:
        request = game.dock_back_to_port()
        if port_has_damaged_ship(request):
            break

        game.port_open_panel_sortie()
        game.sortie_select(3, 2)
        game.sortie_confirm()

        game.combat_map_loading()
        game.combat_compass()
        game.combat_map_moving()
        game.combat_formation_double()

        game.combat_result()
        request = game.combat_retreat()

        game.port_open_panel_supply()
        game.supply_current_fleet()

        if port_has_damaged_ship(request):
            game.dock_open_panel_organize()
            break


def help_battleresult():
    while True:
        game.combat_result()
        point = Point(400, 240)
        point.moveTo()


def auto_destroy_ship():
    game.set_foremost()
    while True:
        print("!! auto destroy ship")
        game.factory_destroy_select_first()
        game.factory_destroy_do_destory()
        random_sleep(0.4)


class AutoExpedition(BaseDFA):
    def __init__(self, run_hours=4):
        # Timestamp of stoping running.
        run_hours = int(run_hours)
        self.stop_time = time.time() + run_hours * 3600
        print("Auto Expedition will run for %d hours." % run_hours)

        # Expedition No for fleet 2,3,4.
        self.exp_no = [None, None, None]
        # Expedition return time
        self.exp_time = [None, None, None]
        # Fleet status
        # 0 = ready
        # 1 = in expedition
        # 2 = need supply
        self.fleet_status = [None, None, None]

        # Argument: Passing port data.
        self.decks = None

    def start(self):
        request = api_server.wait("/kcsapi/api_port/port")
        self.decks = request.body["api_deck_port"]
        for deck in self.decks:
            i = deck["api_id"] - 2
            if i < 0:
                continue
            mission = deck["api_mission"]
            if mission[0] in (1, 2) and mission[1] > 0:
                self.exp_no[i] = mission[1]

        print("Expedition:", self.exp_no)
        random_sleep(1)
        return self.port

    def port(self):
        hasBack = hasSupply = hasDepart = False

        for deck in self.decks:
            i = deck["api_id"] - 2
            if i < 0:
                continue
            if self.exp_no[i] is not None:
                if deck["api_mission"][0] == 1:
                    self.fleet_status[i] = 1
                    self.exp_time[i] = deck["api_mission"][2] / 1000
                if deck["api_mission"][0] == 2:
                    hasBack = True
                    self.fleet_status[i] = 2
                    self.exp_time[i] = deck["api_mission"][2] / 1000

                if self.fleet_status[i] == 0:
                    hasDepart = True
                if self.fleet_status[i] == 2:
                    hasSupply = True

        if hasBack:
            return self.back
        if hasSupply:
            return self.supply
        if hasDepart:
            return self.depart
        else:
            return self.wait

    def wait(self):
        now = time.time()
        end = 2145888000    # 2038-01-01
        for t in self.exp_time:
            if t is not None and t < end:
                end = t
        wait_time = end - now

        if wait_time > 60:
            end_dt = datetime.fromtimestamp(end)
            print("sleep:", end_dt.strftime("%I:%M:%S %p"))
            # TODO: better sleep time
            random_sleep(wait_time - 30, wait_time + 30)

        if time.time() > self.stop_time:
            print("Reach running hours limit.")
            return None

        # Clear API server to avoid affect by player's action.
        api_server.empty()
        request = game.dock_back_to_port()
        self.decks = request.body["api_deck_port"]
        return self.port

    def back(self):
        ''' Take ONE fleet back.
        '''
        request = game.port_expedition_back()
        self.decks = request.body["api_deck_port"]
        return self.port

    def supply(self):
        ''' Supply all.
        '''
        game.port_open_panel_supply()
        for i in range(3):
            if self.exp_no[i] is not None and self.fleet_status[i] == 2:
                game.supply_select_fleet(i + 2)
                game.supply_current_fleet()
                self.fleet_status[i] = 0

        request = game.dock_back_to_port()
        self.decks = request.body["api_deck_port"]
        return self.port

    def depart(self):
        game.port_open_panel_expedition()
        for i in range(3):
            if self.exp_no[i] is not None and self.fleet_status[i] == 0:
                game.expedition_select(self.exp_no[i])
                game.expedition_confirm_1()
                game.expedition_select_fleet(i + 2)
                request = game.expedition_confirm_2()
                self.decks = request.body
        return self.port


def help_e2():
    while True:
        request = api_server.wait("/")

        if request.path == "/kcsapi/api_req_map/start":
            if request.body["api_no"] == 1:
                game.combat_map_loading()
                game.combat_map_moving()
                game.combat_map_enemy_animation()
                game.combat_formation_abreast()
                game.combat_move_to_button_left()
                game.combat_result()
                game.combat_move_to_button_left()

        if request.path == "/kcsapi/api_req_map/next":
            random_sleep(1.4)
            if request.body["api_no"] == 5:
                game.combat_compass()
                game.combat_map_moving()
                game.combat_map_enemy_animation()
                random_click(Point(353, 137-22), Point(366, 153-22))

            if request.body["api_no"] == 9:
                game.combat_map_moving()
                game.combat_formation_diamond()
                game.combat_move_to_button_left()
                game.combat_result()
                game.combat_move_to_button_left()

            if request.body["api_no"] == 18:
                game.combat_map_moving()
                game.combat_formation_line()
                game.combat_move_to_button_left()
                game.combat_result()
                game.combat_move_to_button_left()

            if request.body["api_no"] == 13:
                game.combat_map_moving()
                game.combat_formation_double()
                game.combat_move_to_button_left()
                game.combat_result()
                game.combat_move_to_button_left()

            if request.body["api_no"] == 15:
                game.combat_map_moving()
                game.combat_formation_line()
                game.combat_move_to_button_right()
                game.combat_result()


################################################################
#
#  Script control
#
################################################################

ACTIONS = {
    "11":   auto_1_1,
    "11s":  auto_1_1_single,
    "32":   auto_3_2,
    "d":    auto_destroy_ship,
    "r":    help_battleresult,
    "e":    AutoExpedition,
    "e2":   help_e2,
}


def run_auto():
    while True:
        try:
            cmd = input(">>> ")
        except KeyboardInterrupt:
            sys.exit(0)
        if len(cmd) > 0:
            cmds = cmd.split()
            action = cmds[0]
            args = cmds[1:]

        try:
            func = ACTIONS.get(action)
            if callable(func):
                api_server.empty()
                if issubclass(func, BaseDFA):
                    func(*args).run()
                else:
                    func(*args)
            else:
                print("Unknown command:", cmd)
        except KeyboardInterrupt:
            print()     # newline
        except:
            traceback.print_exc()


if __name__ == '__main__':
    run_auto()
