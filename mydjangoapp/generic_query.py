import environ
from pymongo import MongoClient
import time
from loguru import logger
from bson import ObjectId

env = environ.Env()
environ.Env.read_env()
conn = MongoClient("mongodb://localhost:27017")
db = conn["newsepick_recommendation_dev"]

# env = environ.Env()
# environ.Env.read_env()

# try:
#     # ✅ Create client
#     client = MongoClient(env("MONGO_URL"))

#     # 🔥 Check MongoDB connection
#     client.admin.command("ping")
#     print("MongoDB connection successful!")

#     # ✅ Select database
#     db = client[env("MONGO_DB_NAME")]
#     print("Connected to DB:", db.name)
# except Exception as e:
#     print(" MongoDB connection failed!")
#     print("Error:", e)


def convert_date(date):
    if date=="TODAY":
        now=int(time.time())*1000
        days= 1*24*60*60*1000 #yesterday
        from_ts=now-days

    if date=="YESTERDAY":
        now=int(time.time())*1000
        days= 1*24*60*60*1000 #yesterday
        from_ts=now-days

    if date=="LAST 30 DAYS":
        now=int(time.time())*1000
        days= 30*24*60*60*1000 #30days
        from_ts=now-days
  
    if date=="LAST 90 DAYS":
        now=int(time.time())*1000
        days= 90*24*60*60*1000 #90days
        from_ts=now-days
        
    if date=="LAST 365 DAYS":
        now=int(time.time())*1000
        days= 365*24*60*60*1000 #365days
        from_ts=now-days
        
    return from_ts


        
def evaluate_mcq_submission(classes, date, subjects,userId,size,current_page):
    global db
    logger.critical(f"params are userId==>{userId}-className-{classes}-date-{date}-subjectName-{subjects}-size-{size}-currentpage-{current_page}")
    match_condition = {}
    match_condition["userId"]=userId
    
   
    time_range=convert_date(date)

    if classes !="ALL":
        match_condition["className"]=classes
    if date:
        match_condition["createTime"]={"$gte":time_range}
    if subjects !="ALL":
        match_condition["subjectName"]=subjects
    print(match_condition)
    
    mcq_data_li = list(db.mcq_submission.aggregate([{"$match":match_condition},{"$limit":size},{"$skip":size*current_page}]))
    logger.critical(f"params are matchcondition==>{match_condition}-size-{size}-currentpage-{current_page}")
    

    return mcq_data_li
    
def update_mcq_data(correctAnswer,_id,userId):


    if db.mcq_submission.count_documents({"_id":ObjectId(_id)})==0:
        return "Please enter a valid id",404
    db.mcq_submission.update_one({"_id":ObjectId(_id)},
    {"$set":{"correctAnswer":correctAnswer}})
    return "Succesfully Updated!",200