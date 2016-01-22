import requests
import re
import time
from bs4 import BeautifulSoup
import sys

def filter_links(links,base_link):
	regexp='(.*):(.*)|(.*)Main_Page(.*)|(.*)'+base_link+'(.*)'
	regex=re.compile(regexp)
	links=[link for link in links if not regex.match(link[3])]
	return links

def get_body_content(r):
	soup=BeautifulSoup(r.text,"html.parser")
	#ignore_list=['style','script','head','html','[document]']
	ignore_list=['style','script','html','[document]']
	body=''.join(text for text in soup.find_all(text=True)
              if text.parent.name not in ignore_list)
	return body

def crawl_link(page_source,link):	
	links=re.findall(r'href="(http(s)?://)?(/*)(wiki/.*?)"',page_source.text)
	links=filter_links(links,link)
	return links

def check_if_keyword_present(page_source,link,keyword):
	search_regex='(?is)'+keyword
	regexp=re.compile(search_regex)
	body_content=get_body_content(page_source)
	if re.search(regexp,body_content):
		return True
	else:
		return False

def remove_duplicates(queue):
	unique_list=set()
	return [unique_list.add(element) or element for element in queue if element not in unique_list]

def main(argv):
	start_time=time.time()
	if argv:
		keyword=argv[0]
	else:
		keyword=""
	links_visited=[]
	seed_page="wiki/Hugh_of_Saint-Cher"
	page_queue=[]
	page_queue.append(seed_page)
	relevant_pages=[]
	depth=1
	next_level_queue=[]
	#links_crawled=[]
	is_seed_page=1
	while page_queue and len(links_visited) < 1000:
		time.sleep(1)
		links=[]
		r=requests.get('http://en.wikipedia.org/'+page_queue[0])
		is_keyword_present=check_if_keyword_present(r,page_queue[0],keyword)
		if is_keyword_present or is_seed_page==1 :
			links=crawl_link(r,page_queue[0])
		links_visited.append(page_queue[0])
		if is_keyword_present:
			relevant_pages.append(page_queue[0]) 
		for link in links:
			curr_link=link[3]
			if curr_link not in page_queue:
				next_level_queue.append(link[3])
		del page_queue[0]
		if not page_queue and (depth < 5):
			next_level_queue=remove_duplicates(next_level_queue)
			depth=depth+1
			for link in next_level_queue:
				if link not in links_visited:
					page_queue.append(link) 
			del next_level_queue[:]
		is_seed_page=0
	print("########################### Relevant pages######################")
	for pages in relevant_pages:
		print("https://en.wikipedia.org/"+pages)
	print("################################################################")
	print("Run completed in --- %s seconds ---" % (time.time() - start_time))

main(sys.argv[1:])
