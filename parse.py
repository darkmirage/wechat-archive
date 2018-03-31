#!/usr/bin/env python

import os
import sqlite3
from bs4 import BeautifulSoup

def parse_file(cursor, filename):
  print(filename)
  f = open(os.path.join('input', filename), 'r')
  html = f.read()
  soup = BeautifulSoup(html, 'html.parser')
  print(soup.title)
  cursor.execute("INSERT INTO items VALUES(1, 0, 213124141, 'me', 'message content', 'audio/test.mp3')")

if __name__ == '__main__':
  filenames = os.listdir('input')
  filenames.sort()

  conn = sqlite3.connect('./messages.db')

  parse_file(conn.cursor(), filenames[0])


  conn.commit()
  conn.close()
