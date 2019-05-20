import os
import sys
from datetime import datetime

import PIL
import PIL.ImageEnhance
import pydub
import pydub.playback
import pytesseract
import requests
from werkzeug import urls

import picamera


def take_picture(file_name):
    '''
        Capture an image
    '''

    # create camera object
    c = picamera.PiCamera()

    c.capture('{}.png'.format(file_name))

    # destro camera object
    c.close()

    print('[take_picture] image captured, file_name: {}.png'.format(file_name))


def ocr_image(file_name):
    '''
        Extract text from an image
    '''
    # load image from file
    img = PIL.Image.open('{}.png'.format(file_name))

    # crop image
    crop = img.crop((300,300,1600,800))
    print('[orc_image] Image cropped')

    # enhance contrast
    enhanced = PIL.ImageEnhance.Contrast(crop).enhance(1.4)
    print('[orc_image] Image contrast enhanced')

    # save enhanced image
    enhanced.save('{}-cropped-enhanced.png'.format(file_name))

    # extract text
    txt = pytesseract.image_to_string(enhanced)

    print('[orc_image] text extracted: {}'.format(txt))

    return txt


def text_to_audio(txt, file_name):
    '''
        Send text to google, and get back an mp3 file with that text pronounced
    '''

    # types of audio we can accept
    types = [
        'audio/mpeg', 'audio/x-mpeg', 'audio/mp3', 'audio/x-mp3',
        'audio/mpeg3', 'audio/x-mpeg3', 'audio/mpg', 'audio/x-mpg',
        'audio/x-mpegaudio', 'application/octet-stream', 'audio/mpegurl',
        'audio/mpeg-url', 'audio/x-mpegurl', 'audio/x-scpls', 'audio/scpls',
        'application/pls', 'application/x-scpls', 'application/pls+xml', '*/*'
    ]

    # parameters we need to send to google 
    # parameter 'q' will contain the text we want to be pronounced
    query = {'ie': 'UTF-8', 'client': 'tw-ob', 'q': txt, 'tl': 'En-us'}

    # the url we need to access to get text converted into audio
    url = urls.URL(scheme='http',
                   netloc='translate.google.com',
                   path='/translate_tts',
                   query=urls.url_encode(query),
                   fragment='')

    print('[text_to_audio] google url: {}'.format(url))

    response = requests.get(
        url,
        headers={
            # what application google should think we are using
            'User-Agent': 'mpg123/1.25.10',
            # audio types
            'Accept': ','.join(types)
        })

    print('[text_to_audio] response from google: {}'.format(response.status_code))

    # open a new file in binary mode, and save the audio
    with open('{}.mp3'.format(file_name), 'wb') as out_file:
        out_file.write(response.content)

    print('[text_to_audio] audio saved as: {}.mp3'.format(file_name))

def play_audio(file_name):

    # verify that file exists and is a file
    if os.path.isfile('{}.mp3'.format(file_name)):
        # play the file
        print('[play_audio] Playing audio file')
        sound = pydub.AudioSegment.from_mp3('{}.mp3'.format(file_name))
        pydub.playback.play(sound)
    else:
        print('[play_audio] {}.mp3 is not a valid file'.format(file_name))


def main():

    print('Hello')

    # creates a unique timestamp string, which will be used as a file name
    file_name = datetime.strftime(datetime.now(), '%m%d%y_%H%M%S')

    take_picture(file_name)

    txt = ocr_image(file_name)

    text_to_audio(txt, file_name)

    play_audio(file_name)

    print('Goodbye')

if __name__ == '__main__':
    main()
