import urllib.request
from urllib.parse import urlparse
import sys
from bs4 import BeautifulSoup
import numpy as np
np.set_printoptions(precision=4,suppress=True)

"""
Pobierz dokumenty zaczynając od podanego adresu, a następnie oblicz
ich PageRank.

Wejście:
    adres początkowej strony internetowej.
    
Wyjście:
    lista z wartościami miary PageRank dla dokumentów posortowanych
    wg adresu URL.

Założenia:
    przeprowadź proces crawlingu odszukując wszystkie dostępne strony rozpoczynając od zadanej,
    przy liczeniu PageRank przyjmij d = 0.85,
    wartości PageRank podaj z dokładnością do 4 miejsc po przecinku,
    przy metodzie iteracyjnej kontynuuj obliczenia dopóki zmiany w wartościach występują do 6 miejsca po przecinku.
"""

def make_soup(link):
    with urllib.request.urlopen(link) as response:
        page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    return soup


input_adres = 'http://150.254.36.78/SW-10/01-00.html'
parsed_uri = urlparse( input_adres)
domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)


to_search_list = []
links_list =[]
crawled =[]

main_page = make_soup(input_adres)
for link in main_page.find_all('a'):
    to_search_list.append(link.get('href'))
    if link not in links_list:
        links_list.append(link.get('href'))

#Example link for PageRank is http://150.254.36.78/SW-10/01-00.html
# bs parse url from html tag
while len(to_search_list) > 0:
    to_search_link = to_search_list.pop()
    try:
        to_search_link = make_soup(to_search_link)
    except ValueError:
        to_search_link = make_soup(domain + to_search_link)

    for link in to_search_link.find_all('a'):
        to_search_list.append(link.get('href'))
        crawled.append(link.get('href'))
        if link.get('href') not in links_list:
            links_list.append(link.get('href'))

    for crawled_link in crawled:
        if crawled_link in to_search_list:
            to_search_list.remove(crawled_link)

links_list.sort()
link_contain = {}
temp = []

for key_link in links_list:
    try:
        page = make_soup(key_link)
    except ValueError:
        page = make_soup(domain + key_link)

    for link in page.find_all('a'):
        temp.append(link.get('href'))
    link_contain[key_link] = temp
    temp = []

A = np.zeros((len(link_contain), len(link_contain)))
for key, value in link_contain.items():
    for link_from_value in value:
        key_index = links_list.index(key)
        value_index = links_list.index(link_from_value)
        A[key_index,value_index] = 1

reference_matrix = np.copy(A)
d = .85

for row in range(0, len(A)):
    if 1 not in A[row]:
        A[row] = 1/len(A)

for i in range(0, len(A)):
    for j in range(0, len(A)):
        if reference_matrix[i,j] == 1:
            A[i,j] = 1/np.sum(reference_matrix[i])
            A[i,j] = A[i,j] * d

for i in range(0, len(A)):
    for j in range(0, len(A)):
        if 1 in reference_matrix[i]:
            A[i,j] = A[i,j] + ((1 - d) * (1/len(A)))


y = np.array([1,0,0,0])
y2 = y.dot(A)
while not np.allclose(y2, y, rtol=1.e-6):
    y = y.dot(A)
    y2 = y.dot(A)
print(y2)