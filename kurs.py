from itertools import count
from pprint import pprint
from datetime import datetime
import configparser
import time
from urllib import response
from urllib.error import HTTPError
import requests
import json
import sys
import os
from tqdm import tqdm
# # URL = 'https://api.vk.com/method/users.get'
# # user_id = str(input('Введите user id:'))
# # params = {
# #     'user_ids': user_id ,
# #     'access_token': TOKEN_VK,
# #     'v':'5.131'
# # }
# res =requests.get(URL,params=params)
# pprint(res.json())

class YandexDisk:

    def __init__(self, token):
        self.token = token
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/'
    
    
    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
    # def get_files_list(self):
    #     files_url =self.url + 'files'
    #     headers = self.get_headers()
    #     response = requests.get(files_url,headers=headers)
    #     return response.json()

    def create_folder(self,path):

         url = "https://cloud-api.yandex.net/v1/disk/resources"

         headers = self.get_headers()
         response = requests.put(f'{url}?path={path}', headers=headers) 
         
        
    def upload_file_to_disk(self, url, path):
        upload_url = self.url + 'upload'
        headers = self.get_headers()
        params = {"url": url, "path": path}
        response = requests.post(upload_url, headers=headers, params=params)
        # response.raise_for_status()
        # if response.status_code == 201:
        #     print("Success")
        status = response.status_code
        if 400 > status:
            print('Фотографии загружены на: https://disk.yandex.ru/client/disk/kurs')
        else:
            print('Ошибка загрузки')



class VK:
    
    def __init__(self, token):
        self.token = token
        
    
    def upload_photo(self, id, albom_id = 'profile'):
        
        URL = 'https://api.vk.com/method/photos.get'
        params = {
                'owner_id': id,
                'access_token': TOKEN_VK,
                'album_id': albom_id,
                'extended': 1,
                'rev':0,
                'photo_sizes': 'height',
                'v':'5.131'
                 }
        res =requests.get(URL,params=params)
        # pprint(res.json())
        return res.json()
        
def make_sorted_list(dictionary:dict, num:int = 5) ->list :
    items = dictionary['response']['items']
    names = []
    for item in items:
        item['maxsize'] = -1
        for size in item['sizes']:
            if size['height'] > item['maxsize']:
                item['maxsize'] = size['height']
                item['url'] = size['url']
        if str(item['likes']['count']) in names :
            item['name']  = str(item['likes']['count'])+'_'+ str(item['date'])
        else:
            item['name']  =  str(item['likes']['count'])
        names.append(item['name'])
        del item['sizes']
    sorted_items = sorted(items, key=lambda d: d['maxsize'])
    
    result = items[:num] 
    return result
          
def log(lst):
    diction = {}
    date_str =str(datetime.now().strftime("%Y.%m.%d-%H.%M.%S"))
    diction[date_str] = lst
    with open("log_file.json", "a") as write_file:
         json.dump(diction, write_file,indent=4)
    return
def upload(lst):
    for item in tqdm(lst) :
        url = item['url']
        path ='kurs_photo' + '/'+ str(item['name']) + '.jpg'
        print(path)
        ya.upload_file_to_disk(url,path)
       
        



if __name__ == '__main__':
       

    config = configparser.ConfigParser()
    config.read("config.ini")
    TOKEN_VK=(config.get('VK','token'))
    TOKEN_YD=(config.get('YandexDisc','token'))


    user_input = str(input(
'''
Введите user id, если нужно введите через пробел количество фотографий ,
и, если хотите другой альбом, id этого альбома:
''')).split()
    user_id = user_input[0]
    albom_id = 'profile'
    if len(user_input) == 2 :
        albom_id = str(user_input[1])
    vk = VK(token = TOKEN_VK)
    dict =vk.upload_photo(user_id,albom_id)
    lst = make_sorted_list(dict)
    log(lst)
    ya = YandexDisk(token = TOKEN_YD )

    ya.create_folder('kurs_photo')
    upload(lst)










