from flask import Flask,request
import requests
import os 
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *
import math 
from decimal import Decimal

app = Flask(__name__)
load_dotenv() 
capital = Decimal(os.getenv("CAPITAL"))
amount_bought = 0 
fraction = Decimal("0.20")
prev_position_size = 0 
client = Client(os.getenv("API_KEY"), os.getenv("API_SECRET"), tld='us')

def update_env_variable(key, value, env_path=".env"):
    lines = []
    found = False

    try:
        with open(env_path, "r") as file:
            for line in file:
                if line.strip().startswith(f"{key}="):
                    lines.append(f"{key}={value}\n")
                    found = True
                else:
                    lines.append(line)
    except FileNotFoundError:
        pass  # If .env doesn't exist yet, we'll just create it

    if not found:
        lines.append(f"{key}={value}\n")

    with open(env_path, "w") as file:
        file.writelines(lines)
def order(side, quantity, symbol,order_type= ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity) # side is BUY or SELL , type is LIMIT or MARKET 
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

@app.route('/')
def whats():
    return "hello world"


@app.route('/initialCapital' , methods=["POST"]) # only account managers can initiate the initial capital balance
def get_initialCapital():
    data = request.json # SECURITY MEASURES OUGHT TO BE TAKEN CARE OF , CAUSE USERS CAN SEND ANYTHING IN THIS JSON ! 
    if data['passphrase'] ==  os.getenv("PASSPHRASE") and data['capital'] : # authenticate the SENDER , is he the owner ?! cause anyone can send to this program 
        global capital 
        capital = Decimal(data['capital'])
        update_env_variable("CAPITAL", str(capital))

        return f"<b>Got capital {capital}</b>"
    
    return "capital not changed"


@app.route('/webhook' , methods=["POST"])
def webhook():
    
    data = request.json # this returns a dictionary
    requirements = client.get_symbol_info('BTCUSDT')["filters"]
    
    minPrice =  Decimal(str(requirements[0]["minPrice"]))
    minQty =  Decimal(str(requirements[2]["minQty"]))
    if data['passphrase'] !=  os.getenv("PASSPHRASE") : # really important not to make this public , as it will invoke undesirable trades 
        return "<h1><b>UnAuthenticated</b></h1>"
    
    side = data['strategy']['order_action'].upper() # return BUY not buy . cause this is what binance wants  
    global capital
    price = Decimal(data['strategy']['order_price']) 
    order_response = None
    global amount_bought 
    global prev_position_size 
    
    
    if side == "BUY" :
        # calculate the amount invested 
        # since we are trading cryto , we can enter in any capital amount 
        money_to_enter = capital * fraction if capital * fraction > minPrice else minPrice 
        quanity_to_buy = Decimal(str(money_to_enter / price)) if Decimal(str(money_to_enter / price )) > minQty else 0 # skip buying if you doing have enough funds !
        # binance allow minQuantity to be trading , we need to make sure we don't go bellow it
        # also our quantity needs to be a multiple of the minQuantity 
        # additionally , binance also has a minPrice entry 
        
        if Decimal(str(quanity_to_buy % minQty)).normalize() != Decimal("0"):   # if it outputs an answer like 9e-3 , it is wrong , anothe way ? 
            quanity_to_buy = Decimal(str(math.floor(quanity_to_buy / minQty) * minQty))
        prev_position_size = quanity_to_buy 
        amount_bought =  Decimal(str(quanity_to_buy * price))
        capital = capital - amount_bought
        update_env_variable("CAPITAL", str(capital))

        print(f'amount in ${amount_bought} quantity {quanity_to_buy} Capital :${capital}\n')
        #|uncomment if u want to really buy |order_response = order(side , quanity_to_buy , 'BTCUSDT') # amount_of_share would be later determined as we need to manage risk and balance
    
    if side == "SELL" : 
        # we should sell in all cases , as it might be a stop loss to reduce our LOSSES 

        # we sell the position we bought ( sell all stocks  you prev bought)
        price_to_sell_at = Decimal(str(data['strategy']['order_price']))
        quantity_to_sell = prev_position_size  
        order_size=Decimal(str(price_to_sell_at * quantity_to_sell )) 
        #|uncomment if u want to really buy |order_response = order(side , quantity_to_sell, 'BTCUSDT')
        profit = order_size - amount_bought if order_size > 0 else 0 
        capital = capital + order_size # profit may be negitive 
        prev_position_size -= quantity_to_sell
        print(f'sold and profit is ${profit} Capital :${capital} \n')    
        
    if order_response :
            return f"order executed current capital {capital}"   
    return f"<b>order executed current capital {capital}</b>"   
    

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 