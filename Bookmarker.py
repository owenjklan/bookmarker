import sublime
import sublime_plugin


bookmarks = []


def on_navigate(href_str):
    print(bookmarks[int(href_str)])


class Bookmark(object):
    def __init__(self, view, start_pos, content):
        self.start_pos = start_pos
        self.view_id = view.id()
        self.buffer_id = view.buffer_id()
        self.content = content
        self.tab_name = view.name()

    def __int__(self):
        return int(self.start_pos)

    def __str__(self):
        return "{}|{}".format(self.tab_name, self.start_pos)


class BookmarkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        self.view.insert(edit, 0, "")

        # Only use the first selection, ignore multiple
        sel = selection[0]
        line_region = self.view.line(sel)
        line_content = self.view.substr(line_region)
        bm = Bookmark(self.view, line_region.a, line_content)

        bookmarks.append(bm)


class ListBookmarksCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        bookmark_list = ["{}:{}".format(bm.start_pos, bm.content) for bm in bookmarks]
        self.view.window().show_quick_panel(bookmark_list, on_navigate)