from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
def example_view(request):
    permission_classes = [IsAuthenticated]
    print(request.data)
    return Response(
        {"message": "Hello, World!", "user": str(request.user)},
        status=status.HTTP_200_OK,
    )
