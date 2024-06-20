import uuid

from rest_framework import serializers

from users.models_roles import Role
from users.models_users import User


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

        required_fields = [
            'name',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        ]


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(source="role_id", read_only=True)

    class Meta:
        model = User
        fields = '__all__'

        required_fields = [
            'username',
            'password',
            'email',
            'role_id'
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def create(self, validated_data):

        if self.context['request'].user.is_authenticated:
            validated_data['created_by'] = self.context['request'].user.nim
            validated_data['updated_by'] = self.context['request'].user.nim
        else:
            validated_data['created_by'] = "system"
            validated_data['updated_by'] = "system"

        validated_data['id'] = uuid.uuid4()

        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):

        if self.context['request'].user.is_authenticated:
            validated_data['updated_by'] = self.context['request'].user.nim
        else:
            validated_data['updated_by'] = "system"

        return super(UserSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['role'] = RoleSerializer(instance.role_id).data
        return representation
