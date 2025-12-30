import os
import ui
import globalPluginHandler
import time
import api
import wx
import addonHandler

# Dil desteği başlatılıyor
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		# Kayıt yolu: Documents\Volkan_Clipboard_Records
		self.save_path = os.path.join(os.path.expanduser("~"), "Documents", "Volkan_Clipboard_Records")
		if not os.path.exists(self.save_path):
			os.makedirs(self.save_path, exist_ok=True)
			
		self.last_clipboard_text = ""
		
		# Zamanlayıcı başlatılıyor
		self.timer = wx.PyTimer(self.check_clipboard)
		self.timer.Start(500)

	def check_clipboard(self):
		try:
			text = api.getClipData()
			if text and isinstance(text, str) and text.strip() != self.last_clipboard_text:
				self.last_clipboard_text = text.strip()
				self.save_to_file(text.strip())
		except Exception:
			pass

	def save_to_file(self, text):
		try:
			timestamp = time.strftime("%Y%m%d_%H%M%S")
			# Dosya adı için güvenli prefix oluşturma
			prefix = "".join([c for c in text[:15] if c.isalnum()]).strip()
			if not prefix:
				prefix = "clip"
			
			filename = f"clip_{timestamp}_{prefix}.txt"
			full_path = os.path.join(self.save_path, filename)

			with open(full_path, "w", encoding="utf-8") as f:
				f.write(text)
			
			# Bildirim mesajı yerelleştirildi
			ui.message(_("Copied text saved."))
		except Exception:
			pass

	def terminate(self):
		if hasattr(self, 'timer'):
			self.timer.Stop()