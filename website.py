from typing import List
import requests, bs4, sys, re

class Website:
	"""A class that will take a website's home page as an
	entry point and generates all of the links up to a limit
	that can be set on generation.
	This class will also have methods to get all relevant text
	from all of the gathered links.
	"""

	links = []
	home_page = ""
	def __init__(self, home_page: str, search_limit=10000):
		self.home_page = home_page
		self.links = self._get_links_list(search_limit)

	def _get_links_list(self, limit: int) -> List[str]:
		buffer_unfollowed_links = []
		unfollowed_links = []
		followed_links = []
		unfollowed_links = self._get_page_links(self.home_page)

		#basically just keep going until you hit the limit or you run out of links
		while True:
			try:
				for link in unfollowed_links:
					sys.stderr.write(str((len(followed_links) + len(unfollowed_links) + len(buffer_unfollowed_links))) + '\n')
					if limit and (len(followed_links) + len(unfollowed_links) + len(buffer_unfollowed_links) > limit):
						return followed_links + unfollowed_links + buffer_unfollowed_links

					buffer_unfollowed_links += self._get_page_links(link)
				
				followed_links += unfollowed_links # add links to followed
				unfollowed_links = buffer_unfollowed_links # move the buffer in
				buffer_unfollowed_links = [] # clear the buffer
				if limit and (len(followed_links) + len(unfollowed_links) > limit):
					return followed_links + unfollowed_links + buffer_unfollowed_links
				elif not unfollowed_links:
					return followed_links
			except KeyboardInterrupt as e:
				break

		return followed_links + unfollowed_links + buffer_unfollowed_links

	def _get_page_links(self, page: str) -> List[str]:
		out = []
		p = requests.get(page)
		s = bs4.BeautifulSoup(p.text, 'html.parser')
		links = s.find_all('a')
		for link in links:
			try:
				if link['href'][:4] == 'http':
					out.append(link['href'])
			except KeyError as e:
				sys.stderr.write(str(e)+'\n')
			except KeyboardInterrupt as e:
				break
		return out

	def _get_page_text(self, page_link):
		p = requests.get(page_link)
		soup = bs4.BeautifulSoup(p.text, 'html.parser')
		[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title', 'li', 'footer'])]
		return '\n'.join(e.strip() for e in soup.getText().split('\n') if e.strip())


if __name__ == "__main__":
	ws = Website("https://www.independent.ie/")
	sys.stderr.write("printing\n")
	for link in ws.links:
		print(ws._get_page_text(link))
	