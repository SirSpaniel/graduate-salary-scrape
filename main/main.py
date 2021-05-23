import requests
from bs4 import BeautifulSoup
from time import sleep

# Initial URL
URL = 'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors'

# Get HTML data
response = requests.get(URL)
website_html = response.text

# Initialise BeautifulSoup
soup = BeautifulSoup(website_html, "html.parser")

# Find number of pages
page_buttons = soup.find_all(name='a', class_='pagination__btn')
num_of_pages = int(page_buttons[-2].getText())
page = 1

# Create lists
major = []
early_career = []
mid_career = []
meaning = []

# Go through all all pages of data
print('Scraping...')

while page <= num_of_pages:
    # Changing URL for different pages
    url = f'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/{page}'
    response = requests.get(url)
    website_html = response.text

    # Initialise BeautifulSoup
    soup = BeautifulSoup(website_html, "html.parser")
    # Find names of all majors and append to list
    majors = soup.find_all(name='td', class_='csr-col--school-name')
    major_list = [major.getText().replace('Major:', '') for major in majors]
    # All other stats are group together
    # Make list of all stats and find select data via comprehension
    stats = soup.find_all(name='td', class_='csr-col--right')
    early_career_list = [int(early.getText().replace('Early Career Pay:$', '').replace(',', '')) for early in stats
                         if m'Early' in early.getText()]
    mid_career_list = [int(mid.getText().replace('Mid-Career Pay:$', '').replace(',', '')) for mid in stats
                       if 'Mid' in mid.getText()]
    meaning_list = [meaning.getText().replace('% High Meaning:', '').replace('-', '') for meaning in stats
                    if 'High' in meaning.getText()]

    # Add data from local lists to global lists
    for item in major_list:
        major.append(item)
    for item in early_career_list:
        early_career.append(item)
    for item in mid_career_list:
        mid_career.append(item)
    for item in meaning_list:
        meaning.append(item)

    # Increment page and sleep (reduce number of requests per second)
    page += 1
    sleep(0.5)

print('Complete!')

print('Creating csv...')

# Write data from lists to csv file
with open('graduate_salary_data.csv', 'w') as csv:
    csv.write('Major,Early Career Pay,Mid-Career Pay,% High Meaning\n')
    for n in range(len(major)):
        csv.write(f'{major[n]},{early_career[n]},{mid_career[n]},{meaning[n]}\n')

print('Complete!')
