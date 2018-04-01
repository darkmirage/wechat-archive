#!/usr/bin/env python

import codecs
import sqlite3
from autolink import linkify
from datetime import datetime

template = '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>For Sharon</title>
    <link rel="stylesheet" href="css/style.css">
  </head>
  <body>

%s

  </body>

<!-- My greatest thanks for being a source of inspiration -->
</html>
'''

def render_item(item):
  id, type, timestamp, user_id, content, media_path = item

  if type == 4:
    return ''

  inner = ''
  id_class = ''

  if user_id:
    id_class = ' %s' % user_id
    inner += '<div class="avatar"></div>\n'

  inner += '<div class="container" id="item-%s">\n' % id

  if content:
    inner += '<div class="content">%s</div>\n' % linkify(content)

  if media_path:
    media_path = media_path.replace('output/', '')
    media = ''
    if type == 2:
      media = '<a href="%s"><img src="%s" /></a>\n' % (media_path, media_path)
    elif type == 3:
      media = '<audio controls><source src="%s" type="audio/mpeg"></audio>\n' % media_path
    inner += '<div class="media">%s</div>\n' % media

  if timestamp:
    time = datetime.fromtimestamp(timestamp).strftime('%c')
    inner += '<div class="timestamp"><a href="#item-%s">%s</a></div>\n' % (id, time)

  inner += '</div>\n'

  return '<div class="item%s">\n%s</div>\n' % (id_class, inner)


def render_body():
  conn = sqlite3.connect('./messages.db')
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM items')
  items = [render_item(item) for item in cursor.fetchall()]
  inner = ''.join(items)
  conn.close()
  return '<div class="main">\n%s</div>\n' % inner

f = codecs.open('output/index.html', 'w', 'utf-8')
f.write(template % render_body())
f.close()
