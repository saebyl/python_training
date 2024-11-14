from platform import machine

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300, #300
    "milk": 200, #200
    "coffee": 100,
}
import sys


def format_number(num_type, value):
    """Adds measurement formatting based on the type of number being displayed"""
    if num_type == "water" or num_type == "milk":
        return f"{value}ml"
    elif num_type == "coffee":
        return f"{value}g"
    elif num_type == "money":
        return f"${value}"

def get_drink_description(choice):
    """Returns just the one dictionary item from the menu that we want to evaluate."""
    return MENU[choice]

def get_drink_resources(menu_item):
    """Returns the ingredients needed for the given menu item"""
    return menu_item["ingredients"]

def get_drink_price(menu_item):
    """Returns the drink price for the given menu item."""
    return menu_item["cost"]

def get_drink_ingredient_resources(menu_item, ingredient):
    """Returns just the value of resources needed for an individual ingredient"""
    for item in resources:
        if item not in menu_item:
            menu_item[item] = 0
    return menu_item[ingredient]

def get_machine_resources(ingredient):
    """Returns the available machine resources for the given ingredient."""
    return resources[ingredient]

def calculate_coin_total(q, d, n, p):
    """Calculates total payment provided by user."""
    return (q * .25) + (d * .1) + (n * .05) + (p * .01)

def reduce_machine_resources(d_resources):
    for ingredient in resources:
        resources[ingredient] = resources[ingredient] - d_resources[ingredient]
    return resources
#
# def is_resource_sufficient():


machine_commands = ["espresso","latte","cappuccino","off","report"]
is_machine_off = False
is_transaction_successful = True
money = 0

# TODO 1 Ask user what they want? (espresso/latte/cappuccino)
while not is_machine_off: # This is always true. Off only gets triggered on the sys.exit()
    # should show after last drink has dispensed. Put inside a while loop
    user_choice = input("What would you like? (espresso/latte/cappuccino) ").lower()
    while user_choice not in machine_commands:
        user_choice = input("Incorrect input. Please type in one of the following: espresso/latte/cappuccino. ").lower()

    # TODO 2 Turn off the coffee machine by entering off to the prompt. This exits code immediately
    if user_choice == "off":
        sys.exit()

    # TODO 3 print report
    if user_choice == "report":
        for key in resources:
            print(f"{key.title()}: {format_number(key,resources[key])}")
        print(f"Money: {format_number("money",money)}")
    else:
        # TODO Check resources are sufficient for the chosen drink
        drink_description = get_drink_description(user_choice)
        drink_resources = get_drink_resources(drink_description)
        drink_price = get_drink_price(drink_description)

        unavailable_resources = []
        for key in resources:
            if get_machine_resources(key) < get_drink_ingredient_resources(drink_resources, key):
                unavailable_resources.append(key)
        if len(unavailable_resources) > 0:
            is_transaction_successful = False
            print("Sorry there is not enough of the following ingredients:")
            for key in unavailable_resources:
                print(f"    {key.title()}")
        else:
            print(f"The price is ${round(drink_price,2)}. Please insert coins.")
            quarters = int(input("How many quarters ($0.25)? "))
            dimes = int(input("How many dimes ($0.10)? "))
            nickles = int(input("How many nickles ($0.05)? "))
            pennies = int(input("How many pennies ($0.01)? "))
            coin_total = round(calculate_coin_total(quarters,dimes,nickles,pennies),2)
            print(f"You paid: ${coin_total}.")
            if coin_total < drink_price:
                is_transaction_successful = False
                print("Sorry, that is not enough. Money refunded.")
            elif coin_total >= drink_price:
                is_transaction_successful = True
                if coin_total > drink_price:
                    print(f"Thank you for your payment! Your change is: ${round(coin_total - drink_price,2)}")
                else:
                    is_transaction_successful = True
                    print("Thank you for your payment!")
            # TODO reduce machine resources by drink resources & add money to machine
            if is_transaction_successful:
                print(f"Here is your {user_choice}. Enjoy!")
                money += drink_price
                resources = reduce_machine_resources(drink_resources)