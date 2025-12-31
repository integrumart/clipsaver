# -*- coding: utf-8 -*-
import os
import ui
import globalPluginHandler
import scriptHandler
import time
import api
import wx
import addonHandler

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super().__init__()
		self.save_path = os.path.join(os.path.expanduser("~"), "Documents", "Volkan_Clipboard_Records")
		if not os.path.exists(self.save_path):
			os.makedirs(self.save_path, exist_ok=True)
		self.last_clipboard_text = ""
		self.timer = wx.Timer()
		self.timer.Bind(wx.EVT_TIMER, self.check_clipboard)
		self.timer.Start(500)

	def check_clipboard(self, event=None):
		try:
			text = api.getClipData()
			if text and isinstance(text, str) and text.strip() != self.last_clipboard_text:
				self.last_clipboard_text = text.strip()
				self.save_to_file(text.strip())
		except: pass

	def save_to_file(self, text):
		try:
			timestamp = time.strftime("%Y%m%d_%H%M%S")
			prefix = "".join([c for c in text[:15] if c.isalnum()]).strip() or "clip"
			filename = f"clip_{timestamp}_{prefix}.txt"
			full_path = os.path.join(self.save_path, filename)
			with open(full_path, "w", encoding="utf-8") as f:
				f.write(text)
			ui.message(_("Copied text saved."))
		except: pass

	def terminate(self):
		if hasattr(self, 'timer') and self.timer.IsRunning():
			self.timer.Stop()
		super().terminate()