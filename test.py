from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import requests
import time


# Function for getting the links for each profile of a given product
def get_profiles(soup):
	return 

# Function to extract a Profile Name
def get_name(soup):
	nameList = []
	try:
		soup.find("div", id_="cm_cr-review_list")
		soup.find("div", class_="a-section review aok-relative")
		soup.find("div", class_="a-profile-content")
		dataString = ""
		for profile in soup.find_all("span", class_="a-profile-name"):
			#nameList = nameList + profile.find_all("span", class_="a-profile-name")
			#nameList.append(dataString)
			dataString = dataString + profile.get_text()
			nameList.append(dataString)
			dataString = ""

	except AttributeError:
		name = ""	

	return nameList

# Function to extract textual reviews
def get_review_txt(soup):
	reviewList= []
	try:
		#reviewTxt = soup.find("span", attrs={'class':'a-profile-name'}).string.strip()

		dataString = ""
		for review in soup.find_all("span", class_="a-size-base review-text review-text-content"):
			dataString = dataString + review.get_text()
			reviewList.append(dataString)
			dataString = ""
		
	except AttributeError:
		review_count = ""	

	return reviewList

def get_ratings_value(soup):
	starsList= []
	try:
		#reviewTxt = soup.find("span", attrs={'class':'a-profile-name'}).string.strip()

		dataString = ""
		for stars in soup.find_all("span", class_="a-icon-alt"):
			dataString = dataString + stars.get_text()
			starsList.append(dataString)
			dataString = ""
		
	except AttributeError:
		review_count = ""	
	
	return starsList

# Function to extract Product Title
def get_title(soup):
	
	try:
		# Outer Tag Object
		title = soup.find("span", attrs={"id":'productTitle'})

		# Inner NavigableString Object
		title_value = title.string

		# Title as a string value
		title_string = title_value.strip()

		# # Printing types of values for efficient understanding
		# print(type(title))
		# print(type(title_value))
		# print(type(title_string))
		# print()

	except AttributeError:
		title_string = ""	

	return title_string

# Function to extract Product Price
def get_price(soup):

	try:
		price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

	except AttributeError:
		price = ""	

	return price

# Function to extract Product Rating
def get_rating(soup):

	try:
		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
		
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
	try:
		review_count = soup.find("div", attrs={'class':'a-row a-spacing-base a-size-base'}).string.strip()
		
	except AttributeError:
		review_count = ""	

	return review_count

# Function to extract Availability Status
def get_availability(soup):
	try:
		available = soup.find("div", attrs={'id':'availability'})
		available = available.find("span").string.strip()

	except AttributeError:
		available = ""	

	return available	

if __name__ == '__main__':

	# Headers for request
	HEADERS = ({'User-Agent':
	            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	            'Accept-Language': 'en-US, en;q=0.5'})

	# The webpage URL
	URL = "https://www.amazon.com/product-reviews/B098FKXT8L/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&filterByStar=all_stars&reviewerType=all_reviews&pageNumber=1&sortBy=recent#reviews-filter-bar"

	# HTTP Request
	webpage = requests.get(URL, headers=HEADERS)

	# Soup Object containing all data
	soup = BeautifulSoup(webpage.content, 'lxml')

	driver = webdriver.Chrome(ChromeDriverManager().install())
	
	driver.get(URL)
	time.sleep(5)
	# Function calls to display all necessary product information
	#print("Profile Name of one reviewer = ", get_name(soup))


	profile_urls = []

	for h in soup.findAll("div", class_="a-row a-spacing-mini"):
		a = h.find('a')
		try:
			if 'href' in a.attrs:
				url = a.get('href')
				profile_urls.append("https://www.amazon.com" + url)
		except:
			pass

	for x in range(3, len(profile_urls)):
		print(profile_urls[x])

	namList = get_name(soup)


	#revList = get_review_txt(soup)


	#SCAN ALL PROFILES from the headphone's page
	t = 0
	for x in range(3, len(profile_urls)):

		driver.get(profile_urls[x])
		time.sleep(5)

		print("Current URL: " + driver.current_url)
		
		#webpage = requests.get(profile_urls[x])

		##NEEDED TO ADD THIS for soup to be updated to new page
		pg_src = driver.page_source

		print(webpage.status_code)
		soup = BeautifulSoup(pg_src, 'lxml')

		temp_title = soup.find("span", class_ ="a-size-extra-large")
		print("Profile User: " + t + " " temp_title.get_text())

		t = t +1

		time.sleep(5)

		##FIX THIS
		ratingsList = get_ratings_value(soup)

		
		for y in range(len(ratingsList)):
			print(ratingsList[y])

		#Now need a function that will get list of reviews from each profile

		#driver.back()
		time.sleep(5)

	#for x in range(len(revList)):
		#print(revList[x])

	print("\n")
	print("Product Title =", get_title(soup))
	print("Product Price =", get_price(soup))
	print("Product Rating =", get_rating(soup))
	print("Number of Product Reviews =", get_review_count(soup))
	print("Availability =", get_availability(soup))
	print()
	print()