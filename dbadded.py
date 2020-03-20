import discord
import asyncio
import mysql.connector
import urllib.request
import requests
from bs4 import BeautifulSoup
import re

mydb = mysql.connector.connect(
  host="akumi.caqzlvmetak9.us-west-1.rds.amazonaws.com",
  user="ToBeThriller2479",
  passwd="Akumi123",
  database="Akumi"
)

print(mydb)

mycursor = mydb.cursor(buffered=True)
def insert(t, f):
    sql = "INSERT INTO devil_fruits (fruit_jp, dtype) VALUES (%s, %s)"
    if t == 'p':
        val = (f, "p")
    if t == 'l':
        val = (f, "l")
    if t == 'z':
        val = (f, "z")

    mycursor.execute(sql, val)

    mydb.commit()

print("record inserted.")
f = open("dfdb.txt", "r")
if f.mode == "r":
    text = f.read()
    types = text.split('!\n\n')

    paramecia = types[0]
    paramecia = paramecia[12:]
    zoan = types[1]
    zoan = zoan[7:]
    logia = types[2]
    logia = logia[8:]

    pf = paramecia.split('  •  ')
    zf = zoan.split('  •  ')
    lf = logia.split('  •  ')

sql = "SELECT * FROM devil_fruits WHERE ID >= 136"
mycursor.execute(sql)
results = mycursor.fetchall()

for result in results:
    df_jp = result[3]
    id = result[0]
    df_jp = df_jp.replace(' ', '_')
    url = "https://onepiece.fandom.com/wiki/" + str(df_jp)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    h = soup.find_all("div", class_="pi-data-value pi-font")
    hl = len(h)
    hu = hl-1
    #print(h)
    df_en = str(h[1])
    user = h[hu]
    user = user.find("a")
    n = len(df_en)
    n = n-6
    user = user.get('title')
    df_en = df_en[35:n]
    df_en = df_en.replace('-', ' ')
    print(df_en)
    print(user)
    sql = "UPDATE devil_fruits SET fruit_en = %s, user_name = %s WHERE ID = %s"
    val = (df_en, user, id)
    mycursor.execute(sql, val)

    mydb.commit()

#print(pf)
#for f in pf:
#    insert('p', f)
#for f in zf:
#    insert('z', f)
#for f in lf:
#    insert('l', f)
