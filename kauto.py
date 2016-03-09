#!/usr/bin/env python3

import sys
import time
import traceback
from datetime import datetime

import game
import utils
import battle
from api_server import api_server
from dfa import BaseDFA, BaseDFAStatus
from utils import Point, random_point, random_click
from battle import battle_analyze, battle_timer


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


def advance_has_damaged_ship(request):
    ''' Check whether there is damaged ship when advancing to next cell.
    '''
    ships = request.body['api_ship_data']
    for ship in ships:
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
    utils.random_sleep(1.6)
    game.port_open_panel_supply()
    game.supply_first_ship()


def auto_1_1():
    for i in range(1, 4):
        print("!! auto 1-1 (%d)" % i)
        auto_1_1_single()


class Auto23(BaseDFA):
    def __init__(self):
        self.cell_no = 0
        self.path_dict = {
            0:  self.port,
            1:  self.path_compass_battle,
            2:  self.path_compass_normal,
            3:  self.path_compass_battle,
            4:  self.path_compass_normal,
            5:  self.path_battle,
            6:  self.path_normal,
            7:  self.path_normal,
            8:  self.path_compass_final_normal,
            9:  self.path_compass_final_battle,
            10: self.path_compass_final_battle,
            11: self.path_compass_final_battle,
            12: self.path_normal
        }

    def start(self):
        game.set_foremost()

        request = game.dock_back_to_port()
        if port_has_damaged_ship(request):
            game.port_open_panel_organize()
            return None

        game.port_open_panel_sortie()
        game.sortie_select(2, 3)
        req_next = game.sortie_confirm()
        self.cell_no = req_next.body["api_no"]
        return self.path_dict.get(self.cell_no, None)

    def path_battle(self):
        game.combat_map_moving()
        request = game.combat_to_midnight()
        battle_result = battle.battle_analyze(request)

        if battle_result == battle.BattleResult.Flagship_Damaged:
            game.combat_retreat_flagship_damaged()
            self.cell_no = 0
            return self.port

        if battle_result == battle.BattleResult.Ship_Damaged:
            game.combat_retreat()
            self.cell_no = 0
            return self.port

        if battle_result == battle.BattleResult.Safe:
            req_ship_deck, req_next = game.combat_advance()
            if advance_has_damaged_ship(req_ship_deck):
                game.refresh_page()
                raise Exception("battle_analyze_failure")

            else:
                self.cell_no = req_next.body["api_no"]
                return self.path_dict.get(self.cell_no, None)

    def path_compass_battle(self):
        game.combat_compass()
        return self.path_battle()

    def path_compass_final_battle(self):
        game.combat_compass()
        game.combat_map_moving()
        game.combat_to_midnight()
        self.cell_no = 0
        return self.port

    def path_normal(self):
        game.combat_map_moving()
        req_next = game.combat_map_next()
        self.cell_no = req_next.body["api_no"]
        return self.path_dict.get(self.cell_no, None)

    def path_compass_normal(self):
        game.combat_compass()
        return self.path_normal()

    def path_compass_final_normal(self):
        game.combat_compass()
        game.combat_map_moving()
        game.combat_retreat()
        self.cell_no = 0
        return self.port

    def port(self):
        game.port_open_panel_supply()
        game.supply_current_fleet()
        game.dock_open_panel_organize()
        return None


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


def help_5_4():
    while True:
        request = api_server.wait(("/kcsapi/api_req_map/next",
                                   "/kcsapi/api_req_map/start"))

        # HS: c1d c7 12d c18 19d
        # SS: c2 4d 6n 9 c10d 15d

        if request.body["api_no"] in (1,):
            game.combat_map_loading()
            game.combat_compass()
            game.combat_map_moving()
            game.combat_formation_line()
            game.combat_move_to_button_left()
            game.combat_result()
            game.combat_move_to_button_left()

        if request.body["api_no"] in (2,):
            game.combat_map_loading()
            game.combat_compass()

        if request.body["api_no"] in (7, 18):
            utils.random_sleep(2)
            game.combat_compass()

        if request.body["api_no"] in (10,):
            game.combat_compass()
            game.combat_map_moving()
            game.combat_formation_line()
            game.combat_move_to_button_left()
            game.combat_result()
            game.combat_move_to_button_left()

        if request.body["api_no"] in (4, 6, 10, 12, 15, 19):
            game.combat_map_moving()
            game.combat_formation_line()
            game.combat_move_to_button_left()
            game.combat_result()
            game.combat_move_to_button_left()


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
        utils.random_sleep(0.4)


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
        utils.random_sleep(1)
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
        end = 2145888000    # 2038-01-01
        for t in self.exp_time:
            if t is not None and t < end:
                end = t
        utils.random_sleep_until(end - 50, end + 30, 60)

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


def current_mouse_position():
    while True:
        utils.mouse_position()
        utils.random_sleep(1)


def test_battle_analyze():
    # Assure current fleet is not combined.
    while True:
        battle_request = api_server.wait(['/kcsapi/api_req_sortie/battle', 
                                          '/kcsapi/api_req_sortie/airbattle', 
                                          '/kcsapi/api_req_battle_midnight/battle', 
                                          '/kcsapi/api_req_battle_midnight/sp_midnight', 
                                          '/kcsapi/api_req_sortie/ld_airbattle'])
        battle_analyze(battle_request, 0, True)



################################################################
#
#  Script control
#
################################################################

ACTIONS = {
    "11":   auto_1_1,
    "11s":  auto_1_1_single,
    "32":   auto_3_2,
    "54":   help_5_4,
    "d":    auto_destroy_ship,
    "r":    help_battleresult,
    "e":    AutoExpedition,
    "mp":   current_mouse_position,
    "tba":  test_battle_analyze
}


def run(action, args):
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
    cmds = sys.argv[1:]
    if len(cmds) > 0:
        action = cmds[0]
        args = cmds[1:]
        run(action, args)
        sys.exit(0)

    while True:
        try:
            cmd = input(">>> ")
        except KeyboardInterrupt:
            sys.exit(0)
        if len(cmd) > 0:
            cmds = cmd.split()
            action = cmds[0]
            args = cmds[1:]
        run(action, args)
