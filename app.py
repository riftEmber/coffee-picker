from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.fields.numeric import IntegerField, FloatField

from coffee import CoffeeData, CoffeeDrinker, DATA_FILENAME
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)


class ClearForm(FlaskForm):
    clear_name = StringField("Name", validators=[DataRequired()])

    submit_clear = SubmitField("Remove")


class DrinkerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    drink_name = StringField("Favorite Drink", validators=[DataRequired()])
    drink_cost = FloatField(
        "Cost of drink", validators=[DataRequired(), NumberRange(min=1)]
    )
    times_drink_ordered = IntegerField(
        "Times drink ordered", default=0, validators=[NumberRange(min=0)]
    )
    amount_paid_so_far = FloatField(
        "Amount paid so far", default=0.0, validators=[NumberRange(min=0)]
    )

    submit = SubmitField("Add")


class PurchaseForm(FlaskForm):
    submit_purchase = SubmitField("Decide")


@app.route("/", methods=["GET", "POST"])
def hello_world():
    drinker_form = DrinkerForm()
    purchase_form = PurchaseForm()
    clear_form = ClearForm()

    message = ""
    coffee_data = CoffeeData()
    coffee_data.restore_from_file(DATA_FILENAME)

    any_form_submitted = True
    if drinker_form.submit.data and drinker_form.validate_on_submit():
        new_drinker = CoffeeDrinker(
            drinker_form.name.data,
            drinker_form.drink_name.data,
            drinker_form.drink_cost.data,
            drinker_form.times_drink_ordered.data,
            drinker_form.amount_paid_so_far.data,
        )
        coffee_data.add_drinker(new_drinker)
        message = f"Added drinker {drinker_form.name.data} to coffee chart"
    elif (
        purchase_form
        and purchase_form.submit_purchase.data
        and purchase_form.validate_on_submit()
    ):
        todays_payer = coffee_data.pick_payer_and_pay()
        message = f"{todays_payer.name} is paying for everyone's coffee today!"
    elif (
        clear_form and clear_form.submit_clear.data and clear_form.validate_on_submit()
    ):
        assert clear_form.clear_name.data
        if coffee_data.remove_drinker(clear_form.clear_name.data):
            message = f"Removed drinker '{clear_form.clear_name.data}'"
        else:
            message = f"Could not find drinker with name '{clear_form.clear_name.data}'"
    else:
        any_form_submitted = False

    if any_form_submitted:
        coffee_data.save_to_file(DATA_FILENAME)

    return render_template(
        "index.html",
        drinker_form=DrinkerForm(formdata=None),
        purchase_form=PurchaseForm(formdata=None),
        clear_form=ClearForm(formdata=None),
        message=message,
        drinkers=coffee_data.drinkers,
    )
