#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import time
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

#-------- VAR -------------------------------
s = time.time()
start_num=1000
end_num=9999
db_string="mysql+pymysql://pbxadmin:tmYmT93RWA2XGDmh@10.0.1.120/FLASK"
#----------------------------------------------------
#-------- BODY ------------------------
# ---------------------------------
# === Start Script
# ---------------------------------
start = datetime.now()
start_time = start.strftime("%d-%m-%Y %H:%M:%S")
print("=======================================")
print(f"Start script at: {start_time}")
print("=======================================")

df_aors = pd.DataFrame(columns=['id', 'max_contacts'])
df_auths = pd.DataFrame(columns=['id', 'auth_type', 'password', 'username'])
df_endpoints =pd.DataFrame(columns=['id', 'transport', 'aors', 'auth', 'context', 'disallow', 'allow', 'direct_media'])

for i in range(start_num, end_num):
    try:
        df_aors = df_aors.append({'id': i,
                        'max_contacts': 1}, ignore_index=True)
        df_auths = df_auths.append({'id':i,
                                   'auth_type':'userpass',
                                   'password':'9aLgxxDnwjdneqw',
                                   'username': i}, ignore_index=True)
        df_endpoints = df_endpoints.append({'id': i,
                                            'transport':'transport-udp',
                                            'aors': i,
                                            'auth': i,
                                            'context': 'users',
                                            'disallow': 'all',
                                            'allow': 'alaw',
                                            'direct_media': 'no'
                                            }, ignore_index=True)
    except:
        continue

engine = create_engine(db_string)
df_old_aors = pd.read_sql('SELECT id, max_contacts FROM ps_aors', con=engine)
df_old_auths = pd.read_sql('SELECT id, auth_type, password, username  FROM ps_auths', con=engine)
df_old_endpoints = pd.read_sql('SELECT id, transport, aors, auth, context, disallow, allow, direct_media FROM ps_endpoints', con=engine)

df_aors_clear=pd.concat([df_aors, df_old_aors]).drop_duplicates(keep=False)
df_auths_clear=pd.concat([df_auths, df_old_auths]).drop_duplicates(keep=False)
df_endpoints_clear=pd.concat([df_endpoints, df_old_endpoints]).drop_duplicates(keep=False)


print(df_aors_clear)
print(df_auths_clear)

df_aors_clear.to_sql('ps_aors', engine, index=False, if_exists='append')
df_auths_clear.to_sql('ps_auths', engine, index=False, if_exists='append')
df_endpoints_clear.to_sql('ps_endpoints', engine, index=False, if_exists='append')

end = datetime.now()
end_time = end.strftime("%d-%m-%Y %H:%M:%S")
print("--- %s seconds ---" % (time.time() - s))
print("=======================================")
print(f"End script at: {end_time}")
print("=======================================")
