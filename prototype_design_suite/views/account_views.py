from pyramid.httpexceptions import HTTPNotFound, HTTPFound

from webhelpers.date import time_ago_in_words

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
@view_config(route_name='auth_route', match_param='action=out', renderer='login.jinja2')
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


@view_config(route_name='account_add_route', renderer='registration.jinja2', request_method='POST')
def account_add(request):
    #get the email
    email = request.POST.get('email')
    #make sure it isn't blank
    if email == '':
        return {"invalid_email": "Email cannot be blank"}
    else:
        #make sure the user doesn't already exist
        user = UserData.get_user(email)
        if user[0]:
            return {"invalid_email": "Email already in use"}
        else:

            #make sure nothing is blank
            if request.POST.get('name') == '':
                return {"invalid_name": "Name cannot be blank"}
            if request.POST.get('password') == '':
                return {"invalid_password": "Password cannot be blank"}
            if request.POST.get('confirm_password') == '':
                return {"invalid_password": "Password confirmation cannot be blank"}
            if request.POST.get('country') == 'none':
                return {"invalid_country": "Country cannot be none"}


            #check passwords
            if request.POST.get('password') != request.POST.get('confirm_password'):
                return {"invalid_password": "Passwords do not match"}
            else:
                #add the header info and start a session
                headers = remember(request, email)
                session = request.session
                session.invalidate()
                session['email'] = email

                #add the new user
                UserData.addAccount(email, request.POST.get('password'),request.POST.get('name'), request.POST.get('country'))
                return HTTPFound(location=request.route_url('dashboard_route'), headers=headers)



@view_config(route_name='profile_route', renderer='profile.jinja2', permission='loggedin')
def profile(request):
    session = request.session
    user = UserData.get_user(session['email'])
    if user[0]:
        print user[1].user_reg_date
        user_dict = {
            'email': user[1].user_email,
            'name': user[1].user_name,
            'reg_date': user[1].user_reg_date.ctime(),
            'last_log_in': time_ago_in_words(user[1].user_last_logged_on, granularity='minute'),
            'country': user[1].user_country
        }

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

