import string
import math
import sys

"""Wejście:
        liczba dokumentów do przetworzenia (n)
        n dokumentów
        zapytanie (wielowyrazowe)
        linijka zer i jedynek wskazująca relewantne dokumenty
    Wyjście:
        lista wartości prawdopodobieństwa bycia relewantnym dla każdego
        dokumentu
    Założenia:
        tokenizacja analogicznie do poprzednich zadań, z ujednoliceniem
        wielkości liter, bez lematyzacji,
        wyniki zaokrąglone do 2 miejsc po przecinku
"""

def input_words(words):
    input_words = []
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    with open(words, 'r') as infile:
        for line in infile:
            line = line.lower().translate(translator)
            input_words.append(line.rstrip())
    return input_words

content =(input_words('tekst.txt'))
terms = content[int(content[0])+1].split()
relevance = content[int(content[0])+2].split()
relevance = [int(i) for i in relevance]
S = sum(relevance)
N = int(content[0])
list_of_occures = []
output = []
for term in terms:
    p = 0
    s = 0
    dfi = 0
    x = 0
    c = 0
    list_of_occures = []
    temp_output_list = []
    for sentence in range (1, int(content[0])+1):
        terms_in_sentence = content[sentence].split()

        if term in terms_in_sentence:
            dfi = dfi + 1
            list_of_occures.append(1)
            if relevance[sentence - 1] == 1:
                s = s + 1
        else:
            list_of_occures.append(0)
    p = s/S
    n = (dfi - s)/(N-S)
    x = (((s+0.5)/(S-s+0.5))/((dfi-s+0.5)/(N-dfi-S+s+0.5)))
    c = math.log(x,10)

    temp_output_list = [i*c for i in list_of_occures]
    if not output:
        output = temp_output_list
    else:
        output = [temp_output_list[i] + output[i] for i in range(0, len(temp_output_list))]

    output = [round(i,2) for i in output]
print(output)