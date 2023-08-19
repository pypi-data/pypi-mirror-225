from flask_restful import Resource, reqparse, fields, abort
from hiddifypanel.models import *
from hiddifypanel.panel.database import db


class Manager(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('package_days', type=int, location='args', help='تعداد روز های بسته را وارد کنید',
                            required=True)
        parser.add_argument('usage_limit_GB', type=int, location='args', help='میزان حجم مجاز بسته را وارد کنید',
                            required=True)
        parser.add_argument('name', type=str, location='args', help='نام را وارد کنید', required=True)
        parser.add_argument('user-secret', type=str, location='headers', help='کلید ادمین را وارد کنید', required=True)
        args = parser.parse_args()
        from hiddifypanel.models.admin import get_admin_by_uuid
        admin = get_admin_by_uuid(args['user-secret'])
        if (admin):
            user = User(package_days=1, usage_limit_GB=1, name="test",
                        added_by=admin.id)
            db.session.add(user)
            db.session.commit()
        else:
            abort(403, message='کلید ادمین اشتباه است')
        return args
