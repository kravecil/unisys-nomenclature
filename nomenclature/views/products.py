from rest_framework import mixins, viewsets, filters
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from nomenclature.models.requests import Request
from nomenclature.serializers.generic_request import GenericRequestSerializer
from nomenclature.serializers.request import RequestSerializer
from nomenclature.pagination import CustomPagination

class ProductViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):

    queryset = Request.objects.filter(approved_at__isnull=False)
    pagination_class = CustomPagination
    serializer_class = GenericRequestSerializer
    filter_backends = [SearchFilter]
    search_fields = ['product__name', 'product__notes', 'product__number']

    SIMILARS_ITEMS = 6
    SIMILARS_MAX_ITEMS = 20

    # def get_queryset(self):
    #     if self.request.query_params.get('similars', 0):
    #         return Request.objects.filter(approved_at__isnull=False)[:3]
    #     return super().get_queryset()

    def list(self, request, *args, **kwargs):
        if request.query_params.get('similars', 0):
            search_filter = SearchFilter()
            queryset = search_filter.filter_queryset(
                request=request, queryset=self.queryset, view=self)

            if queryset.count() > self.SIMILARS_MAX_ITEMS: return Response([])
            serializer = RequestSerializer(queryset[:self.SIMILARS_ITEMS], many=True)

            return Response(serializer.data)

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()

        obj.views_count += 1
        obj.save()

        return Response(RequestSerializer(obj).data)
        # return super().retrieve(request, *args, **kwargs)