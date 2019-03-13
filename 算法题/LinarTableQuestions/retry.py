def retry(times=3):
    def wrapper(func):
        def new_func(*args, **kwargs):
            count = times
            while count:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    result = {'code': 3, 'message': e.message, 'result': ''}
                finally:
                    count -= 1
            return result
        return new_func
    return wrapper
