#!/usr/bin/env python3

import argparse
import random

import bottle
from bottle import request, response, view

app = bottle.app()

options = None
use_secure_cookie = None
csrf_token = None


@app.get("/")
def root_view():
    return """
    <html>
        Go to <a href="/test">/test</a> to run CSRF cookie test
    </html>
    """


@app.get("/test")
@view("template.html")
def test_view():
    return {
        "api_url": options.api_url,
        "use_secure_cookie": use_secure_cookie,
    }


def set_cors_headers(response):
    response.set_header("Access-Control-Allow-Origin", options.origin)
    response.set_header("Access-Control-Allow-Credentials", "true")
    response.set_header(
        "Access-Control-Allow-Headers", "credentials, mode, X-CSRFToken"
    )


@app.route("/set-csrf-cookie", method=["GET", "OPTIONS"])
def set_csrf_cookie_view():
    set_cors_headers(response)
    response.set_cookie(
        "x-csrftoken",
        value=csrf_token,
        domain=options.cookie_domain,
        path="/",
        secure=use_secure_cookie,
        samesite="lax",
    )
    return {}


@app.route("/check-csrf-token", method=["POST", "OPTIONS"])
def check_csrf_token_view():
    set_cors_headers(response)
    cookie_token = request.get_cookie("x-csrftoken")
    header_token = request.headers.get("x-csrftoken")
    status = "success" if cookie_token == header_token == csrf_token else "failure"
    return {
        "status": status,
        "cookie": cookie_token,
        "header": header_token,
        "expected": csrf_token,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cookie_domain")
    parser.add_argument("api_url")
    parser.add_argument("origin")
    options = parser.parse_args()

    use_secure_cookie = options.api_url.startswith("https")
    csrf_token = f"token_{random.randint(100, 999)}"

    bottle.run(app, host="::", port=8001, debug=True, reloader=True)
