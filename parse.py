#!/usr/bin/env python

import os
import sqlite3
from base64 import decodestring
from bs4 import BeautifulSoup
from datetime import datetime

id = 1

def get_user_id(tag):
  class_names = tag.attrs['class']
  if 'me' in class_names:
    return 'me'
  for class_ in class_names:
    if class_ not in ['me', 'chatItem', 'you']:
      return class_

def parse_file(cursor, filename):

  def insert_item(type=1, timestamp=None, user_id=None, content=None, media_path=None):
    global id
    cursor.execute("INSERT INTO items VALUES(?, ?, ?, ?, ?, ?)", (id, type, timestamp, user_id, content, media_path))
    id += 1

  print(filename)
  f = open(os.path.join('input', filename), 'r')
  html = f.read()

  soup = BeautifulSoup(html, 'html.parser')
  chatlist = soup.find(id='chat_chatmsglist')

  for child in chatlist.children:
    if child.name != 'div':
      continue
    class_names = child.attrs['class']

    if 'time' in class_names:
      time = child.text.strip()
      insert_item(type=4, content=time)
    elif 'chatItem' in class_names:
      panel = child.find(class_='cloudPannel')
      timestamp = int(datetime.strptime(panel.attrs['title'], '%Y-%m-%d %H:%M:%S').strftime('%s'))
      content = panel.find(class_='cloudContent')
      message = content.text.strip()
      user_id = get_user_id(child)

      type = 1
      media = None

      img = content.find('img')
      if (img):
        type = 2
        data_uri = img.attrs['src']
        encoded_string = data_uri.split(',')[1]
        media = 'output/images/%s.jpg' % timestamp
        mf = open(media, 'wb')
        mf.write(decodestring(encoded_string))
        mf.close()

      audio = content.find('audio')
      if (audio):
        source = audio.find('source')
        type = 3
        data_uri = source.attrs['src']
        encoded_string = data_uri.split(',')[1]
        media = 'output/audio/%s.mp3' % timestamp
        mf = open(media, 'wb')
        mf.write(decodestring(encoded_string))
        mf.close()

      insert_item(type=type, timestamp=timestamp, user_id=user_id, content=message, media_path=media)

    else:
      raise 'Unexpected child type'


if __name__ == '__main__':
  filenames = os.listdir('input')
  filenames.sort()

  conn = sqlite3.connect('./messages.db')
  cursor = conn.cursor()
  cursor.execute('DELETE FROM items');

  for filename in filenames:
    parse_file(cursor, filename)

  print(id)

  conn.commit()
  conn.close()
