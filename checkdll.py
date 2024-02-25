import sys
import os
import ctypes
from ctypes import windll, create_string_buffer
import pefile
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import argparse
import win32api
from pywintypes import error 

    

colorama_init()
def library_import_check(path: str, full_inspect: bool, loaded_dlls) -> int:
    res = 0
    basename = os.path.basename(path).lower()
    handle = None
    path_new = None
    new_loaded = False
    try:
        handle = win32api.LoadLibrary(path)
    except error:
        res += 1
        paths = os.environ["PATH"].split(";")
        for p in paths:
            pd = os.path.join(p, basename)
            if os.path.exists(pd):
                print(f"FOUND: {Fore.YELLOW}{basename}{Style.RESET_ALL} in {pd}")
                res += library_import_check(pd, full_inspect)
    
    if handle is not None:
        path_new = win32api.GetModuleFileName(handle)
        if full_inspect:
            if handle not in loaded_dlls: # avoid recursion
                loaded_dlls.append(handle)
                library_import_check(path_new, full_inspect, loaded_dlls)
                new_loaded = True
        
        #print(f"Library '{basename}' loaded from '{path}'")
    
    if os.path.exists(path):
        pe = pefile.PE(path)
        if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                dll_name = str(entry.dll.decode("utf-8"))
                res += library_import_check(dll_name, full_inspect, loaded_dlls)
    if handle is None:
        print(f"Handle (NONE): {Fore.RED}{path}{Style.RESET_ALL}")
    else:
        if new_loaded: 
            print(f"Handle ({hex(handle)}): {Fore.GREEN}{path}{Style.RESET_ALL} in '{os.path.dirname(path_new)}'")
    
    return res        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='library_import_check')
    parser.add_argument('filename', help="Filename of the Library (*.dll, *.pyd)")
    parser.add_argument('--full_inspect', action='store_true') 
    args = parser.parse_args()
            
    cnt = library_import_check(args.filename, args.full_inspect, [])
    print(f"Errors detected: {cnt}")
