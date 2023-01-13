from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter

from nomenclature.pagination import CustomPagination
from nomenclature.models.units import Unit, UnitSerializer
from nomenclature.models.okpd import Okpd, OkpdSerializer
from nomenclature.models.okved import Okved, OkvedSerializer
from nomenclature.models.ens import Ens, EnsSerializer

class UnitViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class OkpdViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Okpd.objects.all()
    serializer_class = OkpdSerializer

class OkvedViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Okved.objects.all()
    serializer_class = OkvedSerializer

class EnsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Ens.objects.all()
    serializer_class = EnsSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ['number', 'name', 'unit', 'okpd', 'okved', 'notes']
