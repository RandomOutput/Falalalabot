import twitter
import time
import configs
import sys
import re
import random
import logging

class FaLaLaLaBot:

	def __init__(self):
		print 'Starting FaLaLaLaBot'

		self.nextPushTime = 0
		self.pushInterval = 60 * 60
		self.failureInterval = 60 * 2 #wait two minutes on failure and try again
		self.result_type = 'recent'
		self.usedStrings = list()

		logging.basicConfig(filename='falalalalog.log',level=logging.INFO)

		try:
			self.api = twitter.Api(consumer_key=configs.consumer_key, consumer_secret=configs.consumer_secret, access_token_key=configs.access_token_key, access_token_secret=configs.access_token_secret)
			self.api.VerifyCredentials()
		except twitter.TwitterError as e:
			logging.error("TwitterError: " + str(e.message[0]))
			sys.exit(0)
		except:
			logging.error("Unexpected error in API authentication: " + str(sys.exc_info()[0]))
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
			logging.error("TwitterError in search: " + str(e.message[0]))
			self.nextPushTime = time.time() + self.failureInterval
			return
		except:
			logging.error("Unexpected error in Search: " + str(sys.exc_info()[0]))
			self.nextPushTime = time.time() + self.failureInterval
			return

		resultText = list()
		regexedList = list()
		userList = list()

		for r in results:
			resultText.append(r)

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
					self.pushPost(str(post))
					self.usedStrings.append(toBeString)
					break
			else:
				logging.warn("No valid tweets")
				self.nextPushTime = time.time() + self.failureInterval
				break

	def pushPost(self, post):
		try:
			self.nextPushTime = time.time() + self.pushInterval
			status = self.api.PostUpdate(str(post))
			logging.info("\n" + str(time.time()) + "POSTED: " + status.text)
			logging.info("Next Push at: " + str(self.nextPushTime))
		except twitter.TwitterError as e:
			logging.error("TwitterError in push: " + str(e.message[0]))
			self.nextPushTime = time.time() + self.failureInterval
		except NameError as e:
			raise e
		except:
			logging.error("Unexpected error in push: " + str(sys.exc_info()[0]))
			self.nextPushTime = time.time() + self.failureInterval

if __name__ == '__main__':
	bot = FaLaLaLaBot()