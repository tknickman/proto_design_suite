from pyramid.view import forbidden_view_config, notfound_view_config, view_config

#error
@view_config(route_name='errorRoute', renderer='error.jinja2')
def error(request):
    return {'error': "Something went wrong, please try again!"}

#access forbidden
@forbidden_view_config(renderer='error.jinja2')
def access_forbidden(request):
    request.response.status = 403
    return {'error': "You do not have access to this page!"}

#not found
@notfound_view_config(renderer='error.jinja2')
def not_found(request):
    request.response.status = 404
    return {'error': "This page doesn't exist!"}