import error_pages as e
import main_routes as m
from global_parameters import RulesRoutes as Rule


routes = {Rule.main: {'f': m.main, 'm': ['GET'], 'p': False}}

errors = {400: e.c_400,
          401: e.c_401,
          403: e.c_403,
          404: e.c_404,
          405: e.c_405,
          422: e.c_422,
          500: e.c_500,
          502: e.c_502,
          503: e.c_503,
          504: e.c_504}
