from pprint import pprint
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import json
from decouple import config


firebase_email=config('FIREBASE_EMAIL')
firebase_pw=config('FIREBASE_PW')

class Firebase:
    def __init__(self) -> None:
        with open('config.json', 'r') as f:
            config = json.loads(f.read())
        self.pyre = pyrebase.initialize_app(config)
        self.storage = self.pyre.storage()
        self.cred = credentials.Certificate('serviceAccountKey.json')
        self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.collection = 'stories'
        self.auth = self.pyre.auth()
        self.email = firebase_email
        self.pw = firebase_pw
        self.user = self.auth.sign_in_with_email_and_password(self.email, self.pw)
        self.token = self.user['idToken']
       
        
  

# This function will create the story in firestore
    def createStory(self, story):
        isSuccessful = False
        try:
            self.db.collection(self.collection).document(story['storyId']).set(story)
            isSuccessful = True
        except:
            # Should send alert that story could not be posted
            print('Failed, Check log.')
        return isSuccessful

    def addFilesToStorage(self, files, topic):
        clip_id = files[0].split('.')[0]
        self.storage.child('BotStories/{}/{}/{}'.format(topic,clip_id,files[0])).put(files[0])
        self.storage.child('BotStories/{}/{}/{}'.format(topic,clip_id,files[1])).put(files[1])
        return

    def getAudioClipURL(self, filename, topic, clip_id):
        token = self.token
        audioURL = self.storage.child(f'BotStories/{topic}/{clip_id}/{filename}').get_url(token)
        return audioURL
    
    def getImgURL(self,filename, topic, clip_id):
        token = self.token
        imageURL = self.storage.child(f'BotStories/{topic}/{clip_id}/{filename}').get_url(token)
        return imageURL
      
