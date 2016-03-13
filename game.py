#!/usr/bin/env python3

import math

from api_server import api_server
from utils import Point, random_sleep, random_point, random_click, hotkey_refresh, hotkey_switch_panel

# Export api_server.wait to globals
wait = api_server.wait


def set_foremost():
    print("set_foremost")
    point = random_point(Point(500, 10), Point(500, 10))
    point.click()
    random_sleep(0.4)


def refresh_page():
    print("refresh_page")
    point = Point(755, 495)
    point.click()
    random_sleep(0.4)
    hotkey_refresh()


################################################################
#
#   Port
#
################################################################


# 母港：出撃
def port_open_panel_sortie():
    print("port_open_panel_sortie")
    point = random_point(Point(161, 211), Point(238, 298))
    point.click()
    random_sleep(1)
    point.click()
    wait("/kcsapi/api_get_member/mapinfo")
    random_sleep(1.2)   # 动画时间


# 母港：遠征
def port_open_panel_expedition():
    print("port_open_panel_expedition")
    random_click(Point(161, 211), Point(238, 298))
    random_sleep(1)
    random_click(Point(594, 140), Point(765, 300))
    wait("/kcsapi/api_get_member/mission")
    random_sleep(1.2)   # 动画时间


# 母港：補給
def port_open_panel_supply():
    print("port_open_panel_supply")
    point = random_point(Point(48, 211-22), Point(102, 274-22))
    point.click()
    random_sleep(1.2)


# 母港：编成
def port_open_panel_organize():
    print("port_open_panel_supply")
    point = random_point(Point(175, 115), Point(215, 155))
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
    point = random_point(Point(30, 35), Point(75, 70))
    point.click()
    request = wait("/kcsapi/api_port/port")
    random_sleep(1)
    return request


# 船坞：编成
def dock_open_panel_organize():
    print("dock_open_panel_organize")
    point = random_point(Point(10, 157-22), Point(34, 188-22))
    point.click()
    random_sleep(1.2)


################################################################
#
#   Dock: Supply
#
################################################################


def supply_select_fleet_1():
    pass


def supply_select_fleet_2():
    random_click(Point(174, 114), Point(182, 124))


def supply_select_fleet_3():
    random_click(Point(204, 114), Point(212, 124))


def supply_select_fleet_4():
    random_click(Point(234, 114), Point(242, 124))


def supply_select_fleet(i):
    print("supply_select_fleet", i)
    if not (1 <= i <= 4):
        raise ValueError()
    select_fleet = globals()["supply_select_fleet_%d" % i]
    if callable(select_fleet):
        select_fleet()
        random_sleep(1)
    else:
        raise NotImplementedError()


def supply_current_fleet():
    print("supply_current_fleet")
    point = random_point(Point(118, 140-22), Point(124, 146-22))
    point.click()
    wait("/kcsapi/api_req_hokyu/charge")
    random_sleep(1)   # 动画时间


def supply_first_ship():
    print("supply_first_ship")
    point = random_point(Point(175, 150), Point(300, 180))
    point.click()
    random_sleep(0.8)
    point = random_point(Point(660, 430), Point(748, 455))
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
    wait("/kcsapi/api_req_kousyou/destroyship")


################################################################
#
#   Sortie
#
################################################################


# 出击：*-1
def sortie_select_map_1():
    point = random_point(Point(139, 171-22), Point(421, 277-22))
    point.click()


# 出击：*-2
def sortie_select_map_2():
    point = random_point(Point(464, 163-22), Point(659, 282-22))
    point.click()


# 出击：*-3
def sortie_select_map_3():
    point = random_point(Point(138, 311-22), Point(425, 423-22))
    point.click()


# 出击：*-4
def sortie_select_map_4():
    raise NotImplementedError("sortie_select_map_4 is not implemented!")


# 出击：*-5
def sortie_select_map_5():
    point = random_point(Point(682, 236-22), Point(777, 290-22))
    point.click()
    random_sleep(1)
    point.click()


# 出击：1-*
def sortie_select_area_1():
    pass


# 出击：2-*
def sortie_select_area_2():
    point = random_point(Point(215, 425), Point(250, 458))
    point.click()


# 出击：3-*
def sortie_select_area_3():
    point = random_point(Point(280, 447-22), Point(336, 480-22))
    point.click()


# 出击：4-*
def sortie_select_area_4():
    raise NotImplementedError("sortie_select_area_4 is not implemented!")


# 出击：EX-*
def sortie_select_area_ex():
    random_click(Point(670, 450-22), Point(750, 480-22))


# 出击：a-b
def sortie_select(area, map):
    print("sortie_select: %d-%d" % (area, map))
    select_area = globals()["sortie_select_area_%d" % area]
    select_map = globals()["sortie_select_map_%d" % map]
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
    point = random_point(Point(638, 450-22), Point(712, 481-22))
    point.click()
    random_sleep(0.6)
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
    random_sleep(1.6)   # 地图加载
    point = random_point(Point(500, 400-22), Point(750, 450-22))
    point.click()
    random_sleep(4.2)   # 动画时间


# 陣形：複縦陣
def combat_formation_line():
    print("combat_formation_line")
    point = random_point(Point(403, 200-22), Point(492, 216-22))
    point.click()


# 陣形：複縦陣
def combat_formation_double():
    print("combat_formation_double")
    point = random_point(Point(538, 200-22), Point(616, 216-22))
    point.click()


# 陣形：単横陣
def combat_formation_abreast():
    print("combat_formation_abreast")
    point = random_point(Point(607, 355-22), Point(685, 374-22))
    point.click()


# 陣形：
def combat_formation_diamond():
    print("combat_formation_diamond")
    point = random_point(Point(667, 200-22), Point(755, 216-22))
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


# 進撃
def combat_advance():
    print("combat_advance")
    combat_button_left()

    req_ship_deck = wait("/kcsapi/api_get_member/ship_deck")
    req_next = wait("/kcsapi/api_req_map/next")
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
    combat_button_retreat_flagship_damaged()
    request = wait("/kcsapi/api_port/port")
    wait("/kcsapi/api_get_member/useitem")
    random_sleep(1.2)   # 动画时间
    return request


# 战斗结果
def combat_result_operation(request):
    print("combat_result")
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
        random_sleep(7.6)   # 获得舰船
        point.click()
    random_sleep(1)


def combat_result():
    request = wait(['/kcsapi/api_req_sortie/battleresult',
                    '/kcsapi/api_req_combined_battle/battleresult',
                    '/kcsapi/api_req_practice/battle_result'])
    combat_result_operation(request)


def combat_to_midnight():
    print("combat_daytime")
    req_battle = wait('/kcsapi/api_req_sortie/battle')
    combat_move_to_button_left()
    request = wait(['/kcsapi/api_req_sortie/battleresult',
                    '/kcsapi/api_req_combined_battle/battleresult',
                    '/kcsapi/api_req_practice/battle_result',
                    '/kcsapi/api_req_battle_midnight/battle'])
    if request.path == '/kcsapi/api_req_battle_midnight/battle':
        print("combat_night")
        req_battle = request
        combat_result()
    elif request.path in ['/kcsapi/api_req_sortie/battleresult',
                          '/kcsapi/api_req_combined_battle/battleresult',
                          '/kcsapi/api_req_practice/battle_result']:
        combat_result_operation(request)
    else:
        raise NotImplementedError()
    return req_battle


def combat_map_loading():
    print("combat_map_loading")
    random_sleep(5)


def combat_map_moving():
    print("combat_map_moving")
    random_sleep(6)


def combat_map_next():
    print("combat_map_next")
    request = wait("/kcsapi/api_req_map/next")
    return request


def combat_map_enemy_animation():
    print("combat_map_enemy_animation")
    random_sleep(2)


################################################################
#
#   Expedition
#
################################################################


def expedition_select_map_1():
    random_click(Point(119, 422), Point(156, 450))


def expedition_select_map_2():
    random_click(Point(178, 422), Point(216, 450))


def expedition_select_map_3():
    random_click(Point(240, 422), Point(274, 450))


def expedition_select_map_4():
    random_click(Point(290, 422), Point(326, 450))


def expedition_select_map_5():
    random_click(Point(352, 422), Point(387, 450))


def expedition_select_mission_1():
    random_click(Point(265, 164), Point(410, 186))


def expedition_select_mission_2():
    random_click(Point(265, 193), Point(410, 215))


def expedition_select_mission_3():
    random_click(Point(265, 224), Point(410, 246))


def expedition_select_mission_4():
    random_click(Point(265, 253), Point(410, 275))


def expedition_select_mission_5():
    random_click(Point(265, 283), Point(410, 306))


def expedition_select_mission_6():
    random_click(Point(265, 313), Point(410, 336))


def expedition_select_mission_7():
    random_click(Point(265, 344), Point(410, 367))


def expedition_select_mission_8():
    random_click(Point(265, 373), Point(410, 396))


def expedition_select(i):
    print("expedition_select", i)
    map = math.ceil(i / 8)
    mission = i % 8
    select_map = globals()["expedition_select_map_%d" % map]
    select_mission = globals()["expedition_select_mission_%d" % mission]
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
    random_click(Point(418, 112), Point(428, 124))


def expedition_select_fleet_4():
    random_click(Point(448, 112), Point(460, 124))


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
    random_click(Point(642, 432), Point(712, 456))
    random_sleep(0.6)


def expedition_confirm_2():
    print("expedition_confirm_2")
    random_click(Point(579, 432), Point(694, 456))
    request = wait("/kcsapi/api_get_member/deck")
    random_sleep(5)
    return request


################################################################
#
#   POI Operation
#
################################################################
def poi_switch_panel_main():
    hotkey_switch_panel('1')


def poi_switch_panel_prophet():
    hotkey_switch_panel('3')
