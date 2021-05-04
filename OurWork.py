from stellar_sdk import Asset
from stellar_sdk import Server
import numpy as np

class Action:

    def get_holders(asset_arr,pub=False,exceptions=[]):
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
        return(data_array,data_dict)

    def get_members(data_arr):
        member_arr = []
        for i in range(len(data_arr)):
            member_arr.append([])
            for j in range(len(data_arr[i])):
                if data_arr[i][j][0] in member_arr:
                    pass
                else:
                    member_arr.append(data_arr[i][j][0])
        return member_arr

    def get_holders_totals(asset_arr,data_arr,data_dict,members):
        holders_totals = [['account_id']]
        for a in asset_arr: holders_totals[0].append(a[0])
        for member in members:
            staking_tracker = []
            for a in asset_arr: staking_tracker.append(0)
            for i in range(len(data_arr)):
                for account in data_arr[i]:
                    if member in account:
                        staking_tracker[i] = 1
            if np.all(staking_tracker):
                held_arr = [member]
                for a in asset_arr:
                    held_arr.append(data_dict[member][a[0]])
                holders_totals.append(held_arr)
        return holders_totals

    def get_stakes(data_arr, holders_totals):
        percent_stakes = [holders_totals[0]]
        total_arr = ['Total:']
        for i in range(len(data_arr)):
            temp_tot = 0
            for j in range(len(holders_totals)-1):
                temp_tot += float(holders_totals[j+1][i+1])
            total_arr.append(temp_tot)
        for i in range(len(holders_totals)-1):
            new_row = []
            for j in range(len(holders_totals[i])):
                if j == 0:
                    new_row.append(holders_totals[i+1][j])
                else:
                    new_row.append(str(round(100*float(holders_totals[i+1][j])/total_arr[j],6))+"%")
            percent_stakes.append(new_row)
        percent_stakes.append(total_arr)
        return percent_stakes
