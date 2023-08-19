from pprint import pprint

from flask import flash
from flask_restful import Resource, reqparse, fields, abort
from hiddifypanel.models import *
from hiddifypanel.panel.database import db


class addUser(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('package_days', type=int, location='args', help='تعداد روز های بسته را وارد کنید',
                            required=True)
        parser.add_argument('usage_limit_GB', type=int, location='args', help='میزان حجم مجاز بسته را وارد کنید',
                            required=True)
        parser.add_argument('name', type=str, location='args', help='نام را وارد کنید', required=True)
        parser.add_argument('admin-secret', type=str, location='headers', help='کلید ادمین را وارد کنید', required=True)
        args = parser.parse_args()
        from hiddifypanel.models.admin import get_admin_by_uuid
        admin = get_admin_by_uuid(args['admin-secret'])
        if (admin):
            user = User(package_days=1, usage_limit_GB=1, name="test",
                        added_by=admin.id)
            db.session.add(user)
            db.session.commit()
        else:
            return dict(code=403, message='کلید ادمین یافت نشد')
        return dict(code=200, message='کاربر اضافه شد',data=user.to_dict())


class removeUser(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('uuid', type=str, location='args', help='uuid کاربر را وارد کنید', required=True)
        parser.add_argument('admin-secret', type=str, location='headers', help='کلید ادمین را وارد کنید', required=True)
        args = parser.parse_args()
        from hiddifypanel.models.admin import get_admin_by_uuid
        admin = get_admin_by_uuid(args['admin-secret'])
        if admin:
            user = User.query.filter_by(uuid=args['uuid']).first()
            if user:
                db.session.delete(user)
                db.session.commit()
            else:
                return dict(code=404, message='کاربر با uuid وارد شده یافت نشد')
        else:
            return dict(code=403, message='کلید ادمین یافت نشد')
        return dict(code=200, message='کاربر حذف شد',data=user.to_dict())

class getuser(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('uuid', type=str, location='args', help='uuid کاربر را وارد کنید', required=True)
        parser.add_argument('admin-secret', type=str, location='headers', help='کلید ادمین را وارد کنید', required=True)
        args = parser.parse_args()
        from hiddifypanel.models.admin import get_admin_by_uuid
        admin = get_admin_by_uuid(args['admin-secret'])
        if admin:
            user = User.query.filter_by(uuid=args['uuid']).first()
            if user:
                return dict(code=200, message='کاربر یافت شد', data=user.to_dict())
            else:
                return dict(code=404, message='کاربر با uuid وارد شده یافت نشد')
        else:
            return dict(code=403, message='کلید ادمین یافت نشد')

class edituser(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('package_days', type=int, location='args', help='تعداد روز های بسته را وارد کنید',
                            required=True)
        parser.add_argument('usage_limit_GB', type=int, location='args', help='میزان حجم مجاز بسته را وارد کنید',
                            required=True)
        parser.add_argument('name', type=str, location='args', help='نام را وارد کنید', required=True)
        parser.add_argument('uuid', type=str, location='args', help='uuid کاربر را وارد کنید', required=True)
        parser.add_argument('admin-secret', type=str, location='headers', help='کلید ادمین را وارد کنید', required=True)
        args = parser.parse_args()
        from hiddifypanel.models.admin import get_admin_by_uuid
        admin = get_admin_by_uuid(args['admin-secret'])
        if admin:
            user = User.query.filter_by(uuid=args['uuid']).first()
            if user:
                user.package_days=args['package_days']
                user.usage_limit_GB=args['usage_limit_GB']
                user.name=args['name']
                user.package_days=args['package_days']
                return dict(code=200, message='کاربر با موفقیت بروز شد', data=user.to_dict())
            else:
                return dict(code=404, message='کاربر با uuid وارد شده یافت نشد')
        else:
            return dict(code=403, message='کلید ادمین یافت نشد')

class resetday(Resource):
    def get(self):
        parser = reqparse.RequestParser()


        parser.add_argument('reset', type=bool, location='args', help='برای ریست شدن ۱ یا True ارسال شود', required=True)
        parser.add_argument('uuid', type=str, location='args', help='uuid کاربر را وارد کنید', required=True)
        parser.add_argument('admin-secret', type=str, location='headers', help='کلید ادمین را وارد کنید', required=True)
        args = parser.parse_args()
        from hiddifypanel.models.admin import get_admin_by_uuid
        admin = get_admin_by_uuid(args['admin-secret'])
        if admin:
            user = User.query.filter_by(uuid=args['uuid']).first()
            if user:
                if(args['reset']):
                    user.start_date = None
                    user.current_usage_GB = 0
                    db.session.commit()
                    return dict(code=200, message='کاربر با موفقیت بروز شد', data=user.to_dict())
                else:
                    return dict(code=405, message='به دلیل عدم ارسال تایید ریست انجام نشد', data=user.to_dict())

            else:
                return dict(code=404, message='کاربر با uuid وارد شده یافت نشد')
        else:
            return dict(code=403, message='کلید ادمین یافت نشد')
