from faker import Faker
import random
import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Recommend_store.settings')

import django
# Import settings
django.setup()
from first_app.models import Customer
from django.contrib.auth.models import User

fakegen = Faker()


def populate(N=20):
    '''
    Create N Entries of Dates Accessed
    '''

    for entry in range(N):

        # Create Fake Data for entry
        fake_name = fakegen.name().split()
        fake_first_name = fake_name[0]
        fake_last_name = fake_name[1]
        fake_user_name = fake_first_name+fake_last_name
        password='goshtasb'
        user=User.objects.create_user(username=fake_user_name, password=password+fake_user_name)
        user.is_superuser=False
        user.is_staff=False
        user.save()

        # fake_last_name = fake_name[1]
        # fake_email = fakegen.email()
        # fake_address = fakegen.address()
        # fake_number = fakegen.phone_number()
        #
        # # Create new User Entry
        # user = Customer.objects.get_or_create(
        #     user_name=fake_user_name,
        #     first_name=fake_first_name,
        #     last_name=fake_last_name,
        #     email=fake_email,
        #     address=fake_address,
        #     mobile=fake_number)[0]

def f1(x):
    def f2():
        y=f1.x
        return y
if __name__ == '__main__':
    print("Populating the databases...Please Wait")
    print f1(4)

    print('Populating Complete')
