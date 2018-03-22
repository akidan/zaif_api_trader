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

    def trade(self, c_type, c_amount, c_price, c_action):
        try:
            if c_type == 'btc' or c_type == 'eth':
                c_price = int(c_price)
            order = zaif.trade(currency_pair=c_type+'_jpy',action=c_action,amount=c_amount,price=c_price)
            print(order)
            print("Order success!")
            return False
        except:
            import traceback
            traceback.print_exc()
            print("Order error!!")
            return True

if argc > 1 and (argvs[1] == "-b" or argvs[1] == "-a"):
    if argvs[1] == "-b":
        coin_action = 'bid'
    elif argvs[1] == "-a":
        coin_action = 'ask'
    if argc < 3:
        print ("Input coin:")
        coin_type = str(input())
        print(zaif_pub.last_price(coin_type+'_jpy'))
    else:
        coin_type = str(argvs[2])
        print(zaif_pub.last_price(coin_type+'_jpy'))
    if argc < 4:
        print ("Input price:")
        coin_price = float(input())
    else:
        coin_price = float(argvs[3])
    if argc < 5:
        print ("Input amount:")
        coin_amount = float(input())
    else:
        coin_amount = float(argvs[4])
    if argc > 5 and argvs[5] == "F":
        confirm = "Y"
    elif argc > 5 and argvs[5] == "FF":
        confirm = "FF"
    else:
    	confirm = ""
    print ("\nCoin="+coin_type+", Action="+coin_action+", Price="+str(coin_price)+", Amount="+str(coin_amount)+", (Total="+str(coin_price*float(coin_amount))+")")
    while confirm == "":
        print(zaif_pub.last_price(coin_type+'_jpy'))
        print("Are you sure? [YnFF]")
        confirm = input()
    trader = Trader()
    try_num = 1
    if confirm == "FF":
        try_num = 10
    fail = True
    while (fail and try_num > 0 and (confirm == "Y" or confirm == "FF")):
        fail = trader.trade(coin_type, coin_amount, coin_price, coin_action)
        try_num = try_num - 1
        sleep(1)

elif argc > 1 and argvs[1]=="-c" and argc==3:
    coin_order_id = int(argvs[2])
    print(zaif.cancel_order(order_id=coin_order_id))
elif argc > 1 and argvs[1]=="-l":
    print(zaif.active_orders())
elif argc > 1 and argvs[1] in ["btc", "eth", "xem", "mona", "zaif", "mosaic.cms"]:
    coin_type = str(argvs[1])
    print(coin_type+" "+str(zaif_pub.last_price(coin_type+'_jpy')))
else:
    print(coin_type+" "+str(zaif_pub.last_price(coin_type+'_jpy')))
    print("Usage: \npython order.py -b -a [coin] [price] [amount] [F|FF]\n                -c    [trade_id]\n                -l")
