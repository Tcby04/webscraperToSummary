
import requests
from bs4 import BeautifulSoup
import time


url = 'https://finance.yahoo.com/crypto/'
response = requests.get(url)
text = response.text
data = BeautifulSoup(text, 'html.parser')



# since, headings are the first row of the table
headings = data.find_all('tr')[0]
headings_list = [] # list to store all headings

for x in headings:
	headings_list.append(x.text)
# since, we require only the first ten columns
headings_list = headings_list[:10]

print('Headings are: ')
for column in headings_list:
	print(column)


# since we need coins
for x in range(1, 26):
    table = data.find_all('tr')[x]
    c = table.find_all('td')
      
    for x in c:
        print(x.text, end=' ')
    print('')