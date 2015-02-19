# -*- coding: utf-8 -*-
# usedata tasks - cluster code
# copyright 2014 Chibwe Ltd

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from celery import Celery
from django.conf import settings
import gspread
import nltk
from nltk.cluster import GAAClusterer
from nltk.cluster import euclidean_distance
from getdata.models import Setup
from django.core.files.storage import default_storage as s3_storage
from clusterer.settings import MEDIA_URL
import numpy as np
import pandas as pd
import boto
from boto.s3.key import Key
import csv
import itertools
import re
import os
from postmark import PMMail


app = Celery('tasks', broker=settings.BROKER_URL)
import sys
sys.setrecursionlimit(10000)

POSTMARK_API_KEY = os.getenv('POSTMARK_API_KEY')
POSTMARK_SENDER = os.getenv('POSTMARK_SENDER')


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


@app.task
def run_clusters(setupid, em_add):
    setup = Setup.objects.get(pk=setupid)
    datcol = setup.datcol
    clustcol = setup.clustcol
    datfile = s3_storage.open(str(setup.spreadname))
    df = pd.read_csv(datfile)
    data = df[datcol]
    print 'len(data) = ', len(data)
    text_len = AverageLength(data)
    if text_len < 10:
        run_sort(setupid)
    else:
        texts = data
        notext = len(texts)
        cluster = GAAClusterer(20)
        noclusters = 20
        ListWords = make_listwords(texts)
        print ListWords
        #tree = hcluster.hcluster([vectorspaced(text, ListWords) for text in texts], distance=hcluster.L2dist)
        #print tree
        cluster.cluster([vectorspaced(text, ListWords) for text in texts])
        classified_examples = [
            cluster.classify(vectorspaced(text, ListWords)) for text in texts]
        print 'texts clustered'
        i = 1
        colx = pd.Series(np.zeros(len(data)))
        out = s3_storage.open('clust.csv', 'w')
        for cluster_id, text in sorted(zip(classified_examples, texts)):
            x = text + '| ' + str(cluster_id) + '\n'
            out.write(x)
        out.close()
    print 'all done'
    message = PMMail(api_key=POSTMARK_API_KEY,
                     subject="Text Clusterer",
                     sender=POSTMARK_SENDER,
                     to=em_add,
                     text_body="Hello, clustering has finished.  The text and cluster ids can be downloaded from http://osmium.s3.amazonaws.com/media/clust.csv.",
                     tag="data")
    message.send()
    message = PMMail(api_key=POSTMARK_API_KEY,
                     subject="Clusterer use",
                     sender=POSTMARK_SENDER,
                     to='nigel@chibwe.com',
                     #text_body="User with email address " + em_add + " clustered " + str(len(data)) + " documents.",
                     text_body="User with email address clustered documents.",
                     tag="clusterer")
    message.send()


def run_sort(setupid):
    #for sorting short texts...
    # first go through and group on 1st word.
    # then go through and group 1st word groups on second word.
    setup = Setup.objects.get(pk=setupid)
    datcol = setup.datcol
    clustcol = setup.clustcol
    datfile = s3_storage.open(str(setup.spreadname))
    df = pd.read_csv(datfile)
    data = df[datcol]
    texts = data
    print("run_sort: lentexts =" + str(len(texts)))
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
    out = s3_storage.open('nameclust.csv', 'w')
    for x in clust:
        y = texts[i] + ',' + str(x) + '\n'
        out.write(y)
        i += 1
    out.close()
    message = PMMail(api_key=POSTMARK_API_KEY,
                     subject="Name Text Clusterer",
                     sender=POSTMARK_SENDER,
                     to="nigel.legg@gmail.com",
                     text_body="Hello, clustering has finished.  The text and cluster ids can be downloaded from http://osmium.s3.amazonaws.com/media/nameclust.csv.",
                     tag="data")
    message.send()


