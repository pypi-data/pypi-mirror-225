import urllib
import urllib.parse
import json

def list (auth):
    auth.login()
    url = "{}/{}".format(auth.imandra_web_host, "api/instances/list")
    headers = { "X-Auth" : auth.token }

    request = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))

    instances = json.loads(response.read())

    print ("Instances: \n")
    for i in instances:
        print (" [{}] [{}] {}".format(i["assigned_at"], i["pod_type"], i["pod_id"]))

    return instances

def delete (auth, instance_id):
    auth.login()
    url = "{}/{}/{}".format(auth.imandra_web_host, "api/instances/delete", instance_id)
    headers = { "X-Auth" : auth.token }

    data = {}
    request = urllib.request.Request(url, data, headers=headers)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))

    print("Instance killed")


def create (auth, version, instance_type):
    auth.login()
    auth.ensure_zone()
    url = "{}/{}".format(auth.imandra_web_host, "api/instances")
    headers = { "X-Auth" : auth.token, 'Content-Type': 'application/json' }

    req = {}
    req['cluster'] = auth.zone
    req['instance_type'] = instance_type
    if version:
        req['version'] = version


    data = json.dumps(req).encode("utf-8")

    request = urllib.request.Request(url, data, headers=headers)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        raise ValueError(e.read().decode("utf-8"))

    s = response.read()
    instance_response = json.loads(s)

    print("Instance created:")
    print("- url: {}".format(instance_response['new_pod']['url']))
    print("- token: {}".format(instance_response['new_pod']['exchange_token']))
    return instance_response