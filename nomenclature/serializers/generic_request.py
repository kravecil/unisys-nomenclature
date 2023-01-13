from rest_framework import serializers

from nomenclature.models.requests import Request
from nomenclature.models.products import Product
from nomenclature.models.units import Unit
from nomenclature.models.okpd import Okpd
from nomenclature.models.okved import Okved
# from nomenclature.models import Person
from nomenclature.serializers.product import ProductSerializer

class GenericRequestSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
    created_at = serializers.SerializerMethodField()
    approved_at = serializers.SerializerMethodField()

    class Meta:
        model = Request
        fields = ["pk", "created_at", "approved_at", "product"]

    def get_created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    
    def get_approved_at(self, obj):
        return obj.approved_at.strftime('%d.%m.%Y %H:%M') if obj.approved_at else None

    def create(self, validated_data):
        product_dict = validated_data.pop('product')
        product = Product.objects.create(**product_dict)
        if not product.number:
            product.number = product.generate_number()
            product.save()
        return Request.objects.create(
            product=product,
            person_who_created=self.context.get('current_user_id'))

    def update(self, instance, validated_data):
        product_data = validated_data.pop('product')
        product = instance.product
        
        Product.objects.filter(pk=product.pk).update(**product_data)

        product_new = Product.objects.get(pk=product.pk)

        request = self.context.get('request', None)
        generate = request.data.get('generate', False)
        if generate:
            product_new.number = product_new.generate_number()
            product_new.save()
        # product.name = product_data.get('name', product.name)
        # product.notes = product_data.get('notes', product.notes)
        # product.save()

        return instance
