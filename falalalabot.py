import twitter
import time
import configs
import sys
import re
import random

class FaLaLaLaBot:

	def __init__(self):
		print 'Starting FaLaLaLaBot'

		self.nextPushTime = 0
		self.pushInterval = 60 * 60
		self.failureInterval = 60 * 2 #wait two minutes on failure and try again
		self.result_type = 'recent'
		self.usedStrings = list()

		try:
			self.api = twitter.Api(consumer_key=configs.consumer_key, consumer_secret=configs.consumer_secret, access_token_key=configs.access_token_key, access_token_secret=configs.access_token_secret)
			self.api.VerifyCredentials()
		except twitter.TwitterError as e:
			print "Twitter Error: ", e.message
			sys.exit(0)
		except:
			print "Unexpected error in API authentication: ", sys.exc_info()[0]
			sys.exit(0)

		#self.makePost()
		
		#self.makePost()

		while(True):
			if time.time() >= self.nextPushTime:
				self.makePost()

	def makePost(self):
		
		noGo = 'jolly|fa |la |tra '

		for used in self.usedStrings:
			noGo += '|' + str(used)

		try:
			results = self.api.GetSearch(term='tis the season to', result_type=self.result_type)
		except twitter.TwitterError as e:
			print "Twitter Error: ", e.message 
			self.nextPushTime = time.time() + failureInterval
			return
		except:
			print "Unexpected error in twitter search: ", sys.exc_info()[0]
			self.nextPushTime = time.time() + failureInterval
			return

		resultText = list()
		regexedList = list()
		userList = list()

		for r in results:
			resultText.append(r)
		#	print "\n", r.text

		#print "------"

		for t in resultText:
			reged = re.search('(Tis the season to be )([a-zA-Z][a-zA-Z -]+[a-zA-Z])', t.text)

			if(reged != None and re.search(noGo, str(reged.group(2))) == None):
				userList.append(t.user)
				regexedList.append(str(reged.group(2)))
		
		while(True):
			if(len(regexedList) > 0):
				randIndex = random.randint(0,len(regexedList)-1)
				toBeString = regexedList[randIndex]
				user = userList[randIndex]
				post = str("'Tis the season to be " + toBeString + ". Falalalala. Lalalala. via @" + user.screen_name)

				if(len(post) <= 140):
					#print post
					self.pushPost(post)
					self.usedStrings.append(toBeString)
					break
			else:
				print "Error: No valid tweets"
				self.nextPushTime = time.time() + failureInterval
				break

	def pushPost(self, post):
		try:
			self.nextPushTime = time.time() + self.pushInterval
			status = self.api.PostUpdate(str(post))
			print "\n" + str(time.time()), "POSTED: ", status.text
			print "Next Push at: " + str(self.nextPushTime) + "\n"
		except:
			print "Unexpected error in push: ", sys.exc_info()[0]
			self.nextPushTime = time.time() + failureInterval

if __name__ == '__main__':
	bot = FaLaLaLaBot()