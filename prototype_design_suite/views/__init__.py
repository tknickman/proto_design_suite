def includeme(config):

    add_route = config.add_route

    ############################
    ####| account_views.py |####
    ############################
    add_route('home_route', '/')
    add_route('login_route', '/login')
    add_route('registration_route', '/registration')
    add_route('auth_route', '/sign/{action}')
    add_route('account_add_route', '/add_account')


    ###############################
    #######| error_views.py |######
    ###############################
    add_route('errorRoute', '/error')



    config.scan()