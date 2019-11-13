import sublime
import sublime_plugin


class BookmarkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        self.view.insert(edit, 0, "Hello, World!")
        print(selection)