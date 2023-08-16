"""http/1.1 access methods"""


class _bm:
    from ssl import (create_default_context, CERT_NONE, 
                     get_default_verify_paths, SSLError)              
    from urllib.error import URLError, HTTPError
    from json.decoder import JSONDecodeError
    from typing import Union, MutableMapping
    from os.path import abspath, exists
    from urllib.parse import urlencode
    from shutil import copyfileobj
    from json import loads, dumps
    import urllib.request as u

    from .errors import (ConnectionError, StatusCodeError, 
                         UnicodeDecodeError, TimeoutExpired)
    from .sys.info import platform, cpu
    from .info import version
    
    class FileDescriptorOrPath:
        pass
    
    class url_response:
        pass

    class certifs:
        pass


status_codes: dict[int, str] = {
    100: 'Continue',
    101: 'Switching Protocols',
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Content-Length Required',
    412: 'Precondition Failed',
    413: 'Request Entity Too Large',
    414: 'Request URL Too Long',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expectation Failed',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported',
}
"""List of valid HTTP response status codes (100-505)"""

def ctx(verify: bool=True, cert: str=None):
    """Create a custom SSLContext instance"""

    try:
        if type(cert) is not str and (
            cert is not None and not cert is type(tuple)):
            raise TypeError('Certificate must be a valid file path')

        ctx = _bm.create_default_context(cafile=cert)
    except (FileNotFoundError, IsADirectoryError, _bm.SSLError):
        raise FileNotFoundError('Not a valid certificate file path')
    
    if not bool(verify):
        ctx.check_hostname = False
        ctx.verify_mode    = _bm.CERT_NONE
        ctx.                 set_ciphers('RSA')
    
    return ctx

def prep_url(url: _bm.Union[str, bytes], 
             data: dict=None,
             https: bool=True
             ) -> str:
    """Configure a URL making it viable for requests"""

    if url[-1] == '/':
        url = url[:-1]

    if data is None:
        data = {}
    elif type(data) is not dict:
        raise TypeError('Data must be a valid dictionary instance')

    try:
        st = url.strip().startswith
    except AttributeError:
        if type(url) is bytes:
            st = url.decode().strip().startswith
        else:
            raise TypeError('URL must be a valid string instance')

    if data != {}:
        url += '?' + _bm.urlencode(data, doseq=True, safe='/')
    if url[0] == '/':
        if not _bm.exists(url):
            raise _bm.StatusCodeError(404, 'Not Found')
    elif url.startswith('file:///'):
        if not _bm.exists(url[7:]):
            raise _bm.StatusCodeError(404, 'Not Found')
    elif not st('https://') and not st('http://'):
        if https:
            url = 'https://' + url
        else:
            url = 'http://' + url
    
    return str(url)

def where() -> _bm.certifs:
    """Return default certificate file and path locations used by Python"""

    data = _bm.get_default_verify_paths()

    class certifs:
        cafile: str = data.cafile
        capath: str = data.capath

    return certifs

class Redirects(_bm.u.HTTPRedirectHandler):
    """A handler to stop redirects in urllib"""

    def redirect_request(self, req, fp, code, msg, headers, newurl) -> None:
        return None

class request():
    """Prepare and send a http request"""

    def __init__(self, 
                 url: _bm.Union[str, bytes],
                 method: str,
                 auth: tuple=None,
                 data: dict=None,
                 headers: dict=None,
                 cookies: dict=None,
                 cert: _bm.FileDescriptorOrPath=None, 
                 file_name: _bm.FileDescriptorOrPath=None,
                 timeout: int=15, 
                 encoding: str='utf-8',
                 mask: bool=False,
                 agent: str=None,
                 verify: bool=True,
                 redirects: bool=True):

        self.verified:  bool = bool(verify)
        self.redirects: bool = bool(redirects)
        self.mask:      bool = bool(mask)

        u = method.upper()
        if u not in ['GET', 'POST', 'PUT', 'FILE', 
                     'DOWNLOAD', 'PATCH', 'HEAD',
                     'HEADER', 'DELETE']:
            raise ValueError('Invalid http method \'{}\''.format(method))
        elif type(method) is not str:
            raise TypeError('Method must be a valid string instance')
        else:
            if u == 'HEADER':
                self.method = 'HEAD'
            elif u == 'DOWNLOAD':
                self.method = 'FILE'
            else:
                self.method: str = u
        if data is None:
            self.data: dict = {}
        elif type(data) is not dict:
            raise TypeError('Parameters must be a valid dictionary instance')
        else:
            self.data: dict = data
        if cookies is None:
            self.cookies: dict = {}
        elif type(cookies) is not dict:
            raise TypeError('Cookies must be a valid dictionary instance')
        else:
            self.cookies: dict = cookies
        if cert is None:
            self.cert: str = where().cafile
        else:
            if type(cert) is not str:
                raise TypeError('Certificate must be a valid string instance')
            elif not _bm.exists(cert) or cert.split('.')[-1] != 'pem':
                raise FileNotFoundError('Invalid certificate file path')
            elif verify:
                self.cert: str = cert
            else:
                self.cert: str = where().cafile
        if auth is None:
            self.auth = None
        elif len(auth) != 2:
            raise ValueError('Invalid authentication details')
        elif type(auth) is not tuple and type(auth) is not list:
            raise TypeError('Authentiction must be a valid tuple instance')
        else:
            self.auth: tuple = tuple(auth)
        if type(timeout) is not int and type(timeout) is not float:
            raise TypeError('Timeout must be a valid integer instance')
        elif timeout > 999 or timeout < 1:
            raise ValueError('Timeout cannot be bigger than 999 or smaller than 0 seconds')
        else:
            self.timeout: int = int(timeout)
        try:
            if not _bm.exists(file_name):
                self.file_name: str = file_name
            elif not _bm.exists(url.split('/')[-1]):
                self.file_name: str = url.split('/')[-1]
            else:
                raise FileExistsError('Destination file already exists')
        except TypeError:
            if not _bm.exists(url.split('/')[-1]):
                self.file_name: str = url.split('/')[-1]
            else:
                raise FileExistsError('Destination file already exists')
        if agent is None:
            self.agent: str = f'Python-tooltils/{_bm.version}'
        if mask:
            if _bm.platform == 'Windows':
                self.agent: str = 'Mozilla/5.0 (Windows NT 10.0; ' + \
                                  'rv:10.0) Gecko/20100101 Firefox/10.0'
            elif _bm.platform == 'MacOS':
                self.agent: str = f'Mozilla/5.0 (Macintosh; {_bm.cpu} Mac OS' + \
                                  '10.15; rv:10.0) Gecko/20100101 Firefox/10.0'
            else:
                self.agent: str = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) ' + \
                                  'Gecko/20100101 Firefox/10.0'
        if agent is not None:
            self.agent: str = str(agent)
        if headers is None:
            self.headers: dict = {}
        elif type(headers) is not dict:
            raise TypeError('Headers must be a valid dictionary instance')
        else:
            self.headers: dict[str, str] = headers
        if type(encoding) is not str:
            raise TypeError('Encoding must be a valid string instance')
        else:
            self.encoding: str = encoding
        
        self.url: str = prep_url(url, data)

        _ctx = ctx(self.verified, self.cert)
        
        rmethod: str = self.method

        if rmethod == 'POST' or rmethod == 'PUT':
            data = _bm.dumps(self.data).encode()
        elif rmethod == 'FILE':
            rmethod = 'GET'

        req = _bm.u.Request(self.url, data=data, method=rmethod)

        if self.method == 'POST':
            req.add_header('Content-Type', 'application/json; charset=UTF-8')
            req.add_header('Content-Length', str(len(self.data)))

        headers: dict = {'User-Agent': self.agent, 
                         'Accept': '*/*', 
                         'Accept-Encoding': 'gzip, deflate'}
        headers.update(self.headers)

        for i in headers.keys():
            req.add_header(str(i), str(headers[i]))

        for i in self.cookies.keys():
            req.add_header('Cookie', '{}={}'.format(i, self.cookies[i]))

        man = _bm.u.HTTPPasswordMgrWithDefaultRealm()

        if self.auth is not None:
            man.add_password(None, self.url, self.auth[0], self.auth[1])

        _auth = _bm.u.HTTPBasicAuthHandler(man)

        if self.redirects:
            opener = _bm.u.build_opener(_auth, Redirects)
        else:
            opener = _bm.u.build_opener(_auth)
        _bm.u.install_opener(opener)
        
        try:
            rdata = _bm.u.urlopen(req, context=_ctx, 
                                  timeout=self.timeout)
        except _bm.HTTPError as err:
            raise _bm.StatusCodeError(err.code, 
                                      status_codes[err.code])
        except _bm.URLError as err:
            if '[Errno 8]' in str(err):
                try:
                    _bm.u.urlopen('https://httpbin./get', timeout=10, 
                                  context=ctx(False))

                    raise _bm.StatusCodeError(404, 'Not Found')
                except (_bm.URLError, TimeoutError):
                    raise _bm.ConnectionError('Internet connection not found')
                except _bm.HTTPError:
                    raise _bm.ConnectionError('Unspecified urlopen error')
            elif 'SSL' in str(err).upper():
                raise _bm.ConnectionError('SSL Certificate not verified correctly')
            else:
                raise _bm.ConnectionError('Unspecified urlopen error')
        except TimeoutError:
            raise _bm.TimeoutExpired('The request read operation timed out')
        except ValueError:
            raise ValueError('Invalid URL \'' + request.url + '\'')
        except (KeyboardInterrupt, EOFError):
            return None

        self._rdata           = rdata
        self.code:        int = rdata.getcode()
        self.reason:      str = status_codes[self.code]
        self.status_code: str = f'{self.code} {self.reason}'
        self.headers: _bm.MutableMapping[str, str] = rdata.headers['headers']
        
        if method != 'FILE':
            self.text:  str = rdata.read().decode(self.encoding)
            self.raw: bytes = self.text.encode(self.encoding)
            self.html       = None
            self.path       = None
        else:
            with open(self.file_name, 'wb+') as _f:
                _f.write(rdata.read())

            self.path: str = _bm.abspath(self.file_name)

        try:
            self.json: dict = _bm.loads(self.text)
            self.headers: _bm.MutableMapping[str, str] = self.json['headers']
        except _bm.JSONDecodeError:
            self.json = None
            self.headers: _bm.MutableMapping[str, str] = req.headers
            if self.text[0] == '<' or self.text[-1] == '>':
                self.html: str = self.text
        except (UnicodeDecodeError, UnicodeEncodeError):
            raise _bm.UnicodeDecodeError('Unable to decode ' + 
                                         'URL data from codec \'{}\''.
                                         format(self.encoding))
        except AttributeError:
            self.json = None
            self.text = None
            self.raw  = None
            self.html = None
    
    def __str__(self):
        return f'<Request {self.method} [{self.code}]>'
    
    def read(self) -> bytes:
        """Read the file and return the data in bytes"""

        return self.rdata.read()

    def readlines(self) -> list:
        """Read the file and return the data as a list split at every newline"""
    
        return self.rdata.read().decode(self.encoding).splitlines()


def get(url: _bm.Union[str, bytes], 
        auth: tuple=None,
        data: dict=None,
        headers: dict=None,
        cookies: dict=None,
        cert: _bm.FileDescriptorOrPath=None, 
        timeout: int=15, 
        encoding: str='utf-8',
        mask: bool=False,
        agent: str=None,
        verify: bool=True,
        redirects: bool=True
        ) -> _bm.url_response:
    """Send a GET request"""

    return request(url, 'GET', auth, data, 
                   headers, cookies, cert, 
                   None, timeout, encoding, 
                   mask, agent, verify, redirects)

def post(url: _bm.Union[str, bytes], 
         auth: tuple=None,
         data: dict=None,
         headers: dict=None,
         cookies: dict=None,
         cert: _bm.FileDescriptorOrPath=None, 
         timeout: int=15, 
         encoding: str='utf-8',
         mask: bool=False,
         agent: str=None,
         verify: bool=True,
         redirects: bool=True
         ) -> _bm.url_response:
    """Send a POST request"""

    return request(url, 'POST', auth, data, 
                   headers, cookies, cert, 
                   None, timeout, encoding, 
                   mask, agent, verify, redirects)

def download(url: _bm.Union[str, bytes], 
             auth: tuple=None,
             data: dict=None,
             headers: dict=None,
             cookies: dict=None,
             cert: _bm.FileDescriptorOrPath=None, 
             file_name: _bm.FileDescriptorOrPath=None,
             timeout: int=15, 
             encoding: str='utf-8',
             mask: bool=False,
             agent: str=None,
             verify: bool=True,
             redirects: bool=True
             ) -> _bm.url_response:
    """Download a file onto the disk"""

    return request(url, 'FILE', auth, data, 
                   headers, cookies, cert, 
                   file_name, timeout, encoding, 
                   mask, agent, verify, redirects)

def put(url: _bm.Union[str, bytes], 
        auth: tuple=None,
        data: dict=None,
        headers: dict=None,
        cookies: dict=None,
        cert: _bm.FileDescriptorOrPath=None, 
        timeout: int=15, 
        encoding: str='utf-8',
        mask: bool=False,
        agent: str=None,
        verify: bool=True,
        redirects: bool=True
        ) -> _bm.url_response:
    """Send a PUT request"""

    return request(url, 'PUT', auth, data, 
                   headers, cookies, cert, 
                   None, timeout, encoding, 
                   mask, agent, verify, redirects)

def patch(url: _bm.Union[str, bytes], 
          auth: tuple=None,
          data: dict=None,
          headers: dict=None,
          cookies: dict=None,
          cert: _bm.FileDescriptorOrPath=None, 
          timeout: int=15, 
          encoding: str='utf-8',
          mask: bool=False,
          agent: str=None,
          verify: bool=True,
          redirects: bool=True
          ) -> _bm.url_response:
    """Send a PATCH request"""

    return request(url, 'PATCH', auth, data, 
                   headers, cookies, cert, 
                   None, timeout, encoding, 
                   mask, agent, verify, redirects)

def delete(url: _bm.Union[str, bytes], 
           auth: tuple=None,
           data: dict=None,
           headers: dict=None,
           cert: _bm.FileDescriptorOrPath=None,
           cookies: dict=None,
           timeout: int=15, 
           encoding: str='utf-8',
           mask: bool=False,
           verify: bool=True,
           agent: str=None,
           redirects: bool=True
           ) -> _bm.url_response:
    """Send a DELETE request"""
 
    return request(url, 'DELETE', auth, data, 
                   headers, cookies, cert, 
                   None, timeout, encoding, 
                   mask, agent, verify, redirects)
