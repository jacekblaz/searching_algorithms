import sys
"""Wejście:
        liczba testowanych wyszukiwarek (n)
        n linijek z wynikami wyszukiwania z każdej wyszukiwarki w postaci listy
        identyfikatorów dokumentów oddzielonych spacjami
        linijka z ocenami relewancji dokumentów:
            w linijce lista zer i jedynek,
            k-ty element w linijce wskazuje czy dokument o identyfikatorze k jest
            relewantny (1) czy nie (0)
"""
"""
Wyjście:
        n linijek w postaci list, zawierających kolejno:
            precyzję,
            względną pełność,
            miarę F2,
            średnią precyzję,
    Założenia:
        wartości zaokrąglone do 2 miejsc po przecinku,
"""

""""change lines of str to list of int"""
def opener(inp):
    output_list = []
    with open(inp, 'r') as infile:
        for line in infile:
            temp = line.rstrip()
            temp = temp.split()
            output_list.append([int(i) for i in temp])
            temp.clear()
    return output_list


""""how many of found are relevant"""
def precision(search, relevance):
    obtained = 0
    for i in range (0, len(search)):
        if relevance[search[i]] == 1:
            obtained += 1
    precision_out = obtained / len(search)
    return round(precision_out,2)


"""""how many of obtained relevant compare to all relevant found by all searching engines"""
def relativerecall(search, relevance, all_searches):
    obtained_by_search = 0
    for i in range(0, len(search)):
        if relevance[search[i]] == 1:
            obtained_by_search += 1

    obtained_by_all = 0
    all_searches = list(set(all_searches))
    for i in range(0, len(all_searches)):
        if relevance[all_searches[i]] == 1:
            obtained_by_all += 1

    return round(obtained_by_search / obtained_by_all,2)


def recall(search, relevance):
    obtained_by_search = 0
    for i in range(0, len(search)):
        if relevance[search[i]] == 1:
            obtained_by_search += 1
    relevance = sum(relevance)
    return round(obtained_by_search / relevance, 2)


def ftwo(search, relevance):
    return round((3*(precision(search, relevance)*recall(search, relevance)))/((2*precision(search, relevance))+recall(search, relevance)), 2)


def precisionavg(search, relevance):
    avg = 0
    recall = 0
    for i in range(0, len(search)):
        if relevance[search[i]] == 1:
            precision = 1/(i+1)
            recall += 1
            avg += precision
            precision = 0

    avg = avg /recall
    return round(avg, 2)


input_file = opener('test.txt')
relevance = input_file[-1]
list_of_result = []
all_searches = []
for searching_engine in range(1, input_file[0][0]+1):
    all_searches += input_file[searching_engine]

for searching_engine in range(1, input_file[0][0]+1):
    list_of_result.append(precision(input_file[searching_engine], relevance))
    list_of_result.append(relativerecall(input_file[searching_engine], relevance,all_searches))
    list_of_result.append(ftwo(input_file[searching_engine], relevance))
    list_of_result.append(precisionavg(input_file[searching_engine], relevance))

    print(list_of_result)
    list_of_result.clear()