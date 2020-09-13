#coding:utf-8
import json
import os
import subprocess
import youtube_dl

from bottle import route, Bottle, request, static_file, template
from collections import ChainMap
from queue import Queue
from threading import Thread

# Configs
configs_default = {
    'YDL_FORMAT': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'YDL_EXTRACT_AUDIO_FORMAT': None,
    'YDL_EXTRACT_AUDIO_QUALITY': '192',
    'YDL_RECODE_VIDEO_FORMAT': None,
    'YDL_OUTPUT_TEMPLATE': './downloads/%(title)s [%(id)s].%(ext)s',
    'YDL_ARCHIVE_FILE': None,

    'WEB_HOST': '0.0.0.0',
    'WEB_PORT': 80,
    'WEB_ROOT': '/',
    'WEB_TITLE': 'Youtube-DL',
}

configs = ChainMap(os.environ, configs_default)

# Web App
app = Bottle()
app_done = False

@app.route(configs['WEB_ROOT'])
def root():
    return template('root', title = configs['WEB_TITLE'])

@app.route(configs['WEB_ROOT'] + 'query', method = 'GET')
def query_get():
    return { 'success': True, 'queue': json.dumps(list(download_queue.queue)) }

@app.route(configs['WEB_ROOT'] + 'query', method = 'POST')
def query_post():
    url = request.forms.get('url')

    if not url:
        return { 'success': False, 'error': 'URL is empty' }

    options = { 'format': request.forms.get('format') }

    download_queue.put((url, options))
    print('[download] Added [' + url + '] to the download queue')
    return { 'success': True, 'url': url, 'options': options }

@app.route(configs['WEB_ROOT'] + 'update', method = 'GET')
def update():
    command = ['pip', 'install', '--upgrade', 'youtube-dl']
    proc = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    output, error = proc.communicate()
    return {
        'output': output.decode('ascii'),
        'error': error.decode('ascii')
    }

# Download
download_queue = Queue()

def parse_options(options):
    target_format = {
        'YDL_EXTRACT_AUDIO_FORMAT': None,
        'YDL_RECODE_VIDEO_FORMAT': None,
    }

    # bestvideo -> original
    option_format = options.get('format', 'bestvideo')

    if option_format in ['aac', 'flac', 'mp3', 'm4a', 'opus', 'vorbis', 'wav']:
        target_format['YDL_EXTRACT_AUDIO_FORMAT'] = option_format
    elif option_format == 'bestaudio':
        target_format['YDL_EXTRACT_AUDIO_FORMAT'] = 'best'
    elif option_format in ['mp4', 'flv', 'webm', 'ogg', 'mkv', 'avi']:
        target_format['YDL_RECODE_VIDEO_FORMAT'] = option_format

    target_options = ChainMap(target_format, os.environ, configs_default)

    postprocessors = []

    if(target_options['YDL_EXTRACT_AUDIO_FORMAT']):
        postprocessors.append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': target_options['YDL_EXTRACT_AUDIO_FORMAT'],
            'preferredquality': target_options['YDL_EXTRACT_AUDIO_QUALITY'],
        })

    if(target_options['YDL_RECODE_VIDEO_FORMAT']):
        postprocessors.append({
            'key': 'FFmpegVideoConvertor',
            'preferedformat': target_options['YDL_RECODE_VIDEO_FORMAT'],
        })

    return {
        'format': target_options['YDL_FORMAT'],
        'postprocessors': postprocessors,
        'outtmpl': target_options['YDL_OUTPUT_TEMPLATE'],
        'download_archive': target_options['YDL_ARCHIVE_FILE']
    }

def download(url, options):
    with youtube_dl.YoutubeDL(parse_options(options)) as ydl:
        try:
            ydl.download([ url ])
        except Exception as e:
            print('[download] ' + e)


def download_worker():
    while not app_done:
        url, options = download_queue.get()
        download(url, options)
        download_queue.task_done()

# Update ytdl and launch the app
print('[update] Update youtube-dl to the latest version')
update_result = update()
if (update_result['error']):
   print('[update] ERROR: ' + update_result['error'])
else:
   for line in update_result['output'].splitlines():
       print('[update] Updated: ' + line)

download_thread = Thread(target = download_worker)
download_thread.start()
print('[download] Started the download thread')

print('[app] Launch the app')
app.run(host = configs['WEB_HOST'], port = configs['WEB_PORT'])

app_done = True
download_thread.join()