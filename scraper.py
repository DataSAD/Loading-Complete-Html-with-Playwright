from bs4 import BeautifulSoup
import lxml
import pandas as pd
import openpyxl

my_dict = {'artist': [],
           'title': [],
           'cert_date': [],
           'label': [],
           'format': [],
           'rel_date': [],
           'prev_cert': [],
           'category': [],
           'type': [],
           'cert_units': [],
           'genre': []}

with open('page_html.txt', 'r') as f:
    html_text = f.read()

soup = BeautifulSoup(html_text, 'lxml')

top_list = soup.find_all('tr', id=lambda x: x and x.startswith('recent_42'))
print(f'top list length = {len(top_list)}')
bottom_list = soup.find_all('div', id=lambda x: x and x.startswith('recent_42'))
print(f'bottom list length = {len(bottom_list)}')

for top_item, bottom_item in zip(top_list, bottom_list):
    # TOP
    artist_element = top_item.find('td', class_='artists_cell')
    next_siblings = artist_element.find_next_siblings()

    artist = artist_element.text.strip()
    my_dict['artist'].append(artist)

    title = next_siblings[0].text.strip()
    my_dict['title'].append(title)

    cert_date = next_siblings[1].text.strip()
    my_dict['cert_date'].append(cert_date)

    label = next_siblings[2].text.strip()
    my_dict['label'].append(label)

    format = next_siblings[3].text.replace('MORE DETAILS', '').strip()
    my_dict['format'].append(format)

    # BOTTOM

    parent_tr = bottom_item.find('tr', class_='content_recent_table')
    children = list(parent_tr.children)

    rel_date = children[0].text.strip()
    my_dict['rel_date'].append(rel_date)

    prev_cert = children[1].text.replace('&nbsp;', '').strip()
    tables = bottom_item.find_all('tr', class_='content_recent_table')

    for item in tables[1:]:
        prev_cert += ('      ' + item.find('td', class_='col-md-5').text.replace('&nbsp;', ''))

    my_dict['prev_cert'].append(prev_cert)

    category = children[2].text.replace('&nbsp;', ' ').strip()
    my_dict['category'].append(category)

    type = children[3].text.strip()
    my_dict['type'].append(type)

    cert_units = children[4].text.strip()
    my_dict['cert_units'].append(cert_units)

    genre = children[5].text.strip()
    my_dict['genre'].append(genre)


df = pd.DataFrame(my_dict)
df.to_excel('results.xlsx')




