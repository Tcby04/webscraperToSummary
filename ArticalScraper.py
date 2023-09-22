import requests
from bs4 import BeautifulSoup

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

# Read links from the text file
with open('links.txt', 'r') as file:
    links = file.read().splitlines()

# Create a new document to store the scraped text
with open('scraped_text.txt', 'w', encoding='utf-8') as output_file:
    for link in links:
        # Scrape title and text from the link
        scraped_title, scraped_text = scrape_text_and_title_from_url(link.strip())
        
        if scraped_text:
            # Write the article title and scraped text to the output document
            output_file.write(f"Title: {scraped_title}\n")
            output_file.write(scraped_text)
            output_file.write('\n\n')

print("Scraping and writing complete.")
