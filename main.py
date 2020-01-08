import os
import base64

# import setup
from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from model import Donation 
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
if __name__ == "__main__":
    app.run(debug=True)
    #port = int(os.environ.get("PORT", 6738))
    #app.run(host='0.0.0.0', port=port)

