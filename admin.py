from flask import redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class StoreModelView(ModelView):
    def is_accessible(self):
        print(current_user.roles)
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))
