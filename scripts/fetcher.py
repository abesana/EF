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
    open(url.split("/")[-1], "w").write(result)
    return result

def _facebook_like_element(tag):
    return (tag.name == 'meta') and (
        tag.has_attr('name') and
        tag['name'] == 'description')

def _twitter_followers_element(tag):
    '''<a class="js-nav" href="/pepe/followers" data-element-term="follower_stats" data-nav='followers'>  
  <strong>1,548</strong> Followers
</a>'''
    return (tag.name == 'a') and (
        tag.has_attr("data-element-term")) and (
        tag["data-element-term"] == "follower_stats")

def _extract_like(html_string):
    "We assume the first integer literal corresponds to number of likes"
    soup = BeautifulSoup(html_string)
    for content in (tag["content"] for tag in soup.find_all(
        _facebook_like_element)):
        for word in (w.replace(",", "").replace(".", "") for w in
                     content.encode("ASCII", 'ignore').split()):
            if word.isdigit():
                return int(word)

def _extract_followers(html_string):
    '''<a class="js-nav" href="/pepe/followers" data-element-term="follower_stats" data-nav='followers'>  
  <strong>1,548</strong> Followers
</a>'''
    soup = BeautifulSoup(html_string)
    for content in (tag.text for tag in soup.find_all(
        _twitter_followers_element)):
        for word in (w.replace(",", "").replace(".", "") for w in
                     content.encode("ASCII", 'ignore').split()):
            if word.isdigit():
                return int(word)
    
def facebook(username):
    return _extract_like(fetch(FACEBOOK_URL + quote(username)))

def twitter(username):
    return _extract_followers(fetch(TWITTER_URL + quote(username)))
    
if __name__ == "__main__":
    for username in sys.argv[1:]:
        print "=" * 79
        print username
        print "\tfacebook", facebook(username)
        print "\ttwitter", twitter(username)
