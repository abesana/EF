from urllib import urlopen, quote
import sys

from bs4 import BeautifulSoup

FACEBOOK_URL = "http://www.facebook.com/"
TWITTER_URL = "http://www.twitter.com/"
NOT_FOUND = 404

def fetch(url):
    g = urlopen(url)
    result = "<html></html>"
    if g.code != NOT_FOUND:
        result = g.read()
    g.close()
    return result

def _facebook_like_element(tag):
    '''<meta name="description" content="Rihanna, Los Angeles, CA. 74,553,559 likes &#xb7; 553,844 talking about this."'''
    return (tag.name == 'meta' and tag.has_attr('name') and
             'description' in tag['name'] and tag.has_attr('content'))

def _twitter_followers_element(tag):
    '''<a class="js-nav" href="/pepe/followers" data-element-term="follower_stats" data-nav='followers'>  
  <strong>1,548</strong> Followers
</a>'''
    return (tag.name == 'a' and 
            tag.has_attr("data-element-term") and 
            tag["data-element-term"] == "follower_stats")

def _twitter_description_element(tag):
    '''<meta name="description" content="The latest from Beyonc Knowles (@Beyonce).">'''
    return (tag.name == 'meta' and tag.has_attr("name") and
            "description" in tag["name"] and tag.has_attr('content'))

def _facebook_description_element(tag):
    '''<meta property="og:description" content="http://www.rihanna7.com" />'''
    return (tag.name == 'meta' and tag.has_attr("property") and
            'og:description' in tag['property'] and tag.has_attr('content'))
     
 
def _get_count(content):
    for word in content.encode("ASCII", 'ignore').split():
        word = word.replace(",", "").replace(".", "")
        if word.isdigit():
            return int(word)

    

def _facebook_extract(html_string):
    "We assume the first integer literal corresponds to number of likes"
    result = dict(description=None, count=None)
    soup = BeautifulSoup(html_string)    
    elem = soup.find(_facebook_like_element)
    if elem and elem['content']:
        result['count'] = _get_count(elem['content'])
    elem = soup.find(_facebook_description_element)
    # if elem and elem.child.name == 'div':
    #     result['description'] = elem and _normalize(elem.child.text)
    result['description'] = elem and _normalize(elem['content'])
    return result

def _normalize(unicode_text):
    "Convert white spaces in space and ignore encoding"
    return " ".join(unicode_text.encode("ASCII", "ignore").split()) or None
    
def _twitter_extract(html_string):
    result = dict(description=None, count=None)
    soup = BeautifulSoup(html_string)
    elem = soup.find(_twitter_followers_element)
    if elem and elem.text:
        count = _get_count(elem.text)
        result['count'] = count
    elem = soup.find(_twitter_description_element)
    result['description'] = elem and _normalize(_normalize(elem['content']))
    return result
    
def facebook(username):
    return _facebook_extract(fetch(FACEBOOK_URL + quote(username)))

def twitter(username):
    return _twitter_extract(fetch(TWITTER_URL + quote(username)))
    
if __name__ == "__main__":
    for username in sys.argv[1:]:
        print "=" * 79
        print username
        print "\tfacebook", facebook(username)
        print "\ttwitter", twitter(username)
