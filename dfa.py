#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod
from enum import Enum

import battle
import game
import utils
from api_server import api_server


class BaseDFA(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        pass

    def run(self):
        status = self.start
        while True:
            # DFA End
            if status is None:
                break

            print("DFA", "=>", status.__name__)
            if callable(status):
                # DFA Status
                if issubclass(status, BaseDFAStatus):
                    status = status().do()
                # Raw function
                else:
                    status = status()
            # Unknown
            else:
                raise UnknownDFAStatusException()
                break


class BaseDFAStatus(metaclass=ABCMeta):
    @abstractmethod
    def do(self):
        pass


class UnknownDFAStatusException(Exception):
    pass


class Spot:
    def __init__(self, spot_type, wrong_path=False, compass=False, final=False,
                 enemy_animation=False, scout_plane=False, boss_dialog=False,
                 formation=None, click_next=None):
        # General
        self.spot_type = spot_type
        self.wrong_path = wrong_path
        self.compass = compass
        self.final = final
        # Battle
        self.enemy_animation = enemy_animation
        self.scout_plane = scout_plane
        self.boss_dialog = boss_dialog
        self.formation = formation
        # Select
        self.click_next = click_next


class BaseMapDFA(BaseDFA):
    def __init__(self):
        # Initial variables
        self.fleet_status = battle.BattleResult.Safe
        self.spot_no = 0

        # Control Flag
        self.auto_formation = True
        self.auto_night = True
        self.auto_advance = True

        # Variables to be defined
        self.fleet_combined = 0     # 0:通常, 1:機動, 2:水上, 3:輸送
        self.map_area = 0
        self.map_no = 0
        self.message = ""
        self.spot_list = {}         # = {spot_no : Spot(...), ...}
        self.safe_spot_list = []    # spot_battle_with_challenge需要

        self.init_data()
        print("Map {}-{} {}".format(self.map_area, self.map_no, self.message))

    @abstractmethod
    def init_data(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def end(self):
        pass

    def should_night_battle(self):
        return False

    def should_retreat(self):
        return False

    def spot_dispatcher(self):
        spot = self.spot_list.get(self.spot_no, None)
        if spot is None:
            return None
        if spot.wrong_path:
            self.spot_no = 0
            game.poi_refresh_page()
            return None
        if spot.compass:
            game.combat_compass()
        if spot.scout_plane:
            game.combat_map_scout_plane()
        if spot.enemy_animation:
            game.combat_map_enemy_animation()
        game.combat_map_moving()
        return spot.spot_type

    def spot_battle(self):
        spot = self.spot_list[self.spot_no]
        if self.auto_formation and spot.formation is not None:
            spot.formation()
        if spot.boss_dialog:
            game.combat_boss_dialog()

        if self.auto_night:
            battle_request = game.combat_battle(self.should_night_battle())
        else:
            battle_request = api_server.wait('/kcsapi/api_req_sortie/battle')

        self.fleet_status = battle.battle_analyze(
            battle_request, combined=self.fleet_combined)
        game.combat_result()
        if spot.final:
            api_server.wait("/kcsapi/api_get_member/useitem")
            self.spot_no = 0
            return self.end

        elif self.auto_advance:
            if self.should_retreat():
                game.combat_retreat()
                self.spot_no = 0
                return self.end

            if self.fleet_status == battle.BattleResult.Flagship_Damaged:
                game.combat_retreat_flagship_damaged()
                self.spot_no = 0
                return self.end

            if self.fleet_status == battle.BattleResult.Ship_Damaged:
                game.combat_retreat()
                self.spot_no = 0
                return self.end

            if self.fleet_status == battle.BattleResult.Safe:
                req_ship_deck, req_next = game.combat_advance()
                if battle.advance_has_damaged_ship(req_ship_deck):
                    self.fleet_status = battle.BattleResult.Ship_Damaged
                    game.poi_refresh_page()
                    raise Exception("BattleAnalyzeFailure")

                else:
                    self.spot_no = req_next.body["api_no"]
                    return self.spot_dispatcher

    def spot_battle_with_challenge(self):
        spot = self.spot_list[self.spot_no]
        if spot.enemy_animation:
            game.combat_map_enemy_animation()
        if self.auto_formation and spot.formation is not None:
            spot.formation()

        if self.auto_night:
            battle_request = game.combat_battle(self.should_night_battle())
        else:
            battle_request = api_server.wait('/kcsapi/api_req_sortie/battle')

        self.fleet_status = battle.battle_analyze(
            battle_request, combined=self.fleet_combined)
        game.combat_result()
        if spot.final:
            api_server.wait("/kcsapi/api_get_member/useitem")
            self.spot_no = 0
            return self.end

        elif self.auto_advance:
            if self.should_retreat():
                game.combat_retreat()
                self.spot_no = 0
                return self.end

            if self.fleet_status == battle.BattleResult.Flagship_Damaged:
                game.combat_retreat_flagship_damaged()
                self.spot_no = 0
                return self.end

            if self.fleet_status == battle.BattleResult.Ship_Damaged:
                req_ship_deck, req_next = game.combat_advance()
                self.spot_no = req_next.body["api_no"]
                if self.spot_no in self.safe_spot_list:
                    return self.spot_dispatcher
                else:
                    self.spot_no = 0
                    game.poi_refresh_page()
                    return None

            if self.fleet_status == battle.BattleResult.Safe:
                req_ship_deck, req_next = game.combat_advance()
                if battle.advance_has_damaged_ship(req_ship_deck):
                    self.fleet_status = battle.BattleResult.Ship_Damaged
                    game.poi_refresh_page()
                    raise Exception("BattleAnalyzeFailure")

                else:
                    self.spot_no = req_next.body["api_no"]
                    return self.spot_dispatcher

    def spot_avoid(self):
        spot = self.spot_list[self.spot_no]
        if spot.final:
            game.combat_summary()
            self.spot_no = 0
            return self.end
        else:
            req_next = game.combat_map_next()
            self.spot_no = req_next.body["api_no"]
            return self.spot_dispatcher

    def spot_select(self):
        spot = self.spot_list[self.spot_no]
        spot.click_next()
        req_next = game.combat_map_next()
        self.spot_no = req_next.body["api_no"]
        return self.spot_dispatcher


class HelperMapDFA(BaseMapDFA):
    def start(self):
        while True:
            request = api_server.wait(("/kcsapi/api_req_map/next",
                                       "/kcsapi/api_req_map/start",
                                       "/kcsapi/api_port/port"))
            if request.path == "/kcsapi/api_port/port":
                if battle.port_has_damaged_ship(request):
                    self.fleet_status = battle.BattleResult.Ship_Damaged
                else:
                    self.fleet_status = battle.BattleResult.Safe
                return self.start

            if request.path == "/kcsapi/api_req_map/start":
                if request.body['api_maparea_id'] != self.map_area or \
                   request.body['api_mapinfo_no'] != self.map_no or \
                   self.fleet_status != battle.BattleResult.Safe:
                    return None
                else:
                    self.spot_no = request.body["api_no"]
                    game.combat_map_loading()
                    return self.spot_dispatcher

            if request.path == "/kcsapi/api_req_map/next":
                if request.body['api_maparea_id'] != self.map_area or \
                   request.body['api_mapinfo_no'] != self.map_no:
                    return None
                else:
                    self.spot_no = request.body["api_no"]
                    return self.spot_dispatcher

    def end(self):
        return self.start


class AutoOnceMapDFA(BaseMapDFA):
    def start(self):
        game.set_foremost()

        request = game.dock_back_to_port()
        if battle.port_has_damaged_ship(request):
            game.port_open_panel_organize()
            return None

        game.port_open_panel_sortie()
        game.sortie_select(self.map_area, self.map_no)
        req_next = game.sortie_confirm()
        game.poi_switch_panel_prophet()
        game.combat_map_loading()

        self.spot_no = req_next.body["api_no"]
        return self.spot_dispatcher

    def end(self):
        game.poi_switch_panel_main()

        utils.random_sleep(2)  # 动画时间
        game.port_open_panel_supply()
        game.supply_current_fleet()
        return None
