from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from prototype_design_suite.models.models import (
    DBSession,
    Base,
)

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import LoggedInFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    session_factory = UnencryptedCookieSessionFactoryConfig('itsasecret')

    authentication_policy = AuthTktAuthenticationPolicy('itsalsoasecret')
    authorization_policy = ACLAuthorizationPolicy()


    config = Configurator(
        settings=settings,
        session_factory=session_factory,
        authentication_policy=authentication_policy,
        authorization_policy=authorization_policy
    )

    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('prototype_design_suite:views/templates/')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.include('.views')



    return config.make_wsgi_app()
