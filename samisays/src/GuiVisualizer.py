''' Imports '''
from Story import *
from SoundControl import *
from SoundLibrary import *
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
        self.grpBoxClipInfo = wx.StaticBox(self.panel, -1, "Sound Library Information")
        self.grpBoxRecording = wx.StaticBox(self.panel, -1, 'Recording')
        self.title = wx.StaticText(self.panel, -1, 'Story Creation')
        self.instructions = wx.TextCtrl(self.panel, -1, 'Record more clips with the [space bar].  Navigate through clips with the [left and right arrows].  Insert sounds with the [down arrow].', style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_LINEWRAP)
        self.statsLabel = wx.StaticText(self.panel, -1, '')
        self.soundLibLabel = wx.StaticText(self.panel, -1, '')
        self.imgRecOff = wx.Image("art/rec_off.png", wx.BITMAP_TYPE_PNG)
        self.imgRecOn = wx.Image("art/rec_on.png", wx.BITMAP_TYPE_PNG)
        self.picRecord = wx.StaticBitmap(self.panel, -1, wx.NullBitmap)
        self.recOff()
        #self.infoLabel = wx.StaticText(self.panel, -1, 'Story Information')
        #self.instructionLabel = wx.StaticText(self.panel, -1, 'Instructions')
        
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
        self.title.SetFont(wx.Font(22, wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.statsLabel.SetFont(wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.soundLibLabel.SetFont(wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.instructions.SetFont(wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        #self.infoLabel.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        #self.instructionLabel.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: GuiVisualizer.__do_layout
        title_boxesSizer = wx.BoxSizer(wx.VERTICAL)
        labelsSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxesSizer = wx.BoxSizer(wx.HORIZONTAL)
        informationSizer = wx.StaticBoxSizer(self.grpBoxInfo,wx.VERTICAL)
        instructionSizer = wx.StaticBoxSizer(self.grpBoxInstruct,wx.HORIZONTAL)
        clipSizer = wx.StaticBoxSizer(self.grpBoxClipInfo,wx.HORIZONTAL)
        recBtnSizer = wx.StaticBoxSizer(self.grpBoxRecording,wx.HORIZONTAL)
        recBtnSizer.Add(self.picRecord,1,wx.EXPAND,0)
        recSizer = wx.BoxSizer(wx.VERTICAL)
        recSizer.Add((20, 20), 1, 0, 0)
        recSizer.Add((20, 20), 2, 0, 0)
        recSizer.Add(recBtnSizer,0,wx.EXPAND,0)
        recSizer.Add((20, 20), 1, 0, 0)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_sizer.Add((20, 20), 0, 0, 0)
        title_sizer.Add((20, 20), 0, 0, 0)
        title_sizer.Add((20, 20), 1, 0, 0)
        title_sizer.Add(self.title, 0, 0, 0)
        title_sizer.Add((20, 20), 1, 0, 0)
        title_sizer.Add((20, 20), 0, 0, 0)
        title_sizer.Add((20, 20), 0, 0, 0)
        title_boxesSizer.Add(title_sizer, 1, wx.EXPAND, 0)
        title_boxesSizer.Add((5, 5), 0, 0, 0)
        boxesSizer.Add((20, 20), 0, 0, 0)
        informationSizer.Add(self.statsLabel, 0, 0, 0)
        informationSizer.Add((20, 20), 0, 0, 0)
        boxesSizer.Add(informationSizer, 1, wx.EXPAND, 0)
        boxesSizer.Add((20, 20), 0, 0, 0)
        boxesSizer.Add(recSizer, 0, wx.EXPAND,0)
        boxesSizer.Add((20, 20), 0, 0, 0)
        clipSizer.Add(self.soundLibLabel, 1, wx.EXPAND, 0)
        boxesSizer.Add(clipSizer,1,wx.EXPAND, 0)
        instructionSizer.Add(self.instructions, 1,wx.EXPAND,0)
        boxesSizer.Add((20, 20), 0, 0, 0)
        title_boxesSizer.Add(boxesSizer, 10, wx.EXPAND, 0)
        '''labelsSizer.Add((20, 20), 0, 0, 0)
        labelsSizer.Add(self.infoLabel, 0, 0, 0)
        labelsSizer.Add((20, 20), 1, 0, 0)
        labelsSizer.Add(self.instructionLabel, 0, 0, 0)
        labelsSizer.Add((20, 20), 0, 0, 0)
        title_boxesSizer.Add(labelsSizer, 1, wx.EXPAND, 0) '''
        title_boxesSizer.Add(instructionSizer, 4, wx.EXPAND, 0)
        title_boxesSizer.Add((40, 40), 0, 0, 0)
        self.panel.SetSizer(title_boxesSizer)
        self.Layout()
        self.panel.Layout()
        # end wxGlade
        
    def recOn(self):
        self.picRecord.SetBitmap(wx.BitmapFromImage(self.imgRecOn))
        
    def recOff(self):
        self.picRecord.SetBitmap(wx.BitmapFromImage(self.imgRecOff))
        
    def handleFocus(self, event):
        if self.visible:
            self.SetFocus()
    
    def handleShow(self, event):
        if not self.visible:
            self.updateStats()
            self.updateLibraryStats()
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
        
    def updateLibraryStats(self):
        SL = self.env['soundLibrary']
        mode = self.env['auiInsertSound'].mode
        
        if mode == STORY_MODE:
            self.soundLibLabel.SetLabel('')
            return
        
        soundIndex = ''
        soundFileName = ''
        soundName = ''
        
        splitCatName = SL.getCurrCatName().split(' ')
        splitCatName = [w.capitalize() for w in splitCatName]
        catName = ' '.join(splitCatName)
        
        if mode == SND_MODE:
            if SL.currCat == SL.sfxCat :
                soundIndex = '%d (of %d)' % (SL.SFX.currSFX+1, len(SL.SFX.sfxList))
            else :
                soundIndex = '%d (of %d)' % (SL.currSound+1, SL.getCatLen(SL.currCat))
            soundFileName = SL.getCurrSoundName()
            splitFileName = soundFileName.split('.')
            splitSoundName = splitFileName[0].split(' ')
            splitSoundName = [w.capitalize() for w in splitSoundName]
            soundName = ' '.join(splitSoundName)
            
        catLabel = 'Category:  %s\n\n' % (catName)
        indexLabel = 'Sound:  %s\n\n' % (soundIndex)
        nameLabel = 'Name:  %s\n\n' % (soundName)
        
        self.soundLibLabel.SetLabel(catLabel + indexLabel + nameLabel)
        
        
    def onClose(self, event):
        dialog = wx.MessageDialog(None,'Are you sure you want to leave?','Sami Says',wx.YES_NO | wx.ICON_EXCLAMATION)
        if dialog.ShowModal() == wx.ID_YES:
            dialog.Destroy()
            sys.exit()
        else:
            self.SetFocus()
            dialog.Destroy()

# end of class GuiVisualizer


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_5 = GuiVisualizer(None, -1, "")
    app.SetTopWindow(frame_5)
    frame_5.Show()
    app.MainLoop()
