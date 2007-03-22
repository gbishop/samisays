
# system imports
import wx

# project imports
from Class import Class
from GuiStart import GuiStart
from GuiStories import GuiStories
from GuiStudents import GuiStudents

currentClass = Class()
currentClass.load()

app = wx.PySimpleApp(0)
wx.InitAllImageHandlers()
start = GuiStart(None, -1, "")
students = GuiStudents(None, -1, "")
stories = GuiStories(None,-1,"")
env = {'class': currentClass, 'guiStart': start, 'guiStudents': students, 'guiStories': stories}
start.setEnv(env)
students.setEnv(env)
stories.setEnv(env)
app.SetTopWindow(start)
start.Show()
app.MainLoop()

