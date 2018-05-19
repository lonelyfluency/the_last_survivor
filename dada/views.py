from django.shortcuts import render
from django.http import HttpResponse
from logic import refresh, generate_current_data
import json
# Create your views here.

global current_data
global upload_info
global game_begin_cnt
current_data = {}
upload_info = {}
game_begin_cnt = 0


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

        current_data = generate_current_data.generate_data(upload_info)
        #print('game_begin_cnt: ', game_begin_cnt)
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
                'big_item': current_data['big_item_location']
            })
        )

def listen_response(request):
    global current_data
    global upload_info
    global game_begin_cnt
    if request.method == "GET":
        if game_begin_cnt == 4:
            game_begin_cnt = 0
            uid = request.GET.get('id')
            lat = request.GET.get('lati')
            lng = request.GET.get('longi')
            location = (lng, lat)
            print('id: ',uid)
            print('location: ',location)
            upload_info[uid] = location
            refresh.refresh_states(upload_info,current_data)
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