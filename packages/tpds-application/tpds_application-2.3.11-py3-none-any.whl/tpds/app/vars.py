
SETTING_BASE = 'com.microchip/TPDS'
SETTING_GEOMETRY = SETTING_BASE + '/geometry'
SETTING_BASEDIR = SETTING_BASE + '/basedir'
SETTING_EXECUTABLE = SETTING_BASE + '/executable'

_app_ref = None
_core_thread = None


def get_core_thread():
    global _core_thread
    return _core_thread


def set_core_thread(value):
    global _core_thread
    _core_thread = value


def get_app_ref():
    global _app_ref
    return _app_ref


def set_app_ref(value):
    global _app_ref
    _app_ref = value


def get_setting_name(obj, *args):
    return '/'.join([SETTING_BASE, obj.__class__.__name__, *args])


def get_url_base():
    try:
        port = _app_ref.backend.api_port()
    except:
        port = 5001
    return f'http://localhost:{port}'


dict_pckg = [
    {
        'package': 'tpds-application',
        'channel': 'microchiporg',
    },
    {
        'package': 'tpds-core',
        'channel': 'microchiporg',
    }
]

__all__ = [
    'SETTING_BASE',
    'SETTING_GEOMETRY',
    'SETTING_BASEDIR',
    'SETTING_EXECUTABLE',
    'get_core_thread',
    'set_core_thread',
    'get_app_ref',
    'set_app_ref',
    'get_setting_name',
    'get_url_base'
]
