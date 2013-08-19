EF
==

You can install all dependecy using pip:

`sudo pip install -r requirements.txt`
  
script
------

Call the script scraping facebook (likes) and twitter (followers) profile pages

`python apifetch/ftchr/scripts/fetcher.py U2 beyonce ...`

API
---

It is a Django application

Deplyoment

`cd apifetch`
This prepare the sqlite DB (execute it just once):
`python manage.py syncdb`
This will run a local development server
`python manage.py runserver 0.0.0.0:8000`


A rest API is provide using as follows. JSON only version.

'''
GET
http://127.0.0.1:8000/network/twitter/username/foo
http://127.0.0.1:8000/network/facebook/username/foo
'''
popularity counter and description.
In case nothing is found a suitable message is shown. Fetcher call cached in DB.

'''
DELETE
http://127.0.0.1:8000/network/twitter/username/foo
http://127.0.0.1:8000/network/facebook/username/foo
'''
delete the entity.
WARNING: if you get it again the fetcher will be triggered and data re-cached.

'''
UPDATE
http://127.0.0.1:8000/network/twitter/username/foo
http://127.0.0.1:8000/network/facebook/username/foo

{"count": 55, "description": "description updated"}
'''

'''
POST
http://127.0.0.1:8000/network/twitter/username
http://127.0.0.1:8000/network/facebook/username

{"user": "bar", "count": 87, "description": "bar description"}
'''








Improvements
-----

- Use the developer API for both twitter and facebook (no scraping)
- Encapsulating the scraping script (no in-process)
- encoding (depends on deployment environment)
- enrich the API, e.g.: getting lists, more explicit error messages, ...
