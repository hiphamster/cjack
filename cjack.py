import os
import sys
from datetime import datetime

import PIL
import pydub
import pydub.playback
import pytesseract
import requests
from werkzeug import urls


def get_image():
    '''
        This will be the method that takes the photo 
    '''
    test_img = 'img2.png'
    img = PIL.Image.open(test_img)
    print('[get_image] format: {}, size: {}'.format(img.format, img.size))

    return img


def ocr_image(img):
    '''
        Extract text from an image
    '''
    txt = pytesseract.image_to_string(img)
    print('[orc_image] text: {}'.format(txt))

    return txt


def text_to_audio(txt):
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

    # parameters we need to send to google, parameter 'q' will contain
    # the text we want to be pronounced
    query = {'ie': 'UTF-8', 'client': 'tw-ob', 'q': txt, 'tl': 'En-us'}

    # the url we need to access to get text converted into audio
    url = urls.URL(scheme='http',
                   netloc='translate.google.com',
                   path='/translate_tts',
                   query=urls.url_encode(query),
                   fragment='')

    print('[text_to_audio] url: {}'.format(url))

    response = requests.get(
        url,
        headers={
            # what application google should think we are using
            'User-Agent': 'mpg123/1.25.10',
            # audio types
            'Accept': ','.join(types)
        },
    )

    print('[text_to_audio] response: {}'.format(response.status_code))

    # creates a unique timestamp string, which will be used as a file name
    audio_file_name = datetime.strftime(datetime.now(),
                                        '%m%d%y_%H%M%S') + '.mp3'

    # open a new file in binary mode, and save the audio
    with open(audio_file_name, 'wb') as out_file:
        out_file.write(response.content)

    return audio_file_name


def play_audio(aud):

    # verify that file exists and is a file
    if os.path.isfile(aud):
        # play the file
        sound = pydub.AudioSegment.from_mp3(aud)
        pydub.playback.play(sound)
    else:
        print('[play_audio] {} is not a valid file'.format(aud))


def main():

    print('Hello')

    img = get_image()

    txt = ocr_image(img)

    aud = text_to_audio(txt)

    play_audio(aud)


if __name__ == '__main__':
    main()



