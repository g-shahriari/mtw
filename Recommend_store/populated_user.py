from faker import Faker
import random
import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Recommend_store.settings')

import django
# Import settings
django.setup()
from first_app.models import UserProfile
from django.contrib.auth.models import User


fake = Faker()


def populate():
    first_lst=[]
    for _ in range(100):
        first_lst.append(fake.first_name())

    last_lst=[]
    for _ in range(100):
        last_lst.append(fake.last_name())

    full_name=[]
    for i in range(0,100):
        for j in range(0,100):
            if first_lst[i]+'_'+last_lst[j] in full_name:
                pass
            else:
                full_name.append(first_lst[i]+'_'+last_lst[j])




    '''
    Create N Entries of Dates Accessed
    '''

    for i in range(999):

        # Create Fake Data for entry


        password='g'
        user=User.objects.create_user(username=full_name[i], password=password+full_name[i],)
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


if __name__ == '__main__':

    populate()
    print("Populating the databases...Please Wait")



    print('Populating Complete')
