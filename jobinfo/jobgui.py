import subprocess
import wx
from operator import itemgetter
from jobinfo import JobInfo


class MyTable(wx.Panel):
    def __init__(self, parent, jobs_head, sub_frame):
        self.jobs_head = jobs_head
        self.name_list = self.get_sorted_list('Date', sub_frame)
        self.reverse_sort_flag = [True, False, True, True, True, True, True]
        self.index = -1     # Must initialized to be -1!!!!

        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.row_obj_dict = {}

        self.list_ctrl = wx.ListCtrl(self, size=(-1, 500),
                                     style=wx.LC_REPORT | wx.BORDER_SUNKEN)

        self.list_ctrl.InsertColumn(0, '#', width=30)
        self.list_ctrl.InsertColumn(1, 'Date', width=80)
        self.list_ctrl.InsertColumn(2, 'Company', width=140)
        self.list_ctrl.InsertColumn(3, 'Position', width=240)
        self.list_ctrl.InsertColumn(4, 'Folder', width=240)
        self.list_ctrl.InsertColumn(5, 'File', width=240)
        self.list_ctrl.InsertColumn(6, 'Ext', width=50)
        main_sizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        self.show_list()

        self.list_ctrl.Bind(wx.EVT_LIST_COL_CLICK, self.col_press)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.row_press)
        self.list_ctrl.Bind(wx.EVT_LEFT_DCLICK, self.row_double_press)

        edit_button = wx.Button(self, label='Exit')
        edit_button.Bind(wx.EVT_BUTTON, self.on_press)
        main_sizer.Add(edit_button, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(main_sizer)

    def col_press(self, event):
        i = event.GetColumn()
        if 1 <= i <= 6:
            self.list_ctrl.DeleteAllItems()
            self.reverse_sort_flag[i] = not self.reverse_sort_flag[i]

            #self.name_list.sort(key=lambda x: x[i], reverse=self.reverse_sort_flag[i])
            self.name_list.sort(key=itemgetter(i), reverse=self.reverse_sort_flag[i])
            self.show_list()

    def row_press(self, event):
        self.index = event.GetIndex()

    def row_double_press(self, event):
        if self.index != -1:
            folder_name = self.name_list[self.index][4]
            file_name = self.name_list[self.index][5]
            file_ext = self.name_list[self.index][6]

            # Open DOC with its default desktop App
            cmd = f'{folder_name}\\"{file_name}"{file_ext}'
            print("TC", cmd)
            subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

            self.index = -1

    @staticmethod
    def on_press(event):
        event.Destroy()     # This exits all open windows.
                            # Note: the exit code isn't zero.
                            # But for the purpose of the script, who cares at that point.

    def show_list(self):
        index = 0
        row_cnt = 1
        for name in self.name_list:
            self.list_ctrl.InsertItem(index, f'{row_cnt}')
            self.list_ctrl.SetItem(index, 1, name[1])
            self.list_ctrl.SetItem(index, 2, name[2])
            self.list_ctrl.SetItem(index, 3, name[3])
            self.list_ctrl.SetItem(index, 4, name[4])
            self.list_ctrl.SetItem(index, 5, name[5])
            self.list_ctrl.SetItem(index, 6, name[6])
            index += 1
            row_cnt += 1

    def get_sorted_list(self, item_name, sub_frame, reverse_flag=False):
        if sub_frame is True:
            value = self.jobs_head.get_search_value()
            name_list = self.jobs_head.jobs_search_by(item_name, value, reverse_flag)
        else:
            name_list = self.jobs_head.jobs_sorted_by(item_name)
        return name_list


class DisplayFrame(wx.Frame):
    def __init__(self, jobs_head, title_str, sub_frame=False):
        super().__init__(parent=None, title=title_str, size=(600, 600),
                         style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)

        self.panel = MyTable(self, jobs_head, sub_frame)
        self.Show()


class DialogFrame(wx.Frame):
    def __init__(self, jobs_head, title_str):
        self.jobs_head = jobs_head
        self.title_str = title_str
        self.search_value = ''

        super().__init__(parent=None, title="Enter Company Name to Search For",
                         pos=(600, 500), size=(400, 120),
                         style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)

        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        my_btn = wx.Button(panel, label="Press Me")
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(my_sizer)

        self.Show()

    def on_press(self, event):
        v = self.text_ctrl.GetValue()
        search_value = v.strip()

        self.jobs_head.set_search_value(search_value)
        table = DisplayFrame(self.jobs_head, self.title_str, sub_frame=True)


if __name__ == '__main__':
    app = wx.App()

    jobs = JobInfo("c:\\Users\\toddd\\Home\\Todd\\Resume\\JobApplied")
    frame1 = DisplayFrame(jobs, 'Jobs Applied Table (Long Form)')
    frame2 = DialogFrame(jobs, 'Searched List')

    app.MainLoop()
