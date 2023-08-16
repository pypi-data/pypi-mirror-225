from rest_framework import status, serializers

from app_generic_api.api_slugs import RegisteredApiSlugs
from app_generic_api.standard_utils import get_message_response, ErrorCodeText
from app_generic_api.generic_base import NewListModelMixin, NewRetrieveModelMixin, NewCreateModelMixin
from rest_framework.response import Response



class GenericApiService:
    def __init__(self, slugs_list_of_dicts=None):
        if slugs_list_of_dicts is None:
            slugs_list_of_dicts = []
        self.slugs_list_of_dicts = slugs_list_of_dicts
        self.update_api_slugs()

    slugs_list_of_dicts = []
    api_slugs = dict()

    def get_api_slugs(self):
        final_dict = dict()
        for item in self.slugs_list_of_dicts:
            assert isinstance(item, dict)
            for key in item.keys():
                assert key not in final_dict
            final_dict.update(item)
        return final_dict

    def update_api_slugs(self):
        self.api_slugs = self.get_api_slugs()

    def get_generic_api_response(
        self,
        api_slug: str,
        body: dict or None,
        query_params: dict or None,
        method: str,
        request
    ):
        registered_api = self.api_slugs.get(api_slug)
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