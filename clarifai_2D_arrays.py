import urllib2

from clarifai.client import ClarifaiApi
from collections import defaultdict

import unicodedata

clarifai_api = ClarifaiApi()
##############################################################
# Creates three useful arrays: Likes, URL (to photo), Hashtags
# The index of each array corresponds to the index of the photo
# e.g (likes[0] will contain the amount of likes in the first photo)
##############################################################
def remove_backslash(url): #removes the backslashes from the URL
   output = "";
   for char in url:
       if char != '\\':
           output += char
   return output

def get_likes(html):
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

def get_sources(html): #gets the actual URL
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

def get_captions(html):
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

def get_hashtags(caption):
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

def ig_username(username): #concatenates the instagram handle with the username
    str1 = 'https://www.instagram.com/'
    user_url = str1+username+'/'
    return user_url

response = urllib2.urlopen(ig_username("kellylpt"))
html = response.read()

#print get_likes(html)
url = get_sources(html)
#use the urls to get the list of keywords
likeCount = get_likes(html)
#create an empty list
keywords = []

count = 0

for i in url:
  result = clarifai_api.tag_image_urls(i)
  keywords.append([])



  for i in range(len(result['results'][0]["result"]["tag"]["classes"])):
    #keywords.append([])
    aKeyword = result['results'][0]["result"]["tag"]["classes"][i]
    keywords[count].append(aKeyword)
  count+=1
dic = defaultdict(list)

print keywords


captions = get_captions(html)


#print captions

hashtags = []
for i in range(len(captions)):
   hashtags.append(get_hashtags(captions[i]))
