from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.
class Salad(models.Model):
    SALAD_CHOICES = [
        ('Ga', 'Garden'),
        ('Gr', 'Greek'),
        ('A', 'Antipasto'),
        ('T', 'Tuna')
    ]

    salad_type = models.CharField(
        max_length=2,
        choices=SALAD_CHOICES
    )

    def __str__(self):
        if self.salad_type == 'Ga':
            return f"Garden Salad"
        if self.salad_type == 'Gr':
            return f"Greek Salad"
        if self.salad_type == 'A':
            return f"Antipasto"
        if self.salad_type == 'T':
            return f"Salad w/ Tuna"

    def price(self):
        if self.salad_type == 'Ga':
            return 6.25
        else:
            return 8.25

class Pasta(models.Model):
    PASTA_CHOICES = [
        ('Mo', 'Mozzarella'),
        ('Me', 'Meatballs'),
        ('C', 'Chicken')
    ]

    pasta_type = models.CharField(
        max_length=2,
        choices=PASTA_CHOICES
    )

    def __str__(self):
        if self.pasta_type == 'Mo':
            return f"Baked Ziti w/ Mozzarella"
        if self.pasta_type == 'Me':
            return f"Baked Ziti w/ Meatballs"
        if self.pasta_type == 'C':
            return f"Baked Ziti w/ Chicken"

    def price(self):
        if self.pasta_type == 'Mo':
            return 6.50
        if self.pasta_type == 'Me':
            return 8.75
        if self.pasta_type == 'C':
            return 9.75

class DinnerPlatter(models.Model):
    DINNER_PLATTER_CHOICES = [
        ('Ga', 'Garden Salad'),
        ('Gr', 'Greek Salad'),
        ('A', 'Antipasto'),
        ('BZ', 'Baked Ziti'),
        ('MP', 'Meatball Parm'),
        ('CP', 'Chicken Parm')
    ]

    SIZES = [
        ('S', 'Small'),
        ('L', 'Large')
    ]

    platter_type = models.CharField(
        max_length=2,
        choices=DINNER_PLATTER_CHOICES
    )

    size = models.CharField(
        max_length=1,
        choices=SIZES,
        default='S'
    )

    menu_item_id = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.size} {self.platter_type} Dinner Platter"

    def price(self):
        if self.platter_type=='CP':
            if self.size=='S':
                return 55.0
            else:
                return 85.0
        elif self.platter_type=='Ga' or self.platter_type=='BZ':
            if self.size=='S':
                return 40.0
            else:
                return 65.0
        else:
            if self.size=='S':
                return 50.0
            else:
                return 75.0

class Sub1(models.Model):
    SUB1_CHOICES = [
        ('Ch', 'Cheese'),
        ('I', 'Italian'),
        ('HC', 'Ham & Cheese'),
        ('Me', 'Meatball'),
        ('Tn', 'Tuna'),
        ('Tk', 'Turkey'),
        ('CP', 'Chicken Parmigiana'),
        ('EP', 'Eggplant Parmigiana'),
        ('St', 'Steak'),
        ('SC', 'Steak & Cheese')
    ]

    SIZES = [('S', 'Small'), ('L', 'Large')]

    sub_type = models.CharField(
        max_length=2,
        choices=SUB1_CHOICES
    )

    size = models.CharField(
        max_length=1,
        choices=SIZES,
        default='S'
    )

    mushrooms = models.BooleanField(default=False)
    green_peppers = models.BooleanField(default=False)
    onions = models.BooleanField(default=False)
    extra_cheese = models.BooleanField(default=False)

    menu_item_id = models.IntegerField(null=True)

    def __str__(self):
        running_name = f"{self.size} {self.sub_type} Sub"
        toppings = []
        if self.mushrooms:
            toppings.append('Mushrooms')
        if self.green_peppers:
            toppings.append('Green Peppers')
        if self.onions:
            toppings.append('Onions')
        if self.extra_cheese:
            toppings.append('Extra Cheese')

        if len(toppings) == 0:
            return running_name
        else:
            running_name += ' w/ '
            if len(toppings) == 1:
                running_name += toppings[0]
            elif len(toppings) == 2:
                running_name += toppings[0] + ' and ' + toppings[1]
            elif len(toppings) == 3:
                running_name += toppings[0] + ', ' + toppings[1] + ' and ' \
                + toppings[2]
            else:
                running_name += 'the works'

        return running_name

    def base_price(self):
        if self.sub_type=='SC':
            if self.size == 'S':
                return 6.95
            else:
                return 8.50
        elif self.sub_type=='Tk' or self.sub_type=='CP':
            if self.size == 'S':
                return 7.50
            else:
                return 8.50
        else:
            if self.size=='S':
                return 6.50
            else:
                return 7.95

    def price(self):
        num_tops = self.mushrooms + self.green_peppers + self.onions \
            + self.extra_cheese
        return self.base_price() + num_tops * 0.50

class Sub2(models.Model):
    SUB2_CHOICES = [
        ('SPO', 'Sausage, Peppers & Onions'),
        ('H', 'Hamburger'),
        ('C', 'Cheeseburger'),
        ('FC', 'Fried Chicken'),
        ('V', 'Veggie')
    ]

    SIZES = [('S', 'Small'), ('L', 'Large')]

    sub_type = models.CharField(
        max_length=3,
        choices=SUB2_CHOICES
    )

    size = models.CharField(
        max_length=1,
        choices=SIZES,
        default='S'
    )

    menu_item_id = models.IntegerField(null=True)

    extra_cheese = models.BooleanField(default=False)

    def __str__(self):
        running_name = f"{self.size} {self.sub_type} Sub"
        if self.extra_cheese:
            running_name += ' w/ Extra Cheese'
        return running_name

    def price(self):
        if self.sub_type=='SPO':
            return 8.50 + self.extra_cheese * 0.50
        elif self.sub_type=='H':
            if self.size=='S':
                return 4.60 + self.extra_cheese * 0.50
            else:
                return 6.95 + self.extra_cheese * 0.50
        elif self.sub_type=='C':
            if self.size=='S':
                return 5.10 + self.extra_cheese * 0.50
            else:
                return 7.45 + self.extra_cheese * 0.50
        else:
            if self.size=='S':
                return 6.95 + self.extra_cheese * 0.50
            else:
                return 8.50 + self.extra_cheese * 0.50

class Pizza(models.Model):
    PIZZA_TYPES = [('R', 'Regular'), ('Si', 'Sicilian')]

    TOPPINGS = [
        ('Pe', 'Pepperoni'),
        ('Sg', 'Sausage'),
        ('Ms', 'Mushrooms'),
        ('On', 'Onions'),
        ('Ha', 'Ham'),
        ('CB', 'Canadian Bacon'),
        ('Pi', 'Pineapple'),
        ('Ep', 'Eggplant'),
        ('TB', 'Tomato & Basil'),
        ('GP', 'Green Peppers'),
        ('Hb', 'Hamburger'),
        ('Sp', 'Spinach'),
        ('Ar', 'Artichoke'),
        ('Bu', 'Buffalo Chicken'),
        ('Ba', 'Barbecue Chicken'),
        ('Ac', 'Anchovies'),
        ('BO', 'Black Olives'),
        ('Ga', 'Fresh Garlic'),
        ('Zu', 'Zucchini')
    ]

    TOPPING_CODES = [ x[0] for x in TOPPINGS]

    SIZES = [('S', 'Small'), ('L', 'Large')]

    pizza_type = models.CharField(
        max_length=2,
        choices=PIZZA_TYPES
    )

    pizza_top = models.CharField(
        max_length=6,
        default=''
    )

    size = models.CharField(
        max_length=1,
        choices=SIZES,
        default='S'
    )

    menu_item_id = models.IntegerField(null=True)

    def top_code_to_word(s):
        return Pizza.TOPPINGS[Pizza.TOPPING_CODES.index(s)][1]

    def top_word(self):
        if self.pizza_top=='':
            return 'Cheese'
        elif len(self.pizza_top)==2:
            return Pizza.top_code_to_word(self.pizza_top)
        elif len(self.pizza_top)==4:
            if self.pizza_top[:2] == self.pizza_top[2:]:
                return 'Double ' + Pizza.top_code_to_word(self.pizza_top[:2])
            else:
                return Pizza.top_code_to_word(self.pizza_top[:2]) + ' and ' \
                    + Pizza.top_code_to_word(self.pizza_top[2:])
        else:
            self.top1 = self.pizza_top[:2]
            self.top2 = self.pizza_top[2:4]
            self.top3 = self.pizza_top[4:]
            if self.top1 == self.top3:
                return 'Triple ' + Pizza.top_code_to_word(self.top1)
            elif self.top1 == self.top2:
                return 'Double ' + Pizza.top_code_to_word(self.top1) + ' and ' \
                    + Pizza.top_code_to_word(self.top3)
            elif self.top3 == self.top2:
                return 'Double ' + Pizza.top_code_to_word(self.top2) + ' and ' \
                    + Pizza.top_code_to_word(self.top1)
            else:
                return Pizza.top_code_to_word(self.top1) + ', ' \
                    + Pizza.top_code_to_word(self.top2) \
                    + ' and ' + Pizza.top_code_to_word(self.top3)

    def __str__(self):
        if self.pizza_top=='Spec':
            return f"{self.size} {self.pizza_type} Special Pizza"
        elif self.pizza_top=='':
            return f"{self.size} {self.pizza_type} Cheese Pizza"
        else:
            return f"{self.size} {self.pizza_type} Pizza with " \
                + self.top_word()

    def price(self):
        if self.pizza_type=='R':
            if self.pizza_top=='Spec':
                if self.size=='S':
                    return 17.75
                else:
                    return 25.95
            else:
                if len(self.pizza_top)==0:
                    if self.size=='S':
                        return 12.70
                    else:
                        return 17.95
                elif len(self.pizza_top)==2:
                    if self.size=='S':
                        return 13.70
                    else:
                        return 19.95
                elif len(self.pizza_top)==4:
                    if self.size=='S':
                        return 16.20
                    else:
                        return 23.95
                else:
                    if self.size=='S':
                        return 16.20
                    else:
                        return 23.95

        else:
            if self.pizza_top=='Spec':
                if self.size=='S':
                    return 30.45
                else:
                    return 45.70
            else:
                if len(self.pizza_top)==0:
                    if self.size=='S':
                        return 24.45
                    else:
                        return 38.70
                elif len(self.pizza_top)==2:
                    if self.size=='S':
                        return 26.45
                    else:
                        return 40.70
                elif len(self.pizza_top)==4:
                    if self.size=='S':
                        return 28.45
                    else:
                        return 42.70
                else:
                    if self.size=='S':
                        return 29.45
                    else:
                        return 44.70

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_opened = models.DateTimeField(default=datetime.now)
    date_submitted = models.DateTimeField(null=True,blank=True)
    date_closed = models.DateTimeField(null=True,blank=True)
    active = models.BooleanField(default=True)
    cancelled = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    total = models.FloatField(default=0.0)

    def __str__(self):
        return f"Order by {self.user}, initiated {self.date_opened}"

class MenuItem(models.Model):
    ITEM_TYPES = [('Sa', 'Salad'), ('S1', 'Sub1'), ('S2', 'Sub2'), \
    ('Pa', 'Pasta'), ('DP', 'DinnerPlatter'), ('Pi', 'Pizza')]

    name = models.CharField(
        max_length=72
    )
    type = models.CharField(
        max_length=2,
        choices=ITEM_TYPES,
        default='Pi'
    )
    price = models.FloatField()

    def __str__(self):
        return f"{self.name}"

class OrderItem(models.Model):
    QUANTITIES = [ (i, str(i)) for i in range(1,13)]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(
        default=1,
        choices=QUANTITIES
    )
    price = models.FloatField(null=True)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

#    def price(self):
#        return self.quantity * self.menu_item.price
