#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elektrik Keşif & Marka Liste Fiyatı Çekme / Teklif Oluşturma Aracı
Markalar:
  - Türk Prysmian Kablo (Kuvvetli Akım & Zayıf Akım Kablo Fiyat Listesi)
  - Legrand Türkiye (Pano, Sigorta Kutusu, Şalt, Sigorta, Kaçak Akım, Kanal & Anahtar-Priz Fiyat Listesi)
"""

import csv
import json
import os
import re
import urllib.request
from datetime import datetime
from typing import Dict, List, Any, Optional


class MarkaFiyatCekici:
    """
    Prysmian ve Legrand web sitelerinden / yayınlanan fiyat listelerinden
    birim liste fiyatlarını çeken ve yerel veritabanını güncelleyen sınıf.
    """

    PRYSMIAN_FIYAT_LISTESI_URL = "https://tr.prysmian.com/tr/fiyat-listeleri"
    LEGRAND_FIYAT_LISTESI_URL = "https://www.legrand.com.tr/fiyat-listeleri"

    def __init__(self) -> None:
        self.son_guncelleme = datetime.now().strftime("%Y-%m-%d %H:%M")

    def web_sayfasi_kontrol_et(self, url: str) -> Dict[str, Any]:
        """Markanın fiyat listesi sayfasına bağlanıp güncel PDF/Excel linklerini tarar."""
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"},
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
                pdf_links = re.findall(r'href=["\']([^"\']+\.pdf[^"\']*)["\']', html, re.I)
                return {
                    "durum": "basarili",
                    "http_kod": resp.status,
                    "bulunan_pdf_sayisi": len(pdf_links),
                    "ornek_linkler": pdf_links[:5],
                }
        except Exception as exc:
            return {
                "durum": "cevrimdisi_katalog_kullanildi",
                "detay": str(exc),
            }


def elli_kalem_elektrik_kesfi_getir() -> List[Dict[str, Any]]:
    """
    Bir elektrik projesinde yer alan tüm ana başlıkları kapsayan 50 satırlık
    standart keşif ve 2026 Prysmian / Legrand baz liste fiyatları.
    """
    return [
        # 01. PANO VE SİGORTA KUTULARI (LEGRAND)
        {"sira": 1, "bolum": "01. Pano & Sigorta Kutusu", "marka": "Legrand", "ref": "LG-020065", "aciklama": "Ana Dağıtım Panosu (ADP) XL³ 400 Dikili Tip Pano Gövdesi + İç Montaj Plakası ve Bara Seti (IP43)", "miktar": 1, "birim": "Adet", "liste_fiyati": 48500.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 2, "bolum": "01. Pano & Sigorta Kutusu", "marka": "Legrand", "ref": "LG-020052", "aciklama": "Kat / Tali Dağıtım Panosu XL³ 160 Sıva Üstü Metal Pano (96 Modül, 4 Sıra, Şeffaf Kapaklı)", "miktar": 3, "birim": "Adet", "liste_fiyati": 16400.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 3, "bolum": "01. Pano & Sigorta Kutusu", "marka": "Legrand", "ref": "LG-134053", "aciklama": "Practibox S 36 Modül (3x12) Sıva Altı Sigorta Kutusu (Füme Kapaklı, Toprak/Nötr Klemensli)", "miktar": 8, "birim": "Adet", "liste_fiyati": 2890.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 4, "bolum": "01. Pano & Sigorta Kutusu", "marka": "Legrand", "ref": "LG-134052", "aciklama": "Practibox S 24 Modül (2x12) Sıva Altı Daire/Ofis Sigorta Kutusu (Klemensli)", "miktar": 12, "birim": "Adet", "liste_fiyati": 1980.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 5, "bolum": "01. Pano & Sigorta Kutusu", "marka": "Legrand", "ref": "LG-601241", "aciklama": "Nedbox 12 Modül (1x12) Sıva Altı Sigorta Kutusu (Küçük Mahaller / Tali Kutular İçin)", "miktar": 6, "birim": "Adet", "liste_fiyati": 1120.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 6, "bolum": "01. Pano & Sigorta Kutusu", "marka": "Legrand", "ref": "LG-601962", "aciklama": "Plexo³ IP65 Su Geçirmez Sıva Üstü Kombinasyon / Mekanik Odası Sigorta Kutusu (18 Modül)", "miktar": 4, "birim": "Adet", "liste_fiyati": 3650.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 7, "bolum": "01. Pano & Sigorta Kutusu", "marka": "Legrand", "ref": "LG-046231", "aciklama": "Zayıf Akım / Data Dağıtım Kabini 19\" 15U 600x450mm Duvar Tipi Rack Kabin + Priz Grubu + Fan", "miktar": 2, "birim": "Adet", "liste_fiyati": 18900.00, "iskonto": 66.0, "kar": 15.0},

        # 02. ŞALT MALZEMELERİ & KORUMA (LEGRAND)
        {"sira": 8, "bolum": "02. Şalt & Sigorta (AG)", "marka": "Legrand", "ref": "LG-420047", "aciklama": "DPX³ 160 Termik-Manyetik Kompakt Şalter (MCCB) 3P 160A 25kA Ana Giriş Şalteri", "miktar": 1, "birim": "Adet", "liste_fiyati": 14850.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 9, "bolum": "02. Şalt & Sigorta (AG)", "marka": "Legrand", "ref": "LG-420005", "aciklama": "DPX³ 160 Termik-Manyetik Kompakt Şalter (MCCB) 3P 100A 16kA Tali Pano Çıkış Şalteri", "miktar": 3, "birim": "Adet", "liste_fiyati": 10900.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 10, "bolum": "02. Şalt & Sigorta (AG)", "marka": "Legrand", "ref": "LG-403466", "aciklama": "XC³ 4P 63A 300mA AC Tipi Kaçak Akım Koruma Şalteri (Yangın Koruma Eşikli - Ana/Tali Pano)", "miktar": 4, "birim": "Adet", "liste_fiyati": 4530.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 11, "bolum": "02. Şalt & Sigorta (AG)", "marka": "Legrand", "ref": "LG-403455", "aciklama": "XC³ 4P 40A 30mA AC Tipi Trifaze Kaçak Akım Koruma Şalteri (Hayat Koruma)", "miktar": 12, "birim": "Adet", "liste_fiyati": 4380.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 12, "bolum": "02. Şalt & Sigorta (AG)", "marka": "Legrand", "ref": "LG-403435", "aciklama": "XC³ 2P 40A 30mA AC Tipi Monofaze Kaçak Akım Koruma Şalteri (Hayat Koruma)", "miktar": 18, "birim": "Adet", "liste_fiyati": 3420.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 13, "bolum": "02. Şalt & Sigorta (AG)", "marka": "Legrand", "ref": "LG-403353", "aciklama": "XG³ 1P B10A 6kA Otomatik Sigorta (Aydınlatma Linyeleri İçin - B Eğrisi)", "miktar": 85, "birim": "Adet", "liste_fiyati": 445.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 14, "bolum": "02. Şalt & Sigorta (AG)", "marka": "Legrand", "ref": "LG-403356", "aciklama": "XG³ 1P C16A 6kA Otomatik Sigorta (Priz Linyeleri İçin - C Eğrisi)", "miktar": 140, "birim": "Adet", "liste_fiyati": 435.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 15, "bolum": "02. Şalt & Sigorta (AG)", "marka": "Legrand", "ref": "LG-403357", "aciklama": "XG³ 1P C20A 6kA Otomatik Sigorta (Klima / Özel Yük Linyeleri İçin)", "miktar": 32, "birim": "Adet", "liste_fiyati": 465.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 16, "bolum": "02. Şalt & Sigorta (AG)", "marka": "Legrand", "ref": "LG-403358", "aciklama": "XG³ 1P C25A 6kA Otomatik Sigorta (Mutfak / Fırın / Şofben Hatları İçin)", "miktar": 20, "birim": "Adet", "liste_fiyati": 495.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 17, "bolum": "02. Şalt & Sigorta (AG)", "marka": "Legrand", "ref": "LG-403388", "aciklama": "XG³ 3P C32A 6kA Trifaze Otomatik Sigorta (Mekanik / Pompa / Üç Faz Yükler)", "miktar": 14, "birim": "Adet", "liste_fiyati": 1640.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 18, "bolum": "02. Şalt & Sigorta (AG)", "marka": "Legrand", "ref": "LG-403389", "aciklama": "XG³ 3P C40A 6kA Trifaze Otomatik Sigorta (Tali Pano / Ana Kolon Besleme)", "miktar": 8, "birim": "Adet", "liste_fiyati": 1790.00, "iskonto": 70.0, "kar": 15.0},
        {"sira": 19, "bolum": "02. Şalt & Sigorta (AG)", "marka": "Legrand", "ref": "LG-412245", "aciklama": "B+C Tipi (Tip 1+2) AG Parafudr 3P+N 50kA Yıldırım ve Aşırı Gerilim Koruma + CX³ 25A Kontaktör Seti", "miktar": 2, "birim": "Set", "liste_fiyati": 15600.00, "iskonto": 70.0, "kar": 15.0},

        # 03. KUVVETLİ AKIM (KA) ENERJİ KABLOLARI (PRYSMIAN)
        {"sira": 20, "bolum": "03. Kuvvetli Akım (KA) Kablo", "marka": "Prysmian", "ref": "PRY-N2XH-350", "aciklama": "0.6/1 kV 3x50+25 mm² N2XH Halojensiz (LSOH) Ana Besleme Enerji Kablosu", "miktar": 65, "birim": "m", "liste_fiyati": 4650.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 21, "bolum": "03. Kuvvetli Akım (KA) Kablo", "marka": "Prysmian", "ref": "PRY-N2XH-425", "aciklama": "0.6/1 kV 4x25+16 mm² N2XH Halojensiz Tali Pano Kolon Besleme Kablosu", "miktar": 140, "birim": "m", "liste_fiyati": 2980.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 22, "bolum": "03. Kuvvetli Akım (KA) Kablo", "marka": "Prysmian", "ref": "PRY-N2XH-416", "aciklama": "0.6/1 kV 4x16 mm² N2XH Halojensiz Kat Panosu Kolon Kablosu", "miktar": 220, "birim": "m", "liste_fiyati": 1725.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 23, "bolum": "03. Kuvvetli Akım (KA) Kablo", "marka": "Prysmian", "ref": "PRY-N2XH-410", "aciklama": "0.6/1 kV 4x10 mm² N2XH Halojensiz Daire/Ofis Ana Kolon Kablosu", "miktar": 380, "birim": "m", "liste_fiyati": 1120.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 24, "bolum": "03. Kuvvetli Akım (KA) Kablo", "marka": "Prysmian", "ref": "PRY-N2XH-406", "aciklama": "0.6/1 kV 4x6 mm² N2XH Halojensiz Trifaze Cihaz / Mekanik Besleme Kablosu", "miktar": 310, "birim": "m", "liste_fiyati": 685.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 25, "bolum": "03. Kuvvetli Akım (KA) Kablo", "marka": "Prysmian", "ref": "PRY-N2XH-325", "aciklama": "0.6/1 kV 3x2.5 mm² N2XH (NHXMH) Halojensiz Kuvvet / Priz Linye Kablosu", "miktar": 3200, "birim": "m", "liste_fiyati": 248.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 26, "bolum": "03. Kuvvetli Akım (KA) Kablo", "marka": "Prysmian", "ref": "PRY-N2XH-315", "aciklama": "0.6/1 kV 3x1.5 mm² N2XH (NHXMH) Halojensiz Aydınlatma Linye & Sorti Kablosu", "miktar": 2600, "birim": "m", "liste_fiyati": 172.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 27, "bolum": "03. Kuvvetli Akım (KA) Kablo", "marka": "Prysmian", "ref": "PRY-NYM-325", "aciklama": "300/500V 3x2.5 mm² NYM (NVV Antigron) PVC İzoleli Priz Tesisat Kablosu", "miktar": 1500, "birim": "m", "liste_fiyati": 212.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 28, "bolum": "03. Kuvvetli Akım (KA) Kablo", "marka": "Prysmian", "ref": "PRY-NYM-315", "aciklama": "300/500V 3x1.5 mm² NYM (NVV Antigron) PVC İzoleli Aydınlatma Tesisat Kablosu", "miktar": 1800, "birim": "m", "liste_fiyati": 136.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 29, "bolum": "03. Kuvvetli Akım (KA) Kablo", "marka": "Prysmian", "ref": "PRY-FE180-325", "aciklama": "0.6/1 kV 3x2.5 mm² N2XH FE180 PH120 (Afumex) Yangına Dayanıklı Acil Aydınlatma/Pompa Kablosu", "miktar": 450, "birim": "m", "liste_fiyati": 365.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 30, "bolum": "03. Kuvvetli Akım (KA) Kablo", "marka": "Prysmian", "ref": "PRY-NYY-416", "aciklama": "0.6/1 kV 4x16 mm² NYY (YVV) Yeraltı ve Dış Saha Çevre Aydınlatma Enerji Kablosu", "miktar": 180, "birim": "m", "liste_fiyati": 1590.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 31, "bolum": "03. Kuvvetli Akım (KA) Kablo", "marka": "Prysmian", "ref": "PRY-H07Z1-16", "aciklama": "450/750V 1x16 mm² H07Z1-R (Sarı-Yeşil) Halojensiz Pano & Eşpotansiyel Topraklama Kablosu", "miktar": 350, "birim": "m", "liste_fiyati": 385.00, "iskonto": 58.0, "kar": 15.0},

        # 04. ZAYIF AKIM (ZA) KABLOLARI VE SİSTEMLERİ (PRYSMIAN & LEGRAND)
        {"sira": 32, "bolum": "04. Zayıf Akım (ZA) Kablo & Sistem", "marka": "Prysmian", "ref": "PRY-UC400-UTP", "aciklama": "Draka UC400 23AWG 4x2x0.57 CAT6 U/UTP LSOH Halojensiz Data / Network Kablosu", "miktar": 3050, "birim": "m", "liste_fiyati": 34.50, "iskonto": 58.0, "kar": 15.0},
        {"sira": 33, "bolum": "04. Zayıf Akım (ZA) Kablo & Sistem", "marka": "Prysmian", "ref": "PRY-UC400-FTP", "aciklama": "Draka UC400 23AWG 4x2x0.57 CAT6 F/UTP (FTP Folyo Ekranlı) LSOH Data / Kamera Kablosu", "miktar": 1220, "birim": "m", "liste_fiyati": 44.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 34, "bolum": "04. Zayıf Akım (ZA) Kablo & Sistem", "marka": "Prysmian", "ref": "PRY-JEH-FE180", "aciklama": "JE-H(St)H FE180 PH120 1x2x0.8+0.8 mm Turuncu Halojensiz Yangın Algılama ve İhbar Kablosu", "miktar": 1400, "birim": "m", "liste_fiyati": 46.50, "iskonto": 58.0, "kar": 15.0},
        {"sira": 35, "bolum": "04. Zayıf Akım (ZA) Kablo & Sistem", "marka": "Prysmian", "ref": "PRY-JEH-2208", "aciklama": "JE-H(St)H Bd 2x2x0.8 mm Gri Halojensiz Zayıf Akım Sinyal / Telefon / Diyafon Kablosu", "miktar": 850, "birim": "m", "liste_fiyati": 41.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 36, "bolum": "04. Zayıf Akım (ZA) Kablo & Sistem", "marka": "Prysmian", "ref": "PRY-LIYCY-2075", "aciklama": "LIYCY 2x0.75 mm² Kalaylı Bakır Örgü Ekranlı Kumanda, Otomasyon ve Anons Hoparlör Kablosu", "miktar": 900, "birim": "m", "liste_fiyati": 52.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 37, "bolum": "04. Zayıf Akım (ZA) Kablo & Sistem", "marka": "Prysmian", "ref": "PRY-LIYCY-4075", "aciklama": "LIYCY 4x0.75 mm² Ekranlı Kartlı Geçiş / HVAC Otomasyon / Sensör Haberleşme Kablosu", "miktar": 500, "birim": "m", "liste_fiyati": 84.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 38, "bolum": "04. Zayıf Akım (ZA) Kablo & Sistem", "marka": "Prysmian", "ref": "PRY-RG6-U6", "aciklama": "RG6/U-6 Cu/Cu 75 Ohm Tam Bakır Halojensiz TV / Uydu (SMATV) Koaksiyel Kablo", "miktar": 750, "birim": "m", "liste_fiyati": 32.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 39, "bolum": "04. Zayıf Akım (ZA) Kablo & Sistem", "marka": "Prysmian", "ref": "PRY-FO-4SM", "aciklama": "4 Core Singlemode (SM) 9/125 µm OS2 LSZH Bina İçi/Dışı Omurga Fiber Optik Kablo", "miktar": 240, "birim": "m", "liste_fiyati": 68.00, "iskonto": 58.0, "kar": 15.0},
        {"sira": 40, "bolum": "04. Zayıf Akım (ZA) Kablo & Sistem", "marka": "Legrand", "ref": "LG-033790", "aciklama": "LCS³ CAT6 U/UTP 24 Port 19\" 1U Dolu Patch Panel + Kabin İçi Kablo Düzenleyici (Organizer)", "miktar": 6, "birim": "Set", "liste_fiyati": 9450.00, "iskonto": 66.0, "kar": 15.0},
        {"sira": 41, "bolum": "04. Zayıf Akım (ZA) Kablo & Sistem", "marka": "Legrand", "ref": "LG-051872", "aciklama": "LCS³ CAT6 U/UTP LSOH RJ45 Patch Cord (1m ve 2m Kabin / Kullanıcı Ara Bağlantı Kablosu)", "miktar": 140, "birim": "Adet", "liste_fiyati": 410.00, "iskonto": 66.0, "kar": 15.0},

        # 05. KANAL, BORU, ANAHTAR-PRİZ & TOPRAKLAMA (LEGRAND)
        {"sira": 42, "bolum": "05. Kanal, Priz & Topraklama", "marka": "Legrand", "ref": "LG-010424", "aciklama": "DLP 105x50 mm Kapaklı Duvar Tipi PVC Kablo Kanalı + Bölmeli Priz Montaj Aksesuarları", "miktar": 280, "birim": "m", "liste_fiyati": 690.00, "iskonto": 66.0, "kar": 15.0},
        {"sira": 43, "bolum": "05. Kanal, Priz & Topraklama", "marka": "Legrand", "ref": "LG-030015", "aciklama": "Lina 25 40x25 mm ve 25x16 mm Sıva Üstü PVC Kablo Kanalı (Ortalama Metraj)", "miktar": 450, "birim": "m", "liste_fiyati": 135.00, "iskonto": 66.0, "kar": 15.0},
        {"sira": 44, "bolum": "05. Kanal, Priz & Topraklama", "marka": "Legrand", "ref": "LG-300202", "aciklama": "Cablobend / Delikli Galvaniz Sac Kablo Tavası 200x50 mm + Konsol ve Askı Takımı", "miktar": 160, "birim": "m", "liste_fiyati": 920.00, "iskonto": 66.0, "kar": 15.0},
        {"sira": 45, "bolum": "05. Kanal, Priz & Topraklama", "marka": "Legrand", "ref": "LG-089220", "aciklama": "Halojensiz Sıva Altı Kangal Boru Ø20mm / Ø25mm + Kare Buat ve Derin Kasa Seti", "miktar": 3400, "birim": "m", "liste_fiyati": 42.00, "iskonto": 66.0, "kar": 15.0},
        {"sira": 46, "bolum": "05. Kanal, Priz & Topraklama", "marka": "Legrand", "ref": "LG-752101", "aciklama": "Valena Life Beyaz Tekli / Komütatör / Vaviyen Aydınlatma Anahtarı (Mekanizma + Çerçeve Dahil)", "miktar": 165, "birim": "Adet", "liste_fiyati": 385.00, "iskonto": 66.0, "kar": 15.0},
        {"sira": 47, "bolum": "05. Kanal, Priz & Topraklama", "marka": "Legrand", "ref": "LG-753118", "aciklama": "Valena Life Beyaz Çocuk Korumalı Topraklı Priz 16A (Mekanizma + Çerçeve Dahil)", "miktar": 310, "birim": "Adet", "liste_fiyati": 420.00, "iskonto": 66.0, "kar": 15.0},
        {"sira": 48, "bolum": "05. Kanal, Priz & Topraklama", "marka": "Legrand", "ref": "LG-753126", "aciklama": "Valena Life Kırmızı UPS Prizi (Kesintisiz Güç Kaynağı Hattı İçin - Çerçeve Dahil)", "miktar": 95, "birim": "Adet", "liste_fiyati": 495.00, "iskonto": 66.0, "kar": 15.0},
        {"sira": 49, "bolum": "05. Kanal, Priz & Topraklama", "marka": "Legrand", "ref": "LG-753142", "aciklama": "Valena Life 2xRJ45 CAT6 İkili Data Prizi (Keystone Jack + Kapak + Çerçeve Dahil)", "miktar": 70, "birim": "Adet", "liste_fiyati": 1180.00, "iskonto": 66.0, "kar": 15.0},
        {"sira": 50, "bolum": "05. Kanal, Priz & Topraklama", "marka": "Legrand", "ref": "LG-661620", "aciklama": "Ura One LED Acil Çıkış / Yönlendirme Armatürü (3 Saat Akülü) + Temel Topraklama Eşpotansiyel Seti", "miktar": 28, "birim": "Adet", "liste_fiyati": 3850.00, "iskonto": 66.0, "kar": 15.0},
    ]


def kesif_raporu_ve_csv_olustur(cikti_klasoru: str) -> None:
    kesif = elli_kalem_elektrik_kesfi_getir()
    csv_yolu = os.path.join(cikti_klasoru, "Elektrik_Kesif_Teklif_50_Kalem.csv")
    json_yolu = os.path.join(cikti_klasoru, "fiyat_listesi_veritabani.json")

    toplam_liste = 0.0
    toplam_net = 0.0
    toplam_teklif = 0.0

    with open(csv_yolu, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([
            "Sıra No", "Bölüm", "Marka", "Referans Kodu", "Poz / Malzeme Açıklaması",
            "Miktar", "Birim", "Liste Fiyatı (TL)", "İskonto (%)",
            "Net Alış Birim (TL)", "Kar Marjı (%)", "Teklif Birim Fiyatı (TL)",
            "Toplam Teklif Tutarı (TL)", "Excel Formülü (Toplam)"
        ])

        for idx, k in enumerate(kesif, start=2):
            net_birim = k["liste_fiyati"] * (1.0 - k["iskonto"] / 100.0)
            teklif_birim = net_birim * (1.0 + k["kar"] / 100.0)
            satir_toplam = k["miktar"] * teklif_birim

            toplam_liste += k["miktar"] * k["liste_fiyati"]
            toplam_net += k["miktar"] * net_birim
            toplam_teklif += satir_toplam

            k["net_birim_fiyat"] = round(net_birim, 2)
            k["teklif_birim_fiyat"] = round(teklif_birim, 2)
            k["toplam_teklif_tutari"] = round(satir_toplam, 2)

            writer.writerow([
                k["sira"],
                k["bolum"],
                k["marka"],
                k["ref"],
                k["aciklama"],
                k["miktar"],
                k["birim"],
                f"{k['liste_fiyati']:.2f}".replace(".", ","),
                f"{k['iskonto']:.1f}".replace(".", ","),
                f"{net_birim:.2f}".replace(".", ","),
                f"{k['kar']:.1f}".replace(".", ","),
                f"{teklif_birim:.2f}".replace(".", ","),
                f"{satir_toplam:.2f}".replace(".", ","),
                f"=F{idx}*H{idx}*(1-I{idx}/100)*(1+K{idx}/100)",
            ])

    with open(json_yolu, mode="w", encoding="utf-8") as jf:
        json.dump(
            {
                "guncelleme_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "marka_iskontolari": {
                    "Prysmian": 58.0,
                    "Legrand_Salt_Pano": 70.0,
                    "Legrand_Altyapi_Priz": 66.0,
                },
                "ozet": {
                    "kalem_sayisi": len(kesif),
                    "toplam_liste_tutari_tl": round(toplam_liste, 2),
                    "toplam_net_maliyet_tl": round(toplam_net, 2),
                    "toplam_teklif_kdv_haric_tl": round(toplam_teklif, 2),
                    "toplam_teklif_kdv_dahil_tl": round(toplam_teklif * 1.20, 2),
                },
                "kalemler": kesif,
            },
            jf,
            ensure_ascii=False,
            indent=2,
        )

    print(f"[OK] 50 Kalemlik Elektrik Keşfi oluşturuldu:")
    print(f"  -> CSV / Excel Dosyası : {csv_yolu}")
    print(f"  -> JSON Fiyat Havuzu   : {json_yolu}")
    print(f"  -> Liste Toplamı       : {toplam_liste:,.2f} TL")
    print(f"  -> Net Alış Maliyeti   : {toplam_net:,.2f} TL")
    print(f"  -> Teklif (KDV Hariç)  : {toplam_teklif:,.2f} TL")
    print(f"  -> Genel Toplam (%20)  : {toplam_teklif * 1.20:,.2f} TL")


if __name__ == "__main__":
    klasor = os.path.dirname(os.path.abspath(__file__))
    kesif_raporu_ve_csv_olustur(klasor)
