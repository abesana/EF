import os
from scripts import fetcher

from nose.tools import eq_

DIR = os.path.dirname(__file__)

def test_empty_facebook():
    got = fetcher._extract_like(
        open(os.path.join(DIR, "data", "alberto.besana")).read())
    eq_(None, got)

def test_empty_twitter():
    got = fetcher._extract_like(
        open(os.path.join(DIR, "data", "alberto.besana")).read())
    eq_(None, got)

def test_facebook():
    got = fetcher._extract_like(
        open(os.path.join(DIR, "data", "cristiano")).read())
    eq_(59704825, got)

def test_twitter():
    got = fetcher._extract_followers(
        open(os.path.join(DIR, "data", "beyonce")).read())
    eq_(11085008, got)
