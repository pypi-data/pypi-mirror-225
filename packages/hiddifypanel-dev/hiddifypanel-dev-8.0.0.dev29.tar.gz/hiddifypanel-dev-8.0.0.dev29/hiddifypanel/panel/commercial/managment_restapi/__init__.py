from flask import Blueprint
from flask_restful import Api
from . import userController
bp = Blueprint("management", __name__, url_prefix="/<proxy_path>/<user_secret>/api/manage/v1")
api = Api(bp)


def init_app(app):

    api.add_resource(userController.addUser, "/user/add")
    api.add_resource(userController.removeUser, "/user/remove")
    api.add_resource(userController.getuser, "/user")
    api.add_resource(userController.edituser, "/user/edit")
    api.add_resource(userController.resetday, "/user/reset")

    # api.resource('/res', Manager)
    # with app.app_context():
    #     register_bot()
    app.register_blueprint(bp)
