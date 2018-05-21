from django.http import HttpResponse
import random
import time
import json
from math import sin, atan, cos, radians, tan, acos
# Create your views here.

global current_data
global upload_info
global game_begin_cnt
global begin_status
current_data = {}
upload_info = {}
game_begin_cnt = 0
begin_status = 0


def calcDistance(Lat_A, Lng_A, Lat_B, Lng_B):
    ra = 6378.140
    rb = 6356.755
    flatten = (ra - rb) / ra
    rad_lat_A = radians(Lat_A)
    rad_lng_A = radians(Lng_A)
    rad_lat_B = radians(Lat_B)
    rad_lng_B = radians(Lng_B)
    pA = atan(rb / ra * tan(rad_lat_A))
    pB = atan(rb / ra * tan(rad_lat_B))
    xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
    c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
    c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (xx + dr)
    return distance*1000


def cor2dis(loc1, loc2):
    lat1 = float(loc1[1])
    lnt1 = float(loc1[0])
    lat2 = float(loc2[1])
    lnt2 = float(loc2[0])
    return calcDistance(lat1, lnt1, lat2, lnt2)


def generate_safe_circle():
    return [[121.439286, 31.03061], 686, 1]


def in_circle(pos, safe_circle):
    dis = cor2dis(pos, safe_circle[0])
    return dis < safe_circle[1]


def add_health(add,health,limit):
    if add + health >= limit:
        return limit
    return add+health


#种类有：
#1:增加5点攻击力,2：增加10点生命,3：增加5米的真实视野范围,4:增加5米的攻击范围。
def get_small_item_location(safe_circle):
    res = []
    num_2_generate = 3.1416 * safe_circle[1]**2 // 10000

    cnt = 0
    random.seed = time.time()
    while cnt < num_2_generate:
        dlnt = random.randint(-safe_circle[1], safe_circle[1]) * 4.373E-6
        dlat = random.randint(-safe_circle[1], safe_circle[1]) * 8.192E-6
        pos = (dlnt+safe_circle[0][0], dlat+safe_circle[0][1])

        if in_circle(pos, safe_circle):
            s_type = random.randint(1, 4)
            res.append((s_type, pos))
            cnt += 1
    return res


#种类有：
#1:增加15点攻击力,2：增加50点生命,3:增加20点生命上限，4：增加15米的真实视野范围,5：增加15米攻击范围，6：获得永久隐身效果。
def get_big_item_location(safe_circle):
    res = []
    num_2_generate = 3.1416 * safe_circle[1]**2 // 180000

    if num_2_generate < 1:
        num_2_generate = 1

    cnt = 0
    random.seed = time.time()
    while cnt < num_2_generate:
        dlnt = random.randint(-safe_circle[1], safe_circle[1]) * 4.373E-6
        dlat = random.randint(-safe_circle[1], safe_circle[1]) * 8.192E-6
        pos = (dlnt + safe_circle[0][0], dlat + safe_circle[0][1])
        if in_circle(pos, safe_circle):
            b_type = random.randint(1, 6)
            res.append((b_type, pos))
            cnt += 1
    return res


def generate_data(upload_info):
    res = {}

    res['safe_circle'] = generate_safe_circle()

    res['player_location'] = {}
    for uid in upload_info.keys():
        res['player_location'][uid] = upload_info[uid]

    res['small_item_location'] = get_small_item_location(res['safe_circle'])

    res['big_item_location'] = get_big_item_location(res['safe_circle'])

    res['player_blood_limit'] = {}
    for uid in upload_info.keys():
        res['player_blood_limit'][uid] = 100

    res['player_blood'] = {}
    for uid in upload_info.keys():
        res['player_blood'][uid] = 100

    res['player_damage'] = {}
    for uid in upload_info.keys():
        res['player_damage'][uid] = 10

    res['player_atk_range'] = {}
    for uid in upload_info.keys():
        res['player_atk_range'][uid] = 15

    res['player_vision_range'] = {}
    for uid in upload_info.keys():
        res['player_vision_range'][uid] = 30

    res['player_visible'] = {}
    for uid in upload_info.keys():
        res['player_visible'][uid] = 1

    res['player_enemy_location'] = {}
    for uid in upload_info.keys():
        res['player_enemy_location'][uid] = []

    res['player_small_location'] = {}
    for uid in upload_info.keys():
        res['player_small_location'][uid] = []

    res['the_dead'] = []

    return res



# 更新玩家位置信息
def refresh_player_locations(upload_info,current_data):
    for uid in upload_info.keys():
        current_data['player_location'][uid] = upload_info[uid]


# 更新大小物品信息,同时根据物品更新玩家属性。
def refresh_item_locations(current_data):
    for uid in current_data['player_location'].keys():
        # 小物品更新
        delhelper = []
        for s_item in current_data['small_item_location']:
            if cor2dis(s_item[1], current_data['player_location'][uid]) < 3:
                if s_item[0] == 1:
                    current_data['player_damage'][uid] += 5
                elif s_item[0] == 2:
                    current_data['player_blood'][uid] = add_health(10, current_data['player_blood'][uid],
                                                                   current_data['player_blood_limit'][uid])
                elif s_item[0] == 3:
                    current_data['player_vision_range'][uid] += 5
                else:
                    current_data['player_atk_range'][uid] += 5
                delhelper.append(s_item)

        for s_item in delhelper:
            current_data['small_item_location'].remove(s_item)

        # 大物品更新
        delhelper = []
        for b_item in current_data['big_item_location']:
            if cor2dis(b_item[1], current_data['player_location'][uid]) < 3:
                if b_item[0] == 1:
                    current_data['player_damage'][uid] += 15
                elif b_item[0] == 2:
                    current_data['player_blood'][uid] = add_health(50, current_data['player_blood'][uid],
                                                                   current_data['player_blood_limit'][uid])
                elif b_item[0] == 3:
                    current_data['player_blood_limit'][uid] += 20
                elif b_item[0] == 4:
                    current_data['player_vision_range'][uid] += 15
                elif b_item[0] == 5:
                    current_data['player_atk_range'][uid] += 15
                else:
                    current_data['player_visible'][uid] = 0
                delhelper.append(b_item)

        for b_item in delhelper:
            current_data['big_item_location'].remove(b_item)


# 显示敌人列表
def enemy_show(current_data):
    for uid in current_data['player_location'].keys():
        tmp = []
        for eid in current_data['player_location'].keys():
            if uid == eid:
                continue
            if cor2dis(current_data['player_location'][uid],
                       current_data['player_location'][eid]) < current_data['player_vision_range'][uid] and \
                    current_data['player_visible'][eid] == 1:
                tmp.append(current_data['player_location'][eid])
        current_data['player_enemy_location'][uid] = tmp


# 显示小物品列表
def small_item_show(current_data):
    for uid in current_data['player_location'].keys():
        tmp = []
        for loc in current_data['small_item_location']:
            if cor2dis(current_data['player_location'][uid],loc[1]) < current_data['player_vision_range'][uid]:
                tmp.append(loc)
        current_data['player_small_location'][uid] = tmp


# 伤害结算
def refresh_damage(current_data):
    #毒圈伤害
    for uid in current_data['player_location'].keys():
        if not in_circle(current_data['player_location'][uid],current_data['safe_circle']):
            current_data['player_blood'][uid] -= current_data['safe_circle'][2]

    # 敌人伤害
    for uid in current_data['player_location'].keys():
        for eid in current_data['player_location'].keys():
            if uid == eid:
                continue
            if cor2dis(current_data['player_location'][uid],
                       current_data['player_location'][eid]) < current_data['player_atk_range'][eid]:
                current_data['player_blood'][uid] -= current_data['player_damage'][eid]

    # 生死状态
    delhelp = []
    for uid in current_data['player_location'].keys():
        if current_data['player_blood'][uid] <= 0:
            current_data['the_dead'].append(uid)
            delhelp.append(uid)
    for uid in delhelp:
        current_data['player_location'].pop(uid)
        current_data['player_blood_limit'].pop(uid)
        current_data['player_blood'].pop(uid)
        current_data['player_damage'].pop(uid)
        current_data['player_atk_range'].pop(uid)
        current_data['player_vision_range'].pop(uid)
        current_data['player_visible'].pop(uid)
        current_data['player_enemy_location'].pop(uid)
        current_data['player_small_location'].pop(uid)


# 主要操作,每秒一刷新
def refresh_states(upload_info, current_data):
    refresh_player_locations(upload_info, current_data)
    refresh_item_locations(current_data)
    enemy_show(current_data)
    small_item_show(current_data)
    refresh_damage(current_data)


# 刷新毒圈，每5分钟刷新
def refresh_safety(current_data):
    random.seed = time.time()
    rd = 1 if random.random() > 0.5 else -1
    print(current_data['safe_circle'][0], current_data['safe_circle'][1], current_data['safe_circle'][2])
    current_data['safe_circle'][0][0] = current_data['safe_circle'][0][0] + float(current_data['safe_circle'][1]) * \
                                        random.random() * rd / 4 * 4.373E-6
    current_data['safe_circle'][0][1] = current_data['safe_circle'][0][1] + float(current_data['safe_circle'][1]) * \
                                        random.random() * rd / 4 * 8.192E-6
    print(current_data['safe_circle'][0][0], current_data['safe_circle'][0][1])
    current_data['safe_circle'][1] = float(current_data['safe_circle'][1]) / 1.5
    current_data['safe_circle'][2] += 1


# 刷新物品，每五分钟刷新
def refresh_item(current_data):
    current_data['small_item_location'] = get_small_item_location(current_data['safe_circle'])
    current_data['big_item_location'] = get_big_item_location(current_data['safe_circle'])


def initialize(request):
    global current_data
    global upload_info
    global game_begin_cnt
    if request.method == "GET":
        game_begin_cnt += 1
        uid = request.GET.get('id')
        lat = request.GET.get('lati')
        lng = request.GET.get('longi')
        location = (lng, lat)

        upload_info[uid] = location

        current_data = generate_data(upload_info)
        print('game_begin_cnt: ', game_begin_cnt)
        return HttpResponse(
            json.dumps({
                'id': uid,
                'blood': current_data['player_blood'][uid],
                'damage': current_data['player_damage'][uid],
                'blood_limit': current_data['player_blood_limit'][uid],
                'atk_range': current_data['player_atk_range'][uid],
                'vision_range': current_data['player_vision_range'],
                'visible': current_data['player_visible'][uid],
                'enemy': current_data['player_enemy_location'][uid],
                'small_item': current_data['player_small_location'],
                'big_item': current_data['big_item_location'],
                'begin_status': begin_status,
                'safe_circle_radius': current_data['safe_circle'][1],
                'safe_circle_center': current_data['safe_circle'][0]
            })
        )


def listen_response(request):
    global current_data
    global upload_info
    global game_begin_cnt
    global begin_status
    if request.method == "GET":
        if game_begin_cnt % 4 == 0:
            begin_status = 1
        else:
            begin_status = 0
        if begin_status == 1:
            uid = request.GET.get('id')
            lat = request.GET.get('lati')
            lng = request.GET.get('longi')
            location = (lng, lat)
            print('id: ',uid)
            print('location: ',location)
            upload_info[uid] = location
            refresh_states(upload_info,current_data)
            return HttpResponse(
                json.dumps({
                    'id' : uid,
                    'blood' : current_data['player_blood'][uid],
                    'damage' : current_data['player_damage'][uid],
                    'blood_limit' : current_data['player_blood_limit'][uid],
                    'atk_range' : current_data['player_atk_range'][uid],
                    'vision_range' : current_data['player_vision_range'],
                    'visible' : current_data['player_visible'][uid],
                    'enemy' : current_data['player_enemy_location'][uid],
                    'small_item' : current_data['player_small_location'],
                    'big_item' : current_data['big_item_location']
                })
            )
        else:
            return HttpResponse('Waiting other players...')


def refresh_circle(request):
    global current_data
    if request.method == "GET":
        if begin_status == 1:
            refresh_safety(current_data)
            print('safe_circle_refreshed.')
            return HttpResponse(
                json.dumps({
                'center': current_data['safe_circle'][0],
                'radius': current_data['safe_circle'][1]
            })
            )
        else:
            print('game_not_begin.')
            return HttpResponse(
                'game_not_begin.'
            )


def new_item(request):
    global current_data
    if request.method == "GET":
        if begin_status == 1:
            refresh_item(current_data)
            print('item_refreshed.')
            return HttpResponse('item_refreshed.')
        else:
            print('game_not_begin.')
            return HttpResponse('game_not_begin.')