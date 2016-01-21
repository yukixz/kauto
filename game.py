#!/usr/bin/env python3

from api_server import api_server
from utils import Point, random_sleep, random_point, random_click

# Export api_server.wait to globals
wait = api_server.wait


def set_foremost():
    print("set_foremost")
    point = random_point(Point(500, 10), Point(500, 10))
    point.click()
    random_sleep(0.4)


# 母港：出撃
def port_open_panel_sortie():
    print("port_open_panel_sortie")
    point = random_point(Point(161, 235-22), Point(238, 320-22))
    point.click()
    random_sleep(1)
    point.click()
    wait("/kcsapi/api_get_member/mapinfo")
    random_sleep(1.2)   # 动画时间


# 母港：補給
def port_open_panel_supply():
    print("port_open_panel_supply")
    point = random_point(Point(48, 211-22), Point(102, 274-22))
    point.click()
    random_sleep(1.2)


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


# 补给：当前舰队
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


# 出击：1-*
def sortie_select_area_1():
    pass


# 出击：2-*
def sortie_select_area_2():
    raise NotImplementedError("sortie_select_area_2 is not implemented!")


# 出击：3-*
def sortie_select_area_3():
    point = random_point(Point(280, 447-22), Point(336, 480-22))
    point.click()


# 出击：4-*
def sortie_select_area_4():
    raise NotImplementedError("sortie_select_area_4 is not implemented!")


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
    wait("/kcsapi/api_req_map/start")
    random_sleep(1)     # 动画时间


# 战斗：罗盘娘
def combat_compass():
    print("combat_compass")
    point = random_point(Point(500, 400-22), Point(750, 450-22))
    point.click()
    random_sleep(4.2)   # 动画时间


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


def combat_button_left():
    point = random_point(Point(257, 247-22), Point(327, 289-22))
    point.click()


def combat_button_right():
    point = random_point(Point(473, 238-22), Point(551, 289-22))
    point.click()


def combat_move_to_button_left():
    point = random_point(Point(257, 247-22), Point(327, 289-22))
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
    wait("/kcsapi/api_req_map/next")
    random_sleep(2)     # 动画时间


# 撤退
def combat_retreat():
    print("combat_retreat")
    combat_button_right()
    request = wait("/kcsapi/api_port/port")
    wait("/kcsapi/api_get_member/useitem")
    random_sleep(1.2)   # 动画时间
    return request


# 战斗结果
def combat_result():
    print("combat_result")
    point = random_point(Point(500, 320), Point(750, 420))
    request = wait(['/kcsapi/api_req_sortie/battleresult',
                    '/kcsapi/api_req_combined_battle/battleresult',
                    '/kcsapi/api_req_practice/battle_result'])
    random_sleep(7.4)
    point.click()
    if "api_get_ship_exp" in request.body:
        random_sleep(5)
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
    random_sleep(2)


def combat_map_loading():
    print("combat_map_loading")
    random_sleep(3.6)


def combat_map_moving():
    print("combat_map_moving")
    random_sleep(6)
