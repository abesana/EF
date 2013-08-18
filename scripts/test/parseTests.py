import os
from scripts import fetcher

from nose.tools import eq_

DIR = os.path.dirname(__file__)

def test_empty_facebook():
    got = fetcher._facebook_extract(
        open(os.path.join(DIR, "data", "alberto.besana")).read())
    eq_(None, got['count'])
    eq_(None, got['description'])

def test_empty_twitter():
    got = fetcher._twitter_extract(
        open(os.path.join(DIR, "data", "alberto.besana")).read())
    eq_(None, got['count'])
    eq_(None, got['description'])

def test_facebook():
    got = fetcher._facebook_extract(
        open(os.path.join(DIR, "data", "cristiano")).read())
    eq_(59704825, got['count'])
    eq_('TEAM HISTORY: Current Club: Real Madrid Number: 7 Youth career 19931995 -- Andorinha...', got['description'])

def test_twitter():
    got = fetcher._twitter_extract(
        open(os.path.join(DIR, "data", "beyonce")).read())
    eq_(11085008, got['count'])
    eq_('Lo ltimo de Beyonc Knowles (@Beyonce).', got['description'])

