from flask import request, session

import global_parameters as g
from api_responses import api_jr
from mongodb_module import EditNotify, GetNotify


def create_notify():
    if request.method == 'GET':
        return api_jr('Method denied', 405)
    if request.method == 'POST':
        if request.host_url == g.KV.host_url:
            try:
                notify = g.DB.create_notify(**request.json)
                if notify:
                    EditNotify.create(notify)
                    return api_jr(notify)
                else:
                    return api_jr('Incorrect request body', 422)
            except TypeError:
                return api_jr('Incorrect request body', 422)
        else:
            return api_jr('Access denied', 403)
    else:
        return api_jr('Method denied', 405)


def delete_notify():
    if request.method == 'GET':
        return api_jr('Method denied', 405)
    if request.method == 'POST':
        if request.host_url == g.KV.host_url:
            try:
                EditNotify.delete(**request.json)
                return api_jr()
            except TypeError:
                return api_jr('Incorrect request body', 422)
        else:
            return api_jr('Access denied', 403)
    else:
        return api_jr('Method denied', 405)


def update_notify():
    if request.method == 'GET':
        return api_jr('Method denied', 405)
    if request.method == 'POST':
        if request.host_url == g.KV.host_url:
            try:
                update = g.DB.update_notify(**request.json)
                if update:
                    EditNotify.update(update[g.KV.uuid], update[g.KV.data])
                    return api_jr()
                else:
                    return api_jr('Incorrect request body', 422)
            except TypeError:
                return api_jr('Incorrect request body', 422)
        else:
            return api_jr('Access denied', 403)
    else:
        return api_jr('Method denied', 405)


def get_one_notify(*args, **kwargs):
    if request.method == 'GET':
        if ...:
            query = ...
            if query:
                return ...
            else:
                return api_jr('Incorrect url-address', 404)
        else:
            return api_jr('Incorrect url-address', 404)
    if request.method == 'POST':
        return api_jr('Method denied', 405)
    else:
        return api_jr('Method denied', 405)


def get_all_notify(*args, **kwargs):
    if request.method == 'GET':
        if ...:
            query = ...
            if query:
                return ...
            else:
                return api_jr('Incorrect url-address', 404)
        else:
            return api_jr('Incorrect url-address', 404)
    if request.method == 'POST':
        return api_jr('Method denied', 405)
    else:
        return api_jr('Method denied', 405)
