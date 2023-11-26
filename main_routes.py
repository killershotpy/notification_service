from flask import request, render_template, abort

import global_parameters as g
from api_responses import api_jr
from mongodb_module import EditNotify


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
