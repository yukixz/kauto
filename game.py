#!/usr/bin/env python3

'''
COPYRIGHT Dazzy Ding, Peter Zhang 2015-2016
'''

import math
import platform
import pyautogui

import config
from api_server import api_server
from utils import Point, random_sleep, random_point, random_click

# Export api_server.wait to globals
wait = api_server.wait


def set_foremost():
    print("set_foremost")
    point = random_point(Point(500, 10), Point(500, 10))
    point.click()
    random_sleep(0.4)


################################################################
#
#   Port
#
################################################################
# 出击
def port_open_main_sortie():
    print("port_open_main_sortie")
    point = random_point(Point(153, 250), Point(232, 335))
    point.click()
    random_sleep(1.3)

# 母港：出撃
def port_open_panel_sortie():
    random_sleep(2.1)
    port_open_main_sortie()
    point = random_point(Point(144, 175), Point(313, 335))
    point.click()
    wait("/kcsapi/api_get_member/mapinfo")
    random_sleep(2.5)   # 动画时间


# 母港：遠征
def port_open_panel_expedition():
    random_sleep(1)
    port_open_main_sortie()
    print("port_open_panel_expedition")
    random_click(Point(594, 170), Point(750, 340))
    wait("/kcsapi/api_get_member/mission")
    random_sleep(2.2)   # 动画时间


# 母港：補給
def port_open_panel_supply():
    random_sleep(2.2)
    print("port_open_panel_supply")
    point = random_point(Point(50, 230), Point(100, 280))
    point.click()
    random_sleep(2.2)


# 母港：编成
def port_open_panel_organize():
    print("port_open_panel_organize")
    point = random_point(Point(175, 135), Point(215, 190))
    point.click()
    random_sleep(1.2)


def port_expedition_back():
    print("port_expedition_back")
    point = random_point(Point(500, 320), Point(750, 420))
    point.click()
    request = wait("/kcsapi/api_port/port")
    wait("/kcsapi/api_get_member/useitem")
    random_sleep(9)
    point.click()
    random_sleep(1)
    point.click()
    random_sleep(2)
    return request


################################################################
#
#   Dock
#
################################################################


def dock_back_to_port():
    print("dock_back_to_port")
    random_sleep(1)
    point = random_point(Point(30, 35), Point(75, 70))
    point.click()
    request = wait("/kcsapi/api_port/port")
    return request


# 船坞：编成
def dock_open_panel_organize():
    print("dock_open_panel_organize")
    random_sleep(1.2)
    point = random_point(Point(10, 157-22), Point(34, 188-22))
    point.click()


################################################################
#
#   Dock: Supply
#
################################################################


def supply_select_fleet_1():
    pass


def supply_select_fleet_2():
    random_click(Point(170, 145), Point(180, 160))


def supply_select_fleet_3():
    random_click(Point(204, 145), Point(212, 160))


def supply_select_fleet_4():
    random_click(Point(234, 145), Point(242, 160))


def supply_select_fleet(i):
    print("supply_select_fleet", i)
    if not (1 <= i <= 4):
        raise ValueError()
    select_fleet = globals()["supply_select_fleet_%d" % i]
    if callable(select_fleet):
        random_sleep(1)
        select_fleet()
        random_sleep(1)
    else:
        raise NotImplementedError()


def supply_current_fleet():
    print("supply_current_fleet")
    point = random_point(Point(110, 145), Point(125, 160))
    point.click()
    wait("/kcsapi/api_req_hokyu/charge")
    random_sleep(1)   # 动画时间


def supply_first_ship():
    print("supply_first_ship")
    point = random_point(Point(175, 180), Point(300, 220))
    point.click()
    random_sleep(0.8)
    point = random_point(Point(660, 470), Point(748, 495))
    point.click()
    wait("/kcsapi/api_req_hokyu/charge")
    random_sleep(1)   # 动画时间


################################################################
#
#   Dock: Factory
#
################################################################


def factory_destroy_select_first():
    print("factory_destroy_select_first")
    point = random_point(Point(205, 128), Point(550, 144))
    point.click()
    random_sleep(0.6)


def factory_destroy_do_destory():
    print("factory_destroy_do_destory")
    point = random_point(Point(641, 420), Point(743, 452))
    point.click()
    random_sleep(4)
    wait(("/kcsapi/api_req_kousyou/destroyship",
          "/kcsapi/api_req_kousyou/destroyitem2"))


################################################################
#
#   Sortie
#
################################################################


# 出击：*-1
def sortie_select_map_1():
    point = random_point(Point(139, 178), Point(421, 277))
    point.click()


# 出击：*-2
def sortie_select_map_2():
    point = random_point(Point(464, 178), Point(659, 282))
    point.click()


# 出击：*-3
def sortie_select_map_3():
    point = random_point(Point(138, 321), Point(425, 423))
    point.click()


# 出击：*-4
def sortie_select_map_4():
    point = random_point(Point(463, 321), Point(682, 409))
    point.click()


# 出击：*-5
def sortie_select_map_5():
    point = random_point(Point(682, 286), Point(747, 330))
    point.click()
    random_sleep(1)
    point = random_point(Point(170, 180), Point(520, 260))
    point.click()


# 出击：1-*
def sortie_select_area_1():
    pass


# 出击：2-*
def sortie_select_area_2():
    point = random_point(Point(191, 474), Point(233, 495))
    point.click()


# 出击：3-*
def sortie_select_area_3():
    point = random_point(Point(256, 474), Point(296, 495))
    point.click()


# 出击：7-*
def sortie_select_area_7():
    point = random_point(Point(322, 474), Point(359, 495))
    point.click()


# 出击：4-*
def sortie_select_area_4():
    point = random_point(Point(383, 474), Point(425, 495))
    point.click()


# 出击：4-*
def sortie_select_area_5():
    point = random_point(Point(445, 474), Point(486, 495))
    point.click()


# 出击：EX-*
def sortie_select_area_ex():
    random_click(Point(670, 450-22), Point(750, 480-22))


# 出击：a-b
def sortie_select(area, map):
    print("sortie_select: %d-%d" % (area, map))
    if area > 30:
        area = 'ex'
    select_area = globals()["sortie_select_area_{}".format(area)]
    select_map = globals()["sortie_select_map_{}".format(map)]
    if callable(select_area) and callable(select_map):
        select_area()
        random_sleep(0.6)
        select_map()
        random_sleep(1)
    else:
        raise NotImplementedError()


# 出击：决定
def sortie_confirm():
    print("sortie_confirm")
    point = random_point(Point(593, 427), Point(768, 451))
    point.click()
    random_sleep(1.6)
    point = random_point(Point(534, 427), Point(694, 451))
    point.click()
    request = wait("/kcsapi/api_req_map/start")
    random_sleep(1)     # 动画时间
    return request


################################################################
#
#   Combat
#
################################################################


# 战斗：罗盘娘
def combat_compass():
    print("combat_compass")
    random_sleep(1.6)
    point = random_point(Point(500, 400-22), Point(750, 450-22))
    point.click()
    random_sleep(4.2)   # 动画时间


# 陣形：単縦陣
def combat_formation_line():
    print("combat_formation_line")
    point = random_point(Point(403, 200-22), Point(492, 216-22))
    point.click()


# 陣形：複縦陣
def combat_formation_double():
    print("combat_formation_double")
    point = random_point(Point(538, 200-22), Point(616, 216-22))
    point.click()


# 陣形：
def combat_formation_diamond():
    print("combat_formation_diamond")
    point = random_point(Point(667, 200-22), Point(755, 216-22))
    point.click()


# 陣形：単横陣
def combat_formation_abreast():
    print("combat_formation_abreast")
    point = random_point(Point(532, 332), Point(626, 348))
    point.click()


# 陣形：警戒陣
def combat_formation_alert():
    print("combat_formation_alert")
    point = random_point(Point(663, 332), Point(755, 348))
    point.click()




def combat_formation_combined_antisub():
    print("combat_formation_combined_antisub")
    random_click(Point(435, 187-22), Point(563, 208-22))


def combat_formation_combined_forward():
    print("combat_formation_combined_forward")
    random_click(Point(602, 187-22), Point(728, 208-22))


def combat_formation_combined_ring():
    print("combat_formation_combined_ring")
    random_click(Point(435, 324-22), Point(563, 345-22))


def combat_formation_combined_battle():
    print("combat_formation_combined_battle")
    random_click(Point(602, 324-22), Point(728, 345-22))


def combat_button_retreat_flagship_damaged():
    point = random_point(Point(535, 220), Point(605, 260))
    point.click()


def combat_button_left():
    point = random_point(Point(257, 247-22), Point(327, 289-22))
    point.click()


def combat_button_right():
    point = random_point(Point(473, 238-22), Point(551, 289-22))
    point.click()


def combat_move_to_button_left():
    point = random_point(Point(257, 247-22), Point(327, 289-22))
    point.moveTo()


def combat_move_to_button_right():
    point = random_point(Point(473, 238-22), Point(551, 289-22))
    point.moveTo()


# 追撃せず
def combat_no_night():
    print("combat_no_night")
    combat_button_left()
    random_sleep(2)


# 夜戦突入
def combat_night():
    print("combat_night")
    combat_button_right()   # TODO
    random_sleep(2)     # 动画时间


def combat_result():
    print("combat_result")
    request = wait(['/kcsapi/api_req_sortie/battleresult',
                    '/kcsapi/api_req_combined_battle/battleresult',
                    '/kcsapi/api_req_practice/battle_result'])
    point = random_point(Point(500, 320), Point(750, 420))
    random_sleep(7.6)
    point.click()
    if "api_get_ship_exp" in request.body:
        random_sleep(5.3)
        point.click()
    if "api_get_ship_exp_combined" in request.body:
        random_sleep(6.6)
        point.click()
    if "api_get_useitem" in request.body:
        random_sleep(7.6)   # 获得物品
        point.click()
    if "api_get_ship" in request.body:
        random_sleep(9.6)   # 获得舰船
        point.click()
    random_sleep(2)
    return request


# Battle of normal fleet and combined fleet.
# No pratice battle.
def combat_battle(night=False):
    print("combat_battle")
    day_battle = wait([
        '/kcsapi/api_req_sortie/battle',
        '/kcsapi/api_req_sortie/airbattle',
        '/kcsapi/api_req_sortie/ld_airbattle',
        '/kcsapi/api_req_battle_midnight/sp_midnight',
        '/kcsapi/api_req_combined_battle/battle',
        '/kcsapi/api_req_combined_battle/battle_water',
        '/kcsapi/api_req_combined_battle/airbattle',
        '/kcsapi/api_req_combined_battle/sp_midnight',
        '/kcsapi/api_req_practice/battle',
        ])
    if day_battle.body.get('api_midnight_flag', 0) == 0:
        wait([
            '/kcsapi/api_req_sortie/battleresult',
            '/kcsapi/api_req_combined_battle/battleresult',
            ], keep=True)
        return day_battle
    random_sleep(33)
    if night:
        while True:
            combat_night()
            night_battle = wait([
                '/kcsapi/api_req_battle_midnight/battle',
                '/kcsapi/api_req_combined_battle/midnight_battle',
                '/kcsapi/api_req_practice/midnight_battle',
                ], timeout=0)
            if night_battle:
                wait([
                    '/kcsapi/api_req_sortie/battleresult',
                    '/kcsapi/api_req_combined_battle/battleresult',
                    ], keep=True)
                return night_battle
            else:
                random_sleep(6, 10)
    else:
        while True:
            combat_no_night()
            request = wait([
                '/kcsapi/api_req_sortie/battleresult',
                '/kcsapi/api_req_combined_battle/battleresult',
                ], timeout=0, keep=True)
            if request:
                return day_battle
            else:
                random_sleep(8)


def combat_boss_dialog():
    print("combat_boss_dialog")
    request = wait([
        '/kcsapi/api_req_sortie/battle',
        '/kcsapi/api_req_sortie/airbattle',
        '/kcsapi/api_req_battle_midnight/sp_midnight',
        '/kcsapi/api_req_combined_battle/battle',
        '/kcsapi/api_req_combined_battle/battle_water',
        '/kcsapi/api_req_combined_battle/airbattle',
        '/kcsapi/api_req_combined_battle/sp_midnight',
        '/kcsapi/api_req_practice/battle',
        ], keep=True)
    point = random_point(Point(500, 320), Point(750, 420))
    random_sleep(4)
    point.click()
    return request


def combat_map_loading():
    print("combat_map_loading")
    random_sleep(5)


def combat_map_moving():
    print("combat_map_moving")
    random_sleep(7)


def combat_map_next():
    print("combat_map_next")
    request = wait("/kcsapi/api_req_map/next")
    random_sleep(1)     # 动画时间
    return request


def combat_map_scout_plane():
    print("combat_map_scout_plane")
    random_sleep(6)


# 進撃
def combat_advance():
    print("combat_advance")
    combat_button_left()
    req_ship_deck = wait("/kcsapi/api_get_member/ship_deck")
    req_next = wait("/kcsapi/api_req_map/next")
    random_sleep(1)     # 动画时间
    return req_ship_deck, req_next


# 撤退
def combat_retreat():
    print("combat_retreat")
    combat_button_right()
    request = wait("/kcsapi/api_port/port")
    wait("/kcsapi/api_get_member/useitem")
    random_sleep(1.2)   # 动画时间
    return request


# 撤退，旗艦大破
def combat_retreat_flagship_damaged():
    print("combat_retreat_flagship_damaged")
    random_sleep(4)
    combat_button_retreat_flagship_damaged()
    request = wait("/kcsapi/api_port/port")
    wait("/kcsapi/api_get_member/useitem")
    random_sleep(1.2)   # 动画时间
    return request


def combat_map_enemy_animation():
    print("combat_map_enemy_animation")
    random_sleep(2)


def combat_summary():
    print("combat_summary")
    random_sleep(2)
    combat_button_right()
    request = wait("/kcsapi/api_port/port")
    wait("/kcsapi/api_get_member/useitem")
    random_sleep(1.2)  # 动画时间
    return request


################################################################
#
#   Expedition
#
################################################################


def expedition_select_map_1():
    pass


def expedition_select_map_2():
    random_click(Point(158, 470), Point(187, 485))


def expedition_select_map_3():
    random_click(Point(197, 470), Point(228, 485))


def expedition_select_map_4():
    random_click(Point(281, 470), Point(311, 485))


def expedition_select_map_5():
    random_click(Point(322, 470), Point(353, 485))


def expedition_select_mission_1():
    random_click(Point(265, 195), Point(410, 220))


def expedition_select_mission_2():
    random_click(Point(265, 225), Point(410, 250))


def expedition_select_mission_3():
    random_click(Point(265, 255), Point(410, 280))


def expedition_select_mission_4():
    random_click(Point(265, 285), Point(410, 310))


def expedition_select_mission_5():
    random_click(Point(265, 315), Point(410, 340))


def expedition_select_mission_6():
    random_click(Point(265, 345), Point(410, 370))


def expedition_select_mission_7():
    random_click(Point(265, 375), Point(410, 400))


def expedition_select_mission_8():
    random_click(Point(265, 405), Point(410, 430))


def expedition_select_mission_scroll_up():
    random_click(Point(314, 180), Point(314, 180))
    random_sleep(0.5)


def expedition_select_mission_scroll_down():
    random_click(Point(314, 449), Point(314, 449))
    random_sleep(0.5)

def expedition_select_mission_X1():
    expedition_select_mission_scroll_down()
    expedition_select_mission_8()

def expedition_select_mission_X2():
    expedition_select_mission_scroll_down()
    expedition_select_mission_scroll_down()
    expedition_select_mission_8()

def expedition_select_mission_X3():
    expedition_select_mission_scroll_down()
    expedition_select_mission_scroll_down()
    expedition_select_mission_scroll_down()
    expedition_select_mission_8()

def expedition_convert_id_to_display(i):
    if (i >= 100):
        no = i % 10 + 1
        area = int(i / 10)
        return "{area:x}{no}".format(area=area, no=no).upper()

def expedition_select(i):
    print("expedition_select", i)
    if i >= 100:
        map = int(i / 10) % 10 + 1 # 100 -> 1 | 110 -> 2
        no = i % 10 + 1
        mission = "X{no}".format(no=no).upper()
    else:
        map = math.ceil(i / 8)
        mission = i % 8
        if mission == 0:
            mission = 8
    print(map, mission)
    select_map = globals()["expedition_select_map_{}".format(map)]
    select_mission = globals()["expedition_select_mission_{}".format(mission)]
    if callable(select_map) and callable(select_mission):
        select_map()
        random_sleep(0.6)
        select_mission()
        random_sleep(1)
    else:
        raise NotImplementedError()


def expedition_select_fleet_2():
    pass


def expedition_select_fleet_3():
    random_click(Point(418, 140), Point(428, 150))


def expedition_select_fleet_4():
    random_click(Point(448, 140), Point(460, 150))


def expedition_select_fleet(i):
    print("expedition_select_fleet", i)
    if not (2 <= i <= 4):
        raise ValueError()
    select_fleet = globals()["expedition_select_fleet_%d" % i]
    if callable(select_fleet):
        select_fleet()
        random_sleep(1)
    else:
        raise NotImplementedError()


def expedition_confirm_1():
    print("expedition_confirm_1")
    random_click(Point(642, 472), Point(685, 490))
    random_sleep(0.6)


def expedition_confirm_2():
    print("expedition_confirm_2")
    random_click(Point(579, 472), Point(685, 486))
    request = wait("/kcsapi/api_get_member/deck")
    random_sleep(5)
    return request


################################################################
#
#   POI Operation
#
################################################################

def poi_refresh_page():
    print("poi_refresh_page")
    point = Point(755, 495)
    point.click()
    random_sleep(0.4)

    system = platform.system()
    if system == "Windows":
        pyautogui.press('f5')
    if system == "Linux":
        pyautogui.hotkey('ctrl', 'r')
    if system == "Darwin":
        pyautogui.hotkey('command', 'r')


def poi_switch_panel_main():
    if not config.poi_interaction:
        return
    print("poi_switch_panel_main")
    pyautogui.hotkey('ctrl', '1')


def poi_switch_panel_prophet():
    if not config.poi_interaction:
        return
    print("poi_switch_panel_prophet")
    pyautogui.hotkey('ctrl', '3')
