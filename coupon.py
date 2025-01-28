# Example Cart
#  [ {'price': 2.00, 'category': 'fruit'},
#    {'price': 20.00, 'category': 'toy'},
#    {'price': 5.00, 'category': 'clothing'},
#    {'price': 8.00, 'category': 'fruit'}
#  ]
# list of items, price and category cannot be null
# # Example Coupon
#  #
#  # Exactly one of percent_discount and amount_discount will be non-null (error if not).
#  # The two 'minimum_...' values can each be null or non-null.
#  { 'category': 'fruit',
#    'percent_discount': 15, 15 percent off
#    'amount_discount': None, looks like a float, if 5.0 it means 5 dollars off
#    'minimum_num_items_required': 2,
#    'minimum_amount_required': 10.00
#   }
# write a function that takes a coupon and a list of products, returns the price after applying the coupon
# throw an error if coupon is invalid; if both pdicount and adiscount are non-null, throw an error. if both are null throw an error.
# if coupon doesnt apply (if its random, if conditions arent met) just calculate the cart price
# calculate the cost of the cart done
# check validity of coupon pre processing done
# check validity of coupon post-purchasing
# apply coupon to cart

# # Coupons
# [
#   { 'categories': ['clothing', 'toy'],
#     'percent_discount': None,
#     'amount_discount': 6,
#     'minimum_num_items_required': None,
#     'minimum_amount_required': None
#   },
#   { 'categories': ['fruit'],
#     'percent_discount': 15,
#     'amount_discount': None,
#     'minimum_num_items_required': 2,
#     'minimum_amount_required': 10.00
#    }
# ]

class Item:
    def __init__(self, price, category):
        self.price = price
        self.category = category
    
    def __str__(self):
        return "self.price: " + str(self.price) + " self.category: " + self.category


class Coupon:
    def __init__(self, category, percent_discount, amount_discount, minimum_num_items_required, minimum_amount_required):
        self.category = category
        self.percent_discount = percent_discount
        self.amount_discount = amount_discount
        self.minimum_num_items_required = minimum_num_items_required
        self.minimum_amount_required = minimum_amount_required
    
    def is_valid(self):
        if self.percent_discount and self.amount_discount:
            return False
        if not self.percent_discount and not self.amount_discount:
            return False
        return True
    
    def is_valid_for_cart(self, cart):
        filtered_cart_price = 0
        for item in cart:
            filtered_cart_price += item.price
        if self.minimum_num_items_required:
            if len(cart) < self.minimum_num_items_required:
                return False
        if self.minimum_amount_required:
            if filtered_cart_price < self.minimum_amount_required:
                return False
        return True
    
    def apply_discount_to_cart(self, cart):
        cartCost = 0
        for item in cart:
            cartCost += item.price
        if self.percent_discount:
            return cartCost * (1 - (self.percent_discount * .01))
        if cartCost - self.amount_discount < 0:
            return 0
        return cartCost - self.amount_discount


def getTotalCost(coupon: Coupon, cart: list[Item]) -> float:
    totalCost = 0.0
    if not coupon.is_valid():
        raise Exception("coupon is not valid")
    cart_without_coupon_items = list(filter(lambda x: x.category != coupon.category, cart))
    cart_with_coupon_items = list(filter(lambda x: x.category == coupon.category, cart))
    for item in cart_without_coupon_items:
        totalCost += item.price
    if coupon.is_valid_for_cart(cart_with_coupon_items):
        totalCost += coupon.apply_discount_to_cart(cart_with_coupon_items)
    else:
        for item in cart_with_coupon_items:
            totalCost += item.price
    return totalCost

test_coupon_1 = Coupon(category='fruit', percent_discount=15, amount_discount=None, minimum_num_items_required=2, minimum_amount_required=11.00)
test_cart_1 = [
    Item(price=2.00, category='fruit'),
    Item(price=20.00, category='toy'),
    Item(price=5.00, category='clothing'),
    Item(price=8.00, category='fruit'),
]
print(getTotalCost(test_coupon_1, test_cart_1)) # expected 33.5

test_invalid_coupon_both_null = Coupon(category='fruit', percent_discount=None, amount_discount=None, minimum_num_items_required=2, minimum_amount_required=10.00)
test_invalid_coupon_both_non_null = Coupon(category='fruit', percent_discount=15, amount_discount=5.0, minimum_num_items_required=2, minimum_amount_required=10.00)

try:
    getTotalCost(test_invalid_coupon_both_null, test_cart_1)
except:
    print("both null correctly throws exception")

try:
    getTotalCost(test_invalid_coupon_both_non_null, test_cart_1)
except:
    print("both non null correctly throws exception")
