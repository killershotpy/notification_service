import error_pages as e
import main_routes as m
from global_parameters import RulesRoutes as Rule


routes = {Rule.create_notify: {'f': m.create_notify, 'm': ['POST'], 'p': False},
          Rule.delete_notify: {'f': m.delete_notify, 'm': ['POST'], 'p': False},
          Rule.update_notify: {'f': m.update_notify, 'm': ['POST'], 'p': False},
          Rule.get_one_notify: {'f': m.get_one_notify, 'm': ['GET'], 'p': False},
          Rule.get_all_notify: {'f': m.get_all_notify, 'm': ['GET'], 'p': False}}

errors = {500: e.c_500,
          502: e.c_502,
          503: e.c_503,
          504: e.c_504}
