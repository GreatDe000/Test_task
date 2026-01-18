## Запуск Test_task
### Через git:
1. git clone git@github.com:GreatDe000/Test_task.git (или https://github.com/GreatDe000/Test_task.git)
2. cd <...>
3. Создать файл `.env`, в котором:
      ```env
      STRIPE_SECRET_KEY=sk_test_...(ваш ключ)
      STRIPE_PUBLISHABLE_KEY=pk_test_...(ваш клюс)
      DOMAIN=http://127.0.0.1:8000
      ```
4. pip install -r requirements.txt
5. python manage.py migrate
6. python manage.py runserver

### Через docker:
1. docker build -t django-test-task .
2. docker run -p 8000:10000 --env-file .env django-test-task
