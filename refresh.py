#coding:utf-8

'''
upload_info: 所有客户上传信息的字典，字典的key为每位玩家的id，对应的value为每位玩家的位置(经度,纬度)。
current_data: 服务器内储存的当前的所有玩家状态的字典，key为每位玩家的id，对应的value为一个字典，
            这个字典中的key为玩家的各种属性，value为各种属性的值。
'''


def refresh_states(upload_info,current_data):
    res = {}
    for uid in upload_info.keys():  #uid:每位玩家的id。
        res[uid] = {}
        res[uid]['blood'] = get_blood(uid,current_data)
        res[uid]['damage'] = get_damage(uid,current_data)
        res[uid]['vision_range'] = get_vision_range(uid,current_data)
        res[uid]['attack_range'] = get_atk_range(uid,current_data)
        res[uid]['small_item_location'] = get_s_location(uid,current_data)
        res[uid]['big_item_location'] = get_b_location(current_data)   #大物资每位玩家显示相同，因此不用玩家id。
        res[uid]['enemy_location'] = get_enemy_location(uid,current_data)
    return res
