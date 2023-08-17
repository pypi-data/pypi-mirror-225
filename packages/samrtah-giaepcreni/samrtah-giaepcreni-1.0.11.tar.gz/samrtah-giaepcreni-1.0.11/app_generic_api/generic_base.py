from collections import OrderedDict

from django.core.paginator import InvalidPage
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.settings import api_settings

from app_generic_api.standard_utils import ErrorCodeText, get_error_response


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    # take the actual & ovveride functions to substitute request variable

    def get_page_size(self, request):
        raise NotImplementedError

    def paginate_queryset(self, queryset, page_number, view=None, given_page_size=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        if given_page_size is not None:
            page_size = given_page_size
        else:
            page_size = self.page_size
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(paginator, page_number=page_number)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        return list(self.page)

    def get_paginated_response(self, data):

        def next_page_number():
            if not self.page.has_next():
                return None
            next = self.page.next_page_number()
            return next

        def prev_page_number():
            if not self.page.has_previous():
                return None
            page_number = self.page.previous_page_number()
            return page_number

        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', next_page_number()),
            ('previous', prev_page_number()),
            ('results', data)
        ]))

    def get_page_number(self, paginator, page_number=1):
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        return page_number

class NewCreateModelMixin:
    """
    Create a model instance.
    """
    def create_func(
        self,
        request_data,
        request_serializer_class,
        model_serializer_class=None
    ):
        if model_serializer_class is None:
            model_serializer_class = request_serializer_class
        serializer = request_serializer_class(data=request_data)
        if not serializer.is_valid():
            error_response = get_error_response(
                error_code=ErrorCodeText.INVALID_DATA, errors=serializer.errors
            )
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        obj = self._perform_create(serializer)
        response_data = model_serializer_class(obj).data
        headers = self._get_success_headers(response_data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def _perform_create(
        self,
        serializer
    ):
        return serializer.save()

    def _get_success_headers(
        self,
        data
    ):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

def _get_queryset(
    queryset=None,
    model=None
):
    if queryset is None and model is None:
        raise Exception("Either queryset or model must be passed")
    if queryset is None:
        queryset = model.objects.all()
    return queryset

def _get_object(
    queryset,
    filter_kwargs
):
    obj = get_object_or_404(queryset, **filter_kwargs)

    # May raise a permission denied #TODO think about this
    # self.check_object_permissions(self.request, obj)

    return obj

class NewListModelMixin:
    """
    List a queryset.
    """
    pagination_class = CustomPageNumberPagination

    def _list_func_data(self, response_serializer_class, page_number, queryset=None, model=None, page_size=None, filter_kwargs:dict or None= None, order_by: str or None=None):
        queryset = _get_queryset(
            queryset=queryset,
            model=model
        )
        if filter_kwargs is not None:
            queryset = queryset.filter(**filter_kwargs)
        if order_by is not None:
            queryset = queryset.order_by(order_by)
        page = self.paginate_queryset(
            queryset=queryset,
            page_number=page_number,
            given_page_size=page_size
        )
        if page is not None:
            serializer = response_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = response_serializer_class(queryset, many=True)
        return serializer.data

    def list_func(self, response_serializer_class, page_number, queryset=None, model=None, page_size=None, filter_kwargs:dict or None= None, order_by: str or None=None):
        data = self._list_func_data(
            response_serializer_class=response_serializer_class,
            page_number=page_number,
            queryset=queryset,
            model=model,
            page_size=page_size,
            filter_kwargs=filter_kwargs,
            order_by=order_by
        )
        if isinstance(data, Response):
            return data
        return Response(data)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(
            self,
            queryset,
            page_number,
            given_page_size=None
    ):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(
            queryset=queryset,
            page_number=page_number,
            given_page_size=given_page_size,
        )

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class NewRetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    def retrieve_func(self ,response_serializer_class, filter_kwargs=dict, queryset=None, model=None):
        queryset = _get_queryset(
            queryset=queryset,
            model=model
        )
        instance = self._get_object(
            queryset=queryset,
            filter_kwargs=filter_kwargs
        )
        serializer = response_serializer_class(instance)
        return Response(serializer.data)

    def _get_object(self, queryset, filter_kwargs):
        return _get_object(
            queryset=queryset,
            filter_kwargs=filter_kwargs
        )

class NewUpdateModelMixin:
    """
    Update a model instance.
    """
    def update_func(self, update_serializer_class, data_to_update, response_serializer_class=None, queryset=None, model=None, filter_kwargs=dict, *args, **kwargs):
        if response_serializer_class is None:
            response_serializer_class = update_serializer_class
        partial = kwargs.pop('partial', False)
        queryset = _get_queryset(
            queryset=queryset,
            model=model
        )
        instance = self._get_object(
            queryset=queryset,
            filter_kwargs=filter_kwargs
        )
        serializer = update_serializer_class(
            instance=instance,
            data=data_to_update,
            context={
                'partial': partial,
            }
        )
        if not serializer.is_valid():
            error_response = get_error_response(
                error_code=ErrorCodeText.INVALID_DATA, errors=serializer.errors
            )
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        self._perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        response = response_serializer_class(instance).data
        return Response(response)

    def partial_update_func(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update_func(request, *args, **kwargs)

    def _get_object(self, queryset, filter_kwargs):
        return _get_object(
            queryset=queryset,
            filter_kwargs=filter_kwargs
        )

    def _perform_update(self, serializer):
        serializer.save()


class NewDestroyModelMixin:
    """
    Destroy a model instance.
    """
    def destroy_func(self, queryset=None, model=None, filter_kwargs=dict):
        queryset = _get_queryset(
            queryset=queryset,
            model=model
        )
        instance = self._get_object(
            queryset=queryset,
            filter_kwargs=filter_kwargs
        )
        self._perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _perform_destroy(self, instance):
        instance.delete()

    def _get_object(self, queryset, filter_kwargs):
        return _get_object(
            queryset=queryset,
            filter_kwargs=filter_kwargs
        )

class NewGenericApiMixin(NewListModelMixin, NewRetrieveModelMixin, NewCreateModelMixin, NewDestroyModelMixin, NewUpdateModelMixin):
    pass