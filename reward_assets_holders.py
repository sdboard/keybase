from stellar_sdk import Asset
from stellar_sdk import Server
import numpy as np
import pandas as pd
import time
pd.set_option('display.max_colwidth', None)

URTHassets = [
['AIR','GBCZBQ7WLDZM4COTEWXGTJ3RCEQ7CEJVDY6E4P5LO2QTPHQI3CL2N7TW'],
['LAND','GBCZBQ7WLDZM4COTEWXGTJ3RCEQ7CEJVDY6E4P5LO2QTPHQI3CL2N7TW'],
['SEA','GBCZBQ7WLDZM4COTEWXGTJ3RCEQ7CEJVDY6E4P5LO2QTPHQI3CL2N7TW'],
['TREE','GBCZBQ7WLDZM4COTEWXGTJ3RCEQ7CEJVDY6E4P5LO2QTPHQI3CL2N7TW'],
]

testassets = [
['ARST','GB7TAYRUZGE6TVT7NHP5SMIZRNQA6PLM423EYISAOAP3MKYIQMVYP2JO'],
['BRLT','GB7TAYRUZGE6TVT7NHP5SMIZRNQA6PLM423EYISAOAP3MKYIQMVYP2JO']
]

def reward_assets_holders(asset_arr,pub=False,exceptions=[]):
    if pub:
        server = Server(horizon_url="https://horizon.stellar.org")
    else:
        server = Server(horizon_url="https://horizon-testnet.stellar.org")
    data_array = []
    data_dict = {"account_id":{'asset_code':'balance'}}
    for i in range(len(asset_arr)):
        data_array.append([])
        asset = Asset(code=asset_arr[i][0],issuer=asset_arr[i][1])
        accounts = server.accounts().for_asset(asset).limit(200).call()
        while len(accounts['_embedded']['records']) > 0:
            for r in accounts['_embedded']['records']:
                if r['account_id'] in exceptions:
                    pass
                else:
                    for b in r['balances']:
                        if b['asset_code'] == asset_arr[i][0]:
                            if float(b['balance']) > 0:
                                try:
                                    data_dict[r['account_id']][asset_arr[i][0]] = b['balance']
                                except:
                                    data_dict[r['account_id']] = {}
                                    data_dict[r['account_id']][asset_arr[i][0]] = b['balance']
                                data_array[i].append([r['account_id'],b['balance']])
                            break;
            find_cursor_arr = accounts['_links']['next']['href'].split("&")
            for n in find_cursor_arr:
                if ("cursor" in n) and len(n) > 7: cursor = n[7:]
            accounts = server.accounts().for_asset(asset).cursor(cursor).limit(200).call()
    member_arr = []
    for i in range(len(data_array)):
        member_arr.append([])
        for j in range(len(data_array[i])):
            if data_array[i][j][0] in member_arr:
                pass
            else:
                member_arr.append(data_array[i][j][0])
    reward_arr_sub_total = [['account_id']] #URTH Erners
    for a in asset_arr: reward_arr_sub_total[0].append(a[0])
    for member in member_arr:
        staking_tracker = []
        for a in asset_arr: staking_tracker.append(0)
        for i in range(len(data_array)):
            for account in data_array[i]:
                if member in account:
                    staking_tracker[i] = 1
        if np.all(staking_tracker):
            held_arr = [member]
            for a in asset_arr:
                held_arr.append(data_dict[member][a[0]])
            reward_arr_sub_total.append(held_arr)
    total_reward = [['account_id']]
    for a in asset_arr: total_reward[0].append(a[0])
    total_arr = ['Total:']
    for i in range(len(data_array)):
        temp_tot = 0
        for j in range(len(reward_arr_sub_total)-1):
            temp_tot += float(reward_arr_sub_total[j+1][i+1])
        total_arr.append(temp_tot)
    for i in range(len(reward_arr_sub_total)-1):
        new_row = []
        for j in range(len(reward_arr_sub_total[i])):
            if j == 0:
                new_row.append(reward_arr_sub_total[i+1][j])
            else:
                new_row.append(str(round(100*float(reward_arr_sub_total[i+1][j])/total_arr[j],6))+"%")
        total_reward.append(new_row)
    total_reward.append(total_arr)

    print(" ")
    df = pd.DataFrame(reward_arr_sub_total)
    print(df)
    print(" ")
    df2 = pd.DataFrame(total_reward)
    print(df2)
    print(" ")
   
    
    for i in range(1):
    reward_assets_holders(URTHassets,pub=True,exceptions=['GDLA2EKBBPIAYJ3BSOQCMWVZ2T3GM4NFVECRSFCMZW676CSMTVL5NXLP'])
    reward_assets_holders(testassets, exceptions=['GDMSN2PQ3EB32LZY5JVACI4H7GUVQ3YUWOM4437IDTVQHHWHYG7CGA5Z'])
    time.sleep(0.1)
