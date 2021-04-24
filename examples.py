import requests

def generate_keypair():
    pair=Keypair.random()
    print(pair)
    print(type(pair))
    print(pair.__dict__.keys())
    print("secret: ")
    print(pair.secret)
    print("\npublic: ")
    print(pair.public_key)
    print("\nverify key: ")
    print(pair.verify_key)
    print("\nsign_key: ")
    print(pair.signing_key)

def fund_account():
    try:
        url = 'https://friendbot.stellar.org?addr='+pair.public_key
        fetch = requests.get(url)
        response = fetch.json()
        print(response['successful'])
    except:
        print("account fund error")
    if "bad_request" in response['type']:
        pass

def check_ballances():
    #server = Server(horizon_url="https://horizon-testnet.stellar.org")
    #account = server.load_account(pair.public_key())
    account = server.accounts().account_id(public_key).call()
    print("Ballance for account "+str(pair.public_key()))
    for b in account['balances']:
        print("Type: "+b['asset_type']+", Balance: "+b['balance'])

def scan_server_for_assets():
    assets = server.assets().call()
    for asset in assets['_embedded']['records']:
        print(asset['asset_code'])

def list_asset_holders(asset_code,issuer):
    from stellar_sdk import Asset
    from stellar_sdk import Server
    server = Server(horizon_url="https://horizon-testnet.stellar.org")
    asset = Asset(code=asset_code,issuer=issuer)
    account_list_dict = {}
    accounts = server.accounts().for_asset(asset).limit(200).call()
    find_cursor_arr = accounts['_links']['prev']['href'].split("&")
    while len(accounts['_embedded']['records']) > 0:
        for r in accounts['_embedded']['records']:
            temp_account = server.accounts().account_id(r['account_id']).call()
            index = next((index for (index, d) in enumerate(temp_account['balances']) if d["asset_code"] == asset_code), None)
            account_list_dict[r['account_id']] = float(temp_account['balances'][index]['balance'])
        find_cursor_arr = accounts['_links']['next']['href'].split("&")
        for n in find_cursor_arr:
            if ("cursor" in n) and len(n) > 7: cursor = n[7:]
        accounts = server.accounts().for_asset(asset).cursor(cursor).limit(200).call()
    account_list_dict = sorted(account_list_dict.items(),key=lambda x: x[1],reverse=True)
    for a in account_list_dict: print('account '+a[0]+' has '+str(round(a[1],3))+' '+asset_code)

#list_asset_holders('EVTX','GBYZERKKDNUMPBI4OPPQJWLC6LOSG5QT372ZMALWZWNHFUIPW4NAKGYB')

list_asset_holders('ARST','GB7TAYRUZGE6TVT7NHP5SMIZRNQA6PLM423EYISAOAP3MKYIQMVYP2JO')
