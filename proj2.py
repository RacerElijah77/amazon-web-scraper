from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import random

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

#Retrieve the ratings made by each user of multiple products
def get_ratings_value(soup):
	starsList= []
	try:

		dataString = ""
		for stars in soup.find_all("i", class_="profile-at-review-stars"):
			dataString = dataString + stars.get_text()

			getValue = float(dataString[0])

			starsList.append(getValue)
			dataString = ""

	except AttributeError:
		review_count = ""	
	
	return starsList

#Function to get the review header text in a user profile
def get_review_text_each_user(soup):
	reviewList= []
	try:

		dataString = ""
		for revs in soup.find_all("h1", class_="a-size-base a-spacing-none a-color-base profile-at-review-title a-text-bold"):
			dataString = dataString + revs.get_text()
			reviewList.append(dataString)
			dataString = ""

	except AttributeError:
		review_count = ""	
	
	return reviewList

#function to get the Adjusted average review score for each user
def get_persons_avg(list):
	avg = 0.0
	sum = 0.0
	listSize = len(list)

	for i in range(0, listSize):
		sum = sum + list[i]

	avg = sum / listSize

	return avg 
	

# Function to extract Product Title
def get_title(soup):
	
	try:
		# Outer Tag Object
		title = soup.find("h1", attrs={"class":'a-size-large a-text-ellipsis'})

		# Inner NavigableString Object
		title_value = title.string

		# Title as a string value
		title_string = title_value.strip()

	except AttributeError:
		title_string = ""	

	return title_string


# Function to extract Product Rating
def get_rating(soup):

	try:
		# Outer Tag Object
		productRating = soup.find("span", attrs={"class":'a-size-medium a-color-base'})

		# Inner NavigableString Object
		rating_value = productRating.string

		# Title as a string value
		title_string = rating_value.strip()

	except AttributeError:
		title_string = ""	

	return title_string

# Function to extract Number of User Reviews
def get_review_count(soup):
	try:
		review_count = soup.find("div", attrs={'class':'a-row a-spacing-base a-size-base'}).string.strip()
		
	except AttributeError:
		review_count = ""	

	return review_count

if __name__ == '__main__':

	# Headers for request (MAY NEED TO CHANGE if using a different OS)
	HEADERS = {
				'User-Agent':
	            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	            'Accept-Language': 'en-US, en;q=0.5'
			}

	# The starting webpage URL
	URL = "https://www.amazon.com/product-reviews/B09DD2TLYN/ref=acr_dp_hist_5?ie=UTF8&filterByStar=five_star&reviewerType=all_reviews#reviews-filter-bar"

	# HTTP Request
	webpage = requests.get(URL, headers=HEADERS)

	time.sleep(random.randint(4, 7))
	
	# Soup Object containing all data (FIX WHY IT Crashes)
	soup = BeautifulSoup(webpage.content, 'lxml')
	
	#Print HTTP status code when the website loads
	print("Status Code: " + webpage.status_code)

	driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
	driver.get(URL)
	
	time.sleep(random.randint(3, 7))
	

	# Printing out overall rating and product title of product
	print("*****BASIC PRODUCT INFORMATION*****")
	print("Product Title = " + get_title(soup))
	print("Product Rating = " + get_rating(soup)) 
	print()
	print()


	print("*****PRODUCT REVIEWS*****")
	print()
	prod_review_list = get_review_txt(soup)

	for i in prod_review_list:
		print(i)
		print()

	print()

	#Loop that will scrap each of the URLS of a user who placed a review of this product (Headphones)
	profile_urls = []
	for h in soup.findAll("div", class_="a-row a-spacing-mini"):
		a = h.find('a')
		try:
			if 'href' in a.attrs:
				url = a.get('href')
				profile_urls.append("https://www.amazon.com" + url)
		except:
			pass

	print("*****Profile Links to be scrapped and analyzed*****")
	for x in range(3, len(profile_urls)):
		print(profile_urls[x])

	namList = get_name(soup)


	

	#temporary lists that will be used for summary processing
	prof_name_list = []
	adj_ratings_list = []
	biased_list = []
	t = 0
	for x in range(3, len(profile_urls)):

		driver.get(profile_urls[x])
		time.sleep(random.randint(3, 7))

		print("Current URL: " + driver.current_url)
		

		##NEEDED TO ADD THIS for soup to be updated to new page
		pg_src = driver.page_source

		#Print Status code if request to Amazon has been satisfied
		print("Status Code: " + webpage.status_code)
		soup = BeautifulSoup(pg_src, 'lxml')

		#obtain, store, and print the profile user name
		temp_title = soup.find("span", class_ ="a-size-extra-large")
		print("User to analyze: " + temp_title.get_text() + " (ID: " + str(t) + ")" )
		prof_name_list.append(temp_title.get_text())

		t = t +1

		time.sleep(random.randint(3, 7))


		ratingsList = get_ratings_value(soup)
		eachRevList = get_review_text_each_user(soup)


		print("Reviews and Ratings made from " + temp_title.get_text() + " (out of 5 stars) ")
		for y in range(len(ratingsList)):
			print(ratingsList[y])
			print(eachRevList[y])
			print()

		currentAvg = get_persons_avg(ratingsList)
		print("Reviewer's Average (adjusted average score of the reviewer): ", currentAvg)
		adj_ratings_list.append(currentAvg)

		likelyBiased = False

		#Code that determines whether or not the reviewier is biased or not
		for y in range(len(eachRevList)):
			if( (currentAvg < 1.5 or currentAvg > 4.8) and (len(eachRevList[y]) < 10) ):
				likelyBiased = True
			else:
				likelyBiased = False

		if(likelyBiased):
			print("The following reviewer " + temp_title.get_text() + " is likely biased\n")
		else:
			print("The following reviewer " + temp_title.get_text() + " is likely NOT biased\n")

		biased_list.append(likelyBiased)

		time.sleep(random.randint(3, 7))

	
	print("*****SUMMARY*****")
	print("Profiles scrapping information:\n")
	for y in range(len(prof_name_list)):
		print("Username: " + prof_name_list[y] + "\n" + "Adjusted average review score: " + str(adj_ratings_list[y]) + "\n" + "Likely biased? " + str(biased_list[y]) + "\n")

	
	