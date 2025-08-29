from rest_framework import generics, status
from rest_framework.response import Response
from .models import QRCode
from .serializers import QRCodeSerializer

class QRCodeListCreateView(generics.ListCreateAPIView):
    """
    View to list all QR codes and create a new one.
    Handles GET (list) and POST (create) requests.
    """
    queryset = QRCode.objects.all().order_by('-created_at') # Order by newest first
    serializer_class = QRCodeSerializer

    def create(self, request, *args, **kwargs):
        """
        Override the default create method to add custom responses.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            # --- Custom Success Response ---
            response_data = {
                "success": True,
                "message": "QR Code generated successfully.",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            # --- Custom Error Response ---
            response_data = {
                "success": False,
                "message": "Failed to create QR code. Please check the provided data.",
                "errors": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class QRCodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a single QR code instance.
    Handles GET (retrieve), PUT (update), PATCH (partial update), and DELETE.
    """
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Override the default destroy method to add a custom success response.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        
        # --- Custom Success Response for Deletion ---
        response_data = {
            "success": True,
            "message": "QR Code deleted successfully."
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)





















# from rest_framework import generics
# from .models import QRCode
# from .serializers import QRCodeSerializer

# class QRCodeListCreateView(generics.ListCreateAPIView):
#     """
#     View to list all QR codes and create a new one.
#     Handles GET (list) and POST (create) requests.
#     """
#     queryset = QRCode.objects.all()
#     serializer_class = QRCodeSerializer
#     # That's it! DRF's generic view handles all the get() and post() logic for you.

# class QRCodeDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     View to retrieve, update, or delete a single QR code instance.
#     Handles GET (retrieve), PUT (update), PATCH (partial update), and DELETE.
#     """
#     queryset = QRCode.objects.all()
#     serializer_class = QRCodeSerializer
#     # The URL will specify which specific QR code to retrieve via its primary key (pk).
