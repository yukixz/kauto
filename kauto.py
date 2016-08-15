#!/usr/bin/env python3

import sys
import time
import traceback

import dfa
import game
import utils
import battle
from api_server import api_server
from dfa import Spot, BaseDFA, BaseDFAStatus
from utils import Point


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
    game.combat_battle(False)
    game.combat_result()

    game.combat_advance()
    game.combat_compass()
    game.combat_map_moving()
    game.combat_battle(False)
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
    MODE_NAME = {0: "不入夜",
                 1: "补给/轻航点入夜",
                 2: "BOSS点入夜",
                 3: "补给/轻航/BOSS点入夜"}

    def __init__(self, mode='1'):
        self.mode = int(mode)
        print("Mode: {} {}".format(self.mode, Auto23.MODE_NAME[self.mode]))
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
        if battle.port_has_damaged_ship(request):
            game.port_open_panel_organize()
            return None

        game.port_open_panel_sortie()
        game.sortie_select(2, 3)
        req_next = game.sortie_confirm()
        game.poi_switch_panel_prophet()
        game.combat_map_loading()

        self.cell_no = req_next.body["api_no"]
        return self.path_dict.get(self.cell_no, None)

    def should_night_battle(self):
        if self.mode == 0:
            return False
        if self.mode == 1:
            return self.cell_no in (3, 9, 10)
        if self.mode == 2:
            return self.cell_no in (11,)
        if self.mode == 3:
            return self.cell_no in (3, 9, 10, 11)

    def path_battle(self):
        game.combat_map_moving()
        request = game.combat_battle(self.should_night_battle())
        game.combat_result()
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
            if battle.advance_has_damaged_ship(req_ship_deck):
                game.poi_refresh_page()
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
        game.combat_battle(self.should_night_battle())
        game.combat_result()
        api_server.wait("/kcsapi/api_get_member/useitem")
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
        game.combat_summary()
        self.cell_no = 0
        return self.port

    def port(self):
        game.poi_switch_panel_main()

        utils.random_sleep(2)  # 动画时间
        game.port_open_panel_supply()
        game.supply_current_fleet()
        return None


def auto_3_2():
    game.set_foremost()

    while True:
        request = game.dock_back_to_port()
        if battle.port_has_damaged_ship(request):
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

        if battle.port_has_damaged_ship(request):
            game.dock_open_panel_organize()
            break


class Auto42(BaseDFA):
    # D --9 C --6 B --3 A
    #  \   12         10 \
    #  13 /           /   2
    #    H ---11 E ---     .
    #   8 \           \   1
    #  /   \           5 /
    # I     --7 G ----4 F

    def __init__(self):
        self.cell_no = 0
        self.path_dict = {
            0:  self.port,
            1:  self.path_compass_battle,
            2:  self.path_compass_battle,
            3:  self.path_compass_normal,
            4:  self.path_compass_normal,
            5:  self.path_compass_normal,
            6:  self.path_battle,
            7:  self.path_battle,
            8:  self.path_compass_final_battle,
            9:  self.path_compass_final_battle,
            10: self.path_compass_normal,
            11: self.path_battle,
            12: self.path_compass_battle,
            13: self.path_compass_final_battle
        }

    def start(self):
        game.set_foremost()

        request = game.dock_back_to_port()
        if battle.port_has_damaged_ship(request):
            game.port_open_panel_organize()
            return None

        game.port_open_panel_sortie()
        game.sortie_select(4, 2)
        req_next = game.sortie_confirm()
        game.poi_switch_panel_prophet()
        game.combat_map_loading()

        self.cell_no = req_next.body["api_no"]
        return self.path_dict.get(self.cell_no, None)

    def should_night_battle(self):
        if self.cell_no in (8, 9, 13):
            return True
        else:
            return False

    def path_battle(self):
        game.combat_map_moving()
        game.combat_formation_line()
        request = game.combat_battle(self.should_night_battle())
        game.combat_result()
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
            if battle.advance_has_damaged_ship(req_ship_deck):
                game.poi_refresh_page()
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
        game.combat_formation_line()
        game.combat_battle(self.should_night_battle())
        game.combat_result()
        api_server.wait("/kcsapi/api_get_member/useitem")
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
        game.combat_summary()
        self.cell_no = 0
        return self.port

    def port(self):
        game.poi_switch_panel_main()

        utils.random_sleep(2)  # 动画时间
        game.port_open_panel_supply()
        game.supply_current_fleet()
        return None


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


def auto_destroy():
    game.set_foremost()
    while True:
        print("!! auto destroy")
        game.factory_destroy_select_first()
        game.factory_destroy_do_destory()
        utils.random_sleep(0.4)


class AutoExpedition(BaseDFA):
    def __init__(self, run_hours=12):
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
        time.sleep(1)


def test_battle_analyze():
    # Assure current fleet is not combined.
    while True:
        request = api_server.wait([
            '/kcsapi/api_req_sortie/battle',
            '/kcsapi/api_req_sortie/airbattle',
            '/kcsapi/api_req_battle_midnight/battle',
            '/kcsapi/api_req_battle_midnight/sp_midnight',
            '/kcsapi/api_req_sortie/ld_airbattle'])
        battle.battle_analyze(request, 0, True)


class Auto15(dfa.AutoOnceMapDFA):
    def init_data(self):
        self.map_area = 1
        self.map_no = 5
        self.spot_list = {
            1:  Spot(self.spot_battle,
                     formation=game.combat_formation_abreast),
            2:  Spot(self.spot_battle,
                     formation=game.combat_formation_abreast),
            4:  Spot(self.spot_battle, compass=True,
                     formation=game.combat_formation_abreast),
            5:  Spot(self.spot_avoid, compass=True),
            10: Spot(self.spot_battle, compass=True, final=True,
                     formation=game.combat_formation_abreast,
                     enemy_animation=True),
        }


class Auto33(dfa.AutoOnceMapDFA):
    def init_data(self):
        self.map_area = 3
        self.map_no = 3
        self.spot_list = {
            1: Spot(self.spot_battle,
                    formation=game.combat_formation_line),
            2: Spot(self.spot_avoid, compass=True),
            3: Spot(self.spot_battle, compass=True,
                    formation=game.combat_formation_line),
            4: Spot(self.spot_avoid, compass=True),
            5: Spot(self.spot_battle),
            6: Spot(self.spot_avoid, compass=True),
            7: Spot(self.spot_battle_with_challenge, compass=True,
                    formation=game.combat_formation_line),
            8: Spot(self.spot_battle, final=True,
                    formation=game.combat_formation_line),
            9: Spot(self.spot_avoid, compass=True, final=True),
            10: Spot(self.spot_avoid, compass=True, final=True),
            11: Spot(self.spot_battle, final=True,
                     formation=game.combat_formation_line),
            12: Spot(self.spot_battle_with_challenge,
                     formation=game.combat_formation_line),
            13: Spot(self.spot_battle, compass=True, final=True,
                     formation=game.combat_formation_line)
            }
        self.safe_spot_list = [9, 10]

    def should_night_battle(self):
        return self.spot_no in (11, 13)


class Auto43(dfa.AutoOnceMapDFA):
    def init_data(self):
        self.map_area = 4
        self.map_no = 3
        self.spot_list = {
            1:  Spot(self.spot_battle, compass=True,
                     formation=game.combat_formation_line),
            4:  Spot(self.spot_battle, compass=True, enemy_animation=True,
                     formation=game.combat_formation_abreast),
            7:  Spot(self.spot_battle_with_challenge, compass=True,
                     enemy_animation=True,
                     formation=game.combat_formation_abreast),
            11: Spot(self.spot_avoid, compass=True, final=True),
            14: Spot(self.spot_battle, compass=True, enemy_animation=True,
                     formation=game.combat_formation_abreast),
            16: Spot(self.spot_battle, compass=True, enemy_animation=True,
                     formation=game.combat_formation_abreast),
            19: Spot(None, wrong_path=True)
        }
        self.safe_spot_list = [11]

    def should_retreat(self):
        return self.spot_no in (16,)


class Auto51(dfa.AutoOnceMapDFA):
    def init_data(self):
        self.map_area = 5
        self.map_no = 1
        self.spot_list = {
            1:  Spot(self.spot_avoid, compass=True),
            2:  Spot(None, wrong_path=True),
            3:  Spot(self.spot_battle, enemy_animation=True,
                     formation=game.combat_formation_abreast)
        }

    def should_retreat(self):
        return self.spot_no in (3,)


class Auto53(dfa.AutoOnceMapDFA):
    def init_data(self):
        self.map_area = 5
        self.map_no = 3
        self.spot_list = {
            1: Spot(self.spot_avoid),
            2: Spot(self.spot_battle, compass=True,
                    formation=game.combat_formation_line),
            3: Spot(self.spot_battle, compass=True,
                    formation=game.combat_formation_line),
        }

    def should_retreat(self):
        return self.spot_no in (2, )


class HelperE1(dfa.HelperMapDFA):
    # Path: B(2)-E(5)-F(12)-G(7)-I(9)
    def init_data(self):
        self.map_area = 35
        self.map_no = 1
        self.spot_list = {
            2:  Spot(self.spot_battle, compass=True, enemy_animation=True,
                     formation=game.combat_formation_abreast),
            5:  Spot(self.spot_battle, compass=True,
                     formation=game.combat_formation_line),
            12: Spot(self.spot_battle,
                     formation=game.combat_formation_abreast),
            7:  Spot(self.spot_battle,
                     formation=game.combat_formation_line),
            9:  Spot(self.spot_battle, compass=True, final=True,
                     formation=game.combat_formation_abreast,
                     enemy_animation=True, scout_plane=True, boss_dialog=True),
            }

    def should_night_battle(self):
        return False

    def should_retreat(self):
        return False


################################################################
#
#  Script control
#
################################################################

ACTIONS = {
    "11":   auto_1_1,
    "11s":  auto_1_1_single,
    "23":   Auto23,
    "32":   auto_3_2,
    "42":   Auto42,
    "54":   help_5_4,
    "d":    auto_destroy,
    "r":    help_battleresult,
    "e":    AutoExpedition,
    "mp":   current_mouse_position,
    "ba":   test_battle_analyze,
    "15":   Auto15,
    "33":   Auto33,
    "43":   Auto43,
    "51":   Auto51,
    "53":   Auto53,
    "e1":   HelperE1,
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
