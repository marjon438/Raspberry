from urllib import request
from requests import put, get, delete, post

base = "http://192.168.10.138:5000/todos/"

while True:
    print("1 get")
    print("2 post")
    print("3 delete")
    print("4 put")
    userinp = input("input: ")
    if userinp == "1":
        id = input("Id: ")
        answer = get(base, data= {"id":id})
    elif userinp == "2":
        inp = input("Name: ")
        answer = post(base, data= {"name":inp})
    elif userinp == "3":
        id = input("Id: ")
        answer = delete(base, data= {"id":id})
    elif userinp == "4":
        id = input("Id: ")
        inp = input("Name: ")
        answer = put(base, data= {"id":id,"name":inp})
    else:
        break
    print(answer.json())




