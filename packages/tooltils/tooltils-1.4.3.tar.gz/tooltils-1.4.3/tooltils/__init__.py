"""
# tooltils | v1.4.3

An optimised python utility package built on the standard library

```py
>>> import tooltils
>>> req = tooltils.get('httpbin.org/get')
>>> req
'<Request GET [200]>
>>> req.url
'https://httpbin.org/get'
>>> req.status_code
'200 OK'
>>> req.headers
{'Accept': '*/*', 'User-Agent': 'tooltils/1.4.3', ...}
```

## API

Read the full documentation on `API.md` in the project files
"""


import tooltils.requests as requests
import tooltils.errors as errors
import tooltils.info as info
import tooltils.sys as sys


class _bm:
    from datetime import datetime, timezone, timedelta
    from time import time, localtime, gmtime
    from os.path import getsize, exists
    from typing import Any, Union
    from io import TextIOWrapper
    
    class FileDescriptorOrPath:
        pass
    
    class url_response:
        pass
    
    class EPOCH_seconds:
        pass


colours: dict[str, str] = {
    "white":  97,
    "cyan":   36,
    "pink":   35,
    "blue":   34,
    "yellow": 33,
    "green":  32,
    "red":    31,
    "gray":   30,
}
"""List of the main colours as ANSI integer codes"""

months: list[str] = [
    'January', 'February', 
    'March', 'April', 
    'May', 'June', 
    'July', 'August', 
    'September', 'October', 
    'November', 'December'
]
"""List of months in the year"""

python_version: str = sys.info.python_version
"""Current Python interpereter version"""
platform:       str = sys.info.platform
"""Name of current operating system"""

def length(file: _bm.FileDescriptorOrPath) -> float:
    """Get the length of a wave file in seconds"""

    if not isinstance(file, (str, _bm.TextIOWrapper)):
        raise TypeError('File must be a readable instance')

    file: str = file.name if type(file) is _bm.TextIOWrapper else file

    if file.split('.')[-1] != 'wav':
        raise ValueError('File is not a WAVE type')

    try:
        with open(file, encoding='latin-1') as _f:
            _f.seek(28)
            sdata: str = _f.read(4)
    except (FileNotFoundError, IsADirectoryError):
        raise FileNotFoundError('Unable to locate WAVE file')

    rate: int = 0
    for i in range(4):
        rate += ord(sdata[i]) * pow(256, i)

    return round((_bm.getsize(file) - 44) * 1000 / rate / 1000, 2)

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

    return requests.request(url, 'GET', auth, data,
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

    return requests.request(url, 'POST', auth, data,
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

    return requests.request(url, 'FILE', auth, data,
                            headers, cookies, cert,
                            file_name, timeout, encoding, 
                            mask, agent, verify, redirects)

def style(text: str, 
          style: str, 
          fill: bool=False,
          bold: bool=False,
          italic: bool=False,
          crossed: bool=False,
          underline: bool=False,
          double_underline: bool=False,
          flush: bool=True
          ) -> str:
    """Create text in the specified colour and or style"""

    try:
        code = colours[str(style).lower()]
    except KeyError:
        code = style

    style: str = ''

    if flush:
        sys.call('', shell=True)
    if fill:
        code += 10
    if bold:
        style += ';1'
    if italic:
        style += ';3'
    if crossed:
        style += ';9'
    if underline:
        style += ';4'
    if double_underline:
        style += ';21'

    return '\u001b[{0}{1}{2}\u001b[0m'.format(code, style + 'm', text)

def halve(text: str) -> list:
    """Return the halves of a string"""

    i: int = len(text)
    if i % 2 == 0:
        return [text[:i // 2], text[i // 2:]]
    else:
        return [text[:(i // 2 + 1)], text[(i // 2 + 1):]]

def cipher(text: str, shift: int) -> str:
    """A simple caeser cipher"""

    for i in text:
        start: int = 65 if i.isupper() else 97
        text += chr((ord(i) + shift - (start)) % 26 + (start))

    return halve(text)[1]

def call(cmds: _bm.Union[list, str], 
         shell: bool=False, 
         timeout: int=10,
         check: bool=False
         ) -> int:
    """Call a system command and return the exit code"""

    return sys.system(cmds, shell, timeout, check).code

def cstrip(text: str, 
           chars: _bm.Union[str, list]
           ) -> str:
    """Strip a string or list of characters from some text"""

    for i in chars:
        text = text.replace(i, '')

    return text

def mstrip(text: str,
           chars: dict
           ) -> str:
    """Strip/change a dictionary of string pairs from some text"""
    
    for i in chars.keys():
        text = text.replace(i, chars[i])
    
    return text

def date(epoch: _bm.EPOCH_seconds=..., 
         timezone: str='local', 
         format: int=1
         ) -> str:
    """Convert epoch to a readable date"""

    try:
        if epoch == ...:
            epoch = _bm.time()

        tz = timezone
        if tz.lower() == 'local':
            sdate = _bm.localtime(epoch)
        elif tz.lower() == 'gm' or '00:00' in tz.lower():
            sdate = _bm.gmtime(epoch)
        elif tz.startswith('+') or tz.startswith('-'):
            timezone = _bm.timezone(_bm.timedelta(
                       hours=int(tz[:3]), 
                       minutes=int(tz[4:])))
            sdate    = _bm.datetime.fromtimestamp(epoch, 
                       tz=timezone).timetuple()
        else:
            raise ValueError
    except (ValueError, IndexError):
        raise TypeError('Timezone not found')
    except OverflowError:
        raise OverflowError('Epoch timestamp too large')
    except TypeError:
        raise TypeError('Invalid timezone')

    def fv(val: int) -> str:
        return str(val) if val > 9 else f'0{val}'

    if format == 1:
        return '{}/{}/{} {}:{}:{}'.format(sdate.tm_year,
            fv(sdate.tm_mon), fv(sdate.tm_mday), fv(sdate.tm_hour),
            fv(sdate.tm_min), fv(sdate.tm_sec))

    elif format == 2:
        hour: int = sdate.tm_hour % 12 if sdate.tm_hour % 12 != 0 else 12
        end: list = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'
                     ][int(str(sdate.tm_mday)[-1])]
        if sdate.tm_mday in [11, 12, 13]:
            end: str = 'th'

        return '{}:{} {} on the {}{} of {}, {}'.format(hour, fv(sdate.tm_min), 
               'PM' if sdate.tm_hour >= 12 else 'AM', sdate.tm_mday, end, months[sdate.tm_mon - 1], 
               sdate.tm_year)
    else:
        raise TypeError('Format ({}) not found'.format(format))

def epoch(date: str) -> float:
    """Get epoch from a formatted date (`strftime` etc.)"""

    if '/' in date:
        splitDate: list = str(date).split(' ')
    elif '-' in date:
        splitDate: list = str(date).replace('-', '/').split(' ')
    else:
        try:
            # Remove '1st' to avoid stripping Augu[st]
            sdate: list = mstrip(date, 
                          {':': ' ', ' on the': '', 
                           ' of': '', ',': '',
                           'th': '', '1st': '',
                           'nd': '', 'rd': ''}).split(' ')
            hours, minutes, meridan, days, month, year = sdate

            if '1st' in date:
                days = '1'
            if meridan == 'PM':
                hours = str(int(hours) + 12)

            splitDate: list = [year + '/' + str(int(months.index(month)) + 1)
                               + '/' + days, hours + ':' + minutes + ':00']
        except IndexError:
            raise TypeError('Invalid date argument')

    try:
        sdate = _bm.datetime(*[int(i) for i in splitDate[0].split(
                             '/') + splitDate[1].split(':')])
    except IndexError:
        raise TypeError('Invalid date argument')

    days: int = _bm.datetime(sdate.year, sdate.month, 
                             sdate.day, sdate.hour,
                             sdate.minute, sdate.second).toordinal(
                             ) - _bm.datetime(1970, 1, 1).toordinal() - 1
    # Add 14 hours because of obscure bug
    hours = days * 24 + sdate.hour + 14
    minutes = hours * 60 + sdate.minute
    epoch = minutes * 60 + sdate.second
    
    return epoch

def createfile(name: str, 
               extension: str=None,
               data: str=None,
               keep: bool=False
               ) -> _bm.Union[None, _bm.TextIOWrapper]:
    """Create a file with specified name"""

    if extension is not None:
        name = str(name) + '.' + str(extension)
    if _bm.exists(str(name)):
        raise FileExistsError

    try:
        _f = open(str(name), 'a+')

        if data is not None:
            _f.write(data)
        
        if keep:
            return _f
        else:
            _f.close()

    except (FileNotFoundError, IsADirectoryError):
        raise FileNotFoundError('Invalid file name')

def squeeze(array: _bm.Union[list, tuple, set, dict],
            item: _bm.Union[_bm.Any, None]=None
            ) -> _bm.Union[list, tuple, set, dict]:
    """Remove empty or the specified item(s) from an array"""
    
    if not isinstance(array, (list, tuple, set, dict)):
        raise TypeError('Array must be a valid iterable container')

    op = type(array)
    if op is not dict:
        array = list(array)

    if item is None:
        if op is dict:
            for i in tuple(array.keys()):
                if not array[i]:
                    array.pop(i)
        
            return array
        else:
            return op(filter(None, array))
    else:
        if op is dict:
            for i in tuple(array.keys()):
                if array[i] == item:
                    array.pop(i)
        else:
            for i, it in enumerate(array):
                if it == item:
                    array.pop(i)

        return op(array)
