# task_Controller
from flask import Flask,request,jsonify
import os,json,time


class TaskController:


    def __init__(self,data_file_path):
        self.data_file_path = data_file_path

    def read_data(self):
        if not os.path.exists(self.data_file_path):
            return {"Tasks" : [],"Users" : [], "Project" : []}
        with open(self.data_file_path,"r") as r:
            return json.load(r)
        
    def write_data(self,data):
        with open(self.data_file_path,"w") as w:
            return json.dump(data,w, indent = 4)
    def validate_payload(self,payload, is_update = False):
        error = []
        allowed_priorities = ["Critical","High","Medium","Low"]

        if not is_update:
            if not payload.get("title"):
                error.append("task title is required")
            if not payload.get("priority"):
                error.append("priority is required")
            elif payload["priority"] not in allowed_priorities:
                error.append(f"priority must be one of {allowed_priorities}")
            if not payload.get("project_id"):
                error.append("Project Id is required")

        return error
    

    ########
    def create_task(self):
        payload = request.json or {}
        error = self.validate_payload(payload)
        if error:
            return jsonify({"error" : error}), 400
        
        data = self.read_data()

        # if payload.get("assigned_to") and not any(u["user_id"] == payload["assigned_to"] for u in data.get("Users",[])): 

        #     return jsonify({"error" : "Assigened user does not exist"}), 400
        
        # if not any(p["project_id"] == payload["project_id"] for p in data.get("Project",[])):
        #     return jsonify({"error" : "project does not exist"}),400
        
        new_task = {
            "task_id" : int(time.time() * 1000),
            "title" : payload["title"],
            "description" : payload.get("description",""),
            "deadline" : payload.get("deadline"),
            "status" : payload.get("status","pending"),
            "assigned_to" : payload.get("assigned_to"),
            "project_id" : payload["project_id"],
            "dependencies" : payload.get("dependencies",[]),
            "time_spent_hours": payload.get("time_spent_hours")
        }
        data.setdefault("Tasks",[]).append(new_task)
        self.write_data(data)
        return jsonify({"message" : "Task created successfully", "task" : new_task}),201
    
    def get_all_tasks(self):
        data = self.read_data()
        return jsonify(data.get("Tasks",[])), 200
    
    def get_one(self, task_id):
        data = self.read_data()
        task = next((t for t in data.get("Tasks",[]) if t["task_id"] == task_id), None)
        if not task:
            return jsonify({"message" : "Task not found "}),404
        return jsonify(task),200
    
    def update_task(self,task_id):
        payload = request.json or {}
        error = self.validate_payload(payload, is_update=True)
        if error:
            return jsonify({"message" : "Task not found"}),404
        
        data = self.read_data()
        task = next((t for t in data.get("Tasks",[]) if t["task_id"] == task_id),None)

        if not task :
            return jsonify({"message" : "Task not found"}),404
        task.update({
            "title" : payload.get("title" , task["title"]),
            "description": payload.get("description", task["description"]),
            "priority" : payload.get("priority", task["deadline"]),
            "status" : payload.get("status", task["status"]),
            "assigned_to" : payload.get("assigned_to",task["assigned_to"]),
            "project_id" : payload.get("project_id", task["project_id"]),
            "dependencies" : payload.get("dependencies", task["dependencies"]),
            "time_spent_hours" : payload.get("time_spent_hours", task["time_spent_hours"]),
            "update_at" : time.strftime("%Y-%m-%dT%H:%dT%H:%M:%s"),
        })
        print(task["project_id"])
        self.write_data(data)
        return jsonify({"message" : "Task updated successfully", "task": task}), 200
        
    def delete(self, task_id):
        data = self.read_data()
        idx = next((i for i, t in enumerate(data.get("task", [])) if t["task_id"] == task_id),None)
        if idx is None:
            return jsonify({"message" : "Task not found"}), 404
        removed = data["Tasks"].pop(idx)
        self.write_data(data)
        return jsonify({"message" : "Task deleted successfully", "removed_task": removed}),200





















































    
        
        
    
    
                                              
        



        
    
