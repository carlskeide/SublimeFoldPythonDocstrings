import sublime
import sublime_plugin
import re

def fold_comments(view):
    number_lines_to_fold = view.settings().get("fold_python_docstrings_number_of_lines", 1)
    for region in view.find_by_selector('string.quoted.double.block, string.quoted.single.block'):
        lines = view.lines(region)
        if len(lines) > 1:
            region = sublime.Region(lines[0].begin(), lines[-1].end())
            text = view.substr(region).strip()
            if re.match(r"""^[rub]{0,2}["']{3}""", text, re.IGNORECASE):
                fold_region = sublime.Region(lines[number_lines_to_fold-1].end(), lines[-1].end() - 3)
                view.fold(fold_region)


class FoldFilePythonDocstrings(sublime_plugin.EventListener):
    def on_load(self, view):
        if view.settings().get("fold_python_docstrings_onload", True):
            fold_comments(view)


class FoldPythonDocstringsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fold_comments(self.view)


class UnfoldPythonDocstringsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.unfold(self.view.find_by_selector('string'))
