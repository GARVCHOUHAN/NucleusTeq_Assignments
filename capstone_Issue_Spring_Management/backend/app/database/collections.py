from app.database.mongodb import database

users_collection = database["users"]

projects_collection = database["projects"]

issues_collection = database["issues"]

sprints_collection = database["sprints"]

comments_collection = database["comments"]