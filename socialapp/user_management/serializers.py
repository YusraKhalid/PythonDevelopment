from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import serializers

from user_management.models import AcademicInformation, UserProfile, SocialGroup, WorkInformation, Friend, Notification, \
    UserGroup, GroupRequest, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class BasicUserSerializer(serializers.ModelSerializer):
    auth_user = UserSerializer()

    def create(self, validated_data):
        auth_user = validated_data.pop('auth_user', None)
        user_created = User.objects.create_user(**auth_user)
        validated_data['auth_user'] = user_created
        profile_data = UserProfile.objects.create(**validated_data)
        return profile_data

    class Meta:
        model = UserProfile
        fields = ['auth_user', 'date_of_birth', 'phone', 'address']


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    auth_user = UserSerializer()

    def get_work_information_url(self, obj):
        return reverse(viewname='work-information') + "?username={}".format(obj.auth_user.username)

    def get_academic_information_url(self, obj):
        return reverse(viewname='academic-information') + "?username={}".format(obj.auth_user.username)

    work_information_url = serializers.SerializerMethodField(read_only=True)
    academic_information_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['auth_user', 'date_of_birth', 'phone', 'address', 'academic_information_url', 'work_information_url']


class WorkInformationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkInformation
        exclude = ['user_profile', ]


class WorkInformationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkInformation
        fields = '__all__'


class AcademicInformationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicInformation
        exclude = ['user_profile', ]


class AcademicInformationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicInformation
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialGroup
        fields = '__all__'


class GroupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupRequest
        fields = '__all__'


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'


class UserGroupSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user.auth_user.username')
    name = serializers.StringRelatedField(source='group.name', read_only=True, )

    class Meta:
        model = UserGroup
        fields = ['username', 'name', 'is_admin']


class UserSocialGroupsSerializer(serializers.ModelSerializer):
    social_groups = UserGroupSerializer(source='usergroup_set', read_only=True, many=True)

    class Meta:
        model = UserProfile
        fields = ['social_groups', ]


class UserFriendsSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='auth_user.username')
    user_friends = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['username', 'user_friends']

    def get_user_friends(self, obj):
        friends = [UserSerializer(user.auth_user).data for user in obj.user_friends.all()]
        return friends


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['text', 'status', 'type']
