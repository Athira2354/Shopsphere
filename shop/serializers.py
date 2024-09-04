from django.contrib.auth.models import User
from rest_framework import serializers
from shop.models import Product,Category,Brand,Size,Basket,BasketItem,Order


class UserSerializers(serializers.ModelSerializer):
    
    password1=serializers.CharField(write_only=True)#there is no such attributes in model ...only password is there.not password1 and password2

    password2=serializers.CharField(write_only=True) #when we arecreating only we use these ..iin responce we dot want so give it as write only
   
    class Meta:

        model=User
        
        fields=["id","username","email","password1","password2","password"] #we need/ to see the password as hashed...so we add password as read only field

        read_only_fields=["id","password"]                                  #otherwise we dont know whether it is hided or not

    def create(self,validated_data):

        print(" printing validated data",validated_data)  #validated data is a dictionary 

        password1=validated_data.pop("password1")

        password2=validated_data.pop("password2")
        
        if password1!=password2:

            raise serializers.ValidationError('password mismatched')
        
        else:

            return User.objects.create_user(**validated_data,password=password1)  #assingning paswd=any of the passwd1 or paswd2
        
class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model=Category

        fields=["id","name"]

class BrandSerializer(serializers.ModelSerializer):

    class Meta:

        model=Brand

        fields=["id","name"]

class SizeSerializer(serializers.ModelSerializer):

    class Meta:

        model=Size

        fields=["id","name"]


class ProductSerializer(serializers.ModelSerializer):

    category_object=CategorySerializer(read_only=True)

    # category_object=serializers.StringRelatedField(read_only=True)   #only returns the str field in cataegry model:ie the name only
    brand_object=BrandSerializer(read_only=True)

    size_object=SizeSerializer(read_only=True,many=True) #many=True bcoz we had given many to many field in model

    class Meta:

        model=Product

        fields='__all__'

class CartProductSerializer(serializers.ModelSerializer):
    
    class Meta:

        model=Product

        fields=["id","title","price","image"]
    

class BasketItemSerializer(serializers.ModelSerializer):

        item_total=serializers.CharField(read_only=True)

        product_object=CartProductSerializer(read_only=True)

        size_object=serializers.StringRelatedField()
    
        class Meta:

            model=BasketItem

            fields=[
                "id",
                "product_object",
                "size_object",
                "quantity",
                "item_total",
                "created_date"
            ]

class BasketSerializer(serializers.ModelSerializer):
    
    owner=serializers.StringRelatedField()
    
    basketitems=BasketItemSerializer(many=True)

    basket_total=serializers.CharField()

    class Meta:

        model=Basket

        fields=[
            "id",
            'basketitems',
            "owner",
            "basket_total",
        ]

class OrderSerializer(serializers.ModelSerializer):

    order_total=serializers.CharField(read_only=True)

    basket_item_objects=BasketItemSerializer(many=True,read_only=True)

    class Meta:

        model=Order
        
        fields="__all__"