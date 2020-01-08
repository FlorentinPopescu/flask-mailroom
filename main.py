import os
import base64

# import setup
from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from model import Donor, Donation
# ---------------------------------

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()
# ---------------------------------

@app.route('/')
def home():
    return redirect(url_for('all'))
# ---------------------------------

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)
# ---------------------------------

@app.route('/donations/select/', methods=["GET", "POST"])
def select():
    if request.method == "GET":
        donations = Donation.select()
        try:
            don = request.args.get('selected_donor', None)
            if don is None:
                return render_template('select.jinja2')
            try:
                s_donor = Donor.get(Donor.name == don)
                selected_donor = [(donation.donor.name, donation.value) for donation in donations \
                        if don is not None and donation.donor.name == don]
                total_unique = len(selected_donor)
            except Donor.DoesNotExist:
                return render_template('select.jinja2', error="reenter donor's name")
            return render_template("unique.jinja2", selection=selected_donor, text=s_donor.name, counts=total_unique)
        except ValueError:
            return render_template("select.jinja2")
# ---------------------------------

# ---------------------------------
if __name__ == "__main__":
    app.run(debug=True)
    #port = int(os.environ.get("PORT", 6738))
    #app.run(host='0.0.0.0', port=port)

