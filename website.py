from typing import List
import requests, bs4, sys

class Website:
	"""A class that takes a website's home page as an
	entry point and generates all of the links up to a
	predefined limit which can be changed or made
	unlimited by setting it to 0
	"""

	seen_links = {}
	links = []
	home_page = ""

	def __init__(self, home_page: str, search_limit: int=100, keep_to_site: bool=False):
		self.home_page = home_page
		self.links = self._get_links_list(search_limit, keep_to_site)

	"""def __init__(self, home_page: str, links: List[str]):
		self.links = links
		for link in links:"""


	def _get_links_list(self, limit: int, keep_to_site: bool) -> List[str]:
		buffer_unfollowed_links = []
		unfollowed_links = []
		followed_links = []
		unfollowed_links = self._get_page_links(self.home_page, keep_to_site)

		# basically just keep going until you hit the limit or you run out of links
		while True:
			try:
				for link in unfollowed_links:
					# exit if we have exceeded the limit
					if limit and (len(followed_links) + len(unfollowed_links) \
						+ len(buffer_unfollowed_links) > limit):
						return followed_links + unfollowed_links + buffer_unfollowed_links

					# filling the buffer of unfollowed links
					buffer_unfollowed_links += self._get_page_links(link, keep_to_site)
				
				followed_links += unfollowed_links # add links to followed
				unfollowed_links = buffer_unfollowed_links # move the buffer in
				buffer_unfollowed_links = [] # clear the buffer
				if limit and (len(followed_links) + len(unfollowed_links) > limit):
					return followed_links + unfollowed_links + buffer_unfollowed_links
				elif not unfollowed_links:
					return followed_links
			# allows for early exit of link gathering
			except KeyboardInterrupt as e:
				break

		return followed_links + unfollowed_links + buffer_unfollowed_links

	def _get_page_links(self, page: str, keep_to_site: bool) -> List[str]:
		out = []
		p = requests.get(page, verify=False)
		s = bs4.BeautifulSoup(p.text, 'html.parser')
		links = s.find_all('a')
		for link in links:
			try:
				# makes sure is a valid link and not
				# a mailto or some other weird format
				if link['href'][:4] == 'http' and link['href'] not in self.seen_links:
					if not keep_to_site or page.split(".")[1] == link.split(".")[1]:
						self.seen_links[link['href']] = 1
						out.append(link['href'])
			# link tag might not have a href
			except KeyError as e:
				sys.stderr.write(str(e)+'\n')
			# allows for early exit of link gathering
			except KeyboardInterrupt as e:
				break
		return out

	def get_page_text(self, page_link: str) -> str:
		p = requests.get(page_link, verify=False)
		soup = bs4.BeautifulSoup(p.text, 'html.parser')
		[s.extract() for s in soup( \
				['style', 'script', '[document]', 'head', 'title',
				'footer', 'li', 'table', 'h1', 'h2', 'h3', 'h4',
				'h5', 'h6', 'navbar', 'meta', 'link', 'noscript',
				'a', 'nav', 'button', 'form'])]
		return '\n'.join(e.strip() for e in soup.getText().split('\n') if \
			len(e.strip().split()) > 1)


if __name__ == "__main__":
	ws = Website("https://www.independent.ie/")
	sys.stderr.write("printing\n")
	for link in ws.links:
		print(ws._get_page_text(link))
