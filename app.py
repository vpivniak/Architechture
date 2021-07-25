# uwsgi --http :8083 --wsgi-file app.py
VISITS = 1
query = []


def get_handler():
    with open('index.html', 'rb') as f:
        return f.read()


def get_input_form():
    return get_handler()


def get_first_last_name(env_dict):
    with open('table.html', 'r') as f:
        html_table = f.read()

    if env_dict.get('QUERY_STRING') == '':
        if len(query) == 0:
            return b'No any username in table'
        query.sort()
        return ''.join(query).encode()
    else:
        names = env_dict.get('QUERY_STRING').split('&')
        first_name = names[0].split('=')[1]
        last_name = names[1].split('=')[1]
        query.append(html_table.format(first_name.lower(), last_name.lower(), VISITS))
        query.sort()
        return ''.join(query).encode()


def data_from_post(env_dict):
    with open('table.html', 'r') as f:
        html_table = f.read()

    raw_names = env_dict.get('wsgi.input').read(int(env_dict.get('CONTENT_LENGTH')))
    names = raw_names.decode().split('&')
    first_name = names[0].split('=')[1]
    last_name = names[1].split('=')[1]

    query.append(html_table.format(first_name.lower(), last_name.lower(), VISITS))
    query.sort()
    return ''.join(query).encode()


def application(env, start_response):
    global VISITS

    variables = {}
    for k, v in env.items():
        variables[k] = v
    print(variables)
    if variables.get('REQUEST_METHOD') == 'GET' and variables.get('PATH_INFO') == '/':
        VISITS += 1
        status = 'HTTP/1.1 200 OK'
        headers = [('Set-Cookie', f'page_visits={VISITS}'),
                   ('Connection', 'close'),
                   ('Content-type', 'text/html; charset=utf-8\n\n')]
        start_response(status, headers)
        return get_handler()
    elif variables.get('REQUEST_METHOD') == 'GET' and variables.get('PATH_INFO') == '/python/':
        VISITS += 1
        status = 'HTTP/1.1 200 OK'
        headers = [('Set-Cookie', f'page_visits={VISITS}'),
                   ('Connection', 'close'),
                   ('Content-type', 'text/html; charset=utf-8\n\n')]

        start_response(status, headers)
        return get_first_last_name(variables)
    elif variables.get('REQUEST_METHOD') == 'POST' and variables.get('PATH_INFO') == '/python/':
        VISITS += 1
        status = 'HTTP/1.1 200 OK'
        headers = [('Set-Cookie', f'page_visits={VISITS}'),
                   ('Connection', 'close'),
                   ('Content-type', 'text/html; charset=utf-8\n\n')]

        start_response(status, headers)
        return data_from_post(variables)
    else:
        status = 'HTTP/1.1 404 Not Found'
        headers = [('Connection', 'close'),
                   ('Content-type', 'Not Found\n\n')]

        start_response(status, headers)
        return b'Unreachable route'
