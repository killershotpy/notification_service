from flask import Flask
from flask_cors import CORS

from routs import routes as r, errors as e
from time_module import get_any_days as days
from encryptor import load_app_key

# #############################################################################################################
# initialization main application
app = Flask(__name__)
cors = CORS(app)

app.config['SESSION_COOKIE_NAME'] = 's'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = 'True'
app.config['SESSION_REFRESH_EACH_REQUEST'] = False
app.config['SECRET_KEY'] = load_app_key()
app.config['JSON_AS_ASCII'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = days(365)


# ##########################################################___REGISTERED_ERRORS___#################################################
[app.register_error_handler(code, func) for code, func in e.items()]

# ##########################################################___REGISTERED_ROUTES___#################################################
[app.add_url_rule(rule, methods=param.get('m'), view_func=param.get('f')) for rule, param in r.items()]

# ##########################################################___REGISTERED_AFTER_REQUEST___#################################################
# app.after_request(after_requests)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
