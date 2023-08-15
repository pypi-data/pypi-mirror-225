import json
import os
import os.path
import urllib
import urllib.parse
import imandra.auth


def decompose(auth, file, testgen_lang, organization, callback, doc_gen, parent_job_id):
    auth.login()
    path = "api/ipl/jobs"

    params_dict = { "lang": "ipl" }
    if parent_job_id is not None:
        params_dict["parent-job-id"] = parent_job_id

    if file is not None:
        filename = os.path.basename(file)
        params_dict["filename"] = filename
        with open(file, 'r') as ipl_file:
            content = ipl_file.read()
        data = content.encode("utf-8")
    else:
        data = b''

    if testgen_lang is not None:
        params_dict["testgen-lang"] = testgen_lang

    if doc_gen is not None:
        params_dict["doc-gen"] = doc_gen

    if organization is not None:
        params_dict["organization-id"] = organization

    if callback is not None:
        params_dict["callback"] = callback

    params = urllib.parse.urlencode (params_dict)
    url = "{}/{}?{}".format(auth.imandra_web_host, path, params)
    headers = { "X-Auth" : auth.token }
    request = urllib.request.Request(url, data, headers=headers)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))

    print("{}/ipl/jobs/{}".format(auth.imandra_web_host, response.read().decode("utf-8")))

def status(auth, job_id):
    auth.login()
    path = "api/ipl/jobs/{}/status".format(job_id)
    url = "{}/{}".format(auth.imandra_web_host, path)
    headers = { "X-Auth" : auth.token }

    request = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))

    print(response.read().decode("utf-8"))


def data(auth, job_id):
    auth.login()
    path = "api/ipl/jobs/{}/data".format(job_id)
    url = "{}/{}".format(auth.imandra_web_host, path)
    headers = { "X-Auth" : auth.token }

    request = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(request)
        content = response.read()
    except urllib.error.HTTPError as e:
        if e.code == 302:
            content = e.read()
        else:
            raise ValueError(e.read().decode("utf-8"))

    filename = "{}.tar.gz".format(job_id)

    with open(filename, 'wb') as data_file:
        data_file.write(content)

    print(filename)

def simulator(auth, file):
    auth.login()
    path = "simulator/create"
    with open(file, 'r') as ipl_file:
        content = ipl_file.read()
    url = "{}/{}".format(auth.imandra_web_host, path)

    req = \
          { "payload" : content,
            "cluster" : auth.zone,
            "version" : "latest" }

    data = json.dumps(req)
    clen = len(data)
    data = data.encode("utf-8")
    headers = { "X-Auth" : auth.token, 'Content-Type': 'application/json', 'Content-Length': clen}

    request = urllib.request.Request(url, data, headers=headers)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))

    resp = json.loads(response.read())

    urls = dict(resp['new_pod']['urls'])

    print("Simulator available at: {}/".format(urls['http']))

def list_jobs(auth):
    auth.login()
    path = 'api/ipl/jobs?limit=10'
    url = "{}/{}".format(auth.imandra_web_host, path)
    headers = { "X-Auth": auth.token }

    request = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))

    resp = json.loads(response.read())

    if len(resp['jobs']) == 0:
        print("No jobs submitted yet.")
    else:

        colsfmt = "{:<36} {:<16} {:<20} {:<30} {:<30} {:<30}"
        print(colsfmt.format("ID", "Status", "Filename", "Submitted", "Started", "Ended"))
        for job in resp['jobs']:
            endTime = "-"
            if job['status'] == 'cancelled':
                endTime = job['cancelledAt']
            elif job['status'] == 'done':
                endTime = job['completedAt']
            elif job['status'] == 'error':
                endTime = job['failedAt']

            filename = job['iplFile']['filename']
            if len(filename) > 20:
                filename = filename[:17] + "..."

            print(colsfmt.format(job['id'], job['status'], filename, job['queuedAt'], job['startedAt'], endTime))

def cancel(auth, job_id):
    auth.login()
    path = "api/ipl/jobs/{}/cancel".format(job_id)
    url = "{}/{}".format(auth.imandra_web_host, path)
    headers = { "X-Auth" : auth.token }

    request = urllib.request.Request(url, headers=headers, method='POST', data=None)

    try:
        response = urllib.request.urlopen(request)
        content = response.read()
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))

    print("Cancel requested for job: {}".format(job_id))
