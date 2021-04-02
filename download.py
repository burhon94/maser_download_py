from randomstr import randomstr
import requests


def add_queue(url):
    total_sections = 10
    response = requests.head(url)
    a = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

    if response.status_code > 299:
        resp = {
            'code': response.status_code,
            'payload': '',
            'error': 'response status code'
        }
        return resp
    else:
        size = response.headers["Content-Length"]
        each_size = int(int(size) / total_sections)

        for i in range(0, len(a)):
            if i == 0:
                a[i][0] = 0
            else:
                a[i][0] = a[i - 1][1] + 1

            if i < 10 - 1:
                a[i][1] = a[i][0] + each_size
            else:
                a[i][1] = int(size) - 1

        resp = {
            'code': 200,
            'payload': a,
            'error': ''
        }
        return resp


def task(file_name, url, i, start, end):
    session = requests.Session()
    s_header = {'range': 'bytes=' + str(start) + ' - ' + str(end)}
    session.headers.update(s_header)
    response = session.get(url, headers=session.headers)
    if response.status_code > 299:
        a = ("Error: index: " + str(i) + " code: " + str(response.status_code))
        return a
    else:
        b = response.content
        f = open('tmp_dir/tempFile_{}-{}.tmp'.format(file_name[:-4], str(i)), "w")
        f.write(str(b))
        f.close()
        response.close()
        session.close()


def download(file_name, url, sections):
    if str(file_name).strip() == '':
        file_name = randomstr(length=10, charset='alphanumeric', readable=False, capitalization=False)
        split = str.split(url, ".")
        file_format = split[len(split)-1]
        file_name = file_name + "." + file_format

    file_format = url[-4:]
    file_name = file_name + file_format

    for i in range(0, len(sections)):
        a = task(file_name, url, i, sections[i][0], sections[i][1])
        if a is not None:
            return a

    return 200
