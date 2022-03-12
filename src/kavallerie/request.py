import typing as t
import urllib.parse
import functools
import transaction
import horseman.parsers
import horseman.types
import horseman.http
import horseman.meta
from dataclasses import dataclass
from roughrider.routing.meta import Route
from kavallerie.utils import unique


class Request(horseman.meta.Overhead):

    __slots__ = (
        '_data',
        'app',
        'environ',
        'method',
        'path',
        'route',
        'script_name',
        'transaction_manager',
        'utilities',
    )

    app: horseman.meta.Node
    content_type: t.Optional[horseman.http.ContentType]
    cookies: horseman.http.Cookies
    environ: horseman.types.Environ
    method: horseman.types.HTTPMethod
    path: str
    query: horseman.http.Query
    route: t.Optional[Route]
    script_name: str
    utilities: dict

    _data: t.Optional[horseman.parsers.Data]

    def __init__(self,
                 path: str,
                 app: horseman.meta.Node,
                 environ: horseman.types.Environ,
                 transaction_manager: transaction.TransactionManager = None,
                 route: t.Optional[Route] = None):
        self._data = ...
        self.app = app
        self.path = path
        self.environ = environ
        self.method = environ['REQUEST_METHOD'].upper()
        self.route = route
        self.script_name = urllib.parse.quote(environ['SCRIPT_NAME'])
        self.utilities = {}
        if transaction_manager is None:
            transaction_manager = transaction.TransactionManager(explicit=True)
        self.transaction_manager = transaction_manager

    def extract(self) -> horseman.parsers.Data:
        if self._data is not ...:
            return self._data

        if self.content_type:
            self._data = horseman.parsers.parser(
                self.environ['wsgi.input'], self.content_type)

        return self._data

    @unique
    def db_session(self):
        dbconfig = self.app.config.get('database')
        if (factory := dbconfig.get('session_factory')) is not None:
            return factory()

    @unique
    def query(self):
        return horseman.http.Query.from_environ(self.environ)

    @unique
    def cookies(self):
        return horseman.http.Cookies.from_environ(self.environ)

    @unique
    def content_type(self):
        if 'CONTENT_TYPE' in self.environ:
            return horseman.http.ContentType.from_http_header(
                self.environ['CONTENT_TYPE'])

    @unique
    def application_uri(self):
        scheme = self.environ['wsgi.url_scheme']
        http_host = self.environ.get('HTTP_HOST')
        if not http_host:
            server = self.environ['SERVER_NAME']
            port = self.environ.get('SERVER_PORT', '80')
        elif ':' in http_host:
            server, port = http_host.split(':', 1)
        else:
            server = http_host
            port = '80'

        if (scheme == 'http' and port == '80') or \
           (scheme == 'https' and port == '443'):
            return f'{scheme}://{server}{self.script_name}'
        return f'{scheme}://{server}:{port}{self.script_name}'

    def uri(self, include_query=True):
        url = self.application_uri
        path_info = urllib.parse.quote(self.environ.get('PATH_INFO', ''))
        if include_query:
            qs = urllib.parse.quote(self.environ.get('QUERY_STRING'))
            if qs:
                return f"{url}{path_info}?{qs}"
        return f"{url}{path_info}"
