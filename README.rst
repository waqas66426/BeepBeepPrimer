BeepBeep Skeleton
==================

How to run the app
-------------------

For this application to work, you need to create a Strava API application
see https://strava.github.io/api/#access and https://www.strava.com/settings/api

Once you have an application, you will have a "Client Id" and "Client Secret".
You need to export them as environment variables::

    export STRAVA_CLIENT_ID=<ID>
    export STRAVA_CLIENT_SECRET=<SECRET>

It is a good idea to create a file (and add it to .gitignore) that contains both commands. You can 
then run it via::

    source <filename>.sh

As usual, to start the app run::

    $ pip install -r requirements.txt
    $ python setup.py develop

You can then run your application with::

    $ python monolith/app.py
    * Running on http://127.0.0.1:5000/

How to create a new user
------------------------

1. Connect to Strava with the new user's account
2. Browse http://127.0.0.1:5000/create_user and insert data.
3. Login by browsing http://127.0.0.1:5000/
4. Click on "Authorize Strava Access" -- this will perform an OAuth trip to Strava.

Once authorized, you will be able to see your last 10 runs.
But for this, we need to ask the Celery worker to fetch them.

How to run the Celery worker
----------------------------

Make sure you have a redis server running locally on port 6379 by running::

    $ redis-server
    $ redis-cli
    $ 127.0.0.1:6379> ping
        PONG

Then, open another shell and run::

    $ celery worker -A monolith.background

This will run a celery microservice that can fetch runs.
To invoke it, visit http://127.0.0.1:5000/fetch.

Once the runs are retrieved, you should see your last ten runs
on http://127.0.0.1:5000


How to run email reporting
---------------------------

First the email servis creditionals need to be exported:: 

$ export EMAIL_ID=<ID>
$ export EMAIL_PASS=<Password>

In case Gmail is used all the internal params are hardcoded, just need to allow access to less secure apps on Gmail::

https://myaccount.google.com/lesssecureapps?pli=1

In case of other mail provider params in app.py need to be adjusted.After all that is done and celery is running as above you need to run celery beat in other terminal window by::

$ celery -A monolith.background beat -l info

Than servicce is ready to start sending the mail reports! Just log in and select E-mail report from the homepge! 
