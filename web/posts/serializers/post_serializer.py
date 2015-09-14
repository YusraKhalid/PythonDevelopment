from django.utils import timezone
from rest_framework import serializers
from web.constants import TITLE_IS_TOO_SHORT, MUST_BE_NON_NEGATIVE, GIVE_VALID_TIME
from web.posts.models import Post
from web.users.models import Address
from web.users.serializers.address_serializer import AddressSerializer


class PostSerializer(serializers.ModelSerializer):

    location = AddressSerializer()
    user_id = serializers.PrimaryKeyRelatedField(source='posted_by', read_only=True)
    number_of_views = serializers.SerializerMethodField(source='get_number_of_views', read_only=True)
    is_sold = serializers.BooleanField(read_only=True)
    posted_on = serializers.DateTimeField(read_only=True)
    time_until_expired = serializers.SerializerMethodField(source='get_time_until_expired', read_only=True)
    full_name = serializers.SerializerMethodField(source='get_full_name', read_only=True)
    number_of_requests = serializers.SerializerMethodField(source='get_number_of_requests', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user_id', 'title', 'full_name', 'area', 'location', 'description', 'kind', 'number_of_views',
                  'contact_number', 'demanded_price', 'posted_on', 'expired_on', 'is_sold', 'number_of_requests',
                  'time_until_expired')

    # noinspection PyMethodMayBeStatic
    def get_number_of_views(self, post):
        return post.number_of_views

    # noinspection PyMethodMayBeStatic
    def get_time_until_expired(self, post):
        return post.time_until_expired

    # noinspection PyMethodMayBeStatic
    def get_full_name(self, post):
        return post.posted_by.get_full_name()

    # noinspection PyMethodMayBeStatic
    def get_number_of_requests(self, post):
        return post.requests.count()

    # noinspection PyMethodMayBeStatic
    def validate_title(self, title):
        if len(title) < 5:
            raise serializers.ValidationError(TITLE_IS_TOO_SHORT)
        return title

    # noinspection PyMethodMayBeStatic
    def validate_area(self, area):
        if area <= 0.0:
            raise serializers.ValidationError(MUST_BE_NON_NEGATIVE)
        return area

    # noinspection PyMethodMayBeStatic
    def validate_expired_on(self, expired_on):
        time_delta = expired_on - timezone.now()
        if time_delta.total_seconds() < 0:
            raise serializers.ValidationError(GIVE_VALID_TIME)
        return expired_on

    # noinspection PyMethodMayBeStatic
    def validate_demand(self, demand):
        if demand <= 0.0:
            raise serializers.ValidationError(MUST_BE_NON_NEGATIVE)
        return demand

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location = Address.objects.create(**location_data)
        post = Post.objects.create(location=location, **validated_data)
        return post
