import traceback 
import pymongo 

client = pymongo.MongoClient( 
        "mongodb+srv://tevixl:ts9KYeRuK2spsSZ5!v5M@hamisolh.m5vyk.mongodb.net/?retryWrites=true&w=majority&appName=hamisolh" 

) 
result = str(client) 

if "connect=True" in result: 
    try: 
        print("MONGODB CONNECTED SUCCESSFULLY ✅") 
    except: 
        pass 
else: 
    try: 
        print("MONGODB CONNECTION FAILED ❌") 
    except: 
        pass 

folder = client["TEST_DATABASE"] 
MAINDB = folder.MAINDB
chats_auth = folder.CHATS_AUTH 
gcdb = folder.GCDB 
sksdb = client["SKS_DATABASE"].SKS 
confdb = client["SKS_DATABASE"].CONF_DATABASE
