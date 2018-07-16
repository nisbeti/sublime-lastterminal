import os
import sys
import shlex
import ntpath
import subprocess
import sublime
import sublime_plugin
from time import sleep

class LastTerminalCommand(sublime_plugin.WindowCommand):
    def get_paths(self):
        file_name = self.window.active_view().file_name()

        directory = os.path.dirname(os.path.realpath(file_name))

        file_name = file_name.replace(' ', '\ ')

        active_view = self.window.active_view()

        return file_name, active_view, directory

    def get_current_function(self, view):
        sel = view.sel()[0]
        function_regions = view.find_by_selector('entity.name.function')
        cf = None
        for r in reversed(function_regions):
            if r.a < sel.a:
                cf = view.substr(r)
                break
        return cf

    def run_in_terminal(self, command):
        settings = sublime.load_settings("Preferences.sublime-settings")
        terminal_setting = settings.get('lastterminal-sublime-terminal', 'Terminal')

        autofocus = settings.get('lastterminal-sublime-autofocus', False)
        autofocus_delay = settings.get('lastterminal-sublime-autofocus-delay', 250)

        osascript_command = 'osascript '

        if terminal_setting == 'iTerm':
            osascript_command += self.path_to('open_iterm.applescript')
            osascript_command += ' "' + command + '"'
        else:
            osascript_command += self.path_to('run_command.applescript')
            osascript_command += ' "' + command + '"'
            osascript_command += ' "PHPUnit Tests"'

        os.system(osascript_command)

        if (autofocus):
            self.autofocus_sublime(autofocus_delay)

    def autofocus_sublime(self, delay):
        if delay > 0:
            sleep(delay / 1000.0)

        os.system(self.build_autofocus_cmd())

    def build_autofocus_cmd(self):
        osascript_cmd = 'osascript '
        osascript_cmd += self.path_to('tab_to_sublime.applescript')
        return osascript_cmd

    def path_to(self, file):
        return '"' + os.path.dirname(os.path.realpath(__file__)) + '/' + file + '"'

class RunLastTerminalCommand(LastTerminalCommand):

    def run(self, *args, **kwargs):
        file_name, active_view, directory = self.get_paths()

        self.run_in_terminal('!-1')
