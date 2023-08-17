from django.http import HttpResponse
from django.shortcuts import render
# from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import serializers, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from app_generic_api.standard_utils import default_authentication_classes, get_error_response, ErrorCodeText, \
    RequestMethodType
from app_generic_api.generic_standard import GenericApiService
from rest_framework.response import Response


# Create your views here.

class GenericApiView(APIView):
    authentication_classes = default_authentication_classes
    permission_classes = (IsAuthenticated,)

    slugs_list_of_dicts=None

    class GenericApiSerializer(serializers.Serializer):
        api_slug = serializers.CharField(required=True)
        body = serializers.JSONField(required=False)
        query_params = serializers.JSONField(required=False)

    def generic_api_call(self, serializer_data: dict, method: str, request):
        serializer = self.GenericApiSerializer(data=serializer_data)
        if serializer.is_valid():
            api_slug = serializer.validated_data.get("api_slug")
            body = serializer.validated_data.get("body")
            query_params = serializer.validated_data.get("query_params")
            if body is None:
                body = {}
            if query_params is None:
                query_params = {}
            response = GenericApiService(slugs_list_of_dicts=self.slugs_list_of_dicts).get_generic_api_response(
                api_slug=api_slug,
                body=body,
                query_params=query_params,
                method=method,
                request=request
            )
            if isinstance(response, HttpResponse):
                return response
            else:
                error_response = get_error_response(
                    error_code=ErrorCodeText.INVALID_DATA, errors={
                        "error": "Invalid response from api"
                    }
                )
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        error_response = get_error_response(
            error_code=ErrorCodeText.INVALID_DATA, errors=serializer.errors
        )
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    # @swagger_auto_schema(
    #     request_body=no_body,
    #     query_serializer=GenericApiSerializer(),
    # )
    def get(self, *args, **kwargs):
        return self.generic_api_call(serializer_data=self.request.GET, method=RequestMethodType.GET, request=self.request)

    # @swagger_auto_schema(
    #     request_body=GenericApiSerializer,
    # )
    def post(self, *args, **kwargs):
        return self.generic_api_call(serializer_data=self.request.data, method=RequestMethodType.POST, request=self.request)

    # @swagger_auto_schema(
    #     request_body=no_body,
    #     query_serializer=GenericApiSerializer(),
    # )
    def patch(self, *args, **kwargs):
        return self.generic_api_call(serializer_data=self.request.data, method=RequestMethodType.PATCH, request=self.request)

    # @swagger_auto_schema(
    #     request_body=no_body,
    #     query_serializer=GenericApiSerializer(),
    # )
    def put(self, *args, **kwargs):
        return self.generic_api_call(serializer_data=self.request.data, method=RequestMethodType.PUT, request=self.request)

    # @swagger_auto_schema(
    #     request_body=no_body,
    #     query_serializer=GenericApiSerializer(),
    # )
    def delete(self, *args, **kwargs):
        return self.generic_api_call(serializer_data=self.request.data, method=RequestMethodType.DELETE, request=self.request)

