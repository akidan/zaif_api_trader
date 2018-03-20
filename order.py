import sys, os
import json
from zaifapi import *
from time import sleep

argvs = sys.argv
argc = len(argvs)

zaif_pub = ZaifPublicApi()
coin_type = 'btc'

json_str = os.popen("cat ~/.secrets/key.json").read()
json_dict=json.loads(json_str)
key=json_dict['zaif']['key']
secret=json_dict['zaif']['secret']
zaif = ZaifTradeApi(key, secret)

class Trader(object):
    def __init__(self):
        return None

    def trade(self, c_type, c_amount, c_price):
        try:
            order = zaif.trade(currency_pair=c_type+'_jpy',action='ask',amount=c_amount,price=c_price)
            print(order)
            print("Order success!")
            return False
        except:
            import traceback
            traceback.print_exc()
            print("Order error!!")
            return True

if argc > 2:
    coin_type = str(argvs[2])

print(coin_type)
print(zaif_pub.last_price(coin_type+'_jpy'))

if argc > 1 and argvs[1] == "-t":
    if argc == 2:
        print ("Input coin:")
        coin_type = str(input())
        print(zaif_pub.last_price(coin_type+'_jpy'))
    if argc < 3:
        print ("Input price:")
        coin_price = float(input())
    else:
        coin_price = float(argvs[2])
    if argc < 4:
        print ("Input amount:")
        coin_amount = int(input())
    else:
        coin_amount = int(argvs[3])
    if argc > 4 and argvs[4] == "F":
        confirm = "Y"
    elif argc > 4 and argvs[4] == "FF":
        confirm = "FF"
    else:
    	confirm = ""
    print ("\nCoin="+coin_type+", Price="+str(coin_price)+", Amount="+str(coin_amount)+", (Total="+str(coin_price*float(coin_amount))+")")
    while confirm == "":
        print(zaif_pub.last_price(coin_type+'_jpy'))
        print("Are you sure? [YnFF]")
        confirm = input()
    trader = Trader()

    try_num = 1
    if confirm == "FF":
        try_num = 10
    fail = True
    while (fail and try_num > 0 and confirm == "Y" or confirm == "FF"):
        fail = trader.trade(coin_type, coin_amount, coin_price)
        try_num = try_num - 1
        sleep(1)

elif argc > 1 and argvs[1]=="-c" and argc==3:
    coin_leverage_id = int(argvs[2])
    print(zaif.cancel_position(type='margin',leverage_id=coin_leverage_id))
elif argc > 1 and argvs[1]=="-a":
    print(zaif.active_positions(type='margin',currency_pair='xem_jpy'))
else:
    print("Usage: \npython order.py -t [coin] [price] [amount] [F|FF]\npython order.py -c [trade_id]\npython order.py -a")
