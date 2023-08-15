import os,time,random
import shutil
code_srt = random.randint(1000000000000000000000000,9000000000000000000000000)
current_path=os.getcwd()

class CreateBot():

    def __init__(self, namebot):
        self.namebot_ = namebot
        global startapp
        global namebot_
        global startapp_edit
        global namebot_edit
        namebot_=self.namebot_
 



        #this is create startproject django for bot facebook
        creatbot = f"django-admin startproject {namebot_}"
        os.system(creatbot)
        namebot_edit="done create a project"   
        print(namebot_edit)
        time.sleep(2)
        #this is create startapp django for bot facebook
        startapp = str(namebot_ + "_")
        os.chdir(f"{namebot_}")
        creatbotapp = f"python manage.py startapp {startapp}"
        os.system(creatbotapp)
        startapp_edit="done create a app"   
        print(startapp_edit)
        time.sleep(2)
        os.chdir(os.path.join(current_path, namebot_,startapp))
        name_urls = "urls.py"
        with open(name_urls, 'w',encoding='utf-8') as files:
            files.write(
f'''
# yomamabot/fb_yomamabot/urls.py
from django.urls import re_path, include
from .views import YoMamaBotView
urlpatterns = [
    re_path(r'^page{code_srt}/?$', YoMamaBotView.as_view()) 
]
'''
            )
            files.close()

        os.chdir(os.path.join(current_path, namebot_, namebot_))
        files_urls = "urls.py"

        with open(files_urls, 'w',encoding='utf-8') as files:
            files.write(
f'''
from django.urls import re_path, include
from django.contrib import admin
urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^fb/', include('{startapp}.urls')),
]
'''
            )
            files.close()

    def event(self,ev):
        self.getevent=ev
        global getevent
        getevent=self.getevent



    def tokenFb(self, ACCESS_TOKEN, VERYFY_TOKEN):
        self.token = ACCESS_TOKEN
        self.keys = VERYFY_TOKEN
        global token
        global keys
        token=self.token
        keys=self.keys

    def getHost(self, host):
        self.hostname = host
        global hostname
        hostname=self.hostname
        file_path_setting =os.path.join(current_path, namebot_, namebot_)
        os.chdir(file_path_setting)
        name_setting = "settings.py"
        
        def replace_word_in_file(file_path, old_word, new_word):
            try:
                with open(file_path, 'r',encoding='utf-8') as file:
                    content = file.read()
    
                modified_content = content.replace(old_word, new_word)
    
                with open(file_path, 'w',encoding='utf-8') as file:
                    file.write(modified_content)
    
            except FileNotFoundError:
                print("error in this file try again")

        file_path = name_setting
        old_word = 'ALLOWED_HOSTS = []'
        new_word ='ALLOWED_HOSTS = ' + "['{}','localhost']".format(str(hostname))
        print('done add host')
        replace_word_in_file(file_path, old_word, new_word)
        file_path = name_setting
        old_word_app = '''
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]'''
        new_word_app = '''
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '{}',
]
'''.format(str(startapp))
        replace_word_in_file(file_path, old_word_app, new_word_app)



    def chatBot(self, talk,relkt,funsme):
        self.talking=talk
        talking = self.talking
        self.replying=relkt
        replying = self.replying
        
        self.funsing=funsme
        funsing = self.funsing
        os.chdir(os.path.join(current_path, namebot_, startapp))
        file_path_view = "views.py"
        with open(file_path_view, 'w', encoding='utf-8') as file_view:
            file_view.write('''

from django.shortcuts import render
from pprint import pprint
import json, requests, random, re
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
import time


ACCESS_TOKEN=
VERIFY_TOKEN=



start_event{}


def post_facebook_message(fbid, received_message):


    global talks_text

    if 'attachments' in received_message and received_message['attachments'][0]['type'] == 'image' and 'payload' in received_message['attachments'][0] and 'sticker_id' in received_message['attachments'][0]['payload']:
      
        reply = 'thanks for like'
        talks_text = reply
    elif 'attachments' in received_message and received_message['attachments'][0]['type'] == 'image':
        
        reply ='this image'#received_message['attachments'][0]['payload']['url']

        talks_text = reply   
    elif 'attachments' in received_message and received_message['attachments'][0]['type'] == 'video':
        reply ='this video'#received_message['attachments'][0]['payload']['url']
        talks_text = reply   
        
        
    elif 'text' in received_message:
        talks = received_message['text']
        reply = funme(talks)
        talks_text = reply
    else:
        talks_text = ""  # Default value if no match in cases

    post_message_url = f'https://graph.facebook.com/v2.6/me/messages?access_token={ACCESS_TOKEN}'
    response_msg = json.dumps({"message": {"text": talks_text}, "recipient": {"id": fbid}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())

class YoMamaBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(request.body.decode('utf-8'))

        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    pprint(message)

                    received_message = message['message']
                    sender_id = message['sender']['id']

                    post_facebook_message(sender_id, received_message)

        return HttpResponse()
''')
        file_view.close()

        def replace_word_in_file_view(file_path, old_word, new_word):
            try:
                with open(file_path, 'r',encoding='utf-8') as file:
                    content = file.read()
    
                modified_content = content.replace(old_word, new_word)
    
                with open(file_path, 'w',encoding='utf-8') as file:
                    file.write(modified_content)
    
            except FileNotFoundError:
                print("error in this file try again")
        
            #token
        file_path = file_path_view
        old_word_token = 'ACCESS_TOKEN='
        new_word_token ='ACCESS_TOKEN="{}"'.format(token)
        replace_word_in_file_view(file_path, old_word_token, new_word_token)


        #keys
        file_path = file_path_view
        old_word_keys = 'VERIFY_TOKEN='
        new_word_keys ='VERIFY_TOKEN="{}"'.format(keys)
        replace_word_in_file_view(file_path, old_word_keys, new_word_keys)



        #talk
        file_path = file_path_view
        old_word_talk = 'talks'
        new_word_talk =talking
        replace_word_in_file_view(file_path, old_word_talk, new_word_talk)

        file_path = file_path_view
        old_word_reply = 'reply'
        new_word_reply =replying
        replace_word_in_file_view(file_path, old_word_reply, new_word_reply)



        file_path = file_path_view
        old_word_event ='start_event{}'
        new_word_event =str(getevent)
        replace_word_in_file_view(file_path, old_word_event, new_word_event)
        
        
        file_path = file_path_view
        old_word_event ='funme'
        new_word_event =str(funsing)
        replace_word_in_file_view(file_path, old_word_event, new_word_event)
    def runbot(self):
        print(f"open this :https://{hostname}/fb/page{code_srt}")
        os.chdir(os.path.join(current_path, namebot_))
        os.system("python manage.py runserver")

class EditBot:
    def __init__(self, namebot):
        self.namebot_ = namebot
        global startapp
        global namebot_
        global startapp_edit
        global namebot_edit
        namebot_=self.namebot_

        name_bot=os.path.join(current_path, namebot_)
        if os.path.exists(name_bot):
            #if os.access(name_bot, os.W_OK):
            shutil.rmtree(name_bot)
            print("Editing")