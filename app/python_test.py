from bson import ObjectId

# Create a new ObjectId (MongoDB's unique identifier)
new_id = ObjectId()

# Print the ObjectId

# Check if it's a valid ObjectId
print(f"Is it valid? {ObjectId.is_valid("679879142a64498155c21234")}")
