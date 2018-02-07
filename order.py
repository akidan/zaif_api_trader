import sys, os
import json
from zaifapi import *

argvs = sys.argv
argc = len(argvs)

zaif = ZaifPublicApi()
print(zaif.last_price('mona_jpy'))

json_str = os.popen("cat ~/.secrets/key.json").read()
json_dict=json.loads(json_str)
key=json_dict['zaif']['key']
secret=json_dict['zaif']['secret']
zaif = ZaifLeverageTradeApi(key, secret)

if argc > 1 and argvs[1]=="-t" and argc==6:
    mona_price =float(argvs[2])
    mona_amount=int(argvs[3])
    mona_limit =float(argvs[4])
    mona_stop  =float(argvs[5])
    tranx = zaif.create_position(type='margin',currency_pair='mona_jpy',action='ask',amount=mona_amount,price=mona_price,limit=mona_limit,stop=mona_stop,leverage=1)
    print(tranx)
elif argc > 1 and argvs[1]=="-c" and argc==3:
    mona_leverage_id = int(argvs[2])
    print(zaif.cancel_position(type='margin',leverage_id=mona_leverage_id))
elif argc > 1 and argvs[1]=="-a":
    print(zaif.active_positions(type='margin',currency_pair='mona_jpy'))
else:
    print("Usage: \npython order.py -t [price] [amount] [limit] [stop]\npython order.py -c [leverage_id]\npython order.py -a")
