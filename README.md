# ktn

Quiz for TTM4100 at NTNU: [ktn.amund.io](https://ktn.amund.io/)

`ktn/local_settings.py`

```python
SECRET_KEY = '***'
DEBUG = False
ALLOWED_HOSTS = ['ktn.amund.io']
CSRF_TRUSTED_ORIGINS = ['https://ktn.amund.io']
STATIC_ROOT = '/path/to/static'
DB = 'postgres'
DATABASE_NAME = '***'
DATABASE_USER = '***'
DATABASE_PASSWORD = '***'
```

```bash
podman build -t ktn .
podman run --rm -d -p 8000:8000 -v /var/run/postgresql/.s.PGSQL.5432:/var/run/postgresql/.s.PGSQL.5432 --name ktn ktn
```
