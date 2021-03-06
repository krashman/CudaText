import os
import shutil
from cudatext import *
from datetime import datetime
from time import strftime, gmtime

INI = 'cuda_insert_time.ini'

ini = os.path.join(app_path(APP_DIR_SETTINGS), INI)
ini0 = os.path.join(os.path.dirname(__file__), INI)
if not os.path.isfile(ini) and os.path.isfile(ini0):
    shutil.copyfile(ini0, ini)

ITEM_CONFIG = '(Edit config)'


def get_format_lines():
    with open(ini, 'r') as f:
        res = f.read().splitlines()
    res = [s for s in res if s and not s.startswith('#')]
    return res

def do_format(s):
    if s=='rfc':    
        return strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    t = datetime.now()
    return t.strftime(s)
    

class Command:
    def dialog(self):
        lines = get_format_lines()
        lines = [do_format(s) for s in lines] + [ITEM_CONFIG]

        res = dlg_menu(MENU_LIST, '\n'.join(lines))
        if res is None: return
        s = lines[res]
        
        if s==ITEM_CONFIG:
            file_open(ini)
            return

        caret = ed.get_carets()[0]
        x, y = ed.insert(caret[0], caret[1], s)
        ed.set_caret(x, y)
        msg_status('Date/time inserted')
