import urllib2
from clarifai.client import ClarifaiApi
import unicodedata
​
clarifai_api = ClarifaiApi()
##############################################################
# Creates three useful arrays: Likes, URL (to photo), Hashtags
# The index of each array corresponds to the index of the photo
# e.g (likes[0] will contain the amount of likes in the first photo)
##############################################################
def remove_backslash(url): #removes the backslashes from the URL
   output = ""
   for char in url:
       if char != '\\':
           output += char
   return output
​
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
​
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
​
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
​
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
​
def ig_username(username): #concatenates the instagram handle with the username
    str1 = 'https://www.instagram.com/'
    user_url = str1+username+'/'
    return user_url
​
def return_photo_url(html):
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
​
def azureml_main():
    import pandas as pd
​
    response = urllib2.urlopen(ig_username("kellylpt"))
    html = response.read()
    sources = get_sources(html)
    likeCount = get_likes(html)
    keywords = []
​
    count = 0
​
    for i in sources:
        result = clarifai_api.tag_image_urls(i)
        keywords.append([])
        for i in range(len(result['results'][0]["result"]["tag"]["classes"])):
            aKeyword = result['results'][0]["result"]["tag"]["classes"][i]
            keywords[count].append(aKeyword)
        count+=1
​
    data = {}
    data["Likes"] = likeCount
    for j in keywords[0]:
        col = []
        for i in keywords:
            col.append(keywords[i][j])
        data["Tag "+str(j)] = col


    """
    for i in keywords:
        for j in keywords[i]:
            word = keywords[i][j]
            newWord = True
            for key in data:
                if word == key:
                    newWord = False
                    data[key].append(likeCount[i])
                    break
            if newWord:
                data[word] = [likeCount[i]]
    """
​
    result = pd.DataFrame(data)
    return result
