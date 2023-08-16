from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import APIResponseSerializer
from .pagination import CustomPagination


class BaseAPIView(APIView):
    def send_response(self, data=None, status=status.HTTP_200_OK):
        serializer = APIResponseSerializer(
            {"success": True, "status": status, "results": data}
        )
        return Response(serializer.data, status=status)

    def send_error(self, error, status=status.HTTP_400_BAD_REQUEST):
        serializer = APIResponseSerializer(
            {"success": False, "status": status, "error": error}
        )
        return Response(serializer.data, status=status)


class StandardAPIView(BaseAPIView):
    def paginate_response(self, request, data):
        try:
            paginator = CustomPagination()
            paginated_data = paginator.paginate_data(data, request)
            serializer = APIResponseSerializer(
                {
                    "success": True,
                    "status": status.HTTP_200_OK,
                    "results": paginated_data,
                    "count": paginator.count,
                    "next": paginator.get_next_link(),
                    "previous": paginator.get_previous_link(),
                }
            )
            return Response(serializer.data)
        except Exception as e:
            serializer = APIResponseSerializer(
                {
                    "success": False,
                    "status": status.HTTP_400_BAD_REQUEST,
                    "error": str(e),
                }
            )
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def paginate_response_with_extra(self, request, data, extra_data):
        try:
            paginator = CustomPagination()
            paginated_data = paginator.paginate_data(data, request)
            serializer = APIResponseSerializer(
                {
                    "success": True,
                    "status": status.HTTP_200_OK,
                    "results": paginated_data,
                    "extra_data": extra_data,
                    "count": paginator.count,
                    "next": paginator.get_next_link(),
                    "previous": paginator.get_previous_link(),
                }
            )
            return Response(serializer.data)
        except Exception as e:
            serializer = APIResponseSerializer(
                {
                    "success": False,
                    "status": status.HTTP_400_BAD_REQUEST,
                    "error": str(e),
                }
            )
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


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
