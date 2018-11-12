from flask import Blueprint, redirect, render_template, request
from monolith.forms import ReportForm
from flask_login import current_user
from monolith.database import db

report = Blueprint('report', __name__)


@report.route('/report', methods=['GET', 'POST'])
def create_report():
    form = ReportForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.set_email_frequency(form.frequency.data)
            db.session.add(current_user)
            db.session.commit()
            return redirect('/')

    return render_template('report.html', form=form)
