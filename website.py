from typing import List

class Website:
	"""A class that will take a website's home page as an
	entry point and generates all of the links up to a limit
	that can be set on generation.
	This class will also have methods to get all relevant text
	from all of the gathered links.
	"""

	links = []
	home page = ""
	def __init__(self, home_page: str, search_limit=100):
		self.home_page = home_page
		self.links = self._get_links_list(search_limit)

	def _get_links_list(self, limit: int) -> List[str]:
		buffer_unfollowed_links = []
		unfollowed_links = []
		followed_links = []
		unfollowed_links = self._get_page_links(self.home_page)

		#basically just keep going until you hit the limit or you run out of links
		while (len(followed_links + unfollowed_links + buffer_unfollowed_links) < limit)
			or not (buffer_unfollowed_links or unfollowed_links or followed_links):
			for link in unfollowed_links:
				buffer_unfollowed_links += self._get_page_links(link)
			
			followed_links += unfollowed_links # add links to followed
			unfollowed_links = buffer_unfollowed_links # move the buffer in
			buffer_unfollowed_links = [] # clear the buffer

		return followed_links + unfollowed_links + buffer_unfollowed_links

	def _get_page_links(self, page: str) -> List[str]:


if __name__ == "__main__":
	ws = Website("www.reddit.com")
