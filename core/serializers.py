from rest_framework import serializers
from .models import Product, Feedback, Reviews, Brand
from django.contrib.auth.models import User


from .services import validator_of_discount


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for product model.
    """

    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    brand = serializers.SlugRelatedField(slug_field="name", queryset=Brand.objects.all())
    discount = serializers.IntegerField(validators=[validator_of_discount])

    class Meta:
        model = Product
        fields = ("id", "brand", "model", "slug", "description", "image", "created_at", "author", "price", "discount")
        lookup_field = 'slug'
        read_only_fields = ('id', 'slug', 'created_at', 'author')
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registration of user.
    """

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password2',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Method create user model if passwords are equals.
        """
        username = validated_data['username']
        password = validated_data['password']
        password2 = validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': "Passwords don't match"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user model.
    """
    class Meta:
        model = User
        exclude = ('password',)


class FeedbackSerializer(serializers.ModelSerializer):
    """
    Serializer for feedback model.
    """
    class Meta:
        model = Feedback
        fields = ("id", "user", "image", "review", "created_at")
        lookup_field = "id"
        read_only_fields = ("id", "user", "created_at")


class ReviewsSerializer(serializers.ModelSerializer):
    """
    Serializer for review model.
    """
    class Meta:
        model = Reviews
        fields = ("id", "product", "user", "text", "created_at")
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }
        read_only_fields = ("id", "user", "created_at")