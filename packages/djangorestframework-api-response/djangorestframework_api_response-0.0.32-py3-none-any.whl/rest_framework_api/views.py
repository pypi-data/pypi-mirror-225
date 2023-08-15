from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import APIResponseSerializer
from .pagination import CustomPagination


class BaseAPIView(APIView):
    def create_response(
        self, success=True, data=None, error=None, status_code=status.HTTP_200_OK
    ):
        """Create a standardized response."""
        response_data = {"success": success, "status": status_code}

        if data is not None:
            response_data["results"] = data
        if error is not None:
            response_data["error"] = error

        serializer = APIResponseSerializer(data=response_data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_response(self, data=None, status=status.HTTP_200_OK):
        """Send a standardized success response."""
        return self.create_response(success=True, data=data, status_code=status)

    def send_error(self, error, status=status.HTTP_400_BAD_REQUEST):
        """Send a standardized error response."""
        return self.create_response(success=False, error=error, status_code=status)


class StandardAPIView(BaseAPIView):
    def paginate_and_create_response(self, request, data, extra_data=None):
        """Paginate data and create a standardized response."""
        try:
            paginator = CustomPagination()
            paginated_data = paginator.paginate_data(data, request)
            response_data = {
                "success": True,
                "status": status.HTTP_200_OK,
                "results": paginated_data,
                "count": paginator.count,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
            }

            if extra_data:
                response_data["extra_data"] = extra_data

            serializer = APIResponseSerializer(data=response_data)
            if serializer.is_valid():
                return Response(serializer.validated_data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return self.send_error(str(e))

    def paginate_response(self, request, data):
        """Paginate and send a response without extra data."""
        return self.paginate_and_create_response(request, data)

    def paginate_response_with_extra(self, request, data, extra_data):
        """Paginate and send a response with extra data."""
        return self.paginate_and_create_response(request, data, extra_data=extra_data)


# ============= Demo Views ============= #


# BaseAPIView Demos
class BaseDemoSuccessView(BaseAPIView):
    """
    A demo view to showcase sending a successful response with BaseAPIView.
    """

    def get(self, request):
        sample_data = {"message": "This is a success message from BaseDemoSuccessView."}
        return self.send_response(data=sample_data, status=status.HTTP_200_OK)


class BaseDemoErrorView(BaseAPIView):
    """
    A demo view to showcase sending an error response with BaseAPIView.
    """

    def get(self, request):
        error_msg = "This is an error message from BaseDemoErrorView."
        return self.send_error(error=error_msg, status=status.HTTP_400_BAD_REQUEST)


# StandardAPIView Demos
class StandardDemoPaginatedView(StandardAPIView):
    """
    A demo view to showcase basic paginated responses using StandardAPIView.
    """

    def get(self, request):
        sample_data = [
            {"id": i, "content": f"Item {i}"} for i in range(1, 51)  # 50 items
        ]
        return self.paginate_response(request, sample_data)


class StandardDemoPaginatedWithExtraView(StandardAPIView):
    """
    A demo view to showcase paginated responses with extra data using StandardAPIView.
    """

    def get(self, request):
        sample_data = [
            {"id": i, "content": f"Item {i}"} for i in range(1, 51)  # 50 items
        ]
        extra_data = {
            "metadata": "This is some extra data that accompanies the paginated results."
        }
        return self.paginate_response_with_extra(
            request, sample_data, extra_data=extra_data
        )
