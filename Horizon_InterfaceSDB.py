from stellar_sdk import Server, Asset, TransactionBuilder, Network, Account, Keypair
from time import sleep
from numpy import all

from pandas import DataFrame as DF
class Functions:

    def get_percent_holders(asset_arr,exceptions,public=False):
        if public:
            server = Server(horizon_url="https://horizon.stellar.org")
        else:
            server = Server(horizon_url="https://horizon-testnet.stellar.org")
        data_arr = []
        data_dict = {"account_id":{'asset_code':'balance'}}
        for i in range(len(asset_arr)):
            data_arr.append([])
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
                                    data_arr[i].append([r['account_id'],b['balance']])
                                break;
                find_cursor_arr = accounts['_links']['next']['href'].split("&")
                for n in find_cursor_arr:
                    if ("cursor" in n) and len(n) > 7: cursor = n[7:]
                accounts = server.accounts().for_asset(asset).cursor(cursor).limit(200).call()
        member_arr = []
        for i in range(len(data_arr)):
            # member_arr.append([])
            for j in range(len(data_arr[i])):
                if data_arr[i][j][0] in member_arr:
                    pass
                else:
                    member_arr.append(data_arr[i][j][0])
        holders_totals = [['account_id']]
        for a in asset_arr: holders_totals[0].append(a[0])
        holders_totals[0].append("STAKED")
        holders_totals[0].append("MULTIPLIER")
        for member in member_arr:
            staking_tracker = []
            for a in asset_arr: staking_tracker.append(0)
            for i in range(len(data_arr)):
                for account in data_arr[i]:
                    if member in account:
                        staking_tracker[i] = 1
            Multiplier = 1 + 0.05*(sum(staking_tracker)-1)
            held_arr = [member]
            summation = 0
            for a in asset_arr:
                try:
                    amnt = data_dict[member][a[0]]
                    summation += float(amnt)
                    held_arr.append(amnt)
                except:
                    held_arr.append(0)
            held_arr.append(summation)
            held_arr.append(summation * Multiplier)
            holders_totals.append(held_arr)
        total_arr = ['Total:']
        summation = 0
        for i in range(len(data_arr)):
            temp_tot = 0
            for j in range(len(holders_totals)-1):
                amt = holders_totals[j+1][i+1]
                temp_tot += float(amt)
            summation += temp_tot
            total_arr.append(temp_tot)
        total_arr.append(summation)
        summation = 0
        for i in range(len(member_arr)):
            summation += holders_totals[i+1][len(holders_totals[i])-1]
        total_arr.append(summation)
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

    def send_payments(percent_stakes,POT,MEMO,public=False,multiplier=0,fixed_amount=0):
        receipt = " \nMemo: " + MEMO + "\n\n"
        POT = POT[0].split(":")
        pot = float(POT[0])
        asset = POT[1]
        issuer = POT[2]
        sender = POT[3]
        source_keypair = Keypair.from_secret(POT[4])
        receipt += "\n from " +source_keypair.public_key

        if public:
            server = Server(horizon_url="https://horizon.stellar.org")
            passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        else:
            server = Server(horizon_url="https://horizon-testnet.stellar.org")
            passphrase = Network.TESTNET_NETWORK_PASSPHRASE

        sendpot = []
        for i in range(len(percent_stakes)-2):
            if not (multiplier or fixed_amount):
                amt = round(pot*float(percent_stakes[i+1][len(percent_stakes[i+1])-1][:-1])/100,6)
            elif multiplier > 0:
                amt = round(multiplier*float(percent_stakes[i+1][len(percent_stakes[i+1])-1]),6)
            else:
                amt = fixed_amount
            if amt > 0.0000001:
                sendpot.append([percent_stakes[i+1][0],amt])


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
                    MEMO).append_payment_op(
                    destination_p,
                    amount,
                    asset,
                    issuer).set_timeout(30).build()

                transaction.sign(source_keypair)

                response = server.submit_transaction(transaction)
                if response['successful']:
                    receipt += "\nSuccessfully sent "+str(s[1])+" "+asset+" to "+s[0]
                else:
                    print("\n something went wrong...")
            except:
                receipt += "\nfailed to send " + str(s[1]) + " "+asset+" to " +s[0]
        return sendpot, receipt

    def get_balance(public_key,public=False):
        if public:
            server = Server(horizon_url="https://horizon.stellar.org")
        else:
            server = Server(horizon_url="https://horizon-testnet.stellar.org")
        account = server.accounts().account_id(public_key).call()
        # print("Ballance for account "+str(pair.public_key()))
        for b in account['balances']:
            if b['asset_type'] == 'native':
                return float(b['balance'])

    def convert_to_USDC(public_key,filename,amount,public=False):
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

        # try:
        destination_p = sender
        source_acc = server.load_account(sender)
        base_fee = server.fetch_base_fee()
        path = [
        Asset('XLM',None),
        Asset("USDC",'GC5W3BH2MQRQK2H4A6LP3SXDSAAY2W2W64OWKKVNQIAOVWSAHFDEUSDC')
        ]
        transaction = TransactionBuilder(
            source_account=source_acc,
            network_passphrase=passphrase,
            base_fee=base_fee).append_path_payment_strict_send_op(
            destination_p,"XLM",None,amount,"USDC",
            'GC5W3BH2MQRQK2H4A6LP3SXDSAAY2W2W64OWKKVNQIAOVWSAHFDEUSDC',
            '10',path).build()

        transaction.sign(source_keypair)

        response = server.submit_transaction(transaction)
        if response['successful']:
            print("\nSuccessfully sent "+str(amount)+" XLM to USDC")
        else:
            print("\n something went wrong...")
        # except:
        #     print("\nconverstion failed")
