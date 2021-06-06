################################################################################
########################### paging_example.py ##################################
#                                                                              #
# The purpose of this script is to show how I am currently implementing paging #
#                                                                              #
################################################################################
from stellar_sdk import Server, Asset
from pandas import DataFrame as DF
from pandas import set_option
set_option('display.max_rows', None)
set_option('display.max_colwidth', None)

################################################################################
############# Preliminary setup and definitions section ########################
#                                                                              #
# asset -> this is the asset we are interested in viewing the total holders of #
# exceptions -> these are accounts we'd like to exclude for being outliers     #
#                                                                              #
# asset=['ARST','GB7TAYRUZGE6TVT7NHP5SMIZRNQA6PLM423EYISAOAP3MKYIQMVYP2JO']
asset=['BRLT','GB7TAYRUZGE6TVT7NHP5SMIZRNQA6PLM423EYISAOAP3MKYIQMVYP2JO']
#                                                                              #
exceptions =['GDMSN2PQ3EB32LZY5JVACI4H7GUVQ3YUWOM4437IDTVQHHWHYG7CGA5Z',
'GB34PTUQQPYKN7XPWFZCIP77X5ZAEQEB3IN227EHIZFGLUUDS2Y2JVRW',
'GDEFAUQUISB3NLEKFXNVUARIO6MRXI2SD2GLGPIM6TJHR4ZRYOYEBHLW',
'GBKBU7E7TZFV6RPVV5FLXISAICNQKBINW7IDKS7IO5E26P6NQFMWILQL']
#                                                                              #
server = Server(horizon_url="https://horizon-testnet.stellar.org")
asset_obj = Asset(code=asset[0],issuer=asset[1])
accounts = server.accounts().for_asset(asset_obj).limit(200).call()
#                                                                              #
################################################################################


data_arr = []

while len(accounts['_embedded']['records']) > 0: # if we haven't reached the end of pages

    for r in accounts['_embedded']['records']:
        if r['account_id'] in exceptions:
            pass
        else:
            for b in r['balances']:
                if b['asset_code'] == asset[0]:
                    data_arr.append([r['account_id'],b['balance']])
                    break;

    # Here is my brute-force paging implementaiton ....
    #
    # split the href url into components
    find_cursor_arr = accounts['_links']['next']['href'].split("&")
    for n in find_cursor_arr:
        # find the "cursor=G...." and record the "G..."
        if ("cursor" in n) and len(n) > 7: cursor = n[7:]
    # call again with cursor set to "G...."
    accounts = server.accounts().for_asset(asset_obj).cursor(cursor).limit(200).call()

df = DF(data_arr)

print(len(data_arr))

print(df)
