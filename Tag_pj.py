import nxppy
import datetime
import pymongo
import time

# import os

date = datetime.datetime.now()
mifare = nxppy.Mifare()

myclient = pymongo.MongoClient(
    "mongodb+srv://tag_pi:tag_pi@cluster0-q25lj.mongodb.net/test?retryWrites=true&w=majority")

dblist = myclient.list_database_names()
if "zeiterfassung" in dblist:
    print("The database exists.")
    print("Waiting for Tag...")

mydb = myclient["zeiterfassung"]
mycol = mydb["tag_user"]

# Print card UIDs as they are detected
# tag_dict = {}

while True:
    date = datetime.datetime.now()
    try:
        uid = mifare.select()
        if uid is not None:
            print("Tage gescanned...\n")
            if mycol.find_one({"_id": uid}) is not None:
                entry = mycol.find_one({"_id": uid})
                data = entry["Date"]
                time_entry = data["Time"]
                dates = date.strftime("%d-%m-%Y")
                times = date.strftime("%H:%M:%S")
                if mycol.find_one({"_id":uid,"Date._id":dates}):
                    print("Date: OK")
                    test = mycol.find_one({"_id" : uid,"Date._id":dates})
                    mycol.insert_one(mycol.find({"_id":uid,"Date._id":dates}, {"Date.Time._id": times}))
                    

                    #test.insert_one({"Date":{"Time":{"_id":times}}})
                    
                    print(test)
                else:
                    print("Nope...")
                
                
                # {$push:{messages:{_id:ObjectId(), message:"I am message 2."}}})
                # print("Tag_Number: "+entry[
                # "_id"]+"\nDate:       "+data["_id"]+"\nTime:       "+time_entry["_id"]+"\nIn/out:     "+time_entry[
                # "in/out"])

            else:
                name = str(input("Please insert username:\n"))
                dates = date.strftime("%d-%m-%Y")
                times = date.strftime("%H:%M:%S")
                mycol.insert_one({
                    "_id": uid,
                    "Name": name,
                    "Date": {
                        "_id": dates,
                        "Time": {
                            "_id": times,
                            "in/out": "in"}}})
                print("Username entered...")
            uid = None
            time.sleep(3)


    #
    except nxppy.SelectError:
        # SelectError is raised if no card is in the field.
        pass
