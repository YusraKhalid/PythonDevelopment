from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'password')
        read_only_fields = ('is_staff', 'is_superuser',
                            'is_active', 'date_joined',)
        extra_kwargs = {
            'password': {'write_only': True}
        }
