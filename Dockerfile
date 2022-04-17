FROM python

WORKDIR /app

COPY requirements_prod.txt .
RUN python -m pip install --no-cache-dir -q -r requirements_prod.txt

COPY . .
RUN mkdir /log && touch /log/error.log /log/access.log

EXPOSE 8000

# CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "ktn.wsgi", "--access-logfile", "/log/access.log", "--error-logfile", "/log/error.log"]
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "ktn.wsgi", "--access-logfile", "/log/access.log"]
