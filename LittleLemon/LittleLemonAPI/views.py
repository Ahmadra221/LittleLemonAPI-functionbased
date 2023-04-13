from django.shortcuts import render, get_object_or_404
from .serializer import MenuItemSerlializer, CartSerializer, OrderItemSerializer, OrderSerializer
from .models import MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User, Group

from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
from rest_framework.throttling import  AnonRateThrottle, UserRateThrottle





@api_view(['GET','POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def menuitems_api(request):

    
    if request.method == 'GET':        
            items = MenuItem.objects.select_related('category').all()
            for item in items:
             print(item)
      #....some other code checking certain conditions.
            category_name = request.query_params.get('category')
            price = request.query_params.get('price')
            search = request.query_params.get('search')
            perpage = request.query_params.get('perpage', default=2)
            page = request.query_params.get('page', default=1)
            if category_name:
                items = items.filter(category__title = category_name)
            if price:
                items = items.filter(price__lte = price)
            if search:
                items = items.filter(title__icontains = search)

            paginator = Paginator(items, per_page  = perpage)
            try:
             items =paginator.page(number = page)
            except EmptyPage:
             items =[]
          
          
            serialized_items = MenuItemSerlializer(items,many=True,  context={'request': request})
            return Response(serialized_items.data, status.HTTP_200_OK)
    
    if request.method == 'POST':
          if  request.user.groups.filter(name='Manager').exists():
            serialized_item = MenuItemSerlializer(data=request.data)
            if serialized_item.is_valid(raise_exception=True):
           
                serialized_item.save()
                return Response(serialized_item.data, status.HTTP_201_CREATED)
            return Response(MenuItemSerlializer.errors, status.HTTP_400_BAD_REQUEST)
          else:
               return Response({'message':'only managers can add menu items'}, status.HTTP_401_UNAUTHORIZED)
        
    if request.method == 'PUT' or 'PATCH' or 'DELETE':
         if   request.user.groups.filter(name='Manager').exists():
                    return Response({'message':'not applicable'}, status.HTTP_200_OK)
         else:
                    return Response({'message':'only managers can access this'}, status.HTTP_401_UNAUTHORIZED)

               

@api_view(['GET','POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def menu_item(request, pk):
      item = MenuItem.objects.get(pk=pk)
      if request.method == 'GET':
            item = get_object_or_404(MenuItem,pk=pk)
            serlialized_item = MenuItemSerlializer(item)
            return Response(serlialized_item.data, status.HTTP_200_OK)
      
      if request.method == 'POST':
            if  not request.user.groups.filter(name='Manager').exists(): 
                  return Response({'message':'only managers can access this'},
                                   status.HTTP_401_UNAUTHORIZED)
            
      if  request.method == 'PATCH':
            if  not request.user.groups.filter(name='Manager').exists(): 
                  return Response({'message':'only managers can access this'},
                                   status.HTTP_401_UNAUTHORIZED)
            else:
                  serialized_item = MenuItemSerlializer(item, data=request.data, partial=True)
                  if serialized_item.is_valid(raise_exception=True):
                    serialized_item.save()
                    return Response(serialized_item.data, status.HTTP_200_OK)
                  return Response(MenuItemSerlializer.errors, status.HTTP_400_BAD_REQUEST)
      if request.method == 'PUT':
            
            if  not request.user.groups.filter(name='Manager').exists(): 
                  return Response({'message':'only managers can access this'},
                                   status.HTTP_401_UNAUTHORIZED)
            else:
                  serialized_item = MenuItemSerlializer(item, data=request.data)
                  if serialized_item.is_valid(raise_exception=True):
                    serialized_item.save()
                    return Response(serialized_item.data, status.HTTP_200_OK)
                  return Response(MenuItemSerlializer.errors, status.HTTP_400_BAD_REQUEST)

            
      if request.method == 'DELETE':
             if  not request.user.groups.filter(name='Manager').exists(): 
                   return Response({'message':'only managers can access this'},
                                    status.HTTP_401_UNAUTHORIZED)
            
             else:
                  item = get_object_or_404(MenuItem,pk=pk)
                  item.delete()

                  return Response({'msg':'deleted successfully'},
                                   status.HTTP_200_OK)




@api_view(['GET','POST'])  
@permission_classes([IsAdminUser])
@throttle_classes([UserRateThrottle])
def product_managers(request):

    
    managers_group = Group.objects.get(name='Manager')
    
    if  not request.user.groups.filter(name='Manager').exists(): 
                   return Response({'message':'only managers can access this'}, status.HTTP_401_UNAUTHORIZED)
            
    else:
            

            if request.method == 'GET':
                   managers_group = Group.objects.get(name='Manager')
                   managers = managers_group.user_set.all().values()
                   return Response(managers, status.HTTP_200_OK)
            
            if request.method == 'POST':
                   username = request.data['username']
                   if username:
                         
                    user = get_object_or_404(User, username = username)
                    managers_group.user_set.add(user)
                    return Response({'message': 'ok'}, status.HTTP_201_CREATED)
                   return Response({'message': 'User does not exist'}, status.HTTP_400_BAD_REQUEST)
                   
            
      
@api_view(['DELETE'])  
@permission_classes([IsAdminUser])
@throttle_classes([UserRateThrottle])
def product_managers_remove(request, pk):
       if  not request.user.groups.filter(name='Manager').exists(): 
                   return Response({'message':'only managers can access this'}, status.HTTP_401_UNAUTHORIZED)
            
       elif request.method == 'DELETE':
            user = get_object_or_404(User, id = pk)  
            managers_group = Group.objects.get(name='Manager')
            managers_group.user_set.remove(user)
            return Response({'message': 'ok'}, status.HTTP_200_OK)

       


@api_view(['GET','POST'])  
@permission_classes([IsAuthenticated])
def delivery_crew(request):

    
    delivery_men = Group.objects.get(name='Delivery crew')
    
    if  not request.user.groups.filter(name='Manager').exists(): 
                   return Response({'message':'only managers can access this'}, status.HTTP_401_UNAUTHORIZED)
            
    else:
            

            if request.method == 'GET':
                   delivery_men_group = Group.objects.get(name='Delivery crew')
                   delivery_men = delivery_men.user_set.all().values()
                   return Response(delivery_men, status.HTTP_200_OK)
            
            if request.method == 'POST':
                   username = request.data['username']
                   user = get_object_or_404(User, username = username)
                   delivery_men.user_set.add(user)
                   return Response({'message': 'ok'}, status.HTTP_201_CREATED)
            
@api_view(['DELETE'])  
@permission_classes([IsAuthenticated])
def delivery_crew_remove(request, pk):
       
       if  not request.user.groups.filter(name='Manager').exists(): 
                   return Response({'message':'only managers can access this'},
                                    status.HTTP_401_UNAUTHORIZED)
      
       else:
              
            user = get_object_or_404(User, id = pk)
            delivery_men = Group.objects.get(name='Delivery crew')

            if request.method == 'DELETE':
                  delivery_men.user_set.remove(user)
                  return Response({'message': 'ok'}, status.HTTP_200_OK)
            

@api_view(['GET','POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart(request):
       
      if request.method == 'GET':
            
             
            user_id = request.user.id
            #cart = Cart.objects.get(user = user_id)
            cart = get_object_or_404(Cart, user = user_id)

            serliazed_cart = CartSerializer(cart)
            return Response(serliazed_cart.data, status.HTTP_200_OK)
            
      
      if request.method == 'POST':
            user = request.user
            requested_menuitem = request.data['menuitem']
            quantity = request.data['quantity']
            menuitem = get_object_or_404(MenuItem, title = requested_menuitem)
            cart_exist = Cart.objects.filter(user=user, menuitem=menuitem).exists()
            if cart_exist:
                  cart = Cart.objects.get(user=user, menuitem=menuitem)
                  cart.quantity += int(quantity)
                  cart.price = cart.quantity * cart.unit_price
                  cart.save()
                  return Response({'message': 'cart already exists'})
            price = menuitem.price * int(quantity)
            cart = Cart.objects.create(user=user,menuitem=menuitem,quantity=quantity,unit_price =menuitem.price,price=price)
            return Response({'cart item created': 'item added to cart'}, status.HTTP_201_CREATED)
      
      if request.method == 'DELETE':
        user = request.user
        Cart.objects.filter(user=user).delete()
        return Response({'message':'Cart emptied'})
      




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  
@throttle_classes([UserRateThrottle]) 
def order_view(request):
    user = request.user
    if request.method == 'GET':
        if request.user.groups.filter(name ='Manager').exists() or request.user.groups.filter(name='Delivery crew').exists():
            order= Order.objects.prefetch_related('orderitem_set').all()
            rstatus = request.query_params.get('status')
            if rstatus:
                order = order.filter(status=rstatus)
                
            serializer= OrderSerializer(order, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        orders = Order.objects.filter(user=user).prefetch_related('orderitem_set')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=user)
        if not cart_items:
            return Response({'message': 'No item in the cart'}, status.HTTP_400_BAD_REQUEST)
        today = datetime.date.today()
        today_str = today.strftime('%Y-%m-%d')
        order = Order.objects.create(user=user, total=0, date =today_str )
        order_items =[]
        for cart_item in cart_items:
            order_item = OrderItem(
                order=order,
                menuitem = cart_item.menuitem,
                quantity = cart_item.quantity,
                unit_price =cart_item.menuitem.price,
                price = cart_item.quantity * cart_item.menuitem.price
                
                
            )
            order_items.append(order_item)
        
        OrderItem.objects.bulk_create(order_items)
        total = sum([order_item.price for order_item in order_items])
        order.total = total
        order.save()

        cart_items.delete()
        
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def single_order_view(request, pk):
    user = request.user
    if request.method == 'GET':
        if request.user.groups.filter(name='Manager').exists():
            order= get_object_or_404(Order, pk=pk)
            order_items = OrderItem.objects.filter(order=order)
            serializer = OrderItemSerializer(order_items, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        try:
            order = Order.objects.get(pk=pk, user= user)
            order_items = OrderItem.objects.filter(order=order)
            serializer = OrderItemSerializer(order_items, many=True)
            return Response(serializer.data, status.HTTP_200_OK)

        
        except ObjectDoesNotExist:
            return Response({'message': 'Order not found'},status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        if request.user.groups.filter(name='Manager').exists() or request.user.groups.filter(name='Delivery crew').exists():
            order_items = Order.objects.get(pk=pk)
            serialized_item = OrderSerializer(order_items,data=request.data, partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_200_OK)
        return Response({'message':'You are not authorized to pefrorm this operation '}, status.HTTP_401_UNAUTHORIZED)
    if request.method == 'DELETE':
        if request.user.groups.filter(name='manager').exists():
            order = get_object_or_404(Order,pk=pk)
            order.delete()
            return Response({'message':'Order deleted '})


            

        


              
                   
                   

           
            
            