#!/usr/bin/env python3

import sys
import time

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


def auto_battleresult():
    while True:
        game.combat_result()
        point = random_point(Point(400, 240))
        point.moveTo()


def auto_destroy_ship():
    game.set_foremost()
    while True:
        print("!! auto destroy ship")
        game.factory_destroy_select_first()
        game.factory_destroy_do_destory()
        random_sleep(0.4)


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
    "r":    auto_battleresult,
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
        except KeyboardInterrupt:
            print()     # newline


if __name__ == '__main__':
    run_auto()
