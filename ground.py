from typing import List
from website import Website
from nltk.sentiment.vader import SentimentIntensityAnalyzer
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
	lemmatized_tokens = []
	tagged = {}
	nltk_text = nltk.book.text1
	stop_words = set()

	def __init__(self, text_file: str="", sites_file: str="sites.txt", keep_to_sites: bool=False, search_limit: int=10):
		if text_file == "":
			sys.stderr.write("Generating Text\n")
			self.generate_text(sites_file, search_limit, keep_to_sites)
		else:
			with open(text_file, "r") as f:
				self.text = f.read()

		sys.stderr.write("Pre Processing\n")
		self.pre_processing()
		

	def pre_processing(self):
		# Filtering stop words
		self.stop_words = set(nltk.corpus.stopwords.words('english'))
		self.tokens = [w for w in nltk.word_tokenize(self.text) if not w in self.stop_words]

		# Generating nltk text
		self.nltk_text = nltk.Text(self.tokens)

		# Tagging NLTK Text
		self.tagged = nltk.pos_tag(self.tokens)
	
	def lemmatize_tokens(self):
		lemmatize_tokens = tokens[:]
		ltz = nltk.stem.WordNetLemmatizer()
		for i in range(len(self.tokens)):
			self.lemmatized_tokens[i] = ltz.lemmatize(self.tagged[i][0], get_wordnet_pos(self.tagged[i][1]))

	def generate_text(self, sites_file, search_limit, keep_to_sites):
		with open(sites_file, "r") as f:
			for site in f.readlines():
				sys.stderr.write("Working on: " + site + '\n')
				ws = Website(home_page=site, search_limit=search_limit, keep_to_site=keep_to_sites)
				self.sites.append(ws)

		for site in self.sites:
			for link in site.links:
				self.text += site.get_page_text(link)

	def write_out_text(self, file_name: str="text.txt"):
		with open(file_name, "w") as f:
			f.write(self.text)

	def get_related_words(self, word: str):
		print(self.nltk_text.concordance(word))

	def get_sentiment(self, term: str):
		# using Vader sentiment analysis
		sents = [e for sl in [s.split('.') for s in self.text.split('\n')] for e in sl]
		out = 0
		tick = 0
		sid = SentimentIntensityAnalyzer()
		for sent in sents:
			if term in sent.lower():
				tick += 1
				print(sent)
				ss = sid.polarity_scores(sent)
				print(ss)
				out += ss['compound']
		if tick:
			print(out/tick)
		else:
			print(0)

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": nltk.corpus.wordnet.ADJ,
                "N": nltk.corpus.wordnet.NOUN,
                "V": nltk.corpus.wordnet.VERB,
                "R": nltk.corpus.wordnet.ADV}

    return tag_dict.get(tag, nltk.corpus.wordnet.NOUN)

if __name__ == "__main__":
	gd = Ground(keep_to_sites=True, search_limit=1)
	gd.get_sentiment("trump")
	