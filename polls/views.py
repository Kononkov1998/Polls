from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.views import ObtainAuthToken


class GetAuthToken(ObtainAuthToken):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING
            ),
            'password': openapi.Schema(
                type=openapi.TYPE_STRING
            )
        }))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
