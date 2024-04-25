from rest_framework import serializers
from .models import Product, Feedback, Reviews, Brand
from django.contrib.auth.models import User


from .services import validator_of_discount


class ProductSerializer(serializers.ModelSerializer):

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
    class Meta:
        model = User
        exclude = ('password',)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("id", "user", "image", "review", "created_at")
        lookup_field = "id"
        read_only_fields = ("id", "user", "created_at")


class ReviewsSerializer(serializers.ModelSerializer):

    username = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    product = serializers.SlugRelatedField(slug_field="slug", queryset=Product.objects.all())

    class Meta:
        model = Reviews
        fields = ("id", "product", "username", "text", "created_date")
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }