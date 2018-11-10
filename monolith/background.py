import os
from celery import Celery
from stravalib import Client
from monolith.database import db, User, Run
from flask_mail import Mail, Message
import time

BACKEND = BROKER = 'redis://localhost:6379'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

_APP = None


@celery.task
def fetch_all_runs():
    global _APP
    # lazy init
    if _APP is None:
        from monolith.app import create_app
        app = create_app()
        db.init_app(app)

    else:

        app = _APP

    runs_fetched = {}

    with app.app_context():
        q = db.session.query(User)
        for user in q:
            if user.strava_token is None:
                continue
            print('Fetching Strava for %s' % user.email)
            runs_fetched[user.id] = fetch_runs(user)


    return runs_fetched

# Call send report every second
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(schedule=1, sig=send_report.s(), name="test")

@celery.task
def send_report():
    global _APP
    # lazy init
    if _APP is None:
        from monolith.app import create_app
        app = create_app()
        db.init_app(app)
    else:
        app = _APP

    with app.app_context():
        mail=Mail(app)
        q = db.session.query(User)
        # Check all users if they requested report
        for user in q:
            if user.email_frequency is None:
                continue
            # check report freq against the current time - in case worker dies the report would be send with proper freq
            # Opposed to when some counter would be used(the state of counyter would die with it)
            if int(time.time()) % user.email_frequency == 0:
                msg = Message('BeepBeep Email report', sender = os.environ['EMAIL_ID'], recipients = [user.email])
                msg.body = "Report will be filled in as soon as 2.3 is done - it will be simply included here"
                mail.send(msg)

def activity2run(user, activity):
    """Used by fetch_runs to convert a strava run into a DB entry.
    """
    run = Run()
    run.runner = user
    run.strava_id = activity.id
    run.name = activity.name
    run.distance = activity.distance
    run.elapsed_time = activity.elapsed_time.total_seconds()
    run.average_speed = activity.average_speed
    run.average_heartrate = activity.average_heartrate
    run.total_elevation_gain = activity.total_elevation_gain
    run.start_date = activity.start_date
    return run


def fetch_runs(user):
    client = Client(access_token=user.strava_token)
    runs = 0

    for activity in client.get_activities(limit=10):
        if activity.type != 'Run':
            continue
        q = db.session.query(Run).filter(Run.strava_id == activity.id)
        run = q.first()

        if run is None:
            db.session.add(activity2run(user, activity))
            runs += 1

    db.session.commit()
    return runs
