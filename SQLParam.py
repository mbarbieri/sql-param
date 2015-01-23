import re

import sublime
import sublime_plugin
from datetime import datetime

class SqlParamCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        text = view.substr(sublime.Region(0, view.size()))

        query_region = sublime.Region(0, view.find("-----",0).begin())
        self.remove_newlines(edit, query_region)
        params_strings = view.find_all("^PARAM", sublime.IGNORECASE)

        params = {}

        for param in params_strings:
            line = view.substr(view.full_line(param))
            m =re.match(r"^PARAM (\d+) (.*)", line)
            try:
                date = datetime.strptime(m.group(2)[0:19], '%Y-%m-%d %H:%M:%S')
                params[int(m.group(1))] = "'" + date.strftime('%d-%m-%Y') + "'"
            except ValueError as e:
                params[int(m.group(1))] = m.group(2)

        i = 0
        while view.find("\\?", 0):
            region = view.find("\\?", 0)
            view.replace(edit, region, params[i])
            i += 1

        view.run_command('sql_beautifier')
        self.comment_last_line(edit)

    def remove_newlines(self, edit, query_region):
        query_string_cleaned = self.view.substr(query_region).replace('\n','')
        self.view.replace(edit, query_region, query_string_cleaned)

    def comment_last_line(self, edit):
        last_line = self.view.line(self.view.size())
        self.view.replace(edit, last_line, '-- '+self.view.substr(last_line))
