from rest_framework import status, serializers

from app_generic_api.api_slugs import RegisteredApiSlugs
from app_generic_api.standard_utils import get_message_response, ErrorCodeText
from app_generic_api.generic_base import NewListModelMixin, NewRetrieveModelMixin, NewCreateModelMixin
from rest_framework.response import Response


registered_api_slug_dict = RegisteredApiSlugs.get()

class GenericApiService:

    def get_generic_api_response(
        self,
        api_slug: str,
        body: dict or None,
        query_params: dict or None,
        method: str,
        request
    ):
        registered_api = registered_api_slug_dict.get(api_slug)
        if not registered_api:
            return Response(
                get_message_response(
                    message_code=ErrorCodeText.INVALID_DATA,
                    messages=["Invalid api slug"]
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        if registered_api["method"] != method:
            return Response(
                get_message_response(
                    message_code=ErrorCodeText.INVALID_DATA,
                    messages=["Api method not found"]
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        return registered_api["func"](
            body=body,
            query_params=query_params,
            method=method,
            request=request
        )