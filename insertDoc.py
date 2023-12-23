import pymongo
from datetime import datetime

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string

# Specify the order code you are creating
order_code_to_find = "ord-101" #Replace with the actual order code
document = {
    "order_code": order_code_to_find,
    "order_name": "Hydogen",
    "order_package": "200KG",
    "timestamp": datetime.utcnow()
}

# Select the database and collection
db = client["state_orders"]  # Replace with your database name
collection = db["orders"]  # Replace with your collection name
history_collection = db["order_history"]  # Replace with your order history collection name

# Query the collection for a document with the specified order code
existing_document = collection.find_one({"order_code": order_code_to_find})

# Check if a matching document was found
if existing_document:
    print("Document found:")
    # Count documents with the specified order_code in the order_history collection
    count = history_collection.count_documents({"order_code": order_code_to_find})

    # Print the count
    print(f"Number of documents with order_code '{order_code_to_find}' in order_history: {count}")

    # Retrieve the document from the original collection
    original_document = existing_document.copy()
    # Modify the document if needed (e.g., add a timestamp for history)
    original_document["modify_timestamp"] = datetime.utcnow()

    # Retain the original _id field as org_order_id
    original_document["org_order_id"] = original_document.pop('_id', None)
    original_document["sequence"] = count + 1

    # Insert the modified document into the order_history collection
    result = history_collection.insert_one(original_document)

    # Print the inserted document's ID
    print("Inserted document into order_history with ID:", result.inserted_id)

    # ------------------------------------------------------------------------------------

    # Specify the filter criteria to identify the document to update
    filter_criteria = {"order_code": document["order_code"]}

    # Specify the new values you want to set
    new_values = {
        "$set": document
    }

    # Update the document with upsert set to True
    result = collection.update_one(filter_criteria, new_values, upsert=True)

    # -----------------------------------------------------------------------------------------


    # document = collection.find_one({"order_code": order_code_to_find})
    # order_id = document.get("_id")
    # print(f"Order ID for order code '{order_code_to_find}': {order_id}")
    #
    # # Delete the document
    # filter_criteria = {"order_code": order_code_to_find}
    # result = collection.delete_one(filter_criteria)
    #
    # # Insert the document into the collection
    # result = collection.insert_one(document)

    #
    # # Specify the filter criteria to identify the document(s) to update
    # filter_criteria = {"order_code": order_code_to_find}
    #
    # # Specify the new values you want to set
    # new_values = {
    #     "$set": {
    #         "order_name": "genx",
    #         "order_package": "injection pen X 1000",
    #         "timestamp": datetime.utcnow()
    #     }
    # }
    #
    # # Update all documents that match the filter criteria
    # result = collection.update_many(filter_criteria, new_values)

    # Print the number of modified documents
    # print("Matched and modified documents:", result.modified_count)

else:
    print(f"No document found with order code: {order_code_to_find}")

    # Insert the document into the collection
    result = collection.insert_one(document)

    # Print the inserted document's ID
    print("Inserted document ID:", result.inserted_id)

# Close the MongoDB connection
client.close()
