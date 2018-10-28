from .home import home
from .auth import auth
from .users import users
from .strava import strava
from .report import report


blueprints = [home, auth, users, strava, report]
