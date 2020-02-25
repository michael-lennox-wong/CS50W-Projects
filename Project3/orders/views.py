from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError

from .models import Salad, Pasta, DinnerPlatter, Sub1, Sub2, Pizza, MenuItem,\
OrderItem, Order

from datetime import datetime

# Create your views here.
def index(request):
    if request.method=="GET":
        if not request.user.is_authenticated:
            return render(request, "orders/index.html", {"logged_in" : False})
        else:
            is_staff = request.user.is_staff
            return render(request, "orders/index.html", {"logged_in" : True,
                            "user" : request.user, "is_staff" : is_staff})
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not active_order(request):
                open_new_order(request)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message":
            "Invalid credentials"})

def login_page(request):
    return render(request, "orders/login.html")

def login_attempt(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if not active_order(request, username):
            open_new_order(request)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message":
        "Invalid credentials"})

def get_user(username):
    return User.objects.get(username=username)

def active_order(request):
    user = request.user
    f = Order.objects.filter(user=user)
    g = f.filter(active=True)
    return len(g) > 0

def get_active_order(request):
    #user = get_user(username)
    user_orders = Order.objects.filter(user=request.user)
    active_orders = user_orders.filter(active=True)
    return active_orders[0]

def open_new_order(request):
    new_order = Order(user=request.user)
    new_order.save()
    return None

def logout_view(request):
    logout(request)
    return render(request, "orders/index.html", {"logged_in": False})

def new_eater_page(request):
    return render(request, "orders/new_eater.html")

def new_eater_check(request):
    username = request.POST["username"]
    password = request.POST["password"]
    first = request.POST["first"]
    last = request.POST["last"]
    email = request.POST["email"]
    try:
        new_eater = User.objects.create_user(username, email, password)
        new_eater.save()
        new_eater.first_name = first
        new_eater.last_name = last
    except IntegrityError:
        return render(request, "orders/new_eater.html",
        {"message" : "That username already exists.  Please choose another."})

    user = authenticate(request, username=username, password=password)
    login(request, user)
    open_new_order(request)
    return HttpResponseRedirect(reverse("index"))

def display_current_order(request):
    user_orders = Order.objects.filter(user=request.user)
    current_order = user_orders.filter(active=True)
    if len(current_order)==0:
        current_order = Order(user=request.user)
    else:
        current_order = current_order.get()

    order_items = OrderItem.objects.filter(order=current_order)
    item_prices = [ item.price for item in order_items ]
    total_price = sum(item_prices)
    current_order.total = total_price
    current_order.save()
    context = {"item_list" : order_items, "total" : total_price }
    return render(request, "orders/current_order.html", context)

def display_salads(request):
    salads = MenuItem.objects.filter(type='Sa')
    context = {"item_list" : salads, "title" :  "Salads"}
    return render(request, "orders/salad_or_pasta.html", context)

def display_pasta(request):
    pasta = MenuItem.objects.filter(type='Pa')
    context = {"item_list" : pasta, "title" : "Pasta"}
    return render(request, "orders/salad_or_pasta.html", context)

def display_dinner_platters(request):
    return render(request, "orders/dinner_platters.html",
    {"choices" : DinnerPlatter.DINNER_PLATTER_CHOICES,
    "sizes" : DinnerPlatter.SIZES })

def find_dinner_platter(request):
    choice = request.POST["choice"]
    size = request.POST["size"]
    dp_choice = DinnerPlatter.objects.filter(platter_type=choice)
    dp_item = dp_choice.get(size=size)
    id = dp_item.menu_item_id
    menu_item = MenuItem.objects.get(pk=id)

    context = { "item" : menu_item }

    return render(request, "orders/add_item.html", context)

def display_subs(request):
    choices = Sub1.SUB1_CHOICES + Sub2.SUB2_CHOICES
    return render(request, "orders/subs.html", {"choices" : choices})

def sub_size_and_toppings(request):
    sub_type = request.POST["choice"]
    spo = sub_type == 'SPO'
    sub1_codes = [x[0] for x in Sub1.SUB1_CHOICES]
    if sub_type in sub1_codes:
        sub1 = True
        k = sub1_codes.index(sub_type)
        sub1_names = [x[1] for x in Sub1.SUB1_CHOICES]
        sub_name = sub1_names[k]
    else:
        sub1 = None
        sub2_codes = [x[0] for x in Sub2.SUB2_CHOICES]
        sub2_names = [x[1] for x in Sub2.SUB2_CHOICES]
        k = sub2_codes.index(sub_type)
        sub_name = sub2_names[k]
    context = { "sub1" : sub1, "spo" : spo, "sizes" : Sub1.SIZES ,
    "sub_name" : sub_name, "sub_type" : sub_type }
    return render(request, "orders/sub_size_and_toppings.html", context)

def get_sub(request):
    mushrooms = "mush" in request.POST
    green_peppers = "gp" in request.POST
    onions = "o" in request.POST
    extra_cheese = "ec" in request.POST
    size = request.POST["size"]
    sub1 = "sub1" in request.POST
    choice = request.POST["choice"]

    if sub1:
        sub_choice = Sub1.objects.filter(sub_type=choice)
        sub_choice = sub_choice.filter(mushrooms=mushrooms)
        sub_choice = sub_choice.filter(green_peppers=green_peppers)
        sub_choice = sub_choice.filter(onions=onions)
        sub_choice = sub_choice.filter(extra_cheese=extra_cheese)
        sub_item = sub_choice.get(size=size)
        id = sub_item.menu_item_id
        menu_item = MenuItem.objects.get(pk=id)
    else:
        sub_choice = Sub2.objects.filter(sub_type=choice)
        sub_choice = sub_choice.filter(extra_cheese=extra_cheese)
        sub_item = sub_choice.get(size=size)
        id = sub_item.menu_item_id
        menu_item = MenuItem.objects.get(pk=id)

    context = { "item" : menu_item }

    return render(request, "orders/add_item.html", context)

def display_pizza(request):
    pizza_types = Pizza.PIZZA_TYPES
    sizes = Pizza.SIZES
    toppings = Pizza.TOPPINGS

    return render(request, "orders/pizza.html", { "pizza_types" : pizza_types,
    "sizes" : sizes, "toppings" : toppings })

def get_pizza(request):
    type = request.POST["pizza_type"]
    size = request.POST["size"]

    if "special" in request.POST:
        top_code = "Spec"
    else:
        top1 = request.POST["top1"]
        top2 = request.POST["top2"]
        top3 = request.POST["top3"]

        # Now have to retrieve pizza topping code
        inds = []
        if len(top1) > 0:
            inds.append(Pizza.TOPPING_CODES.index(top1))
        if len(top2) > 0:
            inds.append(Pizza.TOPPING_CODES.index(top2))
        if len(top3) > 0:
            inds.append(Pizza.TOPPING_CODES.index(top3))
        inds = sorted(inds)

        top_code = ""
        for i in inds:
            top_code += Pizza.TOPPING_CODES[i]

    pizza_choices = Pizza.objects.filter(pizza_top=top_code)
    pizza_choices = pizza_choices.filter(pizza_type=type)
    pizza_item = pizza_choices.get(size=size)
    id = pizza_item.menu_item_id
    menu_item = MenuItem.objects.get(pk=id)

    context = { "item" : menu_item }

    return render(request, "orders/add_item.html", context)

def choose_item(request):
    menu_item_id = int(request.POST["menu_item"])
    item_name = MenuItem.objects.get(id=menu_item_id)
    context = { "item" : item_name }
    return render(request, "orders/add_item.html", context)

def add_item_to_order(request):
    quantity = int(request.POST["quantity"])
    item_id = int(request.POST["item_id"])
    user_orders = Order.objects.filter(user=request.user)
    current_order = user_orders.filter(active=True)
    if len(current_order)==0:
        current_order = Order(user=request.user)
    else:
        current_order = current_order.get()

    menu_item = MenuItem.objects.get(pk=item_id)

    c_order_items = OrderItem.objects.filter(order=current_order)
    already_here = c_order_items.filter(menu_item=menu_item)
    if len(already_here)>0:
        already_here[0].quantity += quantity
        already_here[0].price = menu_item.price * quantity
        already_here[0].save()
    else:
        order_item = OrderItem(order=current_order,menu_item=menu_item,\
        quantity=quantity,price=menu_item.price * quantity)
        order_item.save()

    order_items = OrderItem.objects.filter(order=current_order)
    item_prices = [ item.price for item in order_items ]
    total_price = sum(item_prices)
    current_order.total = total_price
    current_order.save()
    context = {"item_list" : order_items, "total" : total_price }

    return render(request, "orders/current_order.html", context)

def submit_order(request):
    user_orders = Order.objects.filter(user=request.user)
    current_order = user_orders.get(active=True)
    current_order.active = False
    current_order.submitted = True
    current_order.date_submitted = datetime.now()
    current_order.save()

    return render(request, "orders/submitted.html")

def view_orders(request):
    placed_orders = Order.objects.filter(submitted=True).order_by('-date_submitted')

    context = { "orders" : placed_orders }

    return render(request, "orders/view_orders.html", context)
