import sublime
import sublime_plugin


class Settings:
    settings_base = 'TaskManager.sublime-settings'

    def __init__(self):
        self.settings = sublime.load_settings(Settings.settings_base)

    def get_tasks(self):
        tasks = self.settings.get('builtin-tasks')
        user_tasks = self.settings.get('user-tasks', None)
        if user_tasks:
            tasks.extend(user_tasks)
        window = sublime.active_window()
        project_data = window.project_data()
        if project_data and 'proj-tasks' in project_data:
            tasks.extend(project_data['proj-tasks'])
        return tasks

    def get_global(self, key, default=None):
        return self.settings.get(key, default)

    def get_project(self, key, default=None):
        window = sublime.active_window()
        project_data = window.project_data()
        if (project_data is not None):
            return project_data.get(key, default)
        else:
            return default
