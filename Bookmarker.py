import sublime
import sublime_plugin


bookmarks = {}


def on_navigate(bookmark_index):
    """
    Takes an index into the 'bookmarks_list' global, which is
    re-created each time the list of bookmarks is requested.
    """
    index = int(bookmark_index)
    target_view = bookmark_list[index]
    print("target_view: ", target_view)
    sublime.active_window().focus_view(target_view)
    sublime.active_window().active_view().show(target_view.start_pos)


class Bookmark(object):
    def __init__(self, view, start_pos, content):
        self.start_pos = start_pos
        self.line_number = view.rowcol(start_pos)[0] + 1
        self.view_id = view.id()
        self.view = view
        self.buffer_id = view.buffer_id()
        self.content = content
        self.tab_name = view.file_name()
        if self.tab_name is None:
            self.tab_name = "Untitled"
        elif '/' in self.tab_name:
            self.tab_name = self.tab_name.rsplit('/', 1)[1]

    def __int__(self):
        return int(self.start_pos)

    def __str__(self):
        return "{}|{}".format(self.tab_name, self.line_number)


class BookmarkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        self.view.insert(edit, 0, "")

        # Only use the first selection, ignore multiple
        sel = selection[0]
        line_region = self.view.line(sel)
        line_content = self.view.substr(line_region)
        bm = Bookmark(self.view, line_region.a, line_content)

        self.view.add_regions("bm", [line_region], icon="dot")

        if self.view.id() not in bookmarks:
            bookmarks[self.view.id()] = [bm]
        else:
            bookmarks[self.view.id()].append(bm)

def jump_to_bookmark(self, edit):
    target_bookmark = bookmarks[int(index)]
    self.window.focus_view(target_bookmark)
    self.window.active_view().show(target_bookmark.start_pos)

bookmark_list = []

class ListBookmarksCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global bookmark_list
        bookmark_list = []
        for view_id, bm_list in bookmarks.items():
            for bm in bm_list:
                print(view_id, bm.tab_name, bm.start_pos)
                bookmark_list.append(bm)

        if len(bookmark_list) > 0:
            self.view.window().show_quick_panel(
                ["{}: {}: {}".format(bm.tab_name, bm.line_number, bm.content) for bm in bookmark_list], on_navigate)