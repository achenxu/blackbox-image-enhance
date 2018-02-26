import sys
import glob
import wx
import cv2

APP_EXIT = 1000


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        self.init_dir = kwargs['init_dir'] if 'init_dir' in kwargs else None
        del kwargs['init_dir']

        super(MainFrame, self).__init__(*args, **kwargs)
        self.list_view = None
        self.init_menu()
        self.init_ui()

    def init_menu(self):
        menubar = wx.MenuBar()
        file_menu = wx.Menu()

        m_about = file_menu.Append(wx.ID_ANY, '&About', 'About this progrram...')
        file_menu.AppendSeparator()
        m_open = file_menu.Append(wx.ID_ANY, '&Open\tCtrl+O', 'Open Directory')
        m_save = file_menu.Append(wx.ID_ANY, '&Save JSON\tCtrl+S', 'Save JSON Data File')
        file_menu.AppendSeparator()
        fquit = wx.MenuItem(file_menu, APP_EXIT, '&Quit\tCtrl+Q')

        menubar.Append(file_menu, '&File')
        self.SetMenuBar(menubar)

        # self.statusbar = self.CreateStatusBar()
        # self.statusbar.SetStatusText('Ready')

    def init_ui(self):
        sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        ctrl = wx.BoxSizer(orient=wx.VERTICAL)

        self.list_view = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.list_view.AppendColumn("Filename")
        self.list_view.AppendColumn("Day/night")
        self.list_view.AppendColumn("FOI")
        self.list_view.AppendColumn("Pos")
        ctrl.Add(self.list_view)

        cmd_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        edit_btn = wx.Button(self, label="Edit This File")
        #edit_btn.Bind(wx.EVT_BUTTON, self.on_edit)
        cmd_sizer.Add(edit_btn)
        ctrl.Add(cmd_sizer)

        sizer.Add(ctrl, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)
        self.Show(True)

    def load_files(self):
        self.list_view.DeleteAllItems()
        if self.init_dir:
            files = glob.glob(self.init_dir + '/*.mp4')
            if len(files) == 0:
                return







    def on_edit_button(self, evt):
        pass


def main(init_dir):
    ex = wx.App()
    MainFrame(None, init_dir=init_dir)
    ex.MainLoop()


if __name__ == '__main__':
    init_dir = sys.argv[1] if len(sys.argv) > 1 else None

    main(init_dir)
