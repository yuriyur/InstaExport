import urllib.request
import re
import os
import dropbox
import telebot
from telebot import apihelper
import configparser

def saveimagetodropbox(url, imgname):
    dbx = dropbox.Dropbox(dropbox_token)
    with open(imgname,'rb') as file:
        response = dbx.files_upload(file.read(), '/'+imgname)
        print(response)

def sendposttotelegram(url, imgname, caption):
    apihelper.proxy = proxy
    bot = telebot.TeleBot(telegram_token)
    bot.send_photo(telegram_id_chanel, open(imgname, 'rb'), caption=caption)
    print('Posted image: '+imgname)

def main(url):
    url = url+'?__a=1'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    graphql = response.read().decode('utf-8')

    data_images = re.findall('"display_url.*?(https://.*?)"', graphql)
    data_caption = re.findall("edge_media_to_caption\":{\"edges\":\[{\"node\":{\"text\":\".*?(.*?)\"", graphql)

    print('1 - post to telegram; 2 - save to dropbox;')
    tosave = int(input())
    i = 0
    while i < len(data_images):
        url = data_images[i]
        imgname = re.search("(\w+\.jpg)", url)
        data_caption[i] = bytes(data_caption[i], 'utf-8')
        caption = data_caption[i].decode("raw_unicode_escape").encode('utf-16', 'surrogatepass').decode('utf-16')
        if not os.path.isfile(imgname.group(0)):
            urllib.request.urlretrieve(url, imgname.group(0))
            if tosave==1:
                sendposttotelegram(url, imgname.group(0), caption)
            elif tosave==2:
                saveimagetodropbox(url, imgname.group(0))
            else:
                exit()
        i += 1

def crudConfig(path):
    config = configparser.ConfigParser()
    config.read(path)

    url = config.get("SETTINGS", "url")
    print('Parse url: '+url)

    global proxy
    global dropbox_token
    global telegram_token
    global telegram_id_chanel
    
    proxy = {}
    proxy['https'] = config.get("SETTINGS", "httpsproxy")
    print(proxy)

    dropbox_token = config.get("SETTINGS", "dropbox_token")
    telegram_token = config.get("SETTINGS", "telegram_token")
    telegram_id_chanel = config.get("SETTINGS", "telegram_id_chanel")
    folder_name = config.get("SETTINGS", "folder_name")

    if os.path.exists(folder_name):
        print('Folder to save: '+folder_name)
    else:
        print('Сreate folder')
        os.mkdir(str(folder_name))
    os.chdir(str(folder_name))

    main(url)

path = os.path.dirname(os.path.abspath(__file__))+'\\'+'config.ini'
print('Config file: '+path)
crudConfig(path)