<d>py-uacme</d>
<br/>
<sup>undetected privesc</sup>
<br/>
<a href="https://deepwiki.com/vertigo6622/py-uacme"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"></a>

---

the UACME project is a well-known open-source UAC bypass kit found on [github](https://github.com/hfiref0x/UACME). 

many of the methods contained within are non-functional on the latest windows 11 version, however, both **method 41 (ucmCMLuaUtilShellExecMethod)** and **method 59 (ucmDebugObjectMethod)** are still functional, and spawn an admin shell without any detection by windows defender.

despite this, the `akagi.exe` compiled which has these methods has long been signatured by microsoft and is now immediately removed from the disk upon detection. i have ported both these methods into python, where they are run by `python.exe` and execute successfully. this has been tested to still be fully working on **windows 11 24h2.** 

this works because python scripts are simply text files, and do not have the signature that compiled exes like `akagi.exe` have.

### usage: 

by default, both scripts open a python shell as administrator. to choose which exe to run, edit the main function of the script and place the executable you desire to run as admin here: `sys.exit(method41("python.exe"))` or `sys.exit(method59("python.exe"))`

then run this in powershell:

**method 59:** `.\python.exe method59.py`
**method 41:** `.\python.exe method41.exe`
