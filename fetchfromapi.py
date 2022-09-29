from requests import put, get, delete, post

base = "http://192.168.10.139:5000/Todos/"

while True:
    print("1 get")
    print("2 post")
    print("3 delete")
    print("4 put")
    userinp = input("input: ")
    if userinp == "1":
        id = input("Id: ")
        answer = get(base)
    elif userinp == "2":
        inp = input("Title: ")
        answer = post(base, data= {"title":inp})
    elif userinp == "3":
        id = input("Id: ")
        answer = delete(base, data= {"id":id})
    elif userinp == "4":
        id = input("Id: ")
        inp = input("Title: ")
        answer = put(base, data= {"id":id,"title":inp})
    else:
        break
    print(answer.json())




