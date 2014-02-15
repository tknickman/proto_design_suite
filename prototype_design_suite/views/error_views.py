from pyramid.view import forbidden_view_config, notfound_view_config, view_config

#error
@view_config(route_name='errorRoute', renderer='error.jinja2')
def error(request):
    return {'code': "lol"}

#access forbidden
@forbidden_view_config(renderer='error.jinja2')
def access_forbidden(request):
    request.response.status = 403
    return {'code': "403", 'text': "Access Denied"}

#not found
@notfound_view_config(renderer='error.jinja2')
def not_found(request):
    request.response.status = 404
    return {'code': "404", 'text': "Page Not Found"}