import sys, os
import json
from zaifapi import *

argvs = sys.argv
argc = len(argvs)

zaif_pub = ZaifPublicApi()
print(zaif_pub.last_price('mona_jpy'))

json_str = os.popen("cat ~/.secrets/key.json").read()
json_dict=json.loads(json_str)
key=json_dict['zaif']['key']
secret=json_dict['zaif']['secret']
zaif = ZaifLeverageTradeApi(key, secret)

if argc > 1 and argvs[1]=="-t":
    if argc < 3:
        print ("Input price:")
        mona_price = float(input())
    else:
        mona_price = float(argvs[2])
    if argc < 4:
        print ("Input amount:")
        mona_amount = int(input())
    else:
        mona_amount = int(argvs[3])
    if argc < 5:
        print ("Input limit:")
        mona_limit = float(input())
    else:
        mona_limit =float(argvs[4])
    if argc < 6:
        print ("Input stop:")
        mona_stop = float(input())
    else:
        mona_stop  =float(argvs[5])

    print ("\nPrice="+str(mona_price)+", Amount="+str(mona_amount)+", (Total="+str(mona_price*float(mona_amount))+"), Limit="+str(mona_limit)+", Stop="+str(mona_stop))
    confirm = ""
    while confirm == "":
        print(zaif_pub.last_price('mona_jpy'))
        print("Are you sure? [Yn]")
        confirm = input()
    if confirm == "Y":
        try:
            order = zaif.create_position(type='margin',currency_pair='mona_jpy',action='ask',amount=mona_amount,price=mona_price,limit=mona_limit,stop=mona_stop,leverage=1)
            print(order)
            print("Order success!")
        except:
            import traceback
            traceback.print_exc()
            print("Order error!!")
elif argc > 1 and argvs[1]=="-c" and argc==3:
    mona_leverage_id = int(argvs[2])
    print(zaif.cancel_position(type='margin',leverage_id=mona_leverage_id))
elif argc > 1 and argvs[1]=="-a":
    print(zaif.active_positions(type='margin',currency_pair='mona_jpy'))
else:
    print("Usage: \npython order.py -t [price] [amount] [limit] [stop]\npython order.py -c [leverage_id]\npython order.py -a")
