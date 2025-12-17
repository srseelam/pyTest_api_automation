import uuid
import random
from faker import Faker
from datetime import datetime, timedelta

fake=Faker()
def fake_first_name(): return fake.first_name()
def fake_last_name(): return fake.last_name()
def fake_email(): return fake.email()
def uuid_id(): return uuid.uuid4()
def random_adult_age(): return random.randint(18, 100)
def random_child_age(): return random.randint(1, 17)
def get_date_from_today(daysFromToday):  
    return (datetime.now() + timedelta(days=daysFromToday)).strftime("%m-%d-%Y")