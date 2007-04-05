#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import wx

class guiAssign(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: guiAssign.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel = wx.Panel(self, -1)
        self.sizer_2_staticbox = wx.StaticBox(self.panel, -1, "Students")
        self.list_box_1 = wx.ListBox(self.panel, -1, choices=[])
        self.btnAssign = wx.Button(self.panel, -1, "Assign")
        self.btnCancel = wx.Button(self.panel, -1, "Cancel")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: guiAssign.__set_properties
        self.SetTitle("Sami Says")
        self.SetSize((400, 500))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: guiAssign.__do_layout
        grid_sizer_1 = wx.FlexGridSizer(3, 3, 0, 0)
        grid_sizer_2 = wx.FlexGridSizer(3, 5, 0, 0)
        sizer_2 = wx.StaticBoxSizer(self.sizer_2_staticbox, wx.HORIZONTAL)
        grid_sizer_1.AddSpacer(-1)
        grid_sizer_1.AddSpacer(-1)
        grid_sizer_1.AddSpacer(-1)
        grid_sizer_1.AddSpacer(-1)
        sizer_2.Add(self.list_box_1, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(sizer_2, 1, wx.EXPAND, 1)
        grid_sizer_1.AddSpacer(-1)
        grid_sizer_1.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.Add(self.btnAssign, 0, wx.EXPAND, 0)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.Add(self.btnCancel, 0, wx.EXPAND, 0)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddSpacer(-1)
        grid_sizer_2.AddGrowableRow(1)
        grid_sizer_2.AddGrowableCol(1)
        grid_sizer_2.AddGrowableCol(3)
        grid_sizer_1.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        grid_sizer_1.AddSpacer(-1)
        self.panel.SetSizer(grid_sizer_1)
        grid_sizer_1.AddGrowableRow(1)
        grid_sizer_1.AddGrowableCol(1)
        self.panel.SetSizer(grid_sizer_1)
        self.Layout()
        # end wxGlade

# end of class guiAssign


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    test = guiAssign(None, -1, "")
    app.SetTopWindow(test)
    test.Show()
    app.MainLoop()
    test.Refresh()
