from api_responses import api_jr


def c_504(error):
    return api_jr({'504': 'Response timeout'}, 504)


def c_503(error):
    return api_jr({'503': 'Server is dead ...'}, 503)


def c_502(error):
    return api_jr({'502': 'Upgrade server\'s'}, 502)


def c_500(error):
    return api_jr({'500': 'Server error'}, 500)


def c_401(error):
    return api_jr({'401': 'Need auth'}, 401)


def c_400(error):
    return api_jr({'400': 'Bad request'}, 400)
