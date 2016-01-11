import sublime_plugin
import sublime
import os
from subprocess import Popen
try:
    import _winreg as winreg
except:
    import winreg

try:
    WINMERGE = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\WinMergeU.exe')
except:
    if os.path.isfile(os.path.join(os.environ['ProgramFiles(x86)'], "WinMerge", "WinMergeU.exe")):
        WINMERGE = os.path.join(os.environ['ProgramFiles(x86)'], "WinMerge", "WinMergeU.exe")
    elif os.path.isfile(os.path.join(os.environ['ProgramFiles'], "WinMerge", "WinMergeU.exe")):
        WINMERGE = os.path.join(os.environ['ProgramFiles'], "WinMerge", "WinMergeU.exe")
    elif os.path.isfile(os.path.join(os.path.dirname(os.path.dirname(sublime.executable_path())), "WinMergePortable", "WinMergePortable.exe")):
        WINMERGE = os.path.join(os.path.dirname(os.path.dirname(sublime.executable_path())), "WinMergePortable", "WinMergePortable.exe")
    else:
        # Hope it's in the path
        WINMERGE = '"WinMergeU.exe"'

fileA = fileB = None


def recordActiveFile(f):
    global fileA
    global fileB
    fileB = fileA
    fileA = f


class WinMergeCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        cmd_line = '%s /e /ul /ur "%s" "%s"' % (WINMERGE, fileA, fileB)
        print("WinMerge command: " + cmd_line)
        Popen(cmd_line)


class WinMergeFileListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        if view.file_name() != fileA:
            recordActiveFile(view.file_name())
