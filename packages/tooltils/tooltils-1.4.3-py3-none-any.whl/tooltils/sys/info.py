"""Identifying system information"""

class _bm:
    from subprocess import CalledProcessError, TimeoutExpired, run
    from sys import executable, maxsize, platform, version
    from socket import gethostname

    def check(cmd: str):
        try:
            return _bm.run(cmd, shell=True, 
                           capture_output=True).stdout.decode(
                           ).splitlines()
        except (_bm.CalledProcessError, _bm.TimeoutExpired):
            return
    
    def squeeze(items: list) -> list:
	    return list(filter(None, items))

macOS_releases: dict[str, str] = {
    "10.0":  "Cheetah",
    "10.1":  "Puma",
    "10.2":  "Jaguar",
    "10.3":  "Panther",
    "10.4":  "Tiger",
    "10.5":  "Leopard",
    "10.6":  "Snow Leopard",
    "10.7":  "Lion",
    "10.8":  "Mountain Lion",
    "10.9":  "Mavericks",
    "10.10": "Yosemite",
    "10.11": "El Capitan",
    "10.12": "Sierra",
    "10.13": "High Sierra",
    "10.14": "Mojave",
    "10.15": "Catalina",
    "11":    "Big Sur",
    "12":    "Monterey",
    "13":    "Ventura",
    "14":    "Sonoma"
}
"""List of all current MacOS versions"""

python_version:         str = _bm.version.split(' ')[0]
"""Current Python interpereter version"""
python_version_tuple: tuple = tuple(python_version.split('.'))
"""Current Python interpereter version seperated into major, minor, patch"""
name:                   str = _bm.gethostname()
"""The network name of computer"""
bitsize                     = 32 if not (_bm.maxsize > 2 ** 32) else 64
"""Determine if your computer is 32 or 64-bit"""
interpreter:            str = _bm.executable
"""Location of current Python interpereter"""

st = _bm.platform.startswith
if st('linux'):
    tplatform = 'Linux'
    tdplatform = 'Linux'
elif st('win'):
    tplatform = 'Windows'
    tdplatform = 'Windows'
elif st('cygwin'):
    tplatform = 'Windows'
    tdplatform = 'Cygwin'
elif st('msys'):
    tplatform = 'Windows'
    tdplatform = 'MSYS2'
elif st('darwin'):
    tplatform = 'MacOS'
    tdplatform = 'Darwin'
elif st('os2'):
    tplatform = 'OS2'
    tdplatform = 'OS2'
elif st('risc'):
    tplatform = 'Linux'
    tdplatform = 'RiscOS'
elif st('athe'):
    tplatform = 'Linux'
    tdplatform = 'AtheOS'
elif st('freebsd'):
    tplatform = 'BSD'
    tdplatform = 'FreeBSD'
elif st('openbsd'):
    tplatform = 'BSD'
    tdplatform = 'OpenBSD'
elif st('aix'):
    tplatform = 'AIX'
    tdplatform = 'AIX'
else:
    tplatform = None
    tdplatform = None

platform:          str = tplatform
"""Name of current operating system"""
detailed_platform: str = tdplatform
"""Detailed name of current operating system"""

if platform == 'Windows':
    def wmic(*cmds: tuple) -> str:
        return [i.strip() for i in _bm.check('wmic ' + cmds[0] + ' get ' + cmds[1])][2]

    tcpu:           str = wmic('cpu', 'name')
    tcores:         str = wmic('cpu', 'NumberOfCores')
    tserial_number: str = wmic('bios', 'SerialNumber')
    tarch:          str = wmic('os', 'OSArchitecture').replace('Processor', '').strip()

    tsysinfo: list = _bm.squeeze(_bm.check('systeminfo'))

    tversion:      str = tsysinfo[2]
    tmanufacturer: str = tsysinfo[11]
    tmodel:        str = tsysinfo[12]
    tboot_drive:   str = tsysinfo[19]
    tram:          str = tsysinfo[23]

    for i in ['tname', 'tversion', 'tmanufacturer', 'tmodel', 'tboot_drive', 'tram']:
        locals()[i] = locals()[i].split(': ')[1].strip()

    tpver:  str = tversion.split(' ')[0]
    tram:   int = int(tram.split(' ')[0].replace(',', ''))
    tpver: list = [tpver.split('.')[0], tpver]

elif platform == 'MacOS':
    tpver: list = [_bm.check('sw_vers -productVersion')[0]]

    if len(tpver[0].split('.')) > 1:
        if tpver[0][:2] in ('11', '12', '13', '14'):
            tpver.append(macOS_releases[tpver[0][:2]])
        else:
            tpver.append(macOS_releases['.'.join(tpver[0].split('.')[:2])])
    else:
        tpver.append(macOS_releases[tpver[0]])
    
    tarch:     str = _bm.check('arch')[0]
    tsysinfo: list = _bm.squeeze(_bm.check('system_profiler SPHardwareDataType'))
    tmodel:    str = tsysinfo[2].split(': ')[1]
    tcpu:      str = tsysinfo[5].split(': ')[1]
    tcores:    int = int(tsysinfo[6].split(': ')[1].split(' (')[0])
    tram:      str = tsysinfo[7].split(': ')[1]
    if 'GB' in tram:
        tram: int = int(tram.split(' ')[0]) * 1024
    else:
        tram: int = int(tram.split(' ')[0])
    tserial_number: str = tsysinfo[10].split(': ')[1]
    tboot_drive:    str = _bm.check('bless --info --getBoot')[0]
    
elif platform == 'Linux':
    tcpu:      str = ''
    tarch:     str = ''
    tpver:    list = []
    tmodel:    str = ''
    tcores:    int = 0
    tram:      int = 0
    tserial_number: str = ''
    tboot_drive:    str = ''

    ...
    # Add standard linux implementation
else:
    tcpu:      str = ''
    tarch:     str = ''
    tpver:    list = []
    tmodel:    str = ''
    tcores:    int = 0
    tram:      int = 0
    tserial_number: str = ''
    tboot_drive:    str = ''


cpu:                     str = str(tcpu)
"""Name of the currently in use cpu of your computer"""
arch:                    str = str(tarch)
"""Architecture of your computer"""
platform_version: tuple[str] = tuple([str(i) for i in tpver])
"""Version number and or name of current OS"""
model:                   str = str(tmodel)
"""The model or manufacturer of your computer"""
cores:                   int = int(tcores)
"""The amount of cores in your computer cpu"""
ram:                     int = int(tram)
"""The amount of ram in megabytes in your computer"""
serial_number:           str = str(tserial_number)
"""The identifiable code or tag string of your computer"""
boot_drive:              str = str(tboot_drive)
"""The location of the boot drive currently being used on your computer"""

try:
    del st, tcpu, tarch, tpver, \
        tplatform, tdplatform, tmodel, \
        tcores, tram, tserial_number, \
        tboot_drive, tmanufacturer, _bm

    if platform == 'Windows':
        del wmic, tsysinfo
    elif platform == 'Linux':
        ...

        # Add standard linux implementation
except NameError:
    pass
