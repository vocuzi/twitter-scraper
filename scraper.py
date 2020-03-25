from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import os
import sys
import json
import pandas

def get_tweets(keyword,count=10):
	url = f"https://mobile.twitter.com/search?q={keyword}&s=typd"
	tweets, payload = [],[]
	chromedriver = os.getcwd()+"/chromedriver"
	options = Options()
	driver = webdriver.Chrome(chromedriver, options=options)
	driver.get(url)
	time.sleep(3)
	tweets = driver.find_elements_by_css_selector("div[aria-label='Timeline: Search timeline'] > div > div article")
	def fetch_from_tweets(tweets):
		for tweet in tweets:
			try:
				text = tweet.text.split("\n")
				media = [img.get_attribute("src") for img in tweet.find_elements_by_tag_name("img")][1:]
				temp = {
					"name":text[0],
					"username":text[1],
					"retweets":text[-2],
					"comments":text[-3],
					"likes":text[-1],
					"media":media,
					"text":"\n".join(text[4:][:-3])
				}
				payload.append(temp)
			except Exception as e:
				print("Err ",e)
				continue
	fetch_from_tweets(tweets)
	for i in range(0,count):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(3)
		tweets = driver.find_elements_by_css_selector("div[aria-label='Timeline: Search timeline'] > div > div > div")
		fetch_from_tweets(tweets)
		print("Scrolled again ...")
	return payload

if __name__ == "__main__":
	keyword = input("Keyword to Query : ")
	count = int(input("No. of Pages to Scrape : "))
	tweets = get_tweets(keyword,count)
	json.dump(tweets,open(f"{keyword}.json","w"))
	pandas.read_json(f"{keyword}.json").to_excel(f"{keyword}.xlsx")