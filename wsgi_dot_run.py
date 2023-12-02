from flask import Flask, session, request

import global_parameters as g
from mongodb_module import CreateUser
from routs import routes as r, errors as e
from time_module import get_any_days as days
from encryptor import load_app_key

# #############################################################################################################
# initialization main application
app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 's'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = 'True'
app.config['SESSION_REFRESH_EACH_REQUEST'] = False
app.config['SECRET_KEY'] = load_app_key()
app.config['JSON_AS_ASCII'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = days(7300)

# ##########################################################___REGISTERED_ERRORS___#################################################
[app.register_error_handler(code, func) for code, func in e.items()]

# ##########################################################___REGISTERED_ROUTES___#################################################
[app.add_url_rule(rule, methods=param.get('m'), view_func=param.get('f'), provide_automatic_options=param.get('p', None)) for rule, param in r.items()]


@app.before_request
def open_session():
    if g.KV.token not in session and request.host_url != g.KV.host_app:
        if g.DB.token_users_my is False:
            session[g.KV.token] = g.DB.create_token_cookie()
        else:
            result = {}
            exec(g.DB.token_users_my.replace('{{}}', request.args.get('identificator')), None, result)
            session[g.KV.token] = result['t']()
            del result
        session.modified, session.permanent = True, True
        CreateUser.first_request(session[g.KV.token])
    else:
        pass


if __name__ == "__main__":
    app.run(host=g.config.get('host_app', '127.0.0.1'), port=g.config.get('port_app', None))
