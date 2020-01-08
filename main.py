#d imports
import os
import base64

import setup
from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from model import Donor, Donation 
# ----------------------------------

app = Flask(__name__)
#app.secret_key = b"\xe0\x95\xf2`W8'X,2\xfc\x88Z\x8c\x97\xad~1\xd8k\xbb\xaf\xd7\xab"

app.secret_key = os.environ.get('SECRET_KEY').encode()

# ----------------------------------

@app.route('/')
def home():
    return redirect(url_for('all'))
# ----------------------------------

@app.route('/donations/')
def all():
    return render_template('donations.jinja2', donations=Donation.select())
# ----------------------------------    

@app.route('/donations/create/', methods=['GET', 'POST'])
def new_donation():
    if request.method == "POST":
        try:
            donor = Donor.select().where(Donor.name == request.form['name-input']).get()
        except Donor.DoesNotExist:
            return render_template("create.jinja2", error="donor not in records")
       
        try:
            value = request.form['value-input']
            if not value or not value.isnumeric():
                raise ValueError()
        except ValueError: 
                return render_template("create.jinja2", error="donation amount missing or not a number")
       
        new_donation = Donation(donor=donor, value=value)
        new_donation.save()
      
    else:
        return render_template('create.jinja2', donations=Donation.select())
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
 
# ----------------------------------
if __name__ == "__main__":
    app.run(debug=True)
    #port = int(os.environ.get("PORT", 6738))
    #app.run(host='0.0.0.0', port=port)

