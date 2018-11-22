import numpy
import string
"""
Przygotuj program, który na wejściu będzie przyjmował dwa
jednowyrazowe termy (w osobnych linijkach), a jako rezultat będzie
oddawał liczbę całkowitą oznaczającą wartość miary Levenshteina
pomiędzy podanymi termami.
"""

def input_words(words):
    input_words = []
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    with open(words, 'r') as infile:
        for line in infile:
            line = line.lower().translate(translator)
            input_words.append(line.rstrip())
    return input_words

def levenshtein(tutajinput):

    list_of_words = input_words(tutajinput)
    n = len(list_of_words[0])
    m = len(list_of_words[1])
    first_word = numpy.array(tuple(list_of_words[0]))
    second_word = numpy.array(tuple(list_of_words[1]))

    if n > m:
        first_word = second_word
        second_word = first_word

    first_row = numpy.arange(n + 1)
    for i in second_word:
        next_row = first_row + 1
        next_row[1:] = numpy.minimum(next_row[1:], numpy.add(first_row[:-1], second_word != first_word))
        next_row[1:] = numpy.minimum(next_row[1:], next_row[0:-1] + 1)
        first_row = next_row
    return first_row[-1]

print(levenshtein('przyklad.txt'))



