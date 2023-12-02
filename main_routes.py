from flask import request, session
from json.decoder import JSONDecodeError

import global_parameters as g
from api_responses import api_jr
from mongodb_module import EditNotify, GetNotify


def create_notify():
    if request.method == 'GET':
        return api_jr('Method denied', 405)
    if request.method == 'POST':
        if request.host_url == g.KV.host_app:
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


def delete_notify(uuid: str = None):
    if request.method == 'GET':
        return api_jr('Method denied', 405)
    if request.method == 'POST':
        if request.host_url == g.KV.host_app:
            try:
                EditNotify.delete(uuid)
                return api_jr()
            except TypeError:
                return api_jr('Incorrect request body', 422)
        else:
            return api_jr('Access denied', 403)
    else:
        return api_jr('Method denied', 405)


def update_notify(uuid: str = None):
    if request.method == 'GET':
        return api_jr('Method denied', 405)
    if request.method == 'POST':
        if request.host_url == g.KV.host_app:
            try:
                EditNotify.update(uuid, {g.KV.data: {**request.json}})
                return api_jr()
            except TypeError:
                return api_jr('Incorrect request body', 422)
        else:
            return api_jr('Access denied', 403)
    else:
        return api_jr('Method denied', 405)


def get_one_notify(uuid: str = None):
    if request.method == 'GET':
        try:
            try:
                return api_jr(GetNotify.get_one(uuid, token_cookie=session[g.KV.token]))
            except StopIteration:
                return api_jr('Not found', 404)
        except TypeError:
            return api_jr('Incorrect request body', 422)
    if request.method == 'POST':
        return api_jr('Method denied', 405)
    else:
        return api_jr('Method denied', 405)


def get_all_notify():
    if request.method == 'GET':
        try:
            try:
                return api_jr(GetNotify.get_all(token_cookie=session[g.KV.token], **request.args))
            except StopIteration:
                return api_jr('Not found', 404)
        except (TypeError, JSONDecodeError):
            return api_jr('Incorrect request body', 422)
    if request.method == 'POST':
        return api_jr('Method denied', 405)
    else:
        return api_jr('Method denied', 405)
