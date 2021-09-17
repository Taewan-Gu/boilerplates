# 필수 사항

## 가상환경 설정

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```



## mysql 데이터베이스 설정

```python
# 해당 값들은 입력해주어야 한다.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "yourname",
        "USER": "dbuser",
        "PASSWORD": "dbpw",
        "HOST": "IP or Domain",
        "PORT": "port",
    }
}
```



## 마이그레이션

```bash
python manage.py makemigrations
python manage.py migrate
```
