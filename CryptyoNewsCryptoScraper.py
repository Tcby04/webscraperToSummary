import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

print('Gathering URL\'s....')

url = 'https://cryptonews.com/'
response = requests.get(url)
text = response.text
data = BeautifulSoup(text, 'html.parser')

# Find all the article tags on the page
article_tags = data.find_all('article')

# Extract and print the links to the first 10 articles that have "/news" in their URLs
count = 0  # Initialize a counter
with open('links.txt', 'w') as file:
    with tqdm(total=min(len(article_tags), 10), unit='article') as pbar:
        for article in article_tags:
            article_link = article.find('a', href=True)
            if article_link:
                article_url = urljoin(url, article_link['href'])
                if '/news' in article_url:
                   # print(f"Article {count + 1} URL: {article_url}")
                    file.write(f" {article_url}\n")
                    count += 1
                    pbar.update(1)
                    if count >= 10:
                        break  # Stop after processing the first 10 articles

print("URLs have been Found")
print ('\n') 
