from bs4 import BeautifulSoup
import requests
import time

# Function to extract Profile Name

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
	soup = BeautifulSoup(webpage.content, "lxml")

	# Function calls to display all necessary product information
	#print("Profile Name of one reviewer = ", get_name(soup))

	namList = get_name(soup)
	#revList = get_review_txt(soup)

	print(time.time())


	for x in range(len(namList)):
		print(namList[x])

	#for x in range(len(revList)):
		#print(revList[x])



	print("Product Title =", get_title(soup))
	print("Product Price =", get_price(soup))
	print("Product Rating =", get_rating(soup))
	print("Number of Product Reviews =", get_review_count(soup))
	print("Availability =", get_availability(soup))
	print()
	print()