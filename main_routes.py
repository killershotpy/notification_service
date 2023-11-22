from flask import request, render_template, abort, session

import global_parameters as g
# from api_responses import api_jr
from mongodb_module import TokenAuth
from captcha import Captcha
# from send_email_for_users import SendEmail


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
    return render_template(g.PagesNames.main_users)


def main_og(robots: str = None, lang: str = None, uuid: str = None):
    if request.method == 'GET':
        if uuid and lang:
            query = g.DB.agr_form_get_publication(lang, uuid)
            if query:
                return render_template(g.PagesNames.main_users)
            else:
                return abort(404)
        else:
            return abort(404)
    if request.method == 'POST':
        return abort(405)
    else:
        return abort(405)


def api_get_captcha():  # private API for generate & add in data base captcha
    if request.method == 'GET':
        if request.referrer:
            if any(ref in request.referrer for ref in g.PathNames.list_current_domains) is True:
                if request.args:
                    return Captcha.create(**request.args)
                else:
                    return abort(422)
            else:
                return abort(403)
        else:
            return abort(403)
    if request.method == 'POST':
        return abort(405)
    else:
        return abort(405)
