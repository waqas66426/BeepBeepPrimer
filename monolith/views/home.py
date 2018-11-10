from flask import Blueprint, render_template
from stravalib import Client

from monolith.database import db, Run, Plan
from monolith.auth import current_user


home = Blueprint('home', __name__)


def _strava_auth_url(config):
    client = Client()
    client_id = config['STRAVA_CLIENT_ID']
    redirect = 'http://127.0.0.1:5000/strava_auth'
    url = client.authorization_url(client_id=client_id, redirect_uri=redirect)
    return url

@home.route('/')
def index():
    if current_user is not None and hasattr(current_user, 'id'):
        runs = db.session.query(Run).filter(Run.runner_id == current_user.id)
        stat1 = compare()
        strava_auth_url = _strava_auth_url(home.app.config)
        return render_template("index.html", runs=runs,stat1=stat1 ,strava_auth_url=strava_auth_url)


    else:
        runs = None
    strava_auth_url = _strava_auth_url(home.app.config)

    plans = db.session.query(Plan.start_date,Plan.end_date, Plan.distance).filter(Plan.runner_id == current_user.id)

    return render_template("index.html", runs=runs, plans=plans,
                           strava_auth_url=strava_auth_url)

@home.route('/run/<id>', methods=['GET'])
def run(id):
    name    = None
    date    = None
    values  = None

    run = db.session.query(Run).filter(Run.runner_id == current_user.id).filter(Run.id == id).first()
    if run is not None:
        name    = run.name
        date    = run.start_date.strftime('%A %d/%m/%y at %H:%M')
        values  = [run.distance, run.average_speed, run.elapsed_time, run.total_elevation_gain]

    return render_template("run.html",name=name,date=date,values=values,id=run.id)




=======
    return render_template("index.html", runs=runs,strava_auth_url=strava_auth_url)




def compare():

    runs = db.session.query(Run).filter(Run.runner_id == current_user.id)
    best=0
    run_id=0
    if runs is None:
        print("do nothing")
    else:
        for run in runs:
            if run.distance > best:
                best=run.distance
                run_id=run.id

        bwrd=db.session.query(Run).filter(Run.id == run_id)

    return bwrd
>>>>>>> b7e79eaf6daea0263697d2b7257c81ecbcd63a44



