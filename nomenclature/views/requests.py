from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from nomenclature.models.requests import Request
from nomenclature.serializers.request import RequestSerializer
from nomenclature.serializers.generic_request import GenericRequestSerializer
from nomenclature.pagination import CustomPagination
from nomenclature.services import get_stats
from nomenclature.models.approvers import Approver

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.filter(approved_at__isnull=True)
    pagination_class = CustomPagination
    serializer_class = RequestSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'current_user_id': self.request.auth_user.id})
        return context

    def retrieve(self, request, pk):
        queryset = Request.objects.all()
        request_obj = get_object_or_404(queryset, pk=pk)
        approvements = request_obj.get_approvements()
        approvers_left = request_obj.get_approvers_left()
        response = RequestSerializer(
            request_obj,
            context={
                'approvements': approvements,
                'approvers_left': approvers_left,
                'approvers_all': Approver.objects.all(),
                }
        ).data
        return Response(response)

    def update(self, request, pk=None):
        request_obj = Request.objects.get(pk=pk)
        request_obj.clear_approvements()
        
        return super().update(request, pk)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        recent_approved = GenericRequestSerializer(Request.recent_approved(), many=True)
        recent_created = GenericRequestSerializer(Request.recent_created(), many=True)
        most_popular = GenericRequestSerializer(Request.most_popular(), many=True)
        return Response({
            'recent_approved': recent_approved.data,
            'recent_created': recent_created.data,
            'most_popular': most_popular.data,
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        return Response(get_stats(Request.objects))

    @action(detail=True, methods=['post'], url_path='change-approvement')
    def change_approvement(self, request, pk=None):
        request_obj = Request.objects.get(pk=pk)
        request_obj.change_approvement(
            state=request.data.get('state', 0),
            user_id=request.auth_user.id,
            comment=request.data.get('comment', ''))

        return Response(status=status.HTTP_200_OK)
