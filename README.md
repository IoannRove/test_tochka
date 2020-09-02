# Тестовое задание для Точки
## Установка Docker и Docker-compose
Для запуска сервера необходим **Docker** и **Docker-compose**  
#### Установка Docker  https://docs.docker.com/engine/install/debian/
Удаление старых версий Docker  
```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
``` 
Установка из репозитория  
```bash
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
```
Вывод команды должен содержать строку  
```bash
Key fingerprint = 9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```
#### Установка Docker-compose  https://docs.docker.com/compose/install/
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```
## Запуск проекта
Проект запускается скриптом **start_server.sh**  
```bash
./start_server.sh
```
## Эксплуатация проекта
API может отвечать в виде json и html страницы. Вид ответа зависит от значения заголовка Accept.  
Запрос с `Accept=application/json` получит json, а с `Accept=text/html` - html страницу.  
Каждый ответ имеет следующую структуру:  
```json
{  
    "status": "<http_status>",  
    "result": "<bool:operation_status>",  
    "addition": {},  
    "description": {}  
}  
```
Описание полей:  
- status — http статус запроса
- result — статус проведения текущей операции  
- addition — поля для описания текущей операции (uuid, ФИО, сумма,
статус и т.п.)  
- description — дополнительные описания к текущей операции (прочие
текстовые поля, если необходимо)
### Реализованные методы
#### /api/ping/
http://localhost/api/ping/  
Принимает только `GET` запросы.  
Нужен для проверки работоспособности сервиса. При работе сервиса имеет следующий ответ:  
```json
{  
    "status": 200,  
    "result": true,  
    "addition": {},  
    "description": {}  
}  
```
#### /api/account_list/  
http://localhost/api/account_list/  
Принимает только `GET` запросы.
В ответе возвращает список всех счетов абонентов с полями `uuid`, `fio` и `status`. 
Ответ выглядит следующим образом:  
```json
{  
    "status": 200,  
    "result": true,  
    "addition": [  
        {  
            "uuid": "26c940a1-7228-4ea2-a3bc-e6460b172040",  
            "fio": "Петров Иван Сергеевич",  
            "balance": 1700,  
            "hold": 300,  
            "status": true  
        },  
        {  
            "uuid": "7badc8f8-65bc-449a-8cde-855234ac63e1",  
            "fio": "Kazitsky Jason",  
            "balance": 200,  
            "hold": 200,  
            "status": true  
        }  
    ],  
    "description": {}  
}  
```
#### /api/status/<uuid>
http://localhost/api/status/<uuid>  
Принимает только `GET` запросы. uuid - uuid счёта абонента.  
В ответе содержится баланс и статус счёта абонента. 
Ответ на запрос http://localhost/api/status/867f0924-a917-4711-939b-90b179a96392 выглядит следующим образом:   
```json
{  
    "status": 200,  
    "result": true,  
    "addition": {  
        "balance": 998799,  
        "status": false  
    },  
    "description": {}  
}  
```
#### /api/add/<uuid>
http://localhost/api/add/<uuid>  
Принимает только `POST` запросы. uuid - uuid счёта абонента.  
Тело запроса должно содержать поле `balance` и выглядеть следующим образом:  
```json
{  
    "balance": "11000"  
}  
```
В ответе содержится баланс счёта абонента после операции - сумма отправленного значения и баланса до операции. 
Ответ на запрос http://localhost/api/add/867f0924-a917-4711-939b-90b179a96392 выглядит следующим образом:   
``` json
{  
    "status": 200,  
    "result": true,  
    "addition": {  
        "balance": 998799  
    },  
    "description": {}  
}
```
#### /api/subtract/<uuid>
http://localhost/api/subtract/<uuid>  
Принимает только `POST` запросы. uuid - uuid счёта абонента.  
Тело запроса должно содержать поле `hold` и выглядеть следующим образом:  
```json
{  
    "hold": "4000"  
}  
```
В ответе содержится холд счёта абонента после операции - сумма отправленного значения и холда до операции. 
Данное значение не может превышать баланс счёта абонента.  
Ответ на запрос http://localhost/api/subtract/867f0924-a917-4711-939b-90b179a96392 при соблюдении условия выглядит следующим образом:   
```json
{  
    "status": 200,  
    "result": true,  
    "addition": {  
        "balance": 998799  
    },  
    "description": {}  
}  
```
При запросе к данному методу создаётся таск для celery, который через 10 минут вычтет весь холд из баланса и обнулит холд.  
Ответ на запрос http://localhost/api/subtract/867f0924-a917-4711-939b-90b179a96392 при несоблюдении условия выглядит следующим образом:   
```json
{  
    "status": 200,  
    "result": true,  
    "addition": {  
        "errors": {  
            "message": "Холд не может превышать баланс счёта абонента.",  
            "code": "hold_over_balance"  
        }  
    },  
    "description": {}  
}  
```