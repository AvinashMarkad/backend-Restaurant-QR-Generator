from rest_framework import serializers
from .models import QRCode

class QRCodeSerializer(serializers.ModelSerializer):
    qr_code = serializers.SerializerMethodField()

    class Meta:
        model = QRCode
        fields = ['id', 'link', 'qr_code', 'created_at']
        read_only_fields = ['qr_code', 'created_at']

    def get_qr_code(self, obj):
        if obj.qr_code:
            request = self.context.get("request")
            url = obj.qr_code.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None
