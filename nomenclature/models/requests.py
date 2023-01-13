from django.db import models
import datetime

from nomenclature.models.products import Product
from nomenclature.models.persons import Person
from nomenclature.models.approvers import Approver
from nomenclature.models.approvements import Approvement

class Request(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='request')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null = True)
    views_count = models.IntegerField(default=0)
    person_who_created = models.PositiveBigIntegerField(null=True)
    approvers = models.ManyToManyField(Approver, through=Approvement, related_name='requests')

    SUMMARY_ITEMS_COUNT = 5
    
    class Meta(object):
        app_label = 'nomenclature'
        ordering = ['-created_at']

    @property
    def all_approved(self):
        if self.get_approvers_left().count()==0:
            values = [v.state for v in self.get_approvements()]
            equal = True
            for v in values:
                if v != 1:
                    equal=False
                    break
            if equal: return True
        
        return False

    def get_person_who_created(self):
        if not self.person_who_created: return None
        return Person(self.person_who_created)

    def get_approvements(self):
        return Approvement.objects.filter(request=self)
                
    def get_approvers_left(self):
        values = self.get_approvements().values_list('approver__pk')
        return Approver.objects.all().exclude(pk__in=values)

    def change_approvement(self ,state, user_id, comment):
        approver = Approver.objects.get(auth_id=user_id)
        try:
            approvement = Approvement.objects.get(request=self,approver=approver)
        except Approvement.DoesNotExist:
            approvement = None

        if state==0:
            approvement.delete()
        else:
            approved_at = None
            rejected_at = None
            date = datetime.datetime.now()

            if state==1: approved_at = date
            elif state==-1: rejected_at = date

            if approvement:
                approvement.approved_at = approved_at
                approvement.rejected_at = rejected_at
                approvement.comment = comment
                approvement.save()
            else:
                Approvement.objects.create(
                    request=self,
                    approver=approver,
                    approved_at=approved_at,
                    rejected_at=rejected_at,
                    comment=comment,)
            
            if self.all_approved:
                self.approved_at = datetime.datetime.now()
                self.save()

    def clear_approvements(self, approved_only=True):
        if approved_only: # удалять только согласованные состояния
            list_to_delete = Approvement.objects.filter(request=self,approved_at__isnull=False)
            for a in list_to_delete:
                a.delete()
        else: # удалять все состояния
            self.approvers.clear()

    @staticmethod
    def recent_approved():
        return Request.objects.all().filter(
            approved_at__isnull=False).order_by('-approved_at')[:Request.SUMMARY_ITEMS_COUNT]

    @staticmethod
    def recent_created():
        return Request.objects.all().filter(
            approved_at__isnull=True).order_by('-created_at')[:Request.SUMMARY_ITEMS_COUNT]

    @staticmethod
    def most_popular():
        return Request.objects.filter(
            approved_at__isnull=False).order_by('-views_count')[:Request.SUMMARY_ITEMS_COUNT]