from typing import List
from website import Website
import sys, nltk, nltk.book

class Ground:
	"""This class generates a number
	of Websites with the website class
	which it gets the entry points from
	the sites.txt file by default or
	another file if specified.
	This class also has functions
	to get related words.
	"""

	sites = []
	text = ""
	tokens = []
	nltk_text = nltk.book.text1

	def __init__(self, sites_file: str="sites.txt", keep_to_sites: bool=False, search_limit: int=10):
		with open(sites_file, "r") as f:
			for site in f.readlines():
				sys.stderr.write("Working on: " + site + '\n')
				ws = Website(site)
				self.sites.append(ws)

		sys.stderr.write("Generating Text\n")
		for site in self.sites:
			for link in site.links:
				self.text += site._get_page_text(link)

		sys.stderr.write("Generating NLTK Text\n")
		self.tokens = nltk.word_tokenize(self.text)
		self.nltk_text = nltk.Text(self.tokens)

	def get_related_words(word: str):
		print(self.nltk_text.concordance(word))

