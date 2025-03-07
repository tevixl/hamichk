import pymongo

client = pymongo.MongoClient(
        "mongodb+srv://tevixl:ts9KYeRuK2spsSZ5!v5M@hamisolh.m5vyk.mongodb.net/?retryWrites=true&w=majority&appName=hamisolh"
)

result = str(client)

if "connect=True" in result:
    try:
        print("CONFIG DB CONNECTED SUCCESSFULLY ✅")
    except:
        pass
else:
    try:
        print("CONFIG DB CONNECTION FAILED ❌")
    except:
        pass

COLLECTIONS = client["CONFIG_DATABASE"] 
BLACKLISTED_SKS = COLLECTIONS["BLACKLISTED_SKS"] 
TOKEN_DB = COLLECTIONS["TOKEN_DB"] 
SKS_DB = COLLECTIONS["SKS_DB"]
