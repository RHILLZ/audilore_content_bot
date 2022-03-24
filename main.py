from datetime import datetime
from pprint import pprint
from database import Database
from firebase_ import Firebase
from bot import Bot
import smtplib
from email.message import EmailMessage

# email pw vjobulmastanqclx

def alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    user = 'audilorealert@gmail.com'
    msg['from'] = user
    pw = 'vjobulmastanqclx'
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, pw)
    server.send_message(msg)
    server.quit()

alert('Error','This is audilore son', '6094649737@tmomail.net')

def generateContent():
    db = Database()
    fb = Firebase()
    bot = Bot()
    try:
        # Fetch a clip 
        pprint('Fetching a clip...')
        story = bot.fetchClip()
        clip_id = story['id']
        clip_img = story['imgURL']
        clip_topic = story['topic']
        # Verify clip
        pprint('Verifying clip...')
        isVerified = db.verifyClip(clip_id)
        # convert Audio
        pprint('Transcoding audio.....')
        audio_file = bot.transcodeAudio(clip_id)
        # convert Img
        pprint('Transcoding image.....')
        bot.transcodeImage(clip_img)
        # put story files in firebase storage
        pprint('Storing files to firebase.....')
        fb.addFilesToStorage([audio_file, 'clip.png'], clip_topic)
        # get audio URL
        pprint('Fetching audio URL.....')
        clip_audio_url = fb.getAudioClipURL(audio_file, clip_topic, clip_id)
        # get image URL
        pprint('Fetching image URL.....')
        clip_img_url = fb.getImgURL('clip.png', clip_topic, clip_id)
        # post clip to firebase
        pprint('Creating story in firebase.....')
        story['imgURL'] = clip_img_url
        story['recordingURL'] = clip_audio_url
        story['author'] = 'audilore'
        created_story = fb.createStory(story)
        # delete clip from json
        pprint('Removing clip from json.....')
        if created_story:
            bot.removeClipFromJson(clip_topic, clip_id)
        else:
            print('Clip Not Removed!')
        # add clip to database
        pprint('Adding clip to memory...')
        date = datetime.now().date()
        story_tup = (story['id'], story['topic'], story['title'], story['sub_title'], date)
        try:
            db.insert(story_tup)
        except:
            pprint('Could not insert into memory.')
            return
        # delete files created
        pprint('Discarding files...')
        bot.discardFiles([audio_file, 'clip.png'])
        pprint('Task complete.')
    except:
        msg = 'Im experiencing some kind of issue. Please check my server.'
        alert('Error',msg, '6094649737@tmomail.net')
       

# if __name__ == '__main__':
#     generateContent()