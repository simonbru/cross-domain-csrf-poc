# POC for cross-domain requests with CSRF token in cookie and header

## Try with HTTP
Start api/front server:
```
python app.py portal.localhost http://api.portal.localhost:8001 http://portal.localhost:8001
```

Go to http://portal.localhost:8001/test and wait for tests to complete.

## Try with HTTP and different subdomain
Start api/front server:
```
python app.py portal.localhost http://api.portal.localhost:8001 http://front.portal.localhost:8001
```

Go to http://front.portal.localhost:8001/test and wait for tests to complete.

## Try with HTTPS and secure cookie (using mitmproxy)
Start api/front server:
```
python app.py portal.localhost https://api.portal.localhost:8002 https://portal.localhost:8002
```

Start reverse proxy:
```
mitmproxy -p 8002 -m reverse:http://localhost:8001
```

Go to https://api.portal.localhost:8002 to allow the self-signed certificate.

Go to https://portal.localhost:8002/test and wait for tests to complete.