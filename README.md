# CoC_Announce

COC_Announce is a schedulable python script that reports changes to Clan Roster, Member Level Ups and Member League promotions/demotions.

# Setup

1st Step is to sign up with COC and Twitter for the proper API Keys:

COC: https://developer.clashofclans.com/#/
Twitter: https://apps.twitter.com/

Various API keys and tokens are then entered into the iden.py file (Use the structure found in iden_example.py). Add the Clan Tag of the clan you'd like to report on, and the local folder you'll be storing the python code and data files in. Then put your begin.py and iden.py files into the chosen directory.

Next, you'll want to schedule the job to run once every 5 minutes should do the trick. On Linux I did this with a cronjob.
