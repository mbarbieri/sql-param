import re

import sublime
import sublime_plugin

class SqlParamCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        text = view.substr(sublime.Region(0, view.size()))
        params_strings = view.find_all("^PARAM", sublime.IGNORECASE)

        params = {}

        for param in params_strings:
            line = view.substr(view.full_line(param))
            m =re.match(r"^PARAM (\d+) (.*)", line)
            params[int(m.group(1))] = m.group(2)

        print(view.find_all("\\?"))

        i = 0
        while view.find("\\?", 0):
            region = view.find("\\?", 0)
            print(str(i)+": replace "+view.substr(region) + " with "+params[i])
            view.replace(edit, region, params[i])
            i += 1

        view.run_command('sql_beautifier')

