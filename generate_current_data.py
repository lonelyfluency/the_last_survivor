'''
current_data 是一个保存所有玩家当前游戏状态的一个字典，其中的key和其对应的value为：
            player_location: 字典，key为玩家id，value为玩家位置。
            small_item_location: 列表，里面的元素为元组，格式为(种类,(经度，纬度))。
            big_item_location: 列表，里面的元素为元组，格式为(种类,(经度，纬度))。
            player_blood: 字典，key为玩家id，value为玩家血量。
            player_damage: 字典，key为玩家的id, value 为玩家攻击力。
            player_atk_range: 字典，key为玩家id，value为玩家攻击半径，单位是米。
            player_vision_range: 字典，key为玩家id，value为玩家真实视野半径，单位是米。
            player_visible: 字典，key为玩家id,value 为布尔值，1代表玩家可见，0代表不可见。
            safe_circle: 元组， ((经度,纬度),半径)
'''

import random


def generate_safe_circle():
    return (121.439286, 31.03061), 686


def generate_data(upload_info):
    res = {}

    res['player_location'] = {}
    for uid in upload_info.keys():
        res['player_location'][uid] = upload_info[uid]

    res['small_item_location'] = []


    res['big_item_location'] = []
    res['player_blood'] = {}
    res['player_damage'] = {}
    res['player_atk_range'] = {}
    res['player_vision_range'] = {}
    res['player_visible'] = {}
    res['safe_circle'] = generate_safe_circle()
