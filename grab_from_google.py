import urllib2
####################################
#Grabs the photos off of your google photos.
#You need to input the URL of your SHARED
# google photos album, and it will return an array of URL's
# to the individual photos
####################################

def remove_backslash(url): #removes the backslashes from the URL
   output = "";
   for char in url:
       if char != '\\':
           output += char
   return output

def return_photo_url(html):
    photos = []
    response = urllib2.urlopen(html)
    html = response.read()
    #print html
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

#print return_photo_url("https://photos.google.com/share/AF1QipONERd0AGm-CcUrQ_m56P4R0eypHJDNDLslYs0mrw_KWuLDtzxii6cE_rY7luRxqw?key=X0x3QWFlYmVCQlgtZGgzcFoycGhldWVYVjNzSGd3")
#for testing purposes only
