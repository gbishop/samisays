''' Imports '''
from Story import *
from SoundControl import *
import sys
import wx
from Constants import *

class GuiVisualizer(wx.Frame):
    
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel = wx.Panel(self, -1)
        self.grpBoxInfo = wx.StaticBox(self.panel, -1, "Story Information")
        self.grpBoxInstruct = wx.StaticBox(self.panel, -1, "Instructions")
        self.title = wx.StaticText(self.panel, -1, 'Story Creation')
        self.instructions = wx.TextCtrl(self.panel, -1, 'Record more clips with the [space bar].  Navigate through clips with the [left and right arrows].  Insert sounds with the [down arrow].', style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_LINEWRAP)
        self.statsLabel = wx.StaticText(self.panel, -1, '')
        self.infoLabel = wx.StaticText(self.panel, -1, 'Story Information')
        self.instructionLabel = wx.StaticText(self.panel, -1, 'Instructions')
        
        # binding of events
        self.Bind(wx.EVT_KILL_FOCUS, self.handleFocus, self)
        self.Bind(wx.EVT_SHOW, self.handleShow, self)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        self.visible = False

        self.__set_properties()
        self.__do_layout()

        
    def __set_properties(self):
        # begin wxGlade: GuiVisualizer.__set_properties
        self.SetTitle("Sami Says")
        self.SetPosition((0,0))
        self.SetSize(wx.DisplaySize())
        self.title.SetFont(wx.Font(28, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.statsLabel.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.instructions.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.infoLabel.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.instructionLabel.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: GuiVisualizer.__do_layout
        title_boxesSizer = wx.BoxSizer(wx.VERTICAL)
        labelsSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxesSizer = wx.BoxSizer(wx.HORIZONTAL)
        informationSizer = wx.StaticBoxSizer(self.grpBoxInfo,wx.VERTICAL)
        instructionSizer = wx.StaticBoxSizer(self.grpBoxInstruct,wx.HORIZONTAL)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_sizer.Add((20, 20), 0, 0, 0)
        title_sizer.Add((20, 20), 0, 0, 0)
        title_sizer.Add((20, 20), 1, 0, 0)
        title_sizer.Add(self.title, 0, 0, 0)
        title_sizer.Add((20, 20), 1, 0, 0)
        title_sizer.Add((20, 20), 0, 0, 0)
        title_sizer.Add((20, 20), 0, 0, 0)
        title_boxesSizer.Add(title_sizer, 1, wx.EXPAND, 0)
        boxesSizer.Add((20, 20), 0, 0, 0)
        informationSizer.Add(self.statsLabel, 0, 0, 0)
        informationSizer.Add((20, 20), 0, 0, 0)
        boxesSizer.Add(informationSizer, 1, wx.EXPAND, 0)
        boxesSizer.Add((20, 20), 0, 0, 0)
        instructionSizer.Add(self.instructions, 1,wx.EXPAND,0)
        boxesSizer.Add(instructionSizer, 1, wx.EXPAND, 0)
        boxesSizer.Add((20, 20), 0, 0, 0)
        title_boxesSizer.Add(boxesSizer, 10, wx.EXPAND, 0)
        labelsSizer.Add((20, 20), 0, 0, 0)
        labelsSizer.Add(self.infoLabel, 0, 0, 0)
        labelsSizer.Add((20, 20), 1, 0, 0)
        labelsSizer.Add(self.instructionLabel, 0, 0, 0)
        labelsSizer.Add((20, 20), 0, 0, 0)
        title_boxesSizer.Add(labelsSizer, 1, wx.EXPAND, 0)
        self.panel.SetSizer(title_boxesSizer)
        self.Layout()
        self.panel.Layout()
        # end wxGlade
        
    def handleFocus(self, event):
        if self.visible:
            self.SetFocus()
    
    def handleShow(self, event):
        if not self.visible:
            self.updateStats()
        self.visible = not self.visible
        
    
    def setEnv(self,env): 
        self.env = env

    def setInstructions(self, instrText):
        self.instructions.SetLabel(instrText)

    def updateStats(self):
        story = self.env['story']
        stats = story.getStats()
        min,sec = getDuration(story.getStoryBytes())
        
        if min == 0:
            durInfo = 'Duration:  %.2f s\n\n' % (sec)
        else:
            durInfo = 'Duration:  %d m %.2f s\n\n' % (min, sec)
        
        if story.currClip == 0:
            clipInfo = 'Current Clip:  Title (of %d)\n\n' % (len(story)-1)
        else:
            clipInfo = 'Current Clip:  %d (of %d)\n\n' % (story.currClip, len(story)-1)
            
        statsInfo = ('Recorded Sounds: %d\nInserted Sounds:  %d\nManipulated Sounds:  %d\nLocked (Teacher) Sounds:  %d\nBreaks:  %d' 
                     % (stats[REC], stats[SND], stats[SFX], stats[LCK], stats[BRK]))
        self.statsLabel.SetLabel(durInfo + clipInfo + statsInfo)
        
    def onClose(self, event):
        dialog = wx.MessageDialog(None,'Are you sure you want to leave?','Sami Says',wx.YES_NO | wx.ICON_EXCLAMATION)
        if dialog.ShowModal() == wx.ID_YES:
            dialog.Destroy()
            sys.exit()
        else:
            dialog.Destroy()

# end of class GuiVisualizer


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_5 = GuiVisualizer(None, -1, "")
    app.SetTopWindow(frame_5)
    frame_5.Show()
    app.MainLoop()
