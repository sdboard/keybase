from stellar_sdk import Server, Asset, TransactionBuilder, Network, Account, Keypair
from time import sleep
from numpy import all

class Action:

    def get_holders(asset_arr,exceptions,public=False):
        if public:
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
                                if float(b['balance']) >= 1:
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

    def get_totals(asset_arr,data_arr,data_dict,members):
        holders_totals = [['account_id']]
        for a in asset_arr: holders_totals[0].append(a[0])
        holders_totals[0].append("STAKED")
        for member in members:
            staking_tracker = []
            for a in asset_arr: staking_tracker.append(0)
            for i in range(len(data_arr)):
                for account in data_arr[i]:
                    if member in account:
                        staking_tracker[i] = 1
            if all(staking_tracker):
                held_arr = [member]
                sum = 0
                for a in asset_arr:
                    amnt = data_dict[member][a[0]]
                    sum += float(amnt)
                    held_arr.append(amnt)
                held_arr.append(sum)
                holders_totals.append(held_arr)
        total_arr = ['Total:']
        sum = 0
        for i in range(len(data_arr)):
            temp_tot = 0
            for j in range(len(holders_totals)-1):
                amt = holders_totals[j+1][i+1]
                temp_tot += float(amt)
            sum += temp_tot
            total_arr.append(temp_tot)
        total_arr.append(sum)
        holders_totals.append(total_arr)
        percent_stakes = []
        for i in range(len(holders_totals)):
            new_row = []
            for j in range(len(holders_totals[i])):
                if i == 0 or j == 0:
                    new_row.append(holders_totals[i][j])
                else:
                    new_row.append(str(round(100*float(holders_totals[i][j])/total_arr[j],6))+"%")
            percent_stakes.append(new_row)
        return holders_totals, percent_stakes

    def get_sendpot(pot,percent_stakes):
        sendpot = []
        for i in range(len(percent_stakes)-2):
            amt = round(pot*float(percent_stakes[i+1][len(percent_stakes[i+1])-1][:-1])/100,6)
            if amt > 0.0000001:
                sendpot.append([percent_stakes[i+1][0],amt])
        return sendpot

    def send_payments(sendpot,filename,memo,public=False):
        receipt = ""
        if public:
            server = Server(horizon_url="https://horizon.stellar.org")
            passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        else:
            server = Server(horizon_url="https://horizon-testnet.stellar.org")
            passphrase = Network.TESTNET_NETWORK_PASSPHRASE

        with open(filename) as infile:
            for line in infile:
                line = line.split(" ")
                if len(line[0]) > 10:
                    sender = line[0]
                    source_keypair = Keypair.from_secret(line[1][:-1])
                    receipt += " from " +source_keypair.public_key
                else:
                    asset = [line[0],line[1][:-1]]
                sleep(2)

        for s in sendpot:
            try:
                destination_p = s[0]
                amount = str(s[1])
                source_acc = server.load_account(sender)
                base_fee = server.fetch_base_fee()

                transaction = TransactionBuilder(
                    source_account=source_acc,
                    network_passphrase=passphrase,
                    base_fee=base_fee).add_text_memo(
                    memo).append_payment_op(
                    destination_p,
                    amount,
                    asset[0],
                    asset[1]).set_timeout(30).build()

                transaction.sign(source_keypair)

                response = server.submit_transaction(transaction)
                if response['successful']:
                    receipt += "\nSuccessfully sent "+str(s[1])+" "+asset[0]+" to "+s[0]
                else:
                    print("\n something went wrong...")
            except:
                receipt += "\nfailed to send " + str(s[1]) + " to " +s[0]
        return receipt
