from flask  import jsonify

class HttpErrorCode(object):
    SUCCESS = 200
    ERROR = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FUND = 404
    AUTHORIZED_ERROR = 420
    PARAMS_VALID_ERROR = 421


ERROR_DICT = {
    HttpErrorCode.SUCCESS: 'SUCCESS!',
    HttpErrorCode.UNAUTHORIZED: 'Unauthorized!',
    HttpErrorCode.PARAMS_VALID_ERROR: 'Params validation error!',
    HttpErrorCode.FORBIDDEN: 'No permission!',
    HttpErrorCode.NOT_FUND: 'Not found!',
    HttpErrorCode.AUTHORIZED_ERROR: 'Password is valid!',
}


def response(code, message=None, data={}):
    response_content = {'code': code, 'data': data}
    response_content['message'] = message if message else ERROR_DICT.get(code, 'Unknown error code!')
    return response_content


def response_json(code, msg=None, data={}):
    return jsonify(response(code, msg, data))
