#!/usr/bin/python3
from twython import Twython
from ash.cocapi import *
import csv
import os
import re
import iden



#Pulling api credentials from iden.py, initialize proper connections:
api = cocapi(iden.coc_api_token)
twitter = Twython(iden.twitter_app_key, iden.twitter_app_secret, iden.twitter_oauth_token, iden.twitter_oauth_token_secret)
tag = iden.coc_clan_tag

#STEP 1: GET DATA

results = api.get_clan_members(tag)
os.chdir(iden.home_dir)
current_num = 0
for file in os.listdir():
    num = re.search("0*(\d*).csv", file)
    if int(num.group(1)) > current_num:
        current_num = int(num.group(1))

new_num = current_num + 1
new_zero_num = 8 - len(str(new_num))
old_num = current_num
old_zero_num = 8 - len(str(old_num))
outputFile = open('data' + '0' * new_zero_num + str(new_num) + '.csv', 'w', newline='')
outputWriter = csv.writer(outputFile)

for result in results.items:
    outputWriter.writerow([result.name, result.league['name'], result.expLevel,
                          result.donations, result.donationsReceived, result.role,
                          result.clanRank, result.previousClanRank, result.trophies])
outputFile.close()

#STEP 2: COMPARE DATA

oldFile = open('data' + '0' * old_zero_num + str(old_num) + '.csv')
oldReader = csv.reader(oldFile)
oldData = list(oldReader)

newFile = open('data' + '0' * new_zero_num + str(new_num) + '.csv')
newReader = csv.reader(newFile)
newData = list(newReader)

oldMembers = []
for item in oldData:
    oldMembers.append(item[0])

newMembers = []
for item in newData:
    newMembers.append(item[0])

for member in oldMembers:
    if member not in newMembers:
        twitter.update_status(status = member + ' has left the clan. See ya later!')

if oldMembers != []:
    for member in newMembers:
        if member not in oldMembers:
            twitter.update_status(status = member + ' has joined the clan. Welcome!')

oldLevel = {}
for item in oldData:
    oldLevel[item[0]] = item[2]

newLevel = {}
for item in newData:
    newLevel[item[0]] = item[2]

for member in newMembers:
    if oldLevel[member] != newLevel[member]:
        twitter.update_status(status = member + ' has reached level ' + newLevel[member] + '! Nice!')

oldLeagues = {}
for item in oldData:
    oldLeagues[item[0]] = item[1]

newLeagues = {}
for item in newData:
    newLeagues[item[0]] = item[1]

leagues = {'Unranked': 0,
           'Bronze League III': 1, 'Bronze League II': 2, 'Bronze League I': 3, 'Silver League III': 4,
           'Silver League II': 5, 'Silver League I': 6, 'Gold League III': 7, 'Gold League II': 8,
           'Gold League I': 9, 'Crystal League III': 10, 'Crystal League II': 11, 'Crystal League I': 12,
           'Master League III': 13, 'Master League II': 14, 'Master League I': 15, 'Champion League III': 16,
           'Champion League II': 17, 'Champion League I': 18, 'Titan League III': 19, 'Titan League II': 20,
           'Titan League I': 21}

for member in newMembers:
    if oldLeagues[member] != newLeagues[member]:
        if leagues[oldLeagues[member]] > leagues[newLeagues[member]]:
            twitter.update_status(status = member + ' has been demoted to ' + newLeagues[member] + '. Oh no!')
        else:
            twitter.update_status(status = member + ' has been promoted to ' + newLeagues[member] + '. Way to go!')



#twitter.update_status(status = 'Bleep, bloop, blip, I am a robot ' + str(time.time()))