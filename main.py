from flask import Flask
from Controller.User_Controller import User_Controller
from Controller.Project_Controller import ProjectController
from Controller.Task_Controller import TaskController
from Controller.Notification_Controller import NotificationController
import os 
from flask import Blueprint



# App initialization
app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__),"Data","Data.json")

# email
notifier = NotificationController(
    email="santhoshvijaypeter@gmail.com",
    password="arkw mlff egch vgvh"
)
#create user controller instance 
user_Controller = User_Controller(DATA_FILE,notifier)
User_bp = Blueprint("user_bp", __name__)

#create Project controller instance
project_Controller = ProjectController(DATA_FILE,notifier)
Project_bp = Blueprint("project_bp", __name__)

#create Task Controller instance
taskcontroller = TaskController(DATA_FILE)
Task_bp = Blueprint("Task",__name__)







#Register blueprint 
def register_routes():
    User_bp.route("/users", methods=["POST"])(user_Controller.create_user)
    User_bp.route("/users", methods=["GET"])(user_Controller.get_all_users)
    User_bp.route("/users/<int:user_id>", methods=["GET"])(user_Controller.get_user)
    User_bp.route("/users/<int:user_id>", methods=["PUT"])(user_Controller.update_user)
    User_bp.route("/users/<int:user_id>", methods=["DELETE"])(user_Controller.delete_user)

    # Project routes
    Project_bp.route("/projects", methods = ["POST"])(project_Controller.create_project)
    Project_bp.route("/projects", methods = ["GET"])(project_Controller.get_all_project)
    Project_bp.route("/projects/<int:project_id>", methods = ["GET"])(project_Controller.get_one_project)
    Project_bp.route("/projects/<int:project_id>", methods = ["PUT"])(project_Controller.update_Project)
    Project_bp.route("/projects/<int:project_id>", methods = ["DELETE"])(project_Controller.delete_project)

    # Tasks routes
    Project_bp.route("/task", methods = ["POST"])(taskcontroller.create_task)
    Project_bp.route("/task", methods = ["GET"])(taskcontroller.get_all_tasks)
    Project_bp.route("/task/<int:task_id>", methods = ["GET"])(taskcontroller.get_one)
    Project_bp.route("/task/<int:task_id>", methods = ["PUT"])(taskcontroller.update_task)
    Project_bp.route("/task/<int:task_id>", methods = ["DELETE"])(taskcontroller.delete)

register_routes()
app.register_blueprint(User_bp)
app.register_blueprint(Project_bp)  


if __name__ == "__main__":
    app.run(port=5001, debug=True)


