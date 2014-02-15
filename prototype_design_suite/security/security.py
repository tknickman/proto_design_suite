from pyramid.security import Allow, Everyone, Authenticated


class LoggedInFactory(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, Authenticated, 'loggedin')]

    def __init__(self, request):
        pass