''' Imports '''
import wx
import os
import sys
import shutil
from SoundControl import *
from Constants import *

class GuiPrioritize(wx.Frame):
    
    
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel = wx.Panel(self, -1)
        self.priorityCat = {}
        self.boxPrioritized = wx.StaticBox(self.panel, -1, "Prioritized Sounds")
        self.boxLibrary = wx.StaticBox(self.panel, -1, "Sound Library")
        self.lblTitle = wx.StaticText(self.panel, -1, "Prioritize Sounds", style=wx.ALIGN_CENTRE)
        self.lblTitle.SetFont(wx.Font(26,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.treeLibrary = wx.TreeCtrl(self.panel, -1, style=wx.TR_HAS_BUTTONS|wx.TR_LINES_AT_ROOT|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER)
        self.treeLibrary.SetFont(wx.Font(18,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.lstPriority = wx.wx.ListBox(self.panel, -1, choices=[])
        self.lstPriority.SetFont(wx.Font(18,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnAccept = wx.Button(self.panel, -1, "Accept")
        self.btnAccept.SetFont(wx.Font(18,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnCancel = wx.Button(self.panel, -1, "Cancel")
        self.btnCancel.SetFont(wx.Font(18,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnAdd = wx.Button(self.panel, -1, " Add-->")
        self.btnAdd.SetFont(wx.Font(18,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        self.btnRemove = wx.Button(self.panel, -1, "<--Remove")
        self.btnRemove.SetFont(wx.Font(18,wx.DECORATIVE, wx.NORMAL, wx.NORMAL, 0, "Comic Sans MS"))
        
        self.Bind(wx.EVT_BUTTON, self.btnAcceptPressed, self.btnAccept)
        self.Bind(wx.EVT_BUTTON, self.btnCancelPressed, self.btnCancel)
        self.Bind(wx.EVT_BUTTON, self.btnAddPressed, self.btnAdd)
        self.Bind(wx.EVT_BUTTON, self.btnRemovePressed, self.btnRemove)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.treeLibrarySelected, self.treeLibrary)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.treeLibrarySelected, self.treeLibrary)
        self.Bind(wx.EVT_LISTBOX, self.lstPrioritySelected, self.lstPriority)
        self.Bind(wx.EVT_SHOW, self.onShow)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle("Sami Says")
        self.SetPosition((0,0))
        self.SetSize(wx.DisplaySize())

    def __do_layout(self):
        szrMain = wx.BoxSizer(wx.VERTICAL)
        szrBody = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrBoxes = wx.BoxSizer(wx.HORIZONTAL)
        szrPriority = wx.StaticBoxSizer(self.boxPrioritized, wx.HORIZONTAL)
        szrAddRemove = wx.BoxSizer(wx.VERTICAL)
        szrLibrary = wx.StaticBoxSizer(self.boxLibrary, wx.HORIZONTAL)
        szrMain.Add(self.lblTitle, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        szrBoxes.Add((10, 10), 0, 0, 0)
        szrLibrary.Add(self.treeLibrary, 1, wx.EXPAND, 0)
        szrBoxes.Add(szrLibrary, 1, wx.EXPAND, 0)
        szrBoxes.Add((10, 10), 0, 0, 0)
        szrAddRemove.Add((10, 10), 4, 0, 0)
        szrAddRemove.Add(self.btnAdd, 1, wx.EXPAND, 0)
        szrAddRemove.Add((10, 10), 0, 0, 0)
        szrAddRemove.Add(self.btnRemove, 1, wx.EXPAND, 0)
        szrAddRemove.Add((10, 10), 4, 0, 0)
        szrBoxes.Add(szrAddRemove, 0, wx.EXPAND, 0)
        szrBoxes.Add((10, 10), 0, 0, 0)
        szrPriority.Add(self.lstPriority, 1, wx.EXPAND, 0)
        szrBoxes.Add(szrPriority, 1, wx.EXPAND, 0)
        szrBoxes.Add((10, 10), 0, 0, 0)
        szrMain.Add(szrBoxes, 1, wx.EXPAND, 0)
        szrBody.Add((10, 10), 0, 0, 0)
        szrButtons.Add((10, 10), 0, 0, 0)
        szrButtons.Add(self.btnAccept, 1, wx.EXPAND, 0)
        szrButtons.Add((10, 10), 0, 0, 0)
        szrButtons.Add(self.btnCancel, 1, wx.EXPAND, 0)
        szrButtons.Add((10, 10), 0, 0, 0)
        szrBody.Add(szrButtons, 1, wx.EXPAND, 0)
        szrBody.Add((10, 10), 0, 0, 0)
        szrMain.Add(szrBody, 0, wx.EXPAND, 0)
        szrMain.Add((20, 20), 0, 0, 0)
        self.panel.SetSizer(szrMain)
        self.panel.Layout()
        self.Layout()
        self.populateTree()
        
    '''
    ' setEnv - sets self.env to the specified dictionary
    '''
    def setEnv(self,env): 
        self.env = env 
        
    '''
    ' onClose - Function for handing the close event.
    '''
    def onClose(self, event):
        dialog = wx.MessageDialog(None,'Are you sure you want to leave?','Sami Says',wx.YES_NO | wx.ICON_EXCLAMATION)
        if dialog.ShowModal() == wx.ID_YES:
            dialog.Destroy()
            sys.exit()
        else:
            dialog.Destroy()
    
    def onShow(self, event):
        self.populateTree()
        self.populateList()
        
    def populateTree(self):
        self.treeLibrary.DeleteAllItems()
        self.treeRoot = self.treeLibrary.AddRoot("Sound Library")
        self.treeNodes = []
        directory = os.listdir(SOUND_DIR)
        if '.svn' in directory:
            directory.remove('.svn') # Ignore SVN files
        if 'assigned sounds' in directory:
            directory.remove('assigned sounds')
        for i in directory:
            self.treeNodes.append(self.treeLibrary.AppendItem(self.treeRoot,i))
        for i in self.treeNodes:
            dir = os.listdir(SOUND_DIR + self.treeLibrary.GetItemText(i))
            if '.svn' in dir:
                dir.remove('.svn') # Ignore SVN files
            for e in dir:
                self.treeLibrary.AppendItem(i,e)
        self.treeLibrary.Expand(self.treeRoot)
    
    def populateList(self):
        directory = os.listdir(SOUND_DIR + ASSIGN_DIR)
        if '.svn' in directory:
            directory.remove('.svn')
        self.lstPriority.SetItems(directory)
        for file in directory:
            self.priorityCat[file] = ASSIGN_DIR + file
        
    def lstPrioritySelected(self,event):
        fileName = self.lstPriority.GetItems()[self.lstPriority.GetSelection()]
        if fileName in self.priorityCat.keys():
            self.env['SoundControl'].stopPlay()
            self.env['SoundControl'].playSoundFile(SOUND_DIR + self.priorityCat[fileName])
        else:()
        
    def btnAcceptPressed(self, event):
        directory = os.listdir(SOUND_DIR + ASSIGN_DIR)
        if '.svn' in directory:
            directory.remove('.svn')
        for file in directory:
            try:
                if file in self.priorityCat.keys():
                    if ASSIGN_DIR in self.priorityCat[file]:()
                        # do nothinng
                    else:()
                        # do nothing
                else:
                    if ASSIGN_DIR in self.priorityCat[file]:()
                        # do nothing
                    else:
                        os.remove(SOUND_DIR + ASSIGN_DIR + file)
            except(KeyError):
                os.remove(SOUND_DIR + ASSIGN_DIR + file)
        for file in self.priorityCat.values():
            if ASSIGN_DIR in file:()
                # do nothing
            else:
                shutil.copy(SOUND_DIR + file,SOUND_DIR + ASSIGN_DIR)
        self.btnCancelPressed(None)
        
        
        
    def btnCancelPressed(self, event):
        self.Hide()
        self.env['guiStart'].Show()
    
    def btnAddPressed(self, event):
        selectId = self.treeLibrary.GetSelection()
        fileName = self.treeLibrary.GetItemText(selectId)
        if fileName[-4:] == ".mp3": # handling file adds
            parentId = self.treeLibrary.GetItemParent(selectId)
            itemList = self.lstPriority.GetItems()
            if fileName in itemList:
                return
            else:
                itemList = itemList + [fileName]
                self.lstPriority.SetItems(itemList)
                self.priorityCat[fileName] = self.treeLibrary.GetItemText(parentId) + "/" + fileName
        elif fileName == "Sound Library": # handling attempted add of everything
            return
        else: # handling category adds
            children = os.listdir(SOUND_DIR + fileName)
            if '.svn' in children:
                children.remove('.svn')
            itemList = self.lstPriority.GetItems()
            for child in children:
                 if child in itemList:()
                 else:
                     itemList = itemList + [child]
                     self.priorityCat[child] = fileName + "/" + child
            self.lstPriority.SetItems(itemList)
            
                
    
    def btnRemovePressed(self, event):
        itemList = self.lstPriority.GetItems()
        self.priorityCat.pop(itemList[self.lstPriority.GetSelection()])
        itemList.pop(self.lstPriority.GetSelection())
        self.lstPriority.SetItems(itemList)
                
    
    def treeLibrarySelected(self, event):
        selectId = self.treeLibrary.GetSelection()
        fileName = self.treeLibrary.GetItemText(selectId)
        if fileName[-4:] == ".mp3":
            parentId = self.treeLibrary.GetItemParent(selectId)
            self.env['SoundControl'].stopPlay()
            self.env['SoundControl'].playSoundFile(SOUND_DIR + self.treeLibrary.GetItemText(parentId) + "/" + fileName)
        

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    GuiPrioritize = GuiPrioritize(None, -1, "")
    app.SetTopWindow(GuiPrioritize)
    GuiPrioritize.Show()
    app.MainLoop()
