from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("new_eater/", views.new_eater_page, name="new_eater"),
    path("new_eater_check/", views.new_eater_check, name="new_eater_check"),
    path("current_order/", views.display_current_order, name="current_order"),
    path("salad/", views.display_salads, name="salads"),
    path("pasta/", views.display_pasta, name="pasta"),
    path("dinner_platters/", views.display_dinner_platters,
        name="dinner_platters"),
    path("add_item_view/", views.find_dinner_platter,
        name="find_dinner_platter"),
    path("add_this_item/", views.choose_item, name="choose_item"),
    path("item_added/", views.add_item_to_order, name="add_item_to_order"),
    path("subs/", views.display_subs, name="subs"),
    path("sub_size_and_toppings/", views.sub_size_and_toppings,
        name="sub_size_and_toppings"),
    path("view_sub/", views.get_sub, name="get_sub"),
    path("pizza/", views.display_pizza, name="pizza"),
    path("view_pizza/", views.get_pizza, name="get_pizza"),
    path("place_order/", views.submit_order, name="submit_order"),
    path("placed_orders/", views.view_orders, name="view_orders")
]
