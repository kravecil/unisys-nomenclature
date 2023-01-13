from django.db import models
from .groups import Group
from .units import Unit
from .okpd import Okpd
from .okved import Okved
from .ens import Ens

class Product(models.Model):
    number = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=150)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    okpd = models.ForeignKey(Okpd, on_delete=models.SET_NULL, null=True, blank=True)
    okved = models.ForeignKey(Okved, on_delete=models.SET_NULL, null=True, blank=True)
    ens = models.ForeignKey(Ens, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta(object):
        app_label = 'nomenclature'

    """ 
    Гененируем новый номенклатурный номер согласно соглашениям
    """
    def generate_number(self):
        # получаем строку шифра ОКПД2
        number = str(self.okpd.code).replace('.','') if self.okpd else ''

        # подсчитаем количество ведущих нулей
        sum = 0
        for char in number:
            if char == '0': sum += 1
            else: break

        # если в строке не все цифры, к примеру, имя группы "А", то делаем пустую строку
        if not all(char.isdigit() for char in number): number = ''

        # берём только первые 6 смиволов
        number = number[:6]

        # делаем из него восьмисимвольную строку, заполненную ОКПД слева и нулями
        number = '{:0<10s}'.format(number)

        # ищем изделие с таким же номенклатурным номером
        while Product.objects.filter(number=number).count() > 0:
            # если такое изделие существует, то наращиваем номенклатурный номер на единицу
            converted = int(number)
            number = str(converted + 1)

            #возвращаем ведущие нули
            number = '{:0>10s}'.format(number)

        return number