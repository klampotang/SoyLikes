import urllib2
from clarifai.client import ClarifaiApi
from collections import defaultdict
import unicodedata

def google(self, username):

    # print username 
    # print type(username)
    # print ig_username(self.username)

    self.clarifai_api = ClarifaiApi()

    #self.ig_username = ig_username(username)    

    response = urllib2.urlopen(ig_username(username))
    insta_html = response.read()
    google_html = "https://photos.google.com/share/AF1QipONERd0AGm-CcUrQ_m56P4R0eypHJDNDLslYs0mrw_KWuLDtzxii6cE_rY7luRxqw?key=X0x3QWFlYmVCQlgtZGgzcFoycGhldWVYVjNzSGd3"
    likes = get_likes(insta_html)
    insta_keywords = get_keywords(get_sources(insta_html))
    google_keywords = get_keywords(return_photo_url(google_html))

    highest_likes = 0.0
    for num in likes:
        if num > highest_likes:
            highest_likes = num

    words = []
    for g_keywords in google_keywords:
        for g_tag in g_keywords:
            for word in words:
                if g_tag == word:
                    break
            words.append(g_tag)

    word_ranks = []
    for word in range(len(words)):
        word_ranks.append(0.0)
        instances = 0
        for i_keywords in range(len(insta_keywords)):
            for i_tag in range(len(insta_keywords[i_keywords])):
                if insta_keywords[i_keywords][i_tag] == words[word]:
                    word_ranks[word] += likes[i_keywords]
                    instances += 1
                    break
        if instances > 0:
            word_ranks[word] /= instances

    photo_ranks = []
    for g_keywords in range(len(google_keywords)):
        photo_ranks.append(0.0)
        for g_tag in google_keywords[g_keywords]:
            photo_ranks[g_keywords] += word_ranks[words.index(g_tag)]

    photo_percent = []
    for rank in photo_ranks:
        photo_percent.append(rank/(highest_likes*20))

    google_sources = return_photo_url(google_html)
    for i in range(len(photo_percent)):
        highest = i
        for j in range(i,len(photo_percent)):
            if photo_percent[j] > photo_percent[highest]:
                highest = j
        photo_percent.insert(i, photo_percent.pop(highest))
        google_sources.insert(i, google_sources.pop(highest))

