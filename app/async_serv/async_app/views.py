import json
import time
import random
import requests
from concurrent import futures
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


executor = futures.ThreadPoolExecutor(max_workers=1)
global cnt
cnt = 0
ServerToken = "qwerty"
url = "http://127.0.0.1:8080/api/assemblies/user-form-finish"


def get_random_status():
    if random.random() < 0.5:
        return "Переговоры успешны"
    else:
        return "Переговоры не успешны"


def modify_body(req_body):
    time.sleep(5)
    req_body['status'] = get_random_status()
    return req_body

def status_callback(task):
    try:
      result = task.result()
      print(result)
    except futures._base.CancelledError:
      return
    requests.put(url, data=json.dumps(result), timeout=3)

@api_view(['Put'])
def addRequest(request):
    req_body = json.loads(request.body)

    if req_body["Server_Token"] == ServerToken:
        task = executor.submit(modify_body, req_body)
        task.add_done_callback(status_callback)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


