'''
current_data 是一个保存所有玩家当前游戏状态的一个字典，其中的key和其对应的value为：
            player_location: 字典，key为玩家id，value为玩家位置。
            small_item_location: 列表，里面的元素为元组，格式为(种类,(经度，纬度))。
            big_item_location: 列表，里面的元素为元组，格式为(种类,(经度，纬度))。
            player_blood_limit: 字典，key为玩家id，value为血量上限。
            player_blood: 字典，key为玩家id，value为玩家血量。
            player_damage: 字典，key为玩家的id, value 为玩家攻击力。
            player_atk_range: 字典，key为玩家id，value为玩家攻击半径，单位是米。
            player_vision_range: 字典，key为玩家id，value为玩家真实视野半径，单位是米。
            player_visible: 字典，key为玩家id,value 为布尔值，1代表玩家可见，0代表不可见。
            player_enemy_location: 字典，key为玩家id，value为列表，内容为玩家真实视野内的敌人位置[(),(),(),()]。
            player_small_location: 字典，key为玩家id，value为列表，内容为玩家真实视野内的小物品位置[(),(),(),()]。
            safe_circle: 元组， ((经度,纬度),半径,等级)
            the_dead: 列表，里面是所有死亡玩家的id。
'''

import random
import time
from cor2distance import cor2dis


def generate_safe_circle():
    return (121.439286, 31.03061), 686, 1


def in_circle(pos, safe_circle):
    dis = cor2dis(pos, safe_circle[0])
    return dis < safe_circle[1]


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

