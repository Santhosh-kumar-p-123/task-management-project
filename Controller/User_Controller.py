# User_Controller
import time
from flask import Blueprint, request, jsonify
import json
import os 
import time


class User_Controller:

    def __init__(self,data_file_path,notifier):
        self.data_file_path = data_file_path
        self.notifier = notifier
        
        

    # read data and write data method
    def read_data(self):
        if not os.path.exists(self.data_file_path):
            return {"users": []}
        with open(self.data_file_path, 'r')as f :
            return json.load(f)
        

    def write_data(self,data):
        with open(self.data_file_path, 'w') as f:
            json.dump(data, f, indent = 4)



    def create_user(self):
       data = self.read_data()
       users = data.get("users", [])
       request_data = request.json or {}
       
       new_user = {
           "user_id" : int(round(time.time() * 1000)),
            "name" : request_data.get("name"),
            "email" : request_data.get("email"),
            "role" :  request_data.get("role","member"),
            "permissions" : request_data.get("permissions", [])   
       }
       users.append(new_user)
       data["users"] = users
       self.write_data(data)
       self.notifier.notify_user_created(new_user)
       return jsonify({"message" : "User Created Successfully", "User":new_user}),201
    
    def get_all_users(self):
        data = self.read_data()
        return jsonify(data.get("users",[])), 200
    
    def get_user(self, user_id):
        data = self.read_data()
        users = data.get("users", [])
        user = next((u for u in users if u["user_id"] == user_id ),None)  
        if not user:
            return jsonify({"message" : " User not found"}), 404
        return jsonify(user),200
     
    def update_user(self,user_id):
        data = self.read_data()
        users = data.get("users",[])
        user = next((u for u  in users if u["user_id"] == user_id),None)

        if not user:
            return jsonify({"message" : "User not fount"}),404
        
        user["name"] = request.json.get("name",user["name"])
        user["email"] = request.json.get("email",user["email"])
        user["role"] = request.json.get("role",user["role"])
        user["permissions"] = request.json.get("permissions",user["permissions"])
        self.write_data(data)
        return jsonify({"message":"User updated Successfully", "user": user}),200

    def delete_user(self,  user_id):
        data = self.read_data()
        users = data.get("users",[])
        index = next((i for i, u in enumerate(users) if u["user_id"]== user_id), None)
        if index is None:
            return jsonify({"message" : "User not found"}),404
        
        removed_user = users.pop(index)
        data["users"] = users
        self.write_data(data)

        return jsonify({"message":"user deleted successfully", "removed_user" :removed_user }),200
    ixpu3xMin6aCIzrlUi+gbsF950A0A15pxz2opx4Bl64
    
    
    






    



   
