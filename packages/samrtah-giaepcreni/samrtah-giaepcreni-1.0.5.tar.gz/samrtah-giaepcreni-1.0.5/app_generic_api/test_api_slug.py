import json

from django.contrib.auth import get_user_model

from app_generic_api.views import GenericApiView
User = get_user_model()
# serializer_data = {
#         "api_slug": "list_related_families",
#         "body": {},
#         "query_params": {}
#     }

# serializer_data = {
#         "api_slug": "retrieve_given_family",
#         "body": {},
#         "query_params": {
#             "object_id": "a63917d8-0755-48f2-8428-c6858ec71c32"
#         }
#     }

# serializer_data = {
#         "api_slug": "retrieve_given_person",
#         "body": {},
#         "query_params": {
#             "object_id": "a63917d8-0755-48f2-8428-c6858ec71c32"
#         }
#     }


def test():
    class FakeRequest:
        def __init__(self):
            self.user = User.objects.filter(profile__isnull=False).first()

    serializer_data = {
            "api_slug": "list_related_families",
            "body": {},
            "query_params": {}
        }
    method = "GET"
    response = GenericApiView().generic_api_call(
        serializer_data=serializer_data,
        method=method,
        request=FakeRequest()
    )
    # return response.data
    return json.loads(json.dumps(response.data))