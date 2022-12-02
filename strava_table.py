import sqlite3
import json
import os


conn = sqlite3.connect('/Users/barberer/Desktop/music.sqlite')
cur = conn.cursor()

#delete the table if it already exists 
cur.execute("CREATE TABLE IF NOT EXISTS Track")
###I THINK THIS IS DIFFERENT FOR THE PROJECT#####

#create the table 
cur.execute('CREATE TABLE Tracks (title TEXT, plays INTEGER')


#insert data into the Tracks Table 
cur.execute('INSERT INTO Tracks (title, plays) VALUES (?, ?)'('Thunderstruck', 20))
cur.execute('INSERT INTO Tracks (title, plays) VALUES (?, ?)'('My Way', 15))

#commit the changes 
conn.commit()

#select and print the data 
print('Tracks:')
cur.execute('SELECT title, plays FROM Tracks')
for row in cur:
    print(row)

cur.close()