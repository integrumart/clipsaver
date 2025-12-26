import os
import ui
import globalPluginHandler
import time
import api
import wx

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        # Kayıt yolu: Belgelerim\Volkan_Kopyalama_Kayitlari
        self.save_path = os.path.join(os.path.expanduser("~"), "Documents", "Volkan_Kopyalama_Kayitlari")
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path, exist_ok=True)
            
        # Pano takibi için değişken
        self.last_clipboard_text = ""
        
        # NVDA'nın ana döngüsünde panoyu kontrol eden bir zamanlayıcı (timer) başlatalım
        self.timer = wx.PyTimer(self.check_clipboard)
        self.timer.Start(500)  # Her yarım saniyede bir kontrol eder (Sistemi yormaz)

    def check_clipboard(self):
        try:
            # Pano içeriğini al
            import api
            text = api.getClipData()
            
            # Eğer pano metin içeriyorsa ve son kaydettiğimizden farklıysa
            if text and isinstance(text, str) and text.strip() != self.last_clipboard_text:
                self.last_clipboard_text = text.strip()
                self.save_to_file(text.strip())
        except:
            pass

    def save_to_file(self, text):
        try:
            # Dosya adı için zaman damgası
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            # İlk 15 karakteri dosya adına ekle (Türkçe karakter ve boşlukları temizler)
            prefix = "".join([c for c in text[:15] if c.isalnum()]).strip()
            filename = f"kopya_{timestamp}_{prefix}.txt"
            full_path = os.path.join(self.save_path, filename)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(text)
            
            # Kayıt başarılı bildirimi (Sadece NVDA konuşur, ekranı meşgul etmez)
            ui.message("Kopyalanan metin kaydedildi.")
        except:
            pass

    def terminate(self):
        # Eklenti durduğunda zamanlayıcıyı kapat
        self.timer.Stop()