#!/usr/bin/env python

import io
import os
import sqlite3
import subprocess

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

FNULL = open(os.devnull, 'w')

def transcribe_all():
  client = speech.SpeechClient()
  conn = sqlite3.connect('./messages.db')
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM items WHERE type = 3')

  for item in cursor.fetchall():
    id, type, timestamp, user_id, content, media_path = item

    if not media_path:
      continue

    if content:
      continue

    print(media_path)

    file_name = os.path.join(os.path.dirname(__file__), media_path)
    subprocess.call(['avconv', '-y', '-i', file_name, '/tmp/wechat.flac'], stdout=FNULL, stderr=subprocess.STDOUT)

    with io.open('/tmp/wechat.flac', 'rb') as audio_file:
      content = audio_file.read()
      audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
      encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
      language_code='en-US')

    try:
      response = client.recognize(config, audio)
      for result in response.results:
        transcript = result.alternatives[0].transcript
        print(transcript)
        cursor.execute('UPDATE items SET content = ? WHERE id = ?', (transcript, id))
        conn.commit()
        break
    except e:
      continue

  conn.close()

transcribe_all()
