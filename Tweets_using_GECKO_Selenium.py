from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

# Path to GeckoDriver
firefox_service = FirefoxService(executable_path=r'C:\Users\rohan\Python 3.12\geckodriver.exe')

# Set up Firefox options
options = Options()

# Initialize WebDriver
driver = webdriver.Firefox(service=firefox_service, options=options)

def login_twitter(username, password):
    # Navigate to Twitter login page
    driver.get('https://twitter.com/login')
    
    # Wait for the page to load
    time.sleep(5)
    
    # Find and fill the username and password fields
    try:
        username_field = driver.find_element(By.NAME, 'text')
        username_field.send_keys(username)
        username_field.send_keys(Keys.RETURN)
        time.sleep(5)
        
        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(10)  # Wait for login to complete
    except Exception as e:
        print("Error during login:", e)
    
def scrape_tweets(search_query, num_tweets, output_file):
    # Open Twitter and perform the search
    driver.get(f'https://twitter.com/search?q={search_query}&f=live')
    
    # Wait for the page to load
    time.sleep(5)
    
    tweets = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while len(tweets) < num_tweets:
        # Scroll down to load more tweets
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        
        # Find tweet elements
        tweet_elements = driver.find_elements(By.CSS_SELECTOR, 'article div[lang]')
        
        for tweet_element in tweet_elements:
            if len(tweets) >= num_tweets:
                break
            try:
                tweet_text = tweet_element.text
                tweets.append(tweet_text)
            except Exception as e:
                print("Error extracting tweet:", e)
        
        # Check if the end of the page is reached
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Save tweets to a file
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Tweet"])
        for tweet in tweets:
            writer.writerow([tweet])
    
    print(f"Scraped {len(tweets)} tweets and saved to {output_file}")

# Prompt for Twitter credentials
username = input("Enter your Twitter username: ")
password = input("Enter your Twitter password: ")

# Login and scrape tweets
login_twitter(username, password)
scrape_tweets('Python', 100, 'tweets.csv')

# Clean up
driver.quit()
