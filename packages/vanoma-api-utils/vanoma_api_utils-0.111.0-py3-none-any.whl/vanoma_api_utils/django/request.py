from django.urls import resolve
from django.http.request import HttpRequest
from django.core.handlers.wsgi import WSGIRequest
from django.utils.translation import gettext_lazy as _


def clone_request(request: HttpRequest, method: str, path: str) -> HttpRequest:
    assert isinstance(request, WSGIRequest), _(f"Expected request to be a WSGIRequest but found {type(request)}. Might need to update the logic of cloning the request to support {type(request)}.")
    environ = {**request.environ, "PATH_INFO": path, "REQUEST_METHOD": method}
    new_request = WSGIRequest(environ)
    new_request.resolver_match = resolve(path)
    return new_request
