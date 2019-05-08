import os


class SysCommand:
    @staticmethod
    def clear():
        try:
            os.system('clear')
        except:
            pass
