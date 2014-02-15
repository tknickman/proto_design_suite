from pyramid.httpexceptions import HTTPNotFound, HTTPFound

from pyramid.view import view_config
from pyramid.security import *

from prototype_design_suite.models.models import (
    UserData,
    )




#home
@view_config(route_name='home_route', renderer='coming_soon.jinja2')
def home(request):
    return HTTPFound(location=request.route_url('login_route'))

#account management
@view_config(route_name='registration_route', renderer='registration.jinja2')
def registration(request):
    return{}

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
            headers = remember(request, user.user_email)
            session = request.session
            session.invalidate()
            session['email'] = email
            return HTTPFound(location=request.route_url('dashboard_route'), headers=headers)
        else:
            headers = forget(request)
            return {"invalid": "login"}
    else:
        headers = forget(request)
        return HTTPFound(location=request.route_url('home_route'), headers=headers)


@view_config(route_name='account_add_route', renderer='profile.jinja2')
def account_add(request):
    #get the form from login
    user = UserData.get_user(request.params['email'])
    #make sure the user doesn't already exist
    if user[0]:
        return {"error": "Email already in use!"}
    else:
        headers = remember(request, request.params['email'])
        session = request.session
        session.invalidate()
        session['email'] = request.params['email']
        UserData.addAccount(request.params['email'], request.params['password'], request.params['name'])
        headers = remember(request, request.params['email'])
        return HTTPFound(location=request.route_url('dashboard_route'), headers=headers)



@view_config(route_name='profile_route', renderer='profile.jinja2', permission='loggedin')
def profile(request):
    session = request.session
    user = UserData.get_user(session['email'])
    if user[0]:
        user_dict = {'email': user[1].user_email, 'name': user[1].user_name}
        profile_name = user[1].user_name
        return {'user_dict': user_dict, 'profile_name': profile_name}
    else:
        return {}

@view_config(route_name='dashboard_route', renderer='dashboard.jinja2', permission='loggedin')
def dashboard(request):
    session = request.session
    user = UserData.get_user(session['email'])
    if user[0]:
        profile_name = user[1].user_name
        return {'profile_name': profile_name}
    else:
        return {}

