from guiStart import *
import unittest

class guiStartSizeTest(unittest.TestCase):
	def runTest(self):
		app = wx.PySimpleApp(0)
		wx.InitAllImageHandlers()
		subject = guiStart(None, -1, "")
		assert subject.GetSize() == (289,336), 'incorrect default size'
		
if __name__ == "__main__":
	unittest.main()