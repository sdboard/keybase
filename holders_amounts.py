# This is the first piece of functionality I've written outside of copy-pasting from the guide
# The purpose of this is to list the all the asset holders' addresses and quantity held presumably for staking rewards
# It's currently hard-coded for the testnet in line 9.
# make sure you have installed stellar_sdk prior to running (which requires gcm)

from stellar_sdk import Asset
from stellar_sdk import Server
def list_asset_holders(asset_code,issuer):
    server = Server(horizon_url="https://horizon-testnet.stellar.org")
    asset = Asset(code=asset_code,issuer=issuer)
    account_list_dict = {}
    accounts = server.accounts().for_asset(asset).limit(200).call()
    while len(accounts['_embedded']['records']) > 0:
        for r in accounts['_embedded']['records']:
            for b in r['balances']:
                if b['asset_code'] == asset_code:
                    account_list_dict[r['account_id']] = float(b['balance'])
                    break;
        find_cursor_arr = accounts['_links']['next']['href'].split("&")
        for n in find_cursor_arr:
            if ("cursor" in n) and len(n) > 7: cursor = n[7:]
        accounts = server.accounts().for_asset(asset).cursor(cursor).limit(200).call()
    account_list_dict = sorted(account_list_dict.items(),key=lambda x: x[1],reverse=True)
    for a in account_list_dict: print('account '+a[0]+' has '+str(round(a[1],3))+' '+asset_code)

# I looked up an example on stellar.expert and found ARST as having more than 200, which was the primary challenge, along with the issuer's account
list_asset_holders('ARST','GB7TAYRUZGE6TVT7NHP5SMIZRNQA6PLM423EYISAOAP3MKYIQMVYP2JO') 
