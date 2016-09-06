#!/usr/bin/python3
from twython import Twython
from ash.cocapi import *
import csv
import os
import re
import iden
import os.path


def makelist(data, num):
    file = open(data + '.csv')
    reader = csv.reader(file)
    contents = list(reader)
    output = []
    for item in contents:
        output.append(item[num])
    return output

def makedic(data, num):
    file = open(data + '.csv')
    reader = csv.reader(file)
    contents = list(reader)
    output = {}
    for item in contents:
        output[item[0]] = item[num]
    return output

def write(data, filename):
    outputFile = open( filename + '.csv', 'w', newline='')
    outputWriter = csv.writer(outputFile)
    for result in data.items:
        outputWriter.writerow([result.name, result.league['name'], result.expLevel,
                          result.donations, result.donationsReceived, result.role,
                          result.clanRank, result.previousClanRank, result.trophies])
    outputFile.close()
    return True

#Define Twitter API:
api = cocapi(iden.coc_api_token)
twitter = Twython(iden.twitter_app_key, iden.twitter_app_secret, iden.twitter_oauth_token, iden.twitter_oauth_token_secret)

#Define Clash API and retrieve data:
tag = iden.coc_clan_tag
results = api.get_clan_members(tag)
if type(results[0]) is str:
    twitter.update_status(status = 'Unfortunately, there is an error with your code. COC API returned error ' + results[1] )


#Set Working Directory:
os.chdir(iden.home_dir)

if os.path.isfile("old.csv"):
    write(results, 'new')
else:
    write(results, 'old')

if os.path.isfile("new.csv"):
    oldMembers = makelist('old', 0)
    oldLevel = makedic('old', 2)
    oldLeagues = makedic('old', 1)
    newMembers = makelist('new', 0)
    newLevel = makedic('new', 2)
    newLeagues = makedic('new', 1)
    leagues = {'Unranked': 0,
           'Bronze League III': 1, 'Bronze League II': 2, 'Bronze League I': 3, 'Silver League III': 4,
           'Silver League II': 5, 'Silver League I': 6, 'Gold League III': 7, 'Gold League II': 8,
           'Gold League I': 9, 'Crystal League III': 10, 'Crystal League II': 11, 'Crystal League I': 12,
           'Master League III': 13, 'Master League II': 14, 'Master League I': 15, 'Champion League III': 16,
           'Champion League II': 17, 'Champion League I': 18, 'Titan League III': 19, 'Titan League II': 20,
           'Titan League I': 21}

    #Member Departure Announce
    for member in oldMembers:
        if member not in newMembers:
            twitter.update_status(status = member + ' has left the clan. See ya later!')

    #Member Join Announce
    for member in newMembers:
        if member not in oldMembers:
            twitter.update_status(status = member + ' has joined the clan. Welcome!')

    #Member Level Up Announce
    for member in newMembers:
        if member in oldMembers:
            if newLevel[member] in oldLevel[member]:
                if oldLevel[member] != newLevel[member]:
                    twitter.update_status(status = member + ' has reached level ' + newLevel[member] + '! Nice!')

    #League Change Announce
    newSeasonCheck = 0
    for member in newMembers:
        newSeasonCheck += leagues[oldLeagues[member]]
    if newSeasonCheck == 0 and os.path.isfile('season.txt'):
        twitter.update_status(status = "It's a new season! All members are now unranked!")
        os.remove('season.txt')
    else:
        for member in newMembers:
            if oldLeagues[member] != newLeagues[member]:
                if leagues[eagues[member]] > leagues[newLeagues[member]]:
                    twitter.update_status(status = member + ' has been demoted to ' + newLeagues[member] + '. Oh no!')
                else:
                    twitter.update_status(status = member + ' has been promoted to ' + newLeagues[member] + '. Way to go!')
                file = open('season.txt', 'w+')

    os.remove("old.csv")
    os.rename("new.csv", "old.csv")