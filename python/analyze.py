import os
import tweepy
import requests
from dotenv import load_dotenv
import json 
import csv
import re

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")
URL = os.getenv("URL")
assert SUBSCRIPTION_KEY
documents = {'documents' : []}

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def getInput():
	name = input("Twitter Account or #hashtag: ")
	tweetCount = input("How many tweets(ENTER if all): ")
	while(not tweetCount.isdigit() and tweetCount!=''):
		tweetCount = input("How many tweets(ENTER if all): ")
	
	return name, tweetCount

def scrap(name, tweetCount=20):
	results = []
	try:
		if (tweetCount!=''):
			if (name[0:1]=='#'):
				results_raw = tweepy.Cursor(api.search,q=name,lang="en", tweet_mode="extended").items(int(tweetCount))
			else:
				results_raw = tweepy.Cursor(api.user_timeline, id=name, tweet_mode="extended").items(int(tweetCount))
		else:
			if (name[0:1]=='#'):
				results_raw = tweepy.Cursor(api.search,q=name,lang="en", tweet_mode="extended").items()
			else:
				results_raw = tweepy.Cursor(api.user_timeline, id=name, tweet_mode="extended").items()

		for tweet in results_raw:
			if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
				temp = tweet.full_text.replace('\n', ' ').replace('\r', '')
				results.append(re.sub(r'http\S+', ' ', temp))
	except:
		print("Account Not Found. Program exits.")
		exit(0)
	return results	 

def azure(documents):
	headers   = {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}
	response  = requests.post(URL, headers=headers, json=documents)
	sentiments = response.json()
	return sentiments

def adddoc(i, text):
	doc = {'id': i, 'language': 'en', 'text': text}
	documents['documents'].append(doc)

def display(name, tweets, result):
	print('Twitter account '+name)
	for i in range(0, len(tweets)):
		print(str(result[i]['id']) + '\t'+ str(result[i]['score']) + '\t' + str(tweets [i]))

def writeCSV(name, tweets, result):
	dictionary = {}

	mean = 0;
	for i in range(0, len(tweets)):
		mean = mean + result[i]['score']
	mean = mean/len(tweets)

	filename = name+'_'+str(round(mean,3))+'_twitter.csv'

	with open(filename, mode='w') as analysis:
		fieldnames = ['id', 'score','text']
		writer = csv.DictWriter(analysis, fieldnames=fieldnames)
		writer.writeheader()
		for i in range(0, len(tweets)):
			writer.writerow({'id':str(result[i]['id']),'score':str(result[i]['score']),'text':str(tweets [i])})

def start():
	name, count = getInput() 					#user input
	tweets = scrap(name, count)					#get the tweets

	for i in range(0, len(tweets)):				#azure
		adddoc(str(i),tweets[i])		
	result = azure(documents)

	display(name, tweets, result['documents'])	#display
	writeCSV(name, tweets, result['documents'])	#write to csv


if __name__== "__main__":
	start()
