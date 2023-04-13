from rest_framework import serializers
from .models import MenuItem, Cart, Order, OrderItem
#from datetime import datetime
import datetime
class MenuItemSerlializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
     unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='menuitem.price', read_only=True)
     name = serializers.CharField(source='menuitem.title', read_only=True)

     class Meta:
            model = Cart
            fields = ['user_id', 'menuitem', 'name', 'quantity', 'unit_price', 'price']
            extra_kwargs = {
                'price': {'read_only': True}
            }

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.CharField(source = 'menuitem.title',read_only=True)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='menuitem.price', read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['menuitem', 'quantity', 'unit_price', 'price']
    
    

class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True)
    date = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'orderitem_set']
        
    def get_date(self, obj):
        dt = datetime.combine(obj.date, datetime.min.time())
        return dt.isoformat()
    