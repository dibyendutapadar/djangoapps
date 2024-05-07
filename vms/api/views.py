from rest_framework import viewsets
from ..models import Vendor  # Adjusted import to refer to the parent directory
from .serializers import VendorSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
