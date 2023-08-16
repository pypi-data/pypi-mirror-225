from rest_framework import serializers

from app_generic_api.utils import is_valid_uuid


class ListMethodBaseSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(default=20)

    def validate_page(self, value):
        if value < 1:
            raise serializers.ValidationError("Page must be greater than 0")
        return value

    def validate_page_size(self, value):
        if value < 1:
            raise serializers.ValidationError("Page size must be greater than 0")
        return value

class ObjectIdValidationMixin(serializers.Serializer):
    class IdTypeChoices:
        INT = "int"
        STR = "str"
        UUID = "uuid"

    object_id = serializers.CharField(required=True)
    object_id_type = IdTypeChoices.INT

    def _validate_object_id_int(self, value):
        try:
            value = int(value)
        except ValueError:
            raise serializers.ValidationError("Object id must be integer")
        return value

    def _validate_object_id_str(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Object id must be string")
        return value

    def _validate_object_id_uuid(self, value):
        print("checking uuid")
        if not is_valid_uuid(value):
            raise serializers.ValidationError("Object id must be uuid")
        print("is valid uuid")
        return value



    def validate_object_id(self, value):
        if self.object_id_type == self.IdTypeChoices.INT:
            return self._validate_object_id_int(value)
        elif self.object_id_type == self.IdTypeChoices.STR:
            return self._validate_object_id_str(value)
        elif self.object_id_type == self.IdTypeChoices.UUID:
            print("here")
            return self._validate_object_id_uuid(value)
        else:
            print("here2")
            raise NotImplementedError("Invalid object_id_type")


class RetrieveMethodBaseSerializer(ObjectIdValidationMixin):
    pass

class PutMethodBaseSerializer(ObjectIdValidationMixin):
    data_to_update = serializers.JSONField(required=True)