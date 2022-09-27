from urllib import request
from requests import put, get

base = "http://192.168.10.140:5000/"

answer = get(base+"helloworld")
print(answer.json())