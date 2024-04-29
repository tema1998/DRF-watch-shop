from rest_framework import serializers
from .models import Product, Feedback, Reviews, Brand, OrderProduct, Order
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


class OrderProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = ["product", "quantity", "total_price"]

    def get_product(self,obj):
        return obj.product.model


class CartSerializer(serializers.ModelSerializer):
    ordered_products = OrderProductSerializer(many=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ["user", "ordered_products", "is_ordered", "order_price", "created_at"]


class AddProductToCartSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].default = serializers.CurrentUserDefault()
        self.fields["user"].required = False

    class Meta:
        model = OrderProduct
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
        ordered_product, created = OrderProduct.objects.get_or_create(
            user=user,
            product=product,
            order=order,
        )
        if created:
            ordered_product.order = order
            ordered_product.save()
            return ordered_product
        else:
            ordered_product.quantity += 1
            ordered_product.save()
            return ordered_product


class RemoveProductFromCartSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].default = serializers.CurrentUserDefault()
        self.fields["user"].required = False

    class Meta:
        model = OrderProduct
        fields = ["product", "user"]

    def validate(self, data):
        ordered_product = OrderProduct.objects.filter(user=data["user"], product=data["product"])
        if not ordered_product:
            raise serializers.ValidationError("The product isn't in your cart.")
        return data

    def save(self):
        user = self.validated_data["user"]
        product = self.validated_data["product"]
        ordered_product = OrderProduct.objects.get(user=user, product=product)
        if ordered_product.quantity == 1:
            ordered_product.delete()
            return "The product was successfully removed from your cart."
        else:
            ordered_product.quantity -= 1
            ordered_product.save()
            return "The quantity of product in the your cart was successfully decreased."
