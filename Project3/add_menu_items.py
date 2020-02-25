from orders.models import Salad, Pasta, DinnerPlatter, Sub1, Sub2, Pizza
from orders.models import MenuItem

for x in Salad.SALAD_CHOICES:
    f = Salad(salad_type=x[0])
    f.save()

for x in Pasta.PASTA_CHOICES:
    f = Pasta(pasta_type=x[0])
    f.save()

for platter in DinnerPlatter.DINNER_PLATTER_CHOICES:
   for s in DinnerPlatter.SIZES:
       f = DinnerPlatter(size=s[0],platter_type=platter[0])
       f.save()

# Sub1
def bin_str(n):
     if n > 31:
         return 'Input is too big'
     else:
         s = str(bin(n))[2:]
         if len(s) < 5:
             k = 5 - len(s)
             for i in range(k):
                 s = '0'+s
         return s

def bin_size(s):
     if s[0]=='0':
         return 'S'
     else:
         return 'L'

def bin_mushrooms(s):
    return bool(int(s[1]))

 def bin_green_peppers(s):
    return bool(int(s[2]))

def bin_onions(s):
    return bool(int(s[3]))

def bin_extra_cheese(s):
    return bool(int(s[4]))

for n in range(32):
     s = bin_str(n)
     for st in Sub1.SUB1_CHOICES:
         f = Sub1(sub_type=st[0])
         f.size = bin_size(s)
         f.mushrooms = bin_mushrooms(s)
         f.green_peppers = bin_green_peppers(s)
         f.onions = bin_onions(s)
         f.extra_cheese = bin_extra_cheese(s)
         f.save()

# Sub2
for st in ['H', 'C', 'FC', 'V']:
     for size in ['S', 'L']:
         for extra_cheese in [False, True]:
             f = Sub2(sub_type=st)
             f.size = size
             f.extra_cheese = extra_cheese
             f.save()

for extra_cheese in [False, True]:
     f = Sub2(sub_type='SPO')
     f.size = 'L'
     f.extra_cheese = extra_cheese
     f.save()

# Pizza
TWO_TOPPINGS = []

for i, top1 in enumerate(Pizza.TOPPING_CODES):
     for j, top2 in enumerate(Pizza.TOPPING_CODES):
         if j >= i:
             TWO_TOPPINGS.append(top1 + top2)

THREE_TOPPINGS = []

for i, top1 in enumerate(Pizza.TOPPING_CODES):
     for j, top2 in enumerate(Pizza.TOPPING_CODES):
         if j >= i:
             for k, top3 in enumerate(Pizza.TOPPING_CODES):
                 if k >= j:
                     THREE_TOPPINGS.append(top1 + top2 + top3)

ALL_TOPS = [''] + Pizza.TOPPING_CODES + TWO_TOPPINGS + THREE_TOPPINGS

for top in ALL_TOPS:
     for size in ['S', 'L']:
         for p_type in ['R', 'Si']:
             f = Pizza(pizza_type=p_type,pizza_top=top)
             f.size = size
             f.save()

for size in ['S', 'L']:
      for p_type in ['R', 'Si']:
          f = Pizza(pizza_type=p_type,pizza_top='Spec')
          f.size = size
          f.save()

### Add everything to MenuItem

for class0 in [Salad, Pasta, DinnerPlatter, Sub1, Sub2, Pizza]:
    for item in class0.objects.all():
        f = MenuItem(name=item, price=item.price())
        f.save()

### Forgot to put in type before (use Pizza as default)
for symb, class0 in [('Sa', Salad), ('S1', Sub1), ('S2', Sub2), \
     ('Pa', Pasta), ('DP', DinnerPlatter)]:
    for item in class0.objects.all():
        f = MenuItem(name=item, price=item.price(), type=symb)
        f.save()

### Add MenuItem ids to other class instances
for class0 in [Pizza, DinnerPlatter, Sub1, Sub2]:
    for item in class0.objects.all():
        item.menu_item_id = MenuItem.objects.get(name=str(item))
