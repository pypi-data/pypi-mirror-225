"""System specific methods and information"""


class _bm:
    from subprocess import run, CalledProcessError, TimeoutExpired
    from typing import NoReturn, Union
    from sys import exit
    
    from ..errors import ShellCodeError, ShellCommandError, ShellTimeoutExpired
    
    class shell_response:
        pass


import tooltils.sys.info as info


def exit(details: str='', code: int=0) -> _bm.NoReturn:
    """Exit the current thread with details"""

    if type(code) is not int:
        raise TypeError('Exit code must be a valid integer instance')
    if type(details) is not str:
        raise TypeError('Details must be a valid string instance')

    if details == '':
        print('', end='')
    else:
        print(details)

    _bm.exit(code)

def clear() -> None:
    """OS independent terminal clearing"""

    if info.platform == 'Windows':
        _bm.run(['cls'])
    elif info.platform == 'MacOS' or info.platform == 'Linux':
        _bm.run(['clear'])

def system(cmds: _bm.Union[list, str], 
           shell: bool=False,
           timeout: int=10, 
           check: bool=False,
           clean: bool=False,
           capture: bool=True
           ) -> _bm.shell_response:
    """Call a system program and return some information"""

    try:
        data = _bm.run(args=cmds, shell=shell, check=check, 
                       capture_output=capture, timeout=timeout)

        class shell_response:
            args            = cmds
            code:       int = data.returncode
            raw:      bytes = data.stdout
            text: list[str] = data.stdout.decode().splitlines()

            if clean:
                text = list(filter(None, text))

    except TypeError:
        raise TypeError('Unable to call type {}'.format(type(cmds)))
    except _bm.CalledProcessError as err:
        code: int = err.returncode

        raise _bm.ShellCodeError(code, 'Shell command return non-zero exit code {}'
                                       .format(code))
    except _bm.TimeoutExpired:
        raise _bm.ShellTimeoutExpired('Shell command timeout reached and the process expired')
    except FileNotFoundError:
        raise _bm.ShellCommandError('Binary not found in program files')
    except OSError:
        raise _bm.ShellCommandError('An unknown error occured')

    return shell_response

def check(cmds: _bm.Union[list, str], 
          shell: bool=False, 
          timeout: int=10,
          check: bool=False,
          raw: bool=False,
          clean: bool=False
          ) -> _bm.Union[list[str], bytes]:
    """Call a system program and return the output"""

    data = system(cmds, shell, timeout, check, clean)

    if raw:
        return data.raw
    else:
        return data.text

def call(cmds: _bm.Union[list, str], 
         shell: bool=False, 
         timeout: int=10,
         check: bool=False
         ) -> int:
    """Call a system program and return the exit code"""
    
    return system(cmds, shell, timeout, check).code

def pID(name: str) -> _bm.Union[list[int], int]:
    """Get the process ID of an app or binary by name"""

    if info.platform == 'MacOS':
        cname: str = '[' + name[0] + ']' + name[1:]
        pID:  list = [int(i) for i in check(f'ps -ax | awk \'/{cname}/' + '{print $1}\'', shell=True)]

        for i in pID:
            data: str = check(f'ps -p {i}', shell=True)[1]
            if data.split('/')[-1].lower() == name.lower():
                pID: int = i
                break

    elif info.platform == 'windows':
        ...

    elif info.platform == 'linux':
        ...

    else:
        pID = None

    return pID
