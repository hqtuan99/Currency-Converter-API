# https://free.currencyconverterapi.com/
from requests import get
from pprint import PrettyPrinter

BASE_URL = "https://free.currconv.com"
API_KEY = "your-api-key"

printer = PrettyPrinter()

def get_currencies():
    endpoint = f"/api/v7/currencies?apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()['results']
    
    data = list(data.items())
    data.sort()
    
    return data

def print_currencies(currencies):
    for name, currency in currencies:
        name = currency['currencyName']
        curr_id = currency['id']
        # Try to get the value in the dictionary, otherwise give default value
        symbol = currency.get("currencySymbol", "")
        print(f"{curr_id} - {name} - {symbol}")

def exchange_rate(currency1, currency2):
    endpoint = f"/api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()
    
    if len(data) == 0:
        print("Invalid currencies.\n")
        return
    
    rate = list(data.values())[0]
    print(f"{currency1} -> {currency2} = {rate}\n")
    return rate

def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        return
    
    try:
        amount = float(amount)
    except:
        print("Invalid amount.\n")
        return
    
    converted_amount = rate * amount
    print(f"{amount} {currency1} is equal to {converted_amount} {currency2}\n")
    return converted_amount

def main():
    currencies = get_currencies()
    print("Welcome to the currency converter!")
    
    while True:
        print("*** Command list ***")
        print("List - lists all the currencies.")
        print("Convert - convert from one currency to another.")
        print("Rate - get the exchange rate of two currencies.")
        print("-----------------------------------------------")
        command = input("Enter a command (q to quit): ").lower()
        
        if command == "q":
            break
        elif command == "list":
            print_currencies(currencies)
        elif command == "convert":
            currency1 = input("Enter first currency id: ").upper()
            amount = input(f"Enter an amount in {currency1} to convert: ")
            currency2 = input("Enter second currency id: ").upper()
            convert(currency1, currency2, amount)
        elif command == "rate":
            currency1 = input("Enter first currency id: ").upper()
            currency2 = input("Enter second currency id: ").upper()
            exchange_rate(currency1, currency2)
        else:
            print("Invalid command.\n")
            
main()