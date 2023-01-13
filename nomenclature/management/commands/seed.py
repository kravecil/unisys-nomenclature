from django.core.management import BaseCommand
from django.utils import timezone
from faker import Faker
import random
import datetime

from nomenclature.models.requests import Request
from nomenclature.models.products import Product
from nomenclature.models.approvers import Approver
from nomenclature.models.units import Unit

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Proccessing...')
        """"""

        fake = Faker()

        """ Добавим группы с подгруппами """
        # for _ in range(random.randrange(30)):
        #     # if random.randrange(10) > 3:
        #     #     parent_group_id =
        #     group = Group.objects.create(name=fake.unique.first_name())

        # groupsIds = [entry for entry in (
        #     Group.objects.all().values_list('id', flat=True))]

        # for group in Group.objects.all():
        #     gen = [x for x in groupsIds if x not in [group.pk]]
        #     if random.randrange(10) > 5:
        #         group.parent_group = Group.objects.get(pk=random.choice(
        #             gen))
        #         group.save()

        """ Добавим изделия не более заданного числа """
        # groups = list(Group.objects.all())
        approvers = Approver.objects.all()
        units = Unit.objects.all()
        for _ in range(100):
            product = Product.objects.create(
                name=fake.text(max_nb_chars=20),
                # designation=fake.phone_number(),
                number=fake.random_number(digits=13),
                notes='\n'.join(fake.paragraphs(nb=3)),
                unit=random.choice(list(units)))
            request = Request.objects.create(
                product=product,
                approved_at=timezone.now() + datetime.timedelta(seconds=random.randrange(60 * 60 * 3600))
                    if random.randrange(10) > 3 else None,
                person_who_created=random.randrange(2, 150),
                # person_who_approved=random.randrange(150) if random.randrange(10) > 5 else None,
            )
            for _ in range(approvers.count()):
                approved_at = None
                rejected_at = None
                date = timezone.now() + datetime.timedelta(seconds=random.randrange(60 * 60 * 3600))
                if random.random() * 10 > 5:
                    approved_at = date
                else:
                    rejected_at = date
                request.approvers.add(random.choice(approvers), through_defaults={
                    'approved_at': approved_at,
                    'rejected_at': rejected_at,
                    'comment': '\n'.join(fake.sentences()),
                })

        """"""
        print('Done!')
