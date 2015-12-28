#!/usr/bin/env python3

import random
import sys
import time

import pyautogui


class Point():
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point(%d, %d)" % (self.x, self.y)

    def __str__(self):
        return "%d,%d" % (self.x, self.y)

    def click(self):
        pyautogui.click(self.x, self.y)


base = Point(0, 23)


def random_point(a, b):
    x = base.x + random.randint(a.x, b.x)
    y = base.y + random.randint(a.y, b.y)
    return Point(x, y)


def random_sleep(min, max=None):
    if not max:
        max = 1.2 * min
    seconds = random.uniform(min, max)
    seconds = random.uniform(min, seconds)
    if seconds >= 1:
        print("  sleep %f" % seconds)
    time.sleep(seconds)


def set_foremost():
    print("set_foremost")
    point = random_point(Point(500, 10), Point(500, 10))
    point.click()
    random_sleep(0.4)


################################################################
# 港口界面（主界面）
##

# 出撃
def port_open_panel_sortie():
    print("port_open_panel_sortie")
    point = random_point(Point(161, 235), Point(238, 320))
    point.click()
    random_sleep(1)
    point.click()
    random_sleep(4)


# 補給
def port_open_panel_supply():
    print("port_open_panel_supply")
    point = random_point(Point(48, 211), Point(102, 274))
    point.click()
    random_sleep(2.4)     # 网络 IO + 界面动画


################################################################
# 船坞界面
##

# 編成
def dock_open_panel_organize():
    print("dock_open_panel_organize")
    point = random_point(Point(10, 157), Point(34, 188))
    point.click()


# 補給
def supply_current_fleet():
    print("supply_current_fleet")
    point = random_point(Point(116, 140), Point(124, 146))
    point.click()
    random_sleep(0.8)
    point = random_point(Point(662, 451), Point(746, 476))
    point.click()
    random_sleep(3)     # 网络 IO


################################################################
# 出击界面
##

# 出撃：1-*
def sortie_select_area_1():
    pass


# 出撃：2-*
def sortie_select_area_2():
    raise NotImplementedError("sortie_select_area_2 is not implemented!")


# 出撃：3-*
def sortie_select_area_3():
    point = random_point(Point(280, 447), Point(336, 480))
    point.click()


# 出撃：4-*
def sortie_select_area_4():
    raise NotImplementedError("sortie_select_area_4 is not implemented!")


# 出撃：*-1
def sortie_select_map_1():
    point = random_point(Point(139, 171), Point(421, 277))
    point.click()


# 出撃：*-2
def sortie_select_map_2():
    point = random_point(Point(464, 163), Point(659, 282))
    point.click()


# 出撃：*-3
def sortie_select_map_3():
    point = random_point(Point(138, 311), Point(425, 423))
    point.click()


# 出撃：*-4
def sortie_select_map_4():
    raise NotImplementedError("sortie_select_map_4 is not implemented!")


# 出撃：*-5
def sortie_select_map_5():
    point = random_point(Point(682, 236), Point(777, 290))
    point.click()
    random_sleep(0.8)
    point.click()


# 出撃：a-b
def sortie_select(area, map):
    print("sortie_select: %d-%d" % (area, map))
    select_area = globals()["sortie_select_area_%d" % area]
    select_map = globals()["sortie_select_map_%d" % map]
    if callable(select_area) and callable(select_map):
        select_area()
        random_sleep(0.8)
        select_map()
        random_sleep(0.8)


# 出撃：决定
def sortie_confirm():
    print("sortie_confirm")
    point = random_point(Point(638, 450), Point(712, 481))
    point.click()
    random_sleep(0.8)
    point.click()
    random_sleep(2)     # 网络 IO


################################################################
# 地图和战斗界面
##

def combat_compass():
    print("combat_compass")
    point = random_point(Point(500, 400), Point(750, 450))
    point.click()
    random_sleep(6)     # 罗盘动画时间


# 陣形：複縦陣
def combat_formation_double():
    print("combat_formation_double")
    point = random_point(Point(538, 200), Point(616, 216))
    point.click()


# 陣形：単横陣
def combat_formation_abreast():
    print("combat_formation_abreast")
    point = random_point(Point(607, 355), Point(685, 374))
    point.click()


def combat_button_left():
    point = random_point(Point(257, 247), Point(327, 289))
    point.click()


def combat_button_right():
    point = random_point(Point(473, 238), Point(551, 289))
    point.click()


# 追撃せず
def combat_no_night():
    print("combat_no_night")
    combat_button_left()
    random_sleep(10)     # 网络 IO + 战斗结果动画


# 夜戦突入
def combat_night():
    print("combat_night")
    combat_button_right()
    random_sleep(4)


# 進撃
def combat_advance():
    print("combat_advance")
    combat_button_left()
    random_sleep(4)


# 撤退
def combat_retreat():
    print("combat_retreat")
    combat_button_right()
    random_sleep(12)     # 网络 IO


################################################################
# 自动脚本
##

# 勝利
def combat_result():
    print("combat_result")
    point = random_point(Point(500, 350), Point(750, 450))
    point.click()   # 等级
    random_sleep(5)
    point.click()   # 获得物品/经验
    random_sleep(4)
    point.click()   # 获得舰船
    random_sleep(4)
    point.click()
    random_sleep(3)


def auto_1_1():
    set_foremost()

    port_open_panel_sortie()
    sortie_select(1, 1)
    sortie_confirm()

    random_sleep(12)    # 地图加载动画 + 地图移动动画
    random_sleep(20)    # 战斗动画
    combat_no_night()
    combat_result()

    combat_advance()
    combat_compass()
    random_sleep(6)     # 地图移动动画
    random_sleep(30)    # 战斗动画

    combat_no_night()
    combat_result()

    random_sleep(8)     # 网络 IO

    port_open_panel_supply()
    supply_current_fleet()


def auto_1_5():
    n = random.randint(4, 5)
    print(">> Sortie %d times" % n)
    for _ in range(n):
        set_foremost()

        port_open_panel_sortie()
        sortie_select(1, 5)
        sortie_confirm()

        random_sleep(14)    # 地图加载动画 + 地图移动动画
        combat_formation_abreast()
        random_sleep(40, 45)    # 战斗动画
        combat_result()
        combat_retreat()

        random_sleep(2, 4)

    port_open_panel_supply()
    supply_current_fleet()


def auto_3_2():
    set_foremost()

    port_open_panel_sortie()
    sortie_select(3, 2)
    sortie_confirm()

    random_sleep(6)     # 地图加载动画
    combat_compass()
    random_sleep(8)     # 动图移动动画
    combat_formation_double()

    random_sleep(80)    # 战斗动画

    combat_no_night()
    combat_result()
    combat_retreat()

    port_open_panel_supply()
    supply_current_fleet()
    dock_open_panel_organize()


def auto_3_3():
    set_foremost()

    port_open_panel_sortie()
    sortie_select(3, 3)
    sortie_confirm()

    random_sleep(7)     # 地图加载动画
    combat_compass()
    random_sleep(8)     # 动图移动动画
    combat_formation_double()

    random_sleep(80)    # 战斗动画

    combat_no_night()
    combat_result()
    combat_retreat()

    port_open_panel_supply()
    supply_current_fleet()
    dock_open_panel_organize()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit(0)
    if len(sys.argv) == 2 and sys.argv[1] == "1-1":
        auto_1_1()
    if len(sys.argv) == 2 and sys.argv[1] == "1-5":
        auto_1_5()
    if len(sys.argv) == 2 and sys.argv[1] == "3-2":
        auto_3_2()
    if len(sys.argv) == 2 and sys.argv[1] == "3-3":
        auto_3_3()
