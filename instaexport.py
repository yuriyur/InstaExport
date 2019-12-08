import urllib.request
import re
import os
import dropbox
import telebot

def saveimagetodisk(url, imgname):
    urllib.request.urlretrieve(url, imgname)

def saveimagetodropbox(url, imgname):
    dbx = dropbox.Dropbox(dropbox_token)
    urllib.request.urlretrieve(url, imgname)
    with open(imgname,'rb') as file:
        response = dbx.files_upload(file.read(), '/'+imgname)
        print(response)

def sendposttotelegram(url, imgname, caption):
    apihelper.proxy = proxy
    bot = telebot.TeleBot(telegram_token)

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