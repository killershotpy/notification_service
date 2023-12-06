import json

from werkzeug.wrappers.response import Response

from global_parameters import KV as KV


def api_jr(data=b'',
           status: int = 200,
           cache: list = None):
    """Create standard json response

    :param data: object that can be serialized or [str]
    :param status: status code response
    :param cache: directive caching on frontend current request [index[0-3], int]
    :return: application/json response
    """
    response = Response(response=json.dumps(data, ensure_ascii=False) if isinstance(data, (dict, list, bool)) else data,
                        status=204 if isinstance(data, bytes) else status,
                        mimetype='application/json',
                        headers={'Accept': 'application/json'})
    if KV.frontend_cache_control not in response.headers and not cache:
        response.headers[KV.frontend_cache_control] = 'no-cache, max-age=0'
    else:
        try:
            response.headers.update({KV.frontend_cache_control: f'{KV.frontend_cache_control_types[cache[0]]}, max-age={cache[1]}'})
        except (TypeError, IndexError) as exception:
            raise exception
    return response
