from pyramid.httpexceptions import HTTPNotFound, HTTPFound

from pyramid.view import view_config
from pyramid.security import *

from prototype_design_suite.models.models import (
    UserData,
    )


#home
@view_config(route_name='home_route', renderer='coming_soon.jinja2')
def home(request):
    return {}

#account management
@view_config(route_name='registration_route', renderer='registration.jinja2')
def registration(request):
    return {}

#account management
@view_config(route_name='login_route', renderer='login.jinja2')
def login(request):
    return {}


@view_config(route_name='auth_route', match_param='action=in', renderer='login.jinja2', request_method='POST')
@view_config(route_name='auth_route', match_param='action=out', renderer='coming_soon.jinja2')
def sign_in_out(request):
    email = request.POST.get('email')
    if email:
        user = UserData.by_email(email)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.email)
            session = request.session
            session.invalidate()
            session['username'] = email
            return HTTPFound(location=request.route_url('startRoute'), headers=headers)
        else:
            headers = forget(request)
            return {"error": "Invalid email and password!"}
    else:
        headers = forget(request)
        return HTTPFound(location=request.route_url('home_route'), headers=headers)

@view_config(route_name='account_add_route', renderer='registration.jinja2')
def account_add(request):
    #get the form from login
    user = UserData.get_user(request.params['email'])
    #make sure the user doesn't already exist
    if user[0]:
        return {"error": "Email already in use!"}
    else:
        session = request.session
        session.invalidate()
        session['email'] = request.params['email']
        UserData.addAccount(request.params['email'], request.params['password'], request.params['name'])
        headers = remember(request, request.params['email'])
        return HTTPFound(location=request.route_url('home_route'), headers=headers)






