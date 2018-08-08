import urllib
import gensim
import feedparser
import subprocess
from datetime import datetime
from datetime import timedelta
from threading import Timer
import os

CHECKING_TIME_SECS = 43200
x=datetime.today()
d = timedelta(seconds=CHECKING_TIME_SECS)
secs=d.seconds


SAVE_PATH = str(os.environ['SAVE_PATH'])

def sendmessage(message):
    subprocess.Popen(['notify-send', message])
    return

def check_for_pdf_link(links):
    for l in links:
        if 'title' in l and l['title'] == 'pdf':
            return (True, l['href'])
    return (False, '')

url = 'http://export.arxiv.org/api/query?search_query=cat:cs.DB&sortBy=lastUpdatedDate&sortOrder=descending'

def timer_start():
    t = Timer(secs, check_for_papers)
    t.start()

def check_for_papers():
    print "CHECKING FOR PAPERS"
    data = urllib.urlopen(url).read()
    f = feedparser.parse(data)

    # print f['entries'][0]['links']
    # res =  check_for_pdf_link(f['entries'][0]['links'])
    # if res[0]:
    #     urllib.urlretrieve(res[1],filename='/home/fotis/Desktop/recommended-papers/'+f['entries'][0]['title']+'.pdf')
    #     sendmessage('Recommended Paper added\n{0}'.format(f['entries'][0]['title']))
    # #
    for e in  f['entries']:
        abstract = e['summary']

        #Load pre-trained doc2vec model
        model = gensim.models.doc2vec.Doc2Vec.load('modelDoc2Vec.model')
        str_vector = gensim.utils.simple_preprocess(abstract)
        #Infer vector for new paper
        inferred_vector = model.infer_vector(str_vector)
        #Get similarities with stored papers
        sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
        #Strategy for recommending
        avg_score = sum(map(lambda x : x[1], sims))/float(len(sims))
        THRESH = 0.7
        if avg_score>THRESH:
            links = e['links']
            res =  check_for_pdf_link(links)
            if res[0]:
                urllib.urlretrieve(res[1],filename='/home/fotis/Desktop/recommended-papers/'+e['title']+'.pdf')
                sendmessage('Recommended Paper added\n{0}'.format(e['title']))
        else:
            print "Not recommending with score : {0}".format(avg_score)

    timer_start()
timer_start()
