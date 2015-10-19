import sublime
import sublime_plugin


class Settings:
    settings_base = 'Task Manager.sublime-settings'
    settings = {}

    @staticmethod
    def load():
        Settings.settings = sublime.load_settings(Settings.settings_base)

    @staticmethod
    def get_global(key, default=None):
        return Settings.settings.get(key, default)

    @staticmethod
    def get_project(key, default=None):
        window = sublime.active_window()
        project_data = window.project_data()
        if (project_data is not None and
                'tasks' in project_data):
            return project_data['tasks'].get(key, default)
