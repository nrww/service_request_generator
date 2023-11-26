import random
import requests


femaleFirstNameList = []
maleFirstNameList = []
lastNameList = []
servicesList = []

usersDict = {}
servicesDict = {}
ordersDict = {}
messagesDict = {}


with open('data/female_first_names.txt','r') as f:
    femaleFirstNameList.extend(f.read().splitlines())
with open('data/male_first_names.txt','r') as f:
    maleFirstNameList.extend(f.read().splitlines())
with open('data/last_names.txt','r') as f:
    lastNameList.extend(f.read().splitlines())
with open('data/services.txt','r') as f:
    servicesList.extend(f.read().splitlines())
    
    
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
  
    
def gen_phone():
    first = str(random.randint(100, 999))
    second = str(random.randint(1, 888)).zfill(3)

    last = (str(random.randint(1, 9998)).zfill(4))
    while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
        last = (str(random.randint(1, 9998)).zfill(4))

    return '{}-{}-{}'.format(first, second, last)


def generateUsers(n):
    print(f'Добавление {n} пользователей')
    printProgressBar(0, n, prefix = 'Progress:', suffix = 'Complete', length = 50)
    url = "http://127.0.0.1:8081/user" 
    
    for _ in range(n):
        firstName = random.choice(maleFirstNameList)
        lastName = random.choice(lastNameList)
        data1 = {"first_name": firstName,
                "last_name":lastName,
                "email": lastName +'@gmail.com',
                'phone': gen_phone(),
                "login": firstName + '_' + lastName ,
                'password': lastName + str(random.randint(1, 9998))}
        response = requests.post(url, params=data1)
        if 'inserted_id' in response.text:
            printProgressBar(_ + 1, n, prefix = 'Progress:', suffix = 'Complete', length = 50)
            usersDict[response.json()['inserted_id']] = data1
        else:  
            print(response.text)


def generateServices(n):
    print(f'Добавление {n} сервисов')
    printProgressBar(0, n, prefix = 'Progress:', suffix = 'Complete', length = 50)
    url = "http://127.0.0.1:8082/service" 
    
    for _ in range(n):
        serviceName = random.choice(servicesList)
        data1 = {"name": serviceName,
                "type": serviceName,
                "desc": 'Красочное описание услуги',
                'price': random.randint(0,100000),
                "author_id": random.choice(list(usersDict.keys()))
                }
        response = requests.post(url, params=data1)
        if 'inserted_id' in response.text:
            printProgressBar(_ + 1, n, prefix = 'Progress:', suffix = 'Complete', length = 50)
            servicesDict[response.json()['inserted_id']] = data1
        else:  
            print(response.text)
            
            
def generateOrders(n):
    print(f'Добавление {n} заказов')
    printProgressBar(0, n, prefix = 'Progress:', suffix = 'Complete', length = 50)
    url = "http://127.0.0.1:8083/order" 
    status_list = ['Создан', 'Завершен', 'В работе', 'На обсуждении', 'Закрыт']
    
    for _ in range(n):
        status = random.choice(status_list)
        
        data1 = {"client_id": random.choice(list(usersDict.keys())),
                "service_id": random.choice(list(servicesDict.keys())),
                "status": status,
                "content": 'очень важная информация по заказу'
                }

        response = requests.post(url, params=data1)
        if 'inserted_id' in response.text:
            printProgressBar(_ + 1, n, prefix = 'Progress:', suffix = 'Complete', length = 50)
            ordersDict[response.json()['inserted_id']] = data1
        else:  
            print(response.text)
            
            
def generateMessage(n):
    
    print(f'Добавление {n*10} сообщений')
    printProgressBar(0, n*10, prefix = 'Progress:', suffix = 'Complete', length = 50)
    
    url = "http://127.0.0.1:8084/message" 
    text_list = ['Привет', 'Спасибо', 'Ну как там с заказом', 'До свидания', 'Все отлично!']
    
    for _ in range(n):
        
        order_id = random.choice(list(ordersDict.keys()))
        sender_list = [ordersDict[order_id]['client_id'], servicesDict[ordersDict[order_id]['service_id']]["author_id"]]
        for __ in range(10):
            
            data1 = {"order_id": order_id,
                    "sender_id": random.choice(sender_list),
                    "text": random.choice(text_list),
                    }
            response = requests.post(url, params=data1)
            if 'inserted_id' in response.text:
                printProgressBar(_*10 + __+1 , n*10, prefix = 'Progress:', suffix = 'Complete', length = 50)
                messagesDict[response.json()['inserted_id']] = data1
            else:  
                print(response.text)
    
    
def check_user():
    
    url = 'http://localhost:8081/user'
    for key, value in usersDict.items():
        params = {'id': key}
        response = requests.get(url, params=params)
        for k, i in response.json().items():
            if k != 'user_id' and k != 'password':
                if not value[k] == i:
                    print(response.json())
                    print(value)
                    return False
    return True

def check_services():
    
    url = 'http://localhost:8082/service'
    for key, value in servicesDict.items():
        params = {'id': key}
        response = requests.get(url, params=params)
        for k, i in response.json().items():
            if k != 'id' and k!= 'date':
                if not value[k] == i:
                    if k == 'price':
                        if  float(value[k]) != float(i):
                            return False
                        else: 
                            continue
                    print(response.json())
                    print(value)
                    print(k)
                    return False
    return True

def check_orders():
    
    url = 'http://localhost:8083/order'
    for key, value in ordersDict.items():
        params = {'id': key}
        response = requests.get(url, params=params)
        for k, i in response.json().items():
            if k != 'id' and k!= 'date':
                if not value[k] == i:
                    print(response.json())
                    print(value)
                    print(k)
                    return False
    return True
    
    

if __name__ == "__main__":
    
    nRows = int(input('Введите кол-во добавляемых записей: '))
    
    generateUsers(nRows)
    generateServices(nRows)
    generateOrders(nRows)
    generateMessage(nRows)
    
    if check_user() and check_services() and check_orders():
        print('PASS')
    else:
        print('FAILED')