import os
import sys
import subprocess
import sublime
import sublime_plugin
from .Settings import Settings


class RunTasksCommand(sublime_plugin.WindowCommand):

    def __init__(self, window):
        self.settings = Settings()
        self.window = window

    def run(self, *args):
        self.tasks = self.settings.get_tasks()
        task_names = [t.get('caption') for t in self.tasks]
        self.window.show_quick_panel(task_names, self.on_selected)

    def on_selected(self, index):
        if index == -1:
            return

        task = self.tasks[index]
        if task['sublime-command']:
            self.window.run_command(task['command'], task['args'])
        else:
            folders = self.window.folders()
            if len(folders) > 1:
                def folders_selected(ind):
                    nonlocal cwd
                    cwd = folders[ind]
                self.window.show_quick_panel(folders, folders_selected)
            elif len(folders) == 1:
                cwd = folders[0]
            else:
                cwd = os.path.expanduser('~')
            print([task['command'], task['args']])
            process = subprocess.Popen([task['command'], task['args']],
                                       shell=False,
                                       cwd=cwd,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            out, err = process.communicate()
            encoding = self.settings.get_global('encoding', 'utf-8')
            out = out.decode(encoding)
            err = err.decode(encoding)
            if sublime.platform() == 'windows':
                out = out.replace('\r\n', '\n')
                err = err.replace('\r\n', '\n')
            content = out if err == '' else out + '\n\n>>> ERROR:\n' + err
            panel = self.window.create_output_panel('task_output')
            panel.settings().set('scroll_past_end', False)
            panel.settings().set('auto_indent', False)
            panel.set_read_only(False)
            panel.run_command('insert', {"characters": content})
            panel.set_read_only(True)
            self.window.run_command("show_panel",
                                    {"panel": "output.task_output"})
