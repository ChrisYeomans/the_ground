from typing import List
from website import Website

class Ground:
	"""This class generates a number
	of Websites with the website class
	which it gets the entry points from
	the sites.txt file by default or
	another file if specified.
	This class also has a number of functions
	to get wensit text and compile lists of 
	links.
	"""

	sites = List[Website]
	def __init__(self, sites_file: str="sites.txt", keep_to_sites: bool=False):
