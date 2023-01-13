from django.test import TestCase

from .models import Person
from .models import Group

# Create your tests here.

class PersonTest(TestCase):
    def test_get_person(self):
        person = Person(3)
        print (person.get_shortname())
    def test_group(self):
        # group = Group.objects.get(pk=1)
        # print('Group name is: ', group.name)
        print ('Count is: ', Group.objects.count())