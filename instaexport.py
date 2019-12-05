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
    bot.send_photo(telegram_id_chanel, open(imgname, 'rb'), caption=caption)