# from pyramid.config import Configurator
# from sqlalchemy import engine_from_config
#
# from app.database import init_sql
#
# def main(global_config, **settings):
#     """ This function returns a Pyramid WSGI application.
#     """
#     config = Configurator(settings=settings)
#     config.scan('app.model') # the "important" line
#     engine = engine_from_config(settings, 'sqlalchemy.')
#     init_sql(engine)
#
#     return config.make_wsgi_app()