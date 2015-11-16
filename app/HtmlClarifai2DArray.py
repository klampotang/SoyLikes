import urllib2
from clarifai.client import ClarifaiApi
from collections import defaultdict
import unicodedata

##############################################################
# Creates three useful arrays: Likes, URL (to photo), Hashtags
# The index of each array corresponds to the index of the photo
# e.g (likes[0] will contain the amount of likes in the first photo)
##############################################################

class HtmlClarifai2DArray:
  
# for i in range(len(photo_percent)):
    # print "%s\n%s" % (photo_percent[i],google_sources[i])

  def remove_backslash(self, url): #removes the backslashes from the URL
    output = ""
    for char in url:
       if char != '\\':
           output += char
    return output

  def get_likes(self, html):
    likes = []
    for i in range(len(html)):
       if html[i:i+7] == "\"likes\"":
           count = i+17
           strLikes = ""
           while html[count] != '}':
               strLikes += html[count]
               count += 1
           likes.append(int(strLikes))
    return likes

  def get_sources(self, html): #gets the actual URL
    sources = []
    for i in range(len(html)):
       if html[i:i+15] == "\"thumbnail_src\"":
           count = i+17
           source = ""
           while html[count] != '\"':
               source += html[count]
               count += 1
           sources.append(remove_backslash(source))
    return sources

  def get_captions(self, html):
    captions = []
    for i in range(len(html)):
       if html[i:i+6] == "\"code\"":
           count = i+1
           caption = ""
           while html[count:count+6] != "\"code\"":
               if html[count:count+9] == "\"caption\"":
                   count2 = count+11
                   while html[count2] != '\"':
                       caption += html[count2]
                       count2 += 1
                   break
               count += 1
           captions.append(caption)
    return captions

  def get_hashtags(self, caption):
    hashtags = []
    for i in range(len(caption)):
        if caption[i] == '#':
            hashtag = ""
            count = i+1
            if count < len(caption):
                while caption[count] != ' ':
                    hashtag += caption[count]
                    count += 1
                    if count >= len(caption):
                        break
            if hashtag != "":
                hashtags.append(hashtag)
    return hashtags

  def ig_username(self, username): #concatenates the instagram handle with the username
    str1 = "https://www.instagram.com/"
    user_url = str1+str(username)+"/"
    return user_url

  def return_photo_url(self, html):
    photos = []
    response = urllib2.urlopen(html)
    html = response.read()
    location = 0
    for i in range(len(html)):
        if html[i:i+8] == "id=\"_ij\"":
            location = i+8
            break
    for i in range(location, len(html)):
        if html[i:i+33] == "https://lh3.googleusercontent.com": #33
            count = i
            source = ""
            while html[count] != "\"":
                source += html[count]
                count += 1
            photos.append(remove_backslash(source))
    return photos

  def get_keywords(self, sources):

    keywords = []
    count = 0
    for i in sources:
        result = clarifai_api.tag_image_urls(i)
        keywords.append([])
        for i in range(len(result['results'][0]["result"]["tag"]["classes"])):
            aKeyword = result['results'][0]["result"]["tag"]["classes"][i]
            keywords[count].append(aKeyword)
        count+=1
    return keywords


  def __init__(self, username):

    print username 
    print type(username)
    print ig_username(self.username)

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

