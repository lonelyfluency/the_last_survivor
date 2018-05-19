# coding:utf-8

'''
upload_info: 所有客户上传信息的字典，字典的key为每位玩家的id，对应的value为每位玩家的位置(经度,纬度)。
current_data: 服务器内储存的当前的所有玩家状态的字典，key为每位玩家的id，对应的value为一个字典，
            这个字典中的key为玩家的各种属性，value为各种属性的值。具体见generate_current_data 中的定义。
'''
import random
import time
from cor2distance import cor2dis


def in_circle(pos, safe_circle):
    dis = cor2dis(pos, safe_circle[0])
    return dis < safe_circle[1]


def add_health(add,health,limit):
    if add + health >= limit:
        return limit
    return add+health


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
                elif b_item[0] ==4:
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


# 显示物品列表
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

    current_data['safety_circle'][0][0] = current_data['safety_circle'][0][0] + random.randint(
                                                            -current_data['safety_circle'][1],
                                                            current_data['safety_circle'][1]) / 4 * 4.373E-6
    current_data['safety_circle'][0][1] = current_data['safety_circle'][0][0] + random.randint(
                                                            -current_data['safety_circle'][1],
                                                            current_data['safety_circle'][1]) / 4 * 8.192E-6
    current_data['safety_circle'][1] = current_data['safety_circle'][1] / 1.5
    current_data['safety_circle'][2] += 1


# 随机生成小物品
def get_small_item_location(safe_circle):
    res = []
    num_2_generate = 3.1416 * safe_circle[1]**2 / 2500
    cnt = 0
    random.seed = time.time()
    while cnt < num_2_generate:
        dlnt = random.randint(-safe_circle[1], safe_circle[1]) * 4.373E-6
        dlat = random.randint(-safe_circle[1], safe_circle[1]) * 8.192E-6
        pos = (dlnt, dlat)
        if in_circle(pos, safe_circle):
            s_type = random.randint(1, 4)
            res.append((s_type, pos))
            cnt += 1
    return res


# 随机生成大物品
def get_big_item_location(safe_circle):
    res = []
    num_2_generate = 3.1416 * safe_circle[1]**2 // 70000
    if num_2_generate < 1:
        num_2_generate = 1

    cnt = 0
    random.seed = time.time()
    while cnt < num_2_generate:
        dlnt = random.randint(-safe_circle[1], safe_circle[1]) * 4.373E-6
        dlat = random.randint(-safe_circle[1], safe_circle[1]) * 8.192E-6
        pos = (dlnt, dlat)
        if in_circle(pos, safe_circle):
            b_type = random.randint(1, 6)
            res.append((b_type, pos))
            cnt += 1
    return res


# 刷新物品，每五分钟刷新
def refresh_item(current_data):
    current_data['small_item_location'] = get_small_item_location(current_data['safe_circle'])
    current_data['big_item_location'] = get_big_item_location(current_data['safe_circle'])
