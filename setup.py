# imports
import random

from passlib.hash import pbkdf2_sha256
from datetime import datetime

from model import db, Donor, Donation 
# -----------------------------

# connect to database
db.connect()

# This line allows an "upgrade" an existing database by
# dropping all existing tables from it.

db.drop_tables([Donor, Donation])
db.create_tables([Donor, Donation])
# -----------------------------

alice = Donor(name="Alice", password=pbkdf2_sha256.hash("alice"))
alice.save()

bob = Donor(name="Bob", password=pbkdf2_sha256.hash("bob"))
bob.save()

charlie = Donor(name="Charlie", password=pbkdf2_sha256.hash("charlie"))
charlie.save()

donors = [alice, bob, charlie]
# ---------------------------

for x in range(30):
    Donation(donor=random.choice(donors), value=random.randint(100,
        10000)).save()

