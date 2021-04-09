from flask import url_for, request, abort, flash
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_security import current_user
from werkzeug.utils import redirect
from app.models import User, Role


class AdminMixin:
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('Admin')
        )
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                flash("You have no access, try to change your role")
                return redirect(url_for('main.index'))
            else:
                # login
                return redirect(url_for('auth.login', next=request.url))
    def is_visible(self):
        return True

class MyAdminView(AdminMixin, AdminIndexView):
    pass

class MyRoleView(AdminMixin, ModelView):
    def is_visible(self):
        if current_user.has_role('Admin'):
            return True
        else:
            return False

class MyUserView(AdminMixin, ModelView):
    pass

class MainIndexLink(MenuLink):
    def get_url(self):
        return url_for("main.index")

def init_app(app, db, name="Home", url_prefix="/admin", **kwargs):
    vkwargs = {"name": name, "endpoint": "admin", "url": url_prefix}

    akwargs = {
        "template_mode": "bootstrap3",
        "static_url_path": f"/templates/{url_prefix}",
        "index_view": MyAdminView(**vkwargs),
    }

    admin = Admin(app, **akwargs)
    admin.add_view(MyUserView(User, db.session))
    admin.add_view(MyRoleView(Role, db.session))
    admin.add_link(MainIndexLink(name="Main"))