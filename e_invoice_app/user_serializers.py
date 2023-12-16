from rest_framework import serializers
from e_invoice_app.models import UserDetails


class UserSerializers(serializers.ModelSerializer):

    
    class Meta:
        model = UserDetails
        fields = '__all__'