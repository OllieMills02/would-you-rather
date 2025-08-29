from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager



def scrape_all_titles():
    # Setup Chrome options to run in headless mode (no UI)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver_service = Service(ChromeDriverManager().install())

    # Launch the browser
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)

    # Navigate to the Reddit URL
    driver.get('https://www.reddit.com/r/WouldYouRather/')

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Give time for the new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Get the rendered HTML content
    content = driver.page_source

    # Close the browser
    driver.quit()

    # Now, parse the content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    print(soup.prettify())

    # Use a generic selector that is likely to be stable
    # The new selector is likely a class or data attribute on the title elements
    all_titles = soup.find_all('a', attrs={'slot': 'title'})

    if all_titles:
        for title in all_titles:
            print(title.text.strip())
    else:
        print("No post titles found.")


