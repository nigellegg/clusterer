# -*- coding: utf-8 -*-
# usedata tasks - cluster code
# copyright 2014 Chibwe Ltd

import gspread
import nltk
from nltk.cluster import GAAClusterer
from nltk.cluster import euclidean_distance
import hcluster as hcluster
import numpy as np
import csv
import itertools
import re


def get_words(textsb):
    return [word.lower() for word in re.findall('\w+', textsb)]


def filtered_text(text):
    text2 = ''
    for x in text:
        if ord(x) < 32 or ord(x) > 126:
            x = ''
        else:
            x = x
        text2 = text2+x
    text = text2.lower()
    return text


def make_listwords(texts):
    ListWordsA = []
    textsb = []
    for text in texts:
        #if text == '':
        #    break
        text = filtered_text(text)
        text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
        text = re.sub(re.compile("u'\u2022'", re.UNICODE), ' ', text)
        textsb.append(text+'\n')
    words = get_words(str(textsb))
    ListWordsA.append(words)
    ListWords = []
    #ListWords = list(itertools.chain(*ListWordsA))
    #print 'ListWordsA :\n'+str(ListWordsA)
    x = 0
    for list in ListWordsA:
        for word in list:
            x = 0
            for word1 in ListWords:
                if word == word1:
                    x = 1
                    break
            if x == 0:
                ListWords.append(word)
    return ListWords


def vectorspaced(text, ListWords):
    text = filtered_text(text)
    #print('text = ', text)
    text_words = str(text).split(' ')
    components = [word.lower() for word in text_words]
    vect = np.array([
        word in components for word in ListWords])
    #print('vect = ', vect)
    return vect


def AverageLength(data):
    tokes = []
    i = 0
    while i < 100:
        text = filtered_text(data[i])
        tokens = str(text).split(' ')
        x = len(tokens)
        tokes.append(x)
        i += 1
    ave = sum(tokes)/len(tokes)
    return ave


def run_clusters(setupid):
    data = open('text.txt', 'r')
    text_len = AverageLength(data)
    if text_len < 10:
        run_sort(data, wks, clustcol)
    else:
        texts = data
        notext = len(texts)
        #cluster = GAAClusterer(20)
        #noclusters = 20
        ListWords = make_listwords(texts)
        #print ListWords
        tree = hcluster.hcluster([vectorspaced(text, ListWords) for text in texts], distance=hcluster.L2dist)
        print tree
        #cluster.cluster([vectorspaced(text, ListWords) for text in texts])
        #classified_examples = [
        #    cluster.classify(vectorspaced(text, ListWords)) for text in texts]
        print 'texts clustered'
        i = 1
        colx = []
        while i < notext+1:
            col = clustcol + str(i)
            colx.append(col)
            i += 1
        for x in data:
            i = 0
            for cluster_id, text in sorted(zip(classified_examples, texts)):
                if x == text:
                    wks.update_acell(colx[i], cluster_id)
                i += 1
    print 'all done'
    return HttpResponseRedirect(reverse('sendmail.clusteremail'))


def run_sort(data, wks, clustcol):
    #for sorting short texts...
    # first go through and group on 1st word.
    # then go through and group 1st word groups on second word.
    texts = data
    text2 = []
    for text in texts:
        text = filtered_text(text)
        text2.append(text)
    notext = len(text2)
    clust = np.zeros(len(text2))
    i = 0
    k = 1
    while i < notext:
        tokens = text2[i].split(' ')
        if len(tokens) == 1:
            if text2[i].find('-') > 0:
                z = text2[i].find('-')
                x = text2[i][:z]
            else:
                x = ''
        else:
            x = tokens[0]
        if clust[i] == 0:
            clust[i] = k
            j = i
            while j < len(texts):
                tokes = text2[j].split(' ')
                if len(tokes) == 1:
                    if text2[j].find('-') > 0:
                        z = text2[j].find('-')
                        y = text2[j][:z]
                    else:
                        y = ''
                else:
                    y = tokes[0]
                if y == x:
                    if clust[j] == 0:
                        clust[j] = k
                j += 1
            k += 1
        i += 1

    i = 1
    colx = []
    while i < notext + 1:
        col = clustcol + str(i+1)
        colx.append(col)
        i += 1
    i = 0
    for x in clust:
        wks.update_acell(colx[i], x)
        i += 1
    return HttpResponseRedirect(reverse('sendmail.clusteremail'))


if __name__ == '__main__':
    run_clusters()
