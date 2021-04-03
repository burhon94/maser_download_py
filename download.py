import os
import requests

from randomstr import randomstr


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
    if not os.path.exists('tmp_dir'):
        os.mkdir('tmp_dir', mode=0o777)
    session = requests.Session()
    s_header = {'range': 'bytes=' + str(start) + ' - ' + str(end)}
    session.headers.update(s_header)
    response = session.get(url, headers=session.headers)
    if response.status_code > 299:
        resp = {
            'index': i,
            'code': response.status_code
        }
        return resp
    else:
        b = response.content
        f = open('tmp_dir/tempFile_{}-{}.tmp'.format(file_name[:-4], str(i)), "wb")
        f.write(b)
        f.close()
        response.close()
        session.close()


def do_download(file_name, url, sections):
    resp = {}
    for i in range(0, len(sections)):
        resp = task(file_name, url, i, sections[i][0], sections[i][1])

    return resp


def download(file_name, url, sections):
    if str(file_name).strip() == '':
        file_name = randomstr(length=10, charset='alphanumeric', readable=False, capitalization=False)
        split = str.split(url, ".")
        file_format = split[len(split) - 1]
        file_name = file_name + "." + file_format
        resp = do_download(file_name, url, sections)
        if resp is not None:
            resp = {'code': 500}
            return resp

        else:
            resp = {'code': 200, 'file_name': file_name}
        return resp

    else:
        file_format = url[-4:]
        file_name = file_name + file_format
        resp = do_download(file_name, url, sections)
        if resp is not None:
            resp = {'code': 500}
            return resp

        else:
            resp = {'code': 200, 'file_name': file_name}
        return resp


def merge(file_name):
    found_files = []
    files = os.listdir('tmp_dir')

    for index in range(0, len(files)):
        file_part = files[index]
        f = str(file_name[:-4])
        if str.find(file_part, f) != -1:
            found_files.append(file_part)
            continue
        else:
            continue

    found_files.sort()
    full_file = open(file_name, 'wb')
    for index in range(0, len(found_files)):
        file_part = found_files[index]
        f_n = str('tmp_dir/{}').format(str(file_part))
        read_file = open(f_n, 'rb')
        while byte := read_file.read(1):
            full_file.write(byte)

        read_file.close()
        os.remove(f_n)

    full_file.close()
    remove_tmp_dir()
    return found_files


def remove_tmp_dir():
    files = os.listdir('tmp_dir')

    if len(files) == 0:
        os.rmdir('tmp_dir')
