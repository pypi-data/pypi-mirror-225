def while_try(function, *arguments, error_type: type = Exception):
    while True:
        try:
            return function(*arguments)
        except Exception as e:
            pass
