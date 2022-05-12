FROM python

# nginx

RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    && rm -rf /etc/nginx/sites-enabled \
    && ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

COPY ktn.conf /etc/nginx/conf.d/ktn.conf

# django

COPY requirements_prod.txt .
RUN python -m pip install --no-cache-dir -q \
    -r requirements_prod.txt

ENV KTN_STATIC_ROOT=/app/static \
    KTN_DEBUG=false

COPY . .
RUN echo yes | python manage.py collectstatic

# start

EXPOSE 80

RUN echo "nginx -g 'daemon off;' & gunicorn --workers 3 --bind 127.0.0.1:8000 ktn.wsgi --access-logfile /dev/stdout" > start.sh

CMD ["bash", "start.sh"]
