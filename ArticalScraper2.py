import os
import requests
from bs4 import BeautifulSoup
import datetime

# Function to clean non-ASCII characters from a string
def clean_non_ascii(text):
    return ''.join(char for char in text if ord(char) < 128)

# Function to scrape text and title from a URL
def scrape_text_and_title_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for a successful response
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the title of the article from the <h1> tag in the HTML
        h1_tag = soup.find('h1')
        title = h1_tag.get_text() if h1_tag else "No title found"
        
        # Clean non-ASCII characters from the title
        title = clean_non_ascii(title)

        # Extract the text content from the HTML
        text = ' '.join([p.get_text() for p in soup.find_all('p')])

        # Remove specific words from the text
        words_to_remove = ["A quick 3min read about today's crypto news!"]
        for word in words_to_remove:
            text = text.replace(word, '')

        return title, text
    except requests.exceptions.RequestException as e:
        print(f"Error while scraping {url}: {e}")
        return None, None

# Create a directory with today's date as the name
output_directory = datetime.date.today().strftime("%Y-%m-%d")
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Read links from the text file
with open('links.txt', 'r') as file:
    links = file.read().splitlines()

# Scrape and save each article in the output directory with the title as the filename
for link in links:
    # Scrape title and text from the link
    scraped_title, scraped_text = scrape_text_and_title_from_url(link.strip())
    
    if scraped_text:
        # Clean the title for use as a filename
        cleaned_title = clean_non_ascii(scraped_title)
        
        # Create a file for the article content
        article_filename = os.path.join(output_directory, f"{cleaned_title}.txt")
        with open(article_filename, 'w', encoding='utf-8') as article_file:
            article_file.write(scraped_text)

print("Scraping and writing complete.")
