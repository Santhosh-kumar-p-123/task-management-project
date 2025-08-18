# task controller

from flask import Flask, request, jsonify
import json, os, time

class ProjectController:
    def __init__(self,data_file_path,notifier):
        self.data_file_path = data_file_path
        self.notifier = notifier


    def read_data(self):
        if not os.path.exists(self.data_file_path):
            return {"Project" : [] }
        with open(self.data_file_path,"r") as f:
            return json.load(f)
        
    def write_data(self,data):
        with open(self.data_file_path,"w") as r:
            return json.dump(data,r, indent = 4)
        
    def validation(self,payload, is_update = False):
        error = []
        if not is_update:
            if not payload.get("name"):
                error.append("Project name is required.")
            if not payload.get("start_date"):
                error.append("start_date required")
            if not payload.get("end_date"):
                error.append("end_date required")
        return error


# project operations 
    def create_project(self):
        payload = request.json or {}
        error = self.validation(payload)
        if error :
            return jsonify({"error":error}), 400
        data = self.read_data()
        project = {
            "project_id" : int(time.time()*1000),
            "name" : payload["name"],
            "description" : payload.get("description"),
            "start_date" : payload["start_date"],
            "end_date" : payload["end_date"],
            "created_by" : payload.get("created_by"),
            "tasks" : payload.get("task", [])
        }
        data.setdefault("Project", []).append(project)
        self.write_data(data)

        created_by = next((u for u in data.get('users',[]) if u['user_id'] == payload.get('created_by')), None)
        if created_by:
           print("Sending project created email to:", created_by["email"]) 
           self.notifier.notify_project_created(created_by,project)
        else:
            print("e-mail not sending")

        return jsonify({"message":"Project created successfully","project":project}), 201
    
    def get_all_project(self):
            return jsonify({"Project": self.read_data().get("Project", [])})
    

    def get_one_project(self,project_id):
        data = self.read_data()
        project = next((p for p in data["Project"] if p["project_id"] == project_id),None)
        if not project:
            return jsonify({"message":"Project Not Found"}), 404
        return jsonify(project),200
    
    def update_Project(self,project_id):
        payload = request.json or {}
        error = self.validation(payload, is_update=True)
        if error:
            return jsonify({"error" : error})
        data = self.read_data()
        project = next((p for p in data["Project"] if p["project_id"]== project_id),None)
        if not project:
            return jsonify({"message":"Project not Found"}), 404
        
        project.update({"name" : payload.get("name",project["name"]),
                        "description" : payload.get("description",project["description"]),
                        "start_date" : payload.get("start_date",project["start_date"]),
                        "end_date" : payload.get("end_date",project["end_date"]),
                        "tasks" : payload.get("tasks", project["tasks"])
                        })
        self.write_data(data)
        return jsonify({"message":"project update successfully","Project" :project }),200
    def delete_project(self,project_id):
        data = self.read_data()
        idx = next((i for i,p in enumerate(data["Project"]) if p["project_id"] == project_id),None)
        if idx is None:
            return jsonify({"message":"Project not found"}),404
        removed = data["Project"].pop(idx)
        self.write_data(data)
        return jsonify({"message" : "Project deleted", "removed_project": removed}), 200



    




        




        


        
      
        

