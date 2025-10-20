from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["chai_db"]
collection = db["students"]

student = {"name": "Trentin", "age": 21, "major": "Computer Science"}
result = collection.insert_one(student)
print(f"Inserted document with ID: {result.inserted_id}")

many_students = [
    {"name": "Alice", "age": 22, "major": "Physics"},
    {"name": "Bob", "age": 23, "major": "Mathematics"}
]
collection.insert_many(many_students)

print("\nAll students:")
for s in collection.find():
    print(s)

collection.update_one({"name": "Trentin"}, {"$set": {"major": "Data Science"}})
collection.delete_one({"name": "Bob"})

print("\nAfter update and delete:")
for s in collection.find():
    print(s)
