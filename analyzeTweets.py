import mysql.connector 
from mysql.connector import Error
import os
import re
import pandas as pd 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import matplotlib.pyplot as plt



class TweetObject():
	"""



	"""

	def __init__(self, host, database, user, password):
		self.consumer_key = os.environ['CONSUMER_KEY']
		self.consumer_secret = os.environ['CONSUMER_SECRET']
		self.access_token = os.environ['ACCESS_TOKEN']
		self.access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
		self.host = host
		self.database = database
		self.user = user
		self.password =  password


	def MySQLConnect(self,query):
		"""
		Connects to database and extracts
		raw tweets and any other columns we
		need

		"""

		try:
			con = mysql.connector.connect(host = self.host, database = self.database, \
				user = self.user, password = self.password, charset = 'utf8')

			if con.is_connected():
				print("Successfully connected to database")

				cursor = con.cursor()
				query = query
				cursor.execute(query)

				data = cursor.fetchall()
				# store in dataframe
				df = pd.DataFrame(data,columns = ['date', 'tweet'])
				#print(df.head())



		except Error as e:
			print(e)
		
		cursor.close()
		con.close()

		# dataframe to use in other methods
		return df



	def clean_tweets(self, df):
	
		"""
		Takes raw tweets and cleans them
		so we can carry out analysis
		remove stopwords, punctuation,
		lower case, html, emoticons.
		This will be done using Regex

		? means option so colou?r matches
		both color and colour.
		"""

		# Do some text preprocessing
		stopword_list = stopwords.words('english')
		ps = PorterStemmer()
		df["clean_tweets"] = None
		for i in range(0,len(df['tweet'])):
			# get rid of anythin that isnt a letter

			exclusion_list = ['[^a-zA-Z]','rt', 'http', 'co', 'RT']
			exclusions = '|'.join(exclusion_list)
			text = re.sub(exclusions, ' ' , df['tweet'][i])
			text = text.lower()
			words = text.split()
			words = [word for word in words if not word in stopword_list]
			 # only use stem of word
			words = [ps.stem(word) for word in words]
			df['clean_tweets'][i] = ' '.join(words)
			


		return df



	def sentiment(self):
		pass
		"""
		This function calculates sentiment
		from our base on our cleaned tweets.
		"""


	def save_to_csv(self, df):
		"""
		Save cleaned data to a csv for further
		analysis.
		"""
		try:
			df.to_csv("clean_tweets.csv")
			print("\n")
			print("csv successfully saved. \n")

		
		except Error as e:
			print(e)
		



	def word_cloud(self, df):
		plt.subplots(figsize = (12,10))
		wordcloud = WordCloud(
								background_color = 'white',
								width = 1000,
								height = 800).generate(" ".join(df['clean_tweets']))
		plt.imshow(wordcloud)
		plt.axis('off')
		plt.show()





if __name__ == '__main__':
	t = TweetObject( host = 'localhost', database = 'twitterdb', user = 'root', password = 'titleist920')
	#print(t.consumer_key)
	#print(t.host)
	data  = t.MySQLConnect("SELECT created_at, tweet FROM `TwitterDB`.`Twitter`;")
	#print(data)
	data = t.clean_tweets(data)
	print(data)
	t.save_to_csv(data)
	t.word_cloud(data)



	