from datetime import datetime
import json
from database import Database
from firebase_ import Firebase
from bot import Bot
import smtplib
import schedule
from email.message import EmailMessage
from decouple import config
import random
import logging

logging.basicConfig(filename='bot.log',level=logging.DEBUG, format='%(acstime)s:%(levelname)s:%(message)s')

rhillx=config('TO_RHILLX')
rell=config('TO_RELL')
email=config('ALERT_EMAIL')
password=config('ALERT_EMAIL_PW')
port=config('SMTP_PORT')
author_id=config('FIREBASE_ID')

global running

def alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    user = email
    msg['from'] = user
    pw = password
    server = smtplib.SMTP("smtp.gmail.com", port)
    server.starttls()
    server.login(user, pw)
    server.send_message(msg)
    server.quit()

# alert('!', 'This is a test.', [rhillx, rell])

def generateContent(topic):
    db = Database()
    fb = Firebase()
    bot = Bot()
    try:
        # Fetch a clip 
        logging.debug('Fetching a clip...')
        clip = bot.fetchClip(topic)
        clip_id = clip['id']
        clip_img = clip['imgURL']
        clip_topic = clip['topic']
        # Verify clip
        logging.debug('Verifying clip...')
        db.verifyClip(clip_id)
        # convert Audio
        logging.debug('Transcoding audio.....')
        audio_file = bot.transcodeAudio(clip_id)
        # convert Img
        logging.debug('Transcoding image.....')
        bot.transcodeImage(clip_img)
        # put story files in firebase storage
        logging.debug('Storing files to firebase.....')
        fb.addFilesToStorage([audio_file, 'clip.png'], clip_topic)
        # get audio URL
        logging.debug('Fetching audio URL.....')
        clip_audio_url = fb.getAudioClipURL(audio_file, clip_topic, clip_id)
        # get image URL
        logging.debug('Fetching image URL.....')
        clip_img_url = fb.getImgURL('clip.png', clip_topic, clip_id)
        # post clip to firebase
        logging.debug('Creating story in firebase.....')
        with open('audilore_story.json', 'r') as f:
            story = json.loads(f.read())
        
        story['authorId']=author_id
        story['authorName'] = 'Audilore Cast'
        story['duration'] = clip['duration']
        story['genre'] = topic
        story['postedAt'] = datetime.now()
        story['recordingFileName'] = audio_file
        story['recordingURL'] = clip_audio_url
        story['storyCoverFileName'] = 'clip.png'
        story['storyCoverURL'] = clip_img_url
        story['storyId'] = clip_id
        story['title'] = clip['title']
        created_story = fb.createStory(story)
        # delete clip from json
        logging.debug('Removing clip from json.....')
        if created_story:
            bot.removeClipFromJson(clip_topic, clip_id)
        else:
            print('Clip Not Removed!')
        # add clip to database
        logging.debug('Adding clip to memory...')
        date = datetime.now().date()
        story_tup = (clip['id'], clip['topic'], clip['title'], clip['sub_title'], date)
        try:
            db.insert(story_tup)
        except Exception as e:
            logging.error(e)
            return
        # delete files created
        logging.debug('Discarding files...')
        bot.discardFiles([audio_file, 'clip.png'])
        logging.debug('Task complete.')
    except Exception as err:
        logging.error(err)
        running=False
        msg_ = 'Program on hold!. Im experiencing some kind of issue. Please check my server.'
        alert('!!!' ,msg_, [rhillx, rell])
       

news_topics = ['U.S. News', 'Top Stories', 'World News']
sports='Sports News'
entertainment = 'Entertainment News'
finance = 'Financial Advice'
true_crime='True Crime'
christian = 'Christianity'
meditation = 'Meditation'
mental_health = 'Mental Health'

generateContent(mental_health)

# # TOP STORIES, WORLD NEWS U.S NEWS
# schedule.every(1).days.at("8:00").do(generateContent(random.choice(news_topics)))
# schedule.every(1).days.at("17:00").do(generateContent(random.choice(news_topics)))
# # SPORTS NEWS
# schedule.every().sunday.at("19:00").do(generateContent(sports))
# schedule.every().tuesday.at("19:00").do(generateContent(sports))
# schedule.every().tuesday.at("19:00").do(generateContent(sports))
# # ENTERTAINMENT
# schedule.every().tuesday.at("10:00").do(generateContent(entertainment))
# schedule.every().thursday.at("10:00").do(generateContent(entertainment))
# schedule.every().sunday.at("10:00").do(generateContent(entertainment))
# # FINANCE
# schedule.every().monday.at("16:00").do(generateContent(finance))
# schedule.every().wednesday.at("16:00").do(generateContent(finance))
# schedule.every().friday.at("16:00").do(generateContent(finance))
# # TRUE CRIME
# schedule.every().wednesday.at("12:00").do(generateContent(true_crime))
# schedule.every().saturday.at("12:00").do(generateContent(true_crime))
# # CHRISTIANITY
# schedule.every().sunday.at("13:00").do(generateContent(christian))
# # MEDITATION
# schedule.every().day.at("20:00").do(generateContent(meditation))
# # MENTAL HEALTH
# schedule.every().monday.at("14:00").do(generateContent(mental_health))
# schedule.every().thursday.at("14:00").do(generateContent(mental_health))

def run():
    running = True
    while running:
        schedule.run_pending()
        


# if __name__ == '__main__':
#     run()