from flask import Blueprint, redirect, render_template, request
from monolith.database import db, Plan
from monolith.forms import PlanForm
from monolith.auth import current_user

plan = Blueprint('plan', __name__)

@plan.route('/plan', methods=['GET', 'POST'])
def create_plan():
    form = PlanForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            if current_user is not None and hasattr(current_user, 'id'):
                new_plan = Plan()
                new_plan.runner_id = current_user.id
                form.populate_obj(new_plan)
                db.session.add(new_plan)
                db.session.commit()
                return redirect('/')

    return render_template('plan.html', form=form)
