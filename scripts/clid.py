#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# Импортируем python-модули
import time
import ldap
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from datetime import datetime

#-------- VAR -------------------------------
s = time.time()
LDAP_PROVIDER_URL = 'ldap://cse.ru:389'
LDAP_HOST = 'cse.ru'
# Base DN of your directory
LDAP_BASE_DN = 'dc=cse,dc=ru'
LDAP_FILTER = ["mail", "displayName", "company", "department", "title"]
LDAP_FILTER_CLID = ["displayName", "cn", "telephoneNumber", "mail", "department", "division", "title"]
#LDAP_FILTER_CLID = ['displayName', 'company']
start_num=1000
end_num=9999

db_string="mysql+pymysql://pbxadmin:tmYmT93RWA2XGDmh@10.0.1.120/FLASK"
#----------------------------------------------------

#----------- FUNC ----------------------------
def get_ldap_connection():
    conn = ldap.initialize(LDAP_PROVIDER_URL)
    conn.protocol_version = ldap.VERSION3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    return conn

#-------- BODY ------------------------
# ---------------------------------
# === Start Script
# ---------------------------------
start = datetime.now()
start_time = start.strftime("%d-%m-%Y %H:%M:%S")
print("=======================================")
print(f"Start script at: {start_time}")
print("=======================================")

df = pd.DataFrame(columns=['fullname', 'clid_name', 'clid_num', 'email', 'department', 'division', 'title'])
conn = get_ldap_connection()
usr = 'pavlovsky@cse.ru'
pwd = 'vjuexbq*rjqjn2'
try:
    conn.simple_bind_s(usr, pwd)
except ldap.INVALID_CREDENTIALS:
    print(
        'Invalid username or password. Please try again.',
        'danger')
except ldap.SERVER_DOWN:
    print('AD server not available')
for i in range(start_num, end_num):
    try:
        ldap_filter = f'telephoneNumber={i}'
        data = conn.search_s(LDAP_BASE_DN, ldap.SCOPE_SUBTREE, ldap_filter, LDAP_FILTER_CLID)
        if data[0][1]['telephoneNumber'][0].decode('utf-8') is not None:
            clid_name = data[0][1]['cn'][0].decode('utf-8')
            clid_num = data[0][1]['telephoneNumber'][0].decode('utf-8')
            email = data[0][1]['mail'][0].decode('utf-8')
            if 'displayName' in data[0][1]:
                fullname = data[0][1]['displayName'][0].decode('utf-8')
            else:
                fullname = ''
            if 'department' in data[0][1]:
                department = data[0][1]['department'][0].decode('utf-8')
            else: department=''
            if 'division' in data[0][1]:
                division = data[0][1]['division'][0].decode('utf-8')
            else: division=''
            if 'title' in data[0][1]:
                title = data[0][1]['title'][0].decode('utf-8')
            else: title=''
#            print(f"- NUM: {clid_num} - NAME: {clid_name} - FULLNAME: {fullname}")
            df = df.append({'fullname': fullname,
                            'clid_name': clid_name,
                            'clid_num': clid_num,
                            'email': email,
                            'department': department,
                            'division': division,
                            'title': title}, ignore_index=True)

        else: continue
    except:
        continue
print(df)
engine = create_engine(db_string)
df.to_sql('clid', engine, index=True, index_label='id', if_exists='replace')
conn.unbind()

end = datetime.now()
end_time = end.strftime("%d-%m-%Y %H:%M:%S")
print("--- %s seconds ---" % (time.time() - s))
print("=======================================")
print(f"End script at: {end_time}")
print("=======================================")
