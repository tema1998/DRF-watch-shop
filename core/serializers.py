from rest_framework import serializers
from .models import Product, Feedback, Reviews, Brand, OrderItem, Order
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


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price_with_discount"]

    def get_product(self,obj):
        return obj.product.model


class CartSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ["user", "orderitems", "is_ordered", "order_price", "created_at"]


class AddProductToCartSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].default = serializers.CurrentUserDefault()
        self.fields["user"].required = False

    class Meta:
        model = OrderItem
        fields = ["product", "user"]

    def validate_product(self, value):
        if not value.is_available:
            raise serializers.ValidationError("Product is out of stuck.")
        return value

    def create(self, validated_data):
        user = validated_data["user"]
        product = validated_data["product"]
        order, created = Order.objects.get_or_create(
            user=user,
            is_ordered=False,
        )
        orderitem, created = OrderItem.objects.get_or_create(
            user=user,
            product=product,
            order=order,
        )
        if created:
            orderitem.order = order
            orderitem.save()
            return orderitem
        else:
            orderitem.quantity += 1
            orderitem.save()
            return orderitem

