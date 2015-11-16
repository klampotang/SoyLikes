from clarifai.client import ClarifaiApi
import unicodedata
clarifai_api = ClarifaiApi()  # assumes environment variables are set.
result = clarifai_api.tag_image_urls('http://www.clarifai.com/img/metro-north.jpg')

"""print len()"""
print "\n"
"""print result["results"]["result"]["classes"]"""
"""print result["results"]["result"]["tag"]["classes"]"""
for i in range(len(result['results'][0]["result"]["tag"]["classes"])):
	print result['results'] [0]["result"]["tag"]["classes"][i]

"""print result['results'] [0]["result"]["tag"]["classes"]"""


