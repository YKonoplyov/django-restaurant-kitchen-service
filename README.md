# Restaurant kitchen service
 ## You can find deployed project [here](https://kitchen-service-fvfz.onrender.com/)
   To use functional you need to login:
<br>
<br>
   login: 
```   
visitor.cook
```   
password:
```
SimplePassword4895
```

## Table of Contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Used technogies](#used-technologies)
5. [Usage](#usage)

## Introduction
Restaurant kitchen service is web application created for tracking and managing kitchen process.

### Requirements
* python 3.6
* pip

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/YKonoplyov/django-restaurant-kitchen-service.git
   ```

2. Create virtual environment:
   ```
    python -m venv venv
   ```
   and activate it 
   <br>
   <br>
    - on windows:
    ```
    venv\Scripts\activate
    ```   
    - on Mac:
    ```
    source venv/bin/activate
   ```
3. Install dependencies:
```
pip install -r requirements.txt
```

4. Apply database migrations:
```
python manage.py migrate
```
5. Create superuser:
```
python manage.py createsuperuser
```
6. Run django server using run button or type next command to the console:
```
python manage.py runserver
```
It will run at http://127.0.0.1:8000/.

## Used technologies
- Django framework
- HTML, CSS
- SQLite

## Usage
- Track and control of cooks that cooking  dish
- Track and control dish types
- Track of ingredients
- Track of dish progress
