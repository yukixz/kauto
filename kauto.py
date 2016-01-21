#!/usr/bin/env python3

import json
import random
import sys
import threading
from time import sleep
from http.server import HTTPServer, BaseHTTPRequestHandler

import pyautogui

from dfa import BaseDFA, BaseDFAStatus


################################################################
#
#  Utils
#
################################################################


class Point():
    x = -1
    y = -1

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point(%d, %d)" % (self.x, self.y)

    def click(self):
        try:
            pyautogui.click(self.x, self.y)
        except pyautogui.FailSafeException:
            print("!!", self)

    def moveTo(self):
        pyautogui.moveTo(self.x, self.y)


def random_point(a, b=None):
    if b is None:
        b = a
    x = config.base[0] + random.randint(a.x, b.x)
    y = config.base[1] + random.randint(a.y, b.y)
    return Point(x, y)


def random_sleep(min, max=None, step=1):
    ''' Wait for specified seconds.
        # User can use Control-C to break this wait
    '''
    if max is None:
        max = 1.1 * min
    seconds = random.uniform(min, max)
    # seconds = random.uniform(min, seconds)
    # if seconds > 2.5:
    #     print("sleep: %f" % seconds)
    sleep(seconds)
    # try:
    #     time.sleep(seconds)
    # except KeyboardInterrupt:
    #     pass


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
#  API Server
#
################################################################


class Request():
    path = None
    _body = None

    def __init__(self, path, body=None):
        self.path = path
        self.body = body

    def __str__(self):
        return '''Request(path="%s")''' % self.path

    @property
    def body(self):
        if type(self._body) is str:
            body = None
            try:
                body = json.loads(self._body)
                self._body = body
            finally:
                return body
        else:
            return self._body

    @body.setter
    def body(self, body):
        self._body = body


class APIServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # self.log_request()
        try:
            APIServer.REQUESTS_LOCK.acquire()
            APIServer.REQUESTS.append(Request(self.path))
        finally:
            APIServer.REQUESTS_LOCK.release()
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        # self.log_request()
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')
        try:
            APIServer.REQUESTS_LOCK.acquire()
            APIServer.REQUESTS.append(Request(self.path, body))
        finally:
            APIServer.REQUESTS_LOCK.release()
        self.send_response(200)
        self.end_headers()

    # override
    def send_response(self, code, message=None):
        """ Override to avoid log_request on each response
        """
        self.send_response_only(code, message)
        self.send_header('Server', self.version_string())
        self.send_header('Date', self.date_time_string())

    # override
    def log_request(self, message=''):
        self.log_message("%s %s - %s",
                         self.command, self.path, message)

    # override
    def log_message(self, format, *args):
        sys.stderr.write("[%s] %s\n" %
                         (self.log_date_time_string(),
                          format % args))


class APIServer():
    REQUESTS = []
    REQUESTS_LOCK = threading.Lock()

    def __init__(self):
        self.httpd = HTTPServer(config.host, APIServerHandler)
        self.threaded_httpd = threading.Thread(target=self.httpd.serve_forever)
        self.threaded_httpd.daemon = True
        self.threaded_httpd.start()
        print("Threaded API server listening on %s:%d" % config.host)

    def wait(self, path):
        ''' Wait for specified API request.
            User can use Control-C to break this wait
            @param  API path
            @return Request object
        '''
        if type(path) not in [list, tuple]:
            path = (path,)
        print("wait: %s" % path[0])

        request = None
        while True:
            if len(APIServer.REQUESTS) > 0:
                try:
                    APIServer.REQUESTS_LOCK.acquire()
                    request = APIServer.REQUESTS.pop(0)
                finally:
                    APIServer.REQUESTS_LOCK.release()
                if request.path in path:
                    break
            else:
                sleep(0.2)
        return request

    def empty(self):
        try:
            APIServer.REQUESTS_LOCK.acquire()
            del APIServer.REQUESTS[:]
        finally:
            APIServer.REQUESTS_LOCK.release()


################################################################
#
#  Game control
#
################################################################

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


################################################################
#
#  Automatic Script
#
################################################################

def auto_1_1_single():
    set_foremost()

    dock_back_to_port()

    port_open_panel_sortie()
    sortie_select(1, 1)
    sortie_confirm()

    combat_map_loading()
    combat_map_moving()
    combat_move_to_button_left()
    combat_result()

    combat_advance()
    combat_compass()
    combat_map_moving()
    combat_move_to_button_left()
    combat_result()

    wait("/kcsapi/api_get_member/useitem")
    random_sleep(1.6)
    port_open_panel_supply()
    supply_first_ship()


def auto_1_1():
    set_foremost()
    for i in range(3):
        print("!! auto 1-1 (%d)" % i)
        auto_1_1_single()


def auto_3_2():
    set_foremost()

    while True:
        request = dock_back_to_port()
        if port_has_damaged_ship(request):
            break

        port_open_panel_sortie()
        sortie_select(3, 2)
        sortie_confirm()

        combat_map_loading()
        combat_compass()
        combat_map_moving()
        combat_formation_double()

        combat_result()
        request = combat_retreat()

        port_open_panel_supply()
        supply_current_fleet()

        if port_has_damaged_ship(request):
            dock_open_panel_organize()
            break


def auto_battleresult():
    while True:
        combat_result()
        point = random_point(Point(400, 240))
        point.moveTo()


def auto_destroy_ship():
    set_foremost()
    while True:
        print("!! auto destroy ship")
        factory_destroy_select_first()
        factory_destroy_do_destory()
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

        # debug action
        if action == "show":
            for request in APIServer.REQUESTS:
                print(request)

        if action == "empty":
            server.empty()

        if action == "wait":
            server.empty()
            wait(None)

        try:
            func = ACTIONS.get(action)
            if callable(func):
                server.empty()
                func(*args)
        except KeyboardInterrupt:
            print()     # newline


if __name__ == '__main__':
    server = APIServer()
    wait = server.wait  # Export server.wait to globals

    run_auto()
