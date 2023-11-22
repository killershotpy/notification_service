from flask import request, render_template, abort, session

import global_parameters as g
from api_responses import api_jr
from mongodb_module import FirstClass


class Auth:
    @staticmethod
    def auth(lvl_acs: list = None):
        """Check level access current token auth (auth session).

        :param lvl_acs: list inside tuples [(level, role), ..., (level, role)] access for this function
        :return: call decorate function
        """
        def check_lvl(f):
            def check_acs(*args, **kwargs):
                if request.referrer:
                    if any(ref in request.referrer for ref in g.PathNames.list_current_domains) is True:
                        old_token = TokenAuth.get(**session)
                        return f(*args, **{k: old_token.get(k) for k in f.__code__.co_varnames if k in old_token}, **kwargs)
                    else:
                        return abort(401)
                else:
                    return abort(403)
            check_acs.__name__ = f.__name__  # костыль для переименования функций при инициализации приложения, что бы декоратор не пытался перезаписать сам себя
            return check_acs
        return check_lvl


def main():
    return render_template(g.PagesNames.default_page)


def first_route(*args, **kwargs):
    if request.method == 'GET':
        if ...:
            query = ...
            if query:
                return ...
            else:
                return abort(404)
        else:
            return abort(404)
    if request.method == 'POST':
        return abort(405)
    else:
        return abort(405)
