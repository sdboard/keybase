from OurAssets import URTH
from OurWork import Action
import pandas as pd
pd.set_option('display.max_colwidth', None)  # or 199

(cur_data,cur_dict) = Action.get_holders(URTH.collectables,pub=True,exceptions=URTH.exceptions)

members = Action.get_members(cur_data)

holders_totals, percent_stakes = Action.get_totals(URTH.collectables,cur_data,cur_dict,members)

print(" ")
print("\t Totals ")
df = pd.DataFrame(holders_totals)
print(df)
print(" ")
print(" ")
print("\t Totals by % ")
df = pd.DataFrame(percent_stakes)
print(df)
print(" ")

# reward_assets_holders(URTHassets,pub=True,exceptions=['GDLA2EKBBPIAYJ3BSOQCMWVZ2T3GM4NFVECRSFCMZW676CSMTVL5NXLP'])
