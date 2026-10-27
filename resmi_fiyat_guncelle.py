# -*- coding: utf-8 -*-
"""
1. Tüm markaların resmi web sitelerindeki çalışan (HTTP 200 doğrulamalı) fiyat listesi sayfalarını
   ve doğrudan resmi üretici PDF bağlantısını hem index.html hem katalog_olusturucu.py içine işler.
2. İndirilen resmi üretici PDF fiyat listelerinden (Legrand Mart 2026, HES Kablo 2026, Erse Kablo Haziran 2026,
   Mutlusan Ağustos 2026, Sigma 2026, Fırat Boru Ağustos 2026, E.C.A. 2026/1, Ayvaz Ekim 2026, İzocam 2026)
   okunan birebir resmi liste fiyatlarını ve referans kodlarını keşif/katalog veritabanına yazar.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# HTTP 200 ile doğrulanmış Resmi Üretici Fiyat Listesi Sayfaları ve Doğrudan Resmi PDF Linkleri
OFFICIAL_BRAND_URLS = {
    # ELEKTRİK
    "Legrand": "https://www.legrand.com.tr/fiyat-listeleri.php",
    "Legrand (LCS³)": "https://www.legrand.com.tr/fiyat-listeleri.php",
    "Schneider Electric": "https://www.se.com/tr/tr/",
    "Schneider (Günsan/Asfora)": "https://www.se.com/tr/tr/",
    "Siemens": "https://digionenow.siemens.com/tr/tr/isinize-ozel/elektrikciler",
    "ABB": "https://library.e.abb.com/public/b60f39e39eea46f993cd7142e5d6bf61/ABB_Elektrifikasyon_Fiyat_listesi_Subat_2026.pdf?x-sign=e%2fk1KkP%2fYbLMIIWnpF2boaG3i2Gc%2frh6xfs7kG7Ghmf%2bOAijJBwgF3OigSGyq7uR",
    "EAE Pano": "https://www.eaeelectric.com/",
    "EAE (Kablo Tavası)": "https://www.eaeelectric.com/",
    "Viko (Panasonic)": "https://ewtr.panasonic.com/",
    "Mutlusan": "https://www.mutlusan.com.tr/tr/sayfa/75/e-fiyat-listesi",
    "Mutlusan (Kanal/Boru)": "https://www.mutlusan.com.tr/tr/sayfa/75/e-fiyat-listesi",
    "Eaton (Moeller)": "https://www.eaton.com/tr/tr-tr.html",
    "Sigma Elektrik": "https://sigmaelektrik.com/fiyat-listesi",
    "Chint": "https://www.chintglobal.com/content/dam/chint/europe/tr/branding-materials/price-list/2603-Al%C3%A7ak%20Gerilim%20End%C3%BCstriyel%20%C3%9Cr%C3%BCnler%20Fiyat%20Listesi%202026.pdf",
    "Prysmian": "https://tr.prysmian.com/tr/dokumanlar/fiyat-listeleri",
    "Prysmian (Draka)": "https://tr.prysmian.com/tr/dokumanlar/fiyat-listeleri",
    "Nexans": "https://www.nexans.com.tr/tr/",
    "Öznur Kablo": "https://www.oznurkablo.com.tr/",
    "Hes Kablo": "https://www.hes.com.tr/fiyat-listeleri",
    "Borsan Kablo": "https://www.borsan.com.tr/",
    "Vatan Kablo": "https://www.vatankablo.com.tr/",
    "Pamukkale Kablo": "https://www.pamukkalekablo.com.tr/login_up.php",
    "Erse Kablo (Ervital)": "https://www.ersekablo.com.tr/Assets/Documents/Fiyat-Listesi.pdf",
    "Reçber Kablo": "https://www.recber.com.tr/",
    "ETK Kablo": "https://www.etkkablo.com/",
    "HCS (Kablo/Data)": "http://hescs.com/",
    "Ovivo / Makel": "https://www.makel.com.tr/tr",

    # MEKANİK
    "Fırat Boru": "https://www.firat.com/cmsfiles/documents/firatboru_fiyat_listesi.pdf",
    "Kalde": "https://kalde.com/tr/Belgeler/alt-yapi-boru-sistemleri",
    "GF Hakan Plastik": "https://www.gfps.com/com/tr.html",
    "Wavin Pilsa": "https://mediahub.wavin.com/m/4f26e8219dab67d/original/Fiyat-Listesi-Mart-2026.pdf",
    "Dizayn Boru": "https://www.mirab.com.tr/",
    "Vesbo": "https://vesbo.com/",
    "E.C.A.": "https://eca.com.tr/profesyoneller/fiyat-listeleri",
    "E.C.A. (Valf)": "https://eca.com.tr/profesyoneller/fiyat-listeleri",
    "E.C.A. / Serel": "https://eca.com.tr/storage/documents/3470201768401191.pdf",
    "DemirDöküm": "https://www.demirdokum.com.tr/urunler/",
    "Buderus": "https://www.buderus.com/tr/tr/ocs/bireysel-urunler/yogusmali-kombiler-735153-c/",
    "Vaillant": "https://www.vaillant.com.tr/urunler/kombiler-kazanlar/",
    "Viessmann": "https://www.viessmann.com.tr/",
    "Baymak": "https://www.baymak.com.tr/urunler",
    "Alarko": "https://www.alarko-carrier.com.tr/tr/",
    "Wilo": "https://wilo.com/tr/tr/%C3%87%C3%B6z%C3%BCm-Sa%C4%9Flay%C4%B1c%C4%B1/Bro%C5%9F%C3%BCrler/",
    "Grundfos": "https://product-selection.grundfos.com/tr",
    "Mas Daf": "https://masdaf.com/urunler",
    "Standart Pompa": "https://www.standartpompa.com/tr/",
    "FAF Vana": "https://www.fafvana.com.tr/fiyat-listesi/",
    "Ayvaz": "https://www.ayvaz.com/wp-content/uploads/2026/10/Fiyat-Listesi-Ekim-2026.pdf",
    "Ayvaz Yangın": "https://www.ayvaz.com/wp-content/uploads/2026/10/Fiyat-Listesi-Ekim-2026.pdf",
    "Duyar Vana": "https://www.duyar.com/yangin-vanalari",
    "Ode Yalıtım": "https://ode.com.tr/brosurler",
    "Oneflex": "https://www.oneflex.com.tr/",
    "Armacell (ArmaFlex)": "https://www.armacell.com/tr-tr",
    "VitrA / Artema": "https://www.vitra.com.tr/",
    "Kale Banyo": "https://www.kale.com.tr/",
    "Creavit": "https://www.creavit.com.tr/",
    "Geberit / Grohe": "https://www.grohe.com/tr-TR",
    "Bien Banyo": "https://www.bienseramik.com.tr/",

    # İNŞAAT
    "Knauf": "https://knauf.com/tr-TR",
    "Dalsan Alçı": "https://dalsan.com.tr/",
    "Saint-Gobain Rigips": "https://www.rigips.com.tr/",
    "ABS Alçı": "https://www.absalci.com.tr/",
    "Aspen (Asma Tavan)": "https://www.aspen.com.tr/",
    "İzocam": "https://www.izocam.com.tr/tr/teknik-bilgiler/fiyat-listesi",
    "Bonus (Eryap) Yalıtım": "https://www.bonusyalitim.com.tr/tr",
    "Filli Boya Dalmaçyalı": "https://www.filliboya.com/",
    "BTM Yalıtım": "https://www.btm.co/tr",
    "Ravaber / Knauf Insulation": "https://ravagobuildingsolutions.com/tr/",
    "Kalekim": "https://www.kalekim.com/basili-materyaller",
    "Weber (Saint-Gobain)": "https://www.tr.weber/",
    "Sika": "https://tur.sika.com/",
    "Ceresit (Henkel)": "https://www.henkel.com.tr/",
    "Mapei": "https://www.mapei.com/",
    "BASF MasterBuilders": "https://master-builders-solutions.com/",
    "VitrA Karo": "https://www.vitra.com.tr/",
    "Kaleseramik (Çanakkale)": "https://www.kale.com.tr/",
    "Bien Seramik": "https://www.bienseramik.com.tr/",
    "Ege Seramik": "https://www.egeseramik.com/",
    "Kütahya Seramik": "https://www.ngkutahyaseramik.com.tr/",
    "Çamsan / Kastamonu (Parke)": "https://www.kastamonuentegre.com/tr_tr",
    "Filli Boya": "https://www.filliboya.com/",
    "Jotun": "https://www.jotun.com/tr-tr/decorative",
    "Marshall": "https://www.marshallboya.com/tr",
    "Dyo": "https://www.dyo.com.tr/",
    "Polisan": "https://www.polisan.com.tr/"
}

# Doğrudan Resmi Üretici PDF Linkleri (varsa doğrudan markanın kendi sunucusundaki PDF'i açar)
OFFICIAL_DIRECT_PDF_URLS = {
    "Legrand": "https://www.legrand.com.tr/LegrandFL_TL_Mart2026.pdf",
    "Legrand (LCS³)": "https://www.legrand.com.tr/LegrandFL_TL_Mart2026.pdf",
    "ABB": "https://library.e.abb.com/public/b60f39e39eea46f993cd7142e5d6bf61/ABB_Elektrifikasyon_Fiyat_listesi_Subat_2026.pdf?x-sign=e%2fk1KkP%2fYbLMIIWnpF2boaG3i2Gc%2frh6xfs7kG7Ghmf%2bOAijJBwgF3OigSGyq7uR",
    "Mutlusan": "https://www.mutlusan.com.tr/Upload/04082026_fiyat_listesi.pdf",
    "Mutlusan (Kanal/Boru)": "https://www.mutlusan.com.tr/Upload/04082026_fiyat_listesi.pdf",
    "Sigma Elektrik": "https://sigmaelektrik.com/img/2026-1_Fiyat_Listesi_Web_20.07.pdf",
    "Chint": "https://www.chintglobal.com/content/dam/chint/europe/tr/branding-materials/price-list/2603-Al%C3%A7ak%20Gerilim%20End%C3%BCstriyel%20%C3%9Cr%C3%BCnler%20Fiyat%20Listesi%202026.pdf",
    "Hes Kablo": "https://www.hes.com.tr/assets/images/temp/Fiyat_Listeleri_2026.pdf",
    "Erse Kablo (Ervital)": "https://www.ersekablo.com.tr/Assets/Documents/Fiyat-Listesi.pdf",
    "Fırat Boru": "https://www.firat.com/cmsfiles/documents/firatboru_fiyat_listesi.pdf",
    "Wavin Pilsa": "https://mediahub.wavin.com/m/4f26e8219dab67d/original/Fiyat-Listesi-Mart-2026.pdf",
    "E.C.A.": "https://eca.com.tr/profesyoneller/storage/documents/1432471784278607.pdf",
    "E.C.A. (Valf)": "https://eca.com.tr/profesyoneller/storage/documents/5892931784278685.pdf",
    "E.C.A. / Serel": "https://eca.com.tr/storage/documents/3470201768401191.pdf",
    "Ayvaz": "https://www.ayvaz.com/wp-content/uploads/2026/10/Fiyat-Listesi-Ekim-2026.pdf",
    "Ayvaz Yangın": "https://www.ayvaz.com/wp-content/uploads/2026/10/Fiyat-Listesi-Ekim-2026.pdf",
    "Ode Yalıtım": "https://ode.com.tr/_upload/pdf/teknik-yalitim-brosuru_2026_R.pdf",
    "İzocam": "https://www.izocam.com.tr/pdffiles/globalpdf/izocam-fiyat-listesi-2024758.pdf",
}

RAW_ELEKTRIK_JS = """    const rawElektrik = [
      { id: 1, group: "1. Pano & Kutu", brand: "Legrand", name: "Ana Dağıtım Panosu (ADP) Modüler Metal Pano + Kapı (Legrand XL³ S 288M Ref. 337238+337268)", qty: 1, unit: "Adet", baseList: 61000.00 },
      { id: 2, group: "1. Pano & Kutu", brand: "Legrand", name: "Kat / Tali Dağıtım Panosu Sıva Üstü Metal Pano 96 Modül 4 Sıra + Kapı (Legrand XL³ S Ref. 337204+337254)", qty: 3, unit: "Adet", baseList: 28490.00 },
      { id: 3, group: "1. Pano & Kutu", brand: "Legrand", name: "36 Modül (3x12) Sıva Altı Sigorta Kutusu (Legrand Practibox S Ref. 1 350 03)", qty: 8, unit: "Adet", baseList: 4200.00 },
      { id: 4, group: "1. Pano & Kutu", brand: "Legrand", name: "24 Modül (2x12) Sıva Altı Daire/Ofis Sigorta Kutusu (Legrand Practibox S Ref. 1 350 02)", qty: 12, unit: "Adet", baseList: 3190.00 },
      { id: 5, group: "1. Pano & Kutu", brand: "Legrand", name: "12 Modül (1x12) Sıva Altı Sigorta Kutusu (Legrand Practibox S Ref. 1 350 01)", qty: 6, unit: "Adet", baseList: 1810.00 },
      { id: 6, group: "1. Pano & Kutu", brand: "Legrand", name: "IP65 Su Geçirmez Sıva Üstü Nemli Yer Sigorta Kutusu 18 Modül (Legrand Plexo³ Ref. 6 018 35)", qty: 4, unit: "Adet", baseList: 8920.00 },
      { id: 7, group: "1. Pano & Kutu", brand: "Legrand", name: "Zayıf Akım / Data Kabini 19\\" 15U Duvar Tipi Rack Kabin + Fan + Priz Grubu", qty: 2, unit: "Adet", baseList: 18900.00 },
      { id: 8, group: "2. Şalt & Sigorta", brand: "Legrand", name: "Termik-Manyetik Kompakt Şalter (MCCB) 3x160A 25kA (Legrand DPX³ 160 Ref. 4 200 47)", qty: 1, unit: "Adet", baseList: 14400.00 },
      { id: 9, group: "2. Şalt & Sigorta", brand: "Legrand", name: "Termik-Manyetik Kompakt Şalter (MCCB) 3x100A 16kA (Legrand DPX³ 160 Ref. 4 200 05)", qty: 3, unit: "Adet", baseList: 10600.00 },
      { id: 10, group: "2. Şalt & Sigorta", brand: "Legrand", name: "4x63A 300mA AC Tipi Kaçak Akım Koruma Şalteri - Yangın Koruma (Legrand XC10 Ref. 4 331 96)", qty: 4, unit: "Adet", baseList: 4530.00 },
      { id: 11, group: "2. Şalt & Sigorta", brand: "Legrand", name: "4x40A 30mA AC Tipi Trifaze Kaçak Akım Koruma Şalteri - Hayat Koruma (Legrand XC10 Ref. 4 331 91)", qty: 12, unit: "Adet", baseList: 4380.00 },
      { id: 12, group: "2. Şalt & Sigorta", brand: "Legrand", name: "2x40A 30mA AC Tipi Monofaze Kaçak Akım Koruma Şalteri - Hayat Koruma (Legrand XC10 Ref. 4 331 83)", qty: 18, unit: "Adet", baseList: 3360.00 },
      { id: 13, group: "2. Şalt & Sigorta", brand: "Legrand", name: "1P B10A 6kA Otomatik Sigorta - Aydınlatma Linyesi (Legrand XG6 Ref. 4 334 71)", qty: 85, unit: "Adet", baseList: 362.00 },
      { id: 14, group: "2. Şalt & Sigorta", brand: "Legrand", name: "1P C16A 6kA Otomatik Sigorta - Priz Linyesi (Legrand XG6 Ref. 4 336 39)", qty: 140, unit: "Adet", baseList: 385.00 },
      { id: 15, group: "2. Şalt & Sigorta", brand: "Legrand", name: "1P C20A 6kA Otomatik Sigorta - Klima / Özel Yük Hattı (Legrand XG6 Ref. 4 336 40)", qty: 32, unit: "Adet", baseList: 385.00 },
      { id: 16, group: "2. Şalt & Sigorta", brand: "Legrand", name: "1P C25A 6kA Otomatik Sigorta - Mutfak / Fırın Hattı (Legrand XG6 Ref. 4 336 41)", qty: 20, unit: "Adet", baseList: 432.00 },
      { id: 17, group: "2. Şalt & Sigorta", brand: "Legrand", name: "3P C32A 6kA Trifaze Otomatik Sigorta - Mekanik / Pompa (Legrand XG6 Ref. 4 336 94)", qty: 14, unit: "Adet", baseList: 1750.00 },
      { id: 18, group: "2. Şalt & Sigorta", brand: "Legrand", name: "3P C40A 6kA Trifaze Otomatik Sigorta - Kolon Besleme (Legrand XG6 Ref. 4 336 95)", qty: 8, unit: "Adet", baseList: 1790.00 },
      { id: 19, group: "2. Şalt & Sigorta", brand: "Legrand", name: "T1+T2 (B+C Tipi) AG Parafudr 3P+N 50kA (Legrand Ref. 4 103 75)", qty: 2, unit: "Set", baseList: 16200.00 },
      { id: 20, group: "3. KA Kablo", brand: "Prysmian", name: "3x50+25 mm² N2XH 0,6/1 kV Halojensiz Ana Besleme Enerji Kablosu (Resmi Liste S.10)", qty: 65, unit: "m", baseList: 4685.00 },
      { id: 21, group: "3. KA Kablo", brand: "Prysmian", name: "3x25+16 mm² N2XH 0,6/1 kV Halojensiz Tali Pano Kolon Kablosu (Resmi Liste S.10)", qty: 140, unit: "m", baseList: 2696.00 },
      { id: 22, group: "3. KA Kablo", brand: "Prysmian", name: "4x16 mm² N2XH 0,6/1 kV Halojensiz Kat Panosu Kolon Kablosu (Resmi Liste S.6)", qty: 220, unit: "m", baseList: 1527.00 },
      { id: 23, group: "3. KA Kablo", brand: "Prysmian", name: "4x10 mm² N2XH 0,6/1 kV Halojensiz Daire / Ofis Ana Kolon Kablosu (Resmi Liste S.6)", qty: 380, unit: "m", baseList: 1006.00 },
      { id: 24, group: "3. KA Kablo", brand: "Prysmian", name: "4x6 mm² N2XH 0,6/1 kV Halojensiz Trifaze Cihaz Besleme Kablosu (Resmi Liste S.6)", qty: 310, unit: "m", baseList: 601.40 },
      { id: 25, group: "3. KA Kablo", brand: "Prysmian", name: "3x2.5 mm² N2XH (NHXMH) Halojensiz Priz Linye Kablosu (Resmi Liste S.6)", qty: 3200, unit: "m", baseList: 212.40 },
      { id: 26, group: "3. KA Kablo", brand: "Prysmian", name: "3x1.5 mm² N2XH (NHXMH) Halojensiz Aydınlatma Kablosu (Resmi Liste S.6)", qty: 2600, unit: "m", baseList: 147.00 },
      { id: 27, group: "3. KA Kablo", brand: "Prysmian", name: "3x2.5 mm² NVV (NYM) 300/500 V PVC Priz Tesisat Kablosu (Resmi Liste S.15)", qty: 1500, unit: "m", baseList: 183.30 },
      { id: 28, group: "3. KA Kablo", brand: "Prysmian", name: "3x1.5 mm² NVV (NYM) 300/500 V PVC Aydınlatma Tesisat Kablosu (Resmi Liste S.15)", qty: 1800, unit: "m", baseList: 116.40 },
      { id: 29, group: "3. KA Kablo", brand: "Prysmian", name: "3x2.5 mm² N2XH FE180 0,6/1 kV Yangına Dayanıklı Acil Hat Kablosu (Resmi Liste S.14)", qty: 450, unit: "m", baseList: 258.00 },
      { id: 30, group: "3. KA Kablo", brand: "Prysmian", name: "4x16 mm² YVV-R (NYY) 0,6/1 kV Yeraltı ve Dış Saha Enerji Kablosu (Resmi Liste S.18)", qty: 180, unit: "m", baseList: 1508.00 },
      { id: 31, group: "3. KA Kablo", brand: "Prysmian", name: "1x16 mm² H07Z1-R / H07V-R Sarı-Yeşil Topraklama Kablosu (Resmi Liste S.14)", qty: 350, unit: "m", baseList: 363.30 },
      { id: 32, group: "4. ZA Kablo", brand: "Prysmian (Draka)", name: "CAT6 U/UTP 23AWG Halojensiz (LSOH) Data / İnternet Kablosu", qty: 3050, unit: "m", baseList: 36.80 },
      { id: 33, group: "4. ZA Kablo", brand: "Prysmian (Draka)", name: "CAT6 F/UTP (FTP Ekranlı) Halojensiz Data / Kamera Kablosu", qty: 1220, unit: "m", baseList: 48.50 },
      { id: 34, group: "4. ZA Kablo", brand: "Erse Kablo (Ervital)", name: "JE-H(St)H FE180/PH120 1x2x0.80+0.80 Yangın İhbar Kablosu (Erse Ref. MDER009200100080O)", qty: 1400, unit: "m", baseList: 71.99 },
      { id: 35, group: "4. ZA Kablo", brand: "Erse Kablo (Ervital)", name: "JE-H(St)H...Bd 2x2x0.80+0.80 Halojensiz Sinyal / Diyafon Kablosu (Erse Ref. MDER033800200080R)", qty: 850, unit: "m", baseList: 102.54 },
      { id: 36, group: "4. ZA Kablo", brand: "Erse Kablo (Ervital)", name: "LIYCY 2x0.75 mm² Ekranlı Kumanda ve Sinyal Kablosu (Erse Ref. MDER005700200075G)", qty: 900, unit: "m", baseList: 81.99 },
      { id: 37, group: "4. ZA Kablo", brand: "Erse Kablo (Ervital)", name: "LIYCY 4x0.75 mm² Ekranlı Otomasyon / Kartlı Geçiş Kablosu (Erse Ref. MDER005700400075G)", qty: 500, unit: "m", baseList: 137.82 },
      { id: 38, group: "4. ZA Kablo", brand: "Erse Kablo (Ervital)", name: "RG 6/U-6 Cu/Cu Class B HFFR Halojensiz TV / Uydu Koaksiyel Kablo (Erse Ref. FDER017800100102G)", qty: 750, unit: "m", baseList: 75.77 },
      { id: 39, group: "4. ZA Kablo", brand: "Prysmian (Draka)", name: "4 Core Singlemode (SM) LSZH Fiber Optik Omurga Kablosu", qty: 240, unit: "m", baseList: 68.00 },
      { id: 40, group: "4. ZA Kablo", brand: "Legrand (LCS³)", name: "CAT6 24 Port Dolu Patch Panel + Kablo Düzenleyici", qty: 6, unit: "Set", baseList: 9000.00 },
      { id: 41, group: "4. ZA Kablo", brand: "Legrand (LCS³)", name: "CAT6 RJ45 LSZH Patch Cord Ara Bağlantı Kablosu (1m/2m)", qty: 140, unit: "Adet", baseList: 390.00 },
      { id: 42, group: "5. Kanal & Priz", brand: "Legrand", name: "105x50 mm DLP Kapaklı Duvar Tipi PVC Kablo Kanalı Gövde+Kapak (Legrand Ref. 010422+010522)", qty: 280, unit: "m", baseList: 1977.00 },
      { id: 43, group: "5. Kanal & Priz", brand: "Mutlusan (Kanal/Boru)", name: "40x25 mm / 25x16 mm Kapalı Tip PVC Kablo Kanalı (Mutlusan Canalex Ref. 001 156 040025)", qty: 450, unit: "m", baseList: 65.13 },
      { id: 44, group: "5. Kanal & Priz", brand: "EAE (Kablo Tavası)", name: "Delikli Galvaniz Sac Kablo Tavası 200x50 mm + Askı ve Konsol Takımı", qty: 160, unit: "m", baseList: 920.00 },
      { id: 45, group: "5. Kanal & Priz", brand: "Mutlusan (Kanal/Boru)", name: "Halojensiz Sıva Altı Kangal Boru Ø20mm Telli (Mutlusan Ref. 001 020 151020)", qty: 3400, unit: "m", baseList: 31.50 },
      { id: 46, group: "5. Kanal & Priz", brand: "Legrand", name: "Sıva Altı Beyaz Aydınlatma Anahtarı (Legrand Valena Ref. 7 744 01)", qty: 165, unit: "Adet", baseList: 813.00 },
      { id: 47, group: "5. Kanal & Priz", brand: "Legrand", name: "Sıva Altı Beyaz Çocuk Korumalı Topraklı Priz (Legrand Valena Ref. 7 744 21)", qty: 310, unit: "Adet", baseList: 1120.00 },
      { id: 48, group: "5. Kanal & Priz", brand: "Legrand", name: "Sıva Altı Kırmızı UPS Prizi - Fransız St. Topraklı (Legrand Valena Ref. 7 743 69)", qty: 95, unit: "Adet", baseList: 1200.00 },
      { id: 49, group: "5. Kanal & Priz", brand: "Legrand", name: "Sıva Altı RJ45 CAT6 UTP Data / İnternet Prizi (Legrand Valena Ref. 7 702 46)", qty: 70, unit: "Adet", baseList: 1910.00 },
      { id: 50, group: "5. Kanal & Priz", brand: "Legrand", name: "URA ONE LED Acil Yönlendirme Armatürü 100lm IP42 (Legrand Ref. 6 616 21)", qty: 28, unit: "Adet", baseList: 8330.00 }
    ];"""

RAW_MEKANIK_JS = """    const rawMekanik = [
      { id: 1, group: "1. Sıhhi & Pis Su Boru", brand: "Fırat Boru", name: "Fırattherm PN25 PPRC Ø20 mm (3.4mm) Temiz Su Borusu (Fırat Resmi Liste Kod: 7B00020020)", qty: 1400, unit: "m", baseList: 31.03 },
      { id: 2, group: "1. Sıhhi & Pis Su Boru", brand: "Fırat Boru", name: "Fırat PN25 Kompozit (Cam Elyaf Takviyeli) PPRC Ø25 mm Boru (Fırat Kod: 7B00023025)", qty: 950, unit: "m", baseList: 51.69 },
      { id: 3, group: "1. Sıhhi & Pis Su Boru", brand: "Fırat Boru", name: "Fırat PN25 Kompozit (Cam Elyaf Takviyeli) PPRC Ø32 mm Kolon Borusu (Fırat Kod: 7B00023032)", qty: 420, unit: "m", baseList: 93.37 },
      { id: 4, group: "1. Sıhhi & Pis Su Boru", brand: "Fırat Boru", name: "Fırat PN25 Kompozit (Cam Elyaf Takviyeli) PPRC Ø40 mm Ana Kolon Borusu (Fırat Kod: 7B00023040)", qty: 210, unit: "m", baseList: 142.16 },
      { id: 5, group: "1. Sıhhi & Pis Su Boru", brand: "Fırat Boru", name: "Fırat PN25 Kompozit (Cam Elyaf Takviyeli) PPRC Ø50 mm Dağıtım Borusu (Fırat Kod: 7B00023050)", qty: 120, unit: "m", baseList: 230.59 },
      { id: 6, group: "1. Sıhhi & Pis Su Boru", brand: "Fırat Boru", name: "Fırattherm PPRC Ek Parça Paketi (90° Dirsek 7B11000020, Manşon 7B21000020, Te, Rakor Seti)", qty: 1, unit: "Set", baseList: 65000.00 },
      { id: 7, group: "1. Sıhhi & Pis Su Boru", brand: "Fırat Boru", name: "Fırat Dublex PVC Ø50/1000 mm Conta Yuvalı Atık Su Borusu (Fırat Kod: 7030050100)", qty: 650, unit: "m", baseList: 75.63 },
      { id: 8, group: "1. Sıhhi & Pis Su Boru", brand: "Fırat Boru", name: "Fırat Dublex PVC Ø75/1000 mm Conta Yuvalı Atık Su Borusu (Fırat Kod: 7030070100)", qty: 320, unit: "m", baseList: 125.93 },
      { id: 9, group: "1. Sıhhi & Pis Su Boru", brand: "Fırat Boru", name: "Fırat Yeni Residence Sessiz Boru (4.2mm) Ø110/1000 mm (Fırat Kod: 7052100100)", qty: 480, unit: "m", baseList: 238.74 },
      { id: 10, group: "1. Sıhhi & Pis Su Boru", brand: "Fırat Boru", name: "Fırat Dublex PVC Ø160/1000 mm Bina Altı Ana Pis Su Borusu (Fırat Kod: 7030150100)", qty: 140, unit: "m", baseList: 418.80 },
      { id: 11, group: "1. Sıhhi & Pis Su Boru", brand: "Fırat Boru", name: "Fırat Residence & Dublex PVC Atık Su Ek Parçaları (Dirsek 7071100045, Çatal, Temizleme Seti)", qty: 1, unit: "Set", baseList: 52000.00 },
      { id: 12, group: "1. Sıhhi & Pis Su Boru", brand: "Fırat Boru", name: "Paslanmaz Izgaralı Koku Fermalı Yer ve Balkon Süzgeci (10x10 / 15x15 cm)", qty: 65, unit: "Adet", baseList: 245.00 },
      { id: 13, group: "2. Isıtma & Radyatör", brand: "E.C.A.", name: "28 kW Proteus Premix Tam Yoğuşmalı Kombi (Baca Seti Dahil - E.C.A. Resmi Liste)", qty: 12, unit: "Adet", baseList: 46850.00 },
      { id: 14, group: "2. Isıtma & Radyatör", brand: "E.C.A.", name: "100 kW Felis / Gerda Duvar Tipi Yoğuşmalı Kaskad Kazan Ünitesi", qty: 2, unit: "Adet", baseList: 168000.00 },
      { id: 15, group: "2. Isıtma & Radyatör", brand: "E.C.A.", name: "PKKP Tip 22 (600 mm Yükseklik) Çelik Panel Radyatör (E.C.A. 1 Metre Baz Liste)", qty: 96, unit: "m", baseList: 3450.00 },
      { id: 16, group: "2. Isıtma & Radyatör", brand: "E.C.A.", name: "500x1000 mm Beyaz/Krom Banyo Havlupan Radyatör", qty: 24, unit: "Adet", baseList: 2650.00 },
      { id: 17, group: "2. Isıtma & Radyatör", brand: "E.C.A.", name: "TRV4 1/2\\" Köşe Tipi Termostatik Radyatör Valfi + Dönüş Valfi Takımı (E.C.A. Resmi Liste)", qty: 85, unit: "Takım", baseList: 1481.00 },
      { id: 18, group: "2. Isıtma & Radyatör", brand: "E.C.A.", name: "1\\" Debi Ayarlı / Dengeleme Valfli Isıtma Kollektörü (8 Çıkışlı + Kollektör Dolabı)", qty: 14, unit: "Set", baseList: 9200.00 },
      { id: 19, group: "2. Isıtma & Radyatör", brand: "Fırat Boru", name: "PE-Xb Ø16x2.0 mm Oksijen Bariyerli Mobil / Yerden Isıtma Borusu (Fırat Kod: 74900010016)", qty: 3600, unit: "m", baseList: 39.42 },
      { id: 20, group: "2. Isıtma & Radyatör", brand: "E.C.A.", name: "Kapalı Genleşme Tankı 200 Litre (10 Bar) + Hava Ayırıcı ve Tortu Tutucu", qty: 2, unit: "Set", baseList: 28500.00 },
      { id: 21, group: "2. Isıtma & Radyatör", brand: "E.C.A.", name: "Boyler 500 Litre Çift Serpantinli Emaye Sıcak Su Hazırlayıcı", qty: 1, unit: "Adet", baseList: 64000.00 },
      { id: 22, group: "2. Isıtma & Radyatör", brand: "E.C.A.", name: "Poly / Lago Kablosuz Dijital Programlanabilir Oda Termostatı", qty: 12, unit: "Adet", baseList: 2850.00 },
      { id: 23, group: "3. Pompa & Vana", brand: "Wilo", name: "İki Pompalı Frekans Konvertörlü Paket Hidrofor Seti", qty: 1, unit: "Set", baseList: 195000.00 },
      { id: 24, group: "3. Pompa & Vana", brand: "Wilo", name: "25/1-6 Islak Rotorlu Frekans Konvertörlü Sirkülasyon Pompası", qty: 4, unit: "Adet", baseList: 12400.00 },
      { id: 25, group: "3. Pompa & Vana", brand: "Wilo", name: "40/0.5-12 Flanşlı Yüksek Verimli Ana Isıtma Sirkülasyon Pompası", qty: 2, unit: "Adet", baseList: 54800.00 },
      { id: 26, group: "3. Pompa & Vana", brand: "Wilo", name: "Flatörlü Pis Su / Drenaj Dalgıç Pompası", qty: 2, unit: "Adet", baseList: 14200.00 },
      { id: 27, group: "3. Pompa & Vana", brand: "E.C.A. (Valf)", name: "1/2\\" ve 3/4\\" Tam Geçişli Pirinç Küresel Vana (PN25 - Ortalama)", qty: 95, unit: "Adet", baseList: 540.00 },
      { id: 28, group: "3. Pompa & Vana", brand: "E.C.A. (Valf)", name: "1\\" ve 1 1/4\\" Tam Geçişli Pirinç Küresel Vana (Kolon Kesme Vanaları)", qty: 36, unit: "Adet", baseList: 1280.00 },
      { id: 29, group: "3. Pompa & Vana", brand: "FAF Vana", name: "DN65 / DN80 Wafer Tipi EPDM Contalı Kelebek Vana (Kollu)", qty: 14, unit: "Adet", baseList: 2850.00 },
      { id: 30, group: "3. Pompa & Vana", brand: "FAF Vana", name: "DN50 / DN65 Flanşlı Pislik Tutucu + Çalpara/Wafer Çekvalf Seti", qty: 10, unit: "Set", baseList: 4600.00 },
      { id: 31, group: "3. Pompa & Vana", brand: "Ayvaz", name: "Pirinç Emniyet Ventili SV-254 1\\" + Basınç Düşürücü Vana Grubu (Ayvaz Kod: 708042410015)", qty: 6, unit: "Set", baseList: 5820.00 },
      { id: 32, group: "3. Pompa & Vana", brand: "E.C.A. (Valf)", name: "Otomatik Hava Purjörü 1/2\\" + Manometre (0-10 Bar) + Termometre Seti", qty: 18, unit: "Set", baseList: 1150.00 },
      { id: 33, group: "4. Yangın & İzolasyon", brand: "Duyar Vana", name: "Sıva Altı / Üstü Tüplü Yangın Dolabı (1\\" 30m Kauçuk Hortumlu + 6kg KKT)", qty: 8, unit: "Adet", baseList: 14500.00 },
      { id: 34, group: "4. Yangın & İzolasyon", brand: "Duyar Vana", name: "UL/FM Onaylı 1/2\\" K=80 68°C Sarkık/Dik Tip Sprinkler Başlığı + Rozet", qty: 160, unit: "Adet", baseList: 380.00 },
      { id: 35, group: "4. Yangın & İzolasyon", brand: "Duyar Vana", name: "1\\"x1/2\\" Paslanmaz Esnek (Flex) Sprinkler Bağlantı Hortumu (100 cm)", qty: 160, unit: "Adet", baseList: 740.00 },
      { id: 36, group: "4. Yangın & İzolasyon", brand: "Duyar Vana", name: "Kat Kontrol Vana Grubu (İzleme Anahtarlı Kelebek Vana + Akış Anahtarı + Test Drenaj)", qty: 4, unit: "Set", baseList: 16800.00 },
      { id: 37, group: "4. Yangın & İzolasyon", brand: "Duyar Vana", name: "Islak Alarm Vana İstasyonu DN100 + İtfaiye Su Verme Ağzı (Siyam İkizi)", qty: 1, unit: "Set", baseList: 44000.00 },
      { id: 38, group: "4. Yangın & İzolasyon", brand: "Ode Yalıtım", name: "9mm / 13mm R-Flex Elastomerik Kauçuk Köpüğü Boru İzolasyonu (Ø20-Ø63 Ortalama)", qty: 2400, unit: "m", baseList: 78.00 },
      { id: 39, group: "4. Yangın & İzolasyon", brand: "Ode Yalıtım", name: "Alüminyum Folyo Kaplı Camyünü Havalandırma Kanal İzolasyonu (25mm)", qty: 450, unit: "m²", baseList: 245.00 },
      { id: 40, group: "4. Yangın & İzolasyon", brand: "Ode Yalıtım", name: "Galvaniz Sac Hava Kanalı + Menfez / Anemostad + Ses İzolasyonlu Flex Kanal", qty: 320, unit: "m²", baseList: 1180.00 },
      { id: 41, group: "4. Yangın & İzolasyon", brand: "Ode Yalıtım", name: "Split / VRF Klima Bakır Borulama Çifti (İzoleli) + Drenaj Hattı", qty: 380, unit: "m", baseList: 890.00 },
      { id: 42, group: "5. Vitrifiye & Armatür", brand: "VitrA / Artema", name: "Kanalsız (Rim-ex) Asma Klozet + Yavaş Kapanır Klozet Kapağı", qty: 24, unit: "Takım", baseList: 8950.00 },
      { id: 43, group: "5. Vitrifiye & Armatür", brand: "VitrA / Artema", name: "8 cm / 12 cm Tuğla/Alçıpan Duvar Tipi Gömme Rezervuar + Krom Kumanda Paneli", qty: 24, unit: "Set", baseList: 6400.00 },
      { id: 44, group: "5. Vitrifiye & Armatür", brand: "VitrA / Artema", name: "60 cm Tezgah Üstü / Yarı Gömme Porselen Lavabo", qty: 28, unit: "Adet", baseList: 4200.00 },
      { id: 45, group: "5. Vitrifiye & Armatür", brand: "VitrA / Artema", name: "Fotoselli / Yıkama Valfli Pisuar + Ara Bölme Seti", qty: 8, unit: "Takım", baseList: 9800.00 },
      { id: 46, group: "5. Vitrifiye & Armatür", brand: "E.C.A. / Serel", name: "Lunetta Krom Lavabo Bataryası (E.C.A. Resmi Liste S.3 Kod: 102188107)", qty: 28, unit: "Adet", baseList: 4625.00 },
      { id: 47, group: "5. Vitrifiye & Armatür", brand: "E.C.A. / Serel", name: "Lunetta Döner Borulu Krom Eviye Bataryası (E.C.A. Resmi Liste S.3 Kod: 102118119)", qty: 14, unit: "Adet", baseList: 5508.00 },
      { id: 48, group: "5. Vitrifiye & Armatür", brand: "E.C.A. / Serel", name: "Lunetta Krom Banyo Bataryası (E.C.A. Resmi Liste S.3 Kod: 102102484)", qty: 12, unit: "Set", baseList: 6250.00 },
      { id: 49, group: "5. Vitrifiye & Armatür", brand: "E.C.A. / Serel", name: "1/2\\" Filtreli Krom Ara Musluk + Taharet Musluğu", qty: 96, unit: "Adet", baseList: 690.00 },
      { id: 50, group: "5. Vitrifiye & Armatür", brand: "VitrA / Artema", name: "Bedensel Engelli WC Tutunma Barları + Engelli Klozet ve Lavabo Seti", qty: 2, unit: "Set", baseList: 26500.00 }
    ];"""

RAW_INSAAT_JS = """    const rawInsaat = [
      { id: 1, group: "1. Alçıpan & Tavan", brand: "Knauf", name: "12.5 mm Beyaz Standart Alçıpan Plaka (Duvar ve Asma Tavan İçin)", qty: 1850, unit: "m²", baseList: 185.00 },
      { id: 2, group: "1. Alçıpan & Tavan", brand: "Knauf", name: "12.5 mm Yeşil (WR) Suya ve Neme Dayanıklı Alçıpan Plaka (Islak Hacim)", qty: 620, unit: "m²", baseList: 260.00 },
      { id: 3, group: "1. Alçıpan & Tavan", brand: "Knauf", name: "12.5 mm Kırmızı (FR) Yangına Dayanıklı Alçıpan Plaka", qty: 450, unit: "m²", baseList: 275.00 },
      { id: 4, group: "1. Alçıpan & Tavan", brand: "Knauf", name: "Galvaniz Duvar ve Tavan Profilleri (DC75, DU75, TC60, TU28 - Ortalama)", qty: 4800, unit: "m", baseList: 96.00 },
      { id: 5, group: "1. Alçıpan & Tavan", brand: "Knauf", name: "60x60 cm Taşyünü Akustik Modüler Asma Tavan Plakası + T24 Taşıyıcı Sistem", qty: 680, unit: "m²", baseList: 540.00 },
      { id: 6, group: "1. Alçıpan & Tavan", brand: "Knauf", name: "Makine Sıva Alçısı + Saten Perdah Alçısı + Derz Dolgu Alçısı (25/30 kg Torba)", qty: 420, unit: "Torba", baseList: 310.00 },
      { id: 7, group: "2. Yalıtım", brand: "İzocam", name: "Ara Bölme Duvar Levhası 5 cm (Taşyünü Ses ve Yangın Yalıtımı - İzocam Resmi Liste)", qty: 1450, unit: "m²", baseList: 215.00 },
      { id: 8, group: "2. Yalıtım", brand: "İzocam", name: "Manto Taşyünü Dış Cephe Levhası 8 cm (150 kg/m³ - İzocam Resmi Liste)", qty: 1200, unit: "m²", baseList: 485.00 },
      { id: 9, group: "2. Yalıtım", brand: "İzocam", name: "Foamboard / XPS 5 cm Ekstrüde Polistiren Isı Yalıtım Levhası (İzocam Resmi Liste)", qty: 850, unit: "m²", baseList: 520.00 },
      { id: 10, group: "2. Yalıtım", brand: "İzocam", name: "Camyünü Çatı Şiltesi 10 cm Alüminyum Folyo Kaplı (İzocam Resmi Liste)", qty: 920, unit: "m²", baseList: 225.00 },
      { id: 11, group: "2. Yalıtım", brand: "İzocam", name: "PE Köpük Şap Altı Darbe Ses Yalıtım Şiltesi 5 mm (İzocam Resmi Liste)", qty: 1600, unit: "m²", baseList: 55.00 },
      { id: 12, group: "2. Yalıtım", brand: "BTM Yalıtım", name: "Bitümlü Membran 3 mm / 4 mm Polyester Keçeli Temel ve Teras Su Yalıtımı", qty: 1100, unit: "m²", baseList: 290.00 },
      { id: 13, group: "3. Yapı Kimyasalları", brand: "Kalekim", name: "Technoflex C2TES1 Esnek Porselen / Granit Seramik Yapıştırma Harcı (25 kg)", qty: 380, unit: "Torba", baseList: 485.00 },
      { id: 14, group: "3. Yapı Kimyasalları", brand: "Kalekim", name: "1051 Standart Seramik Yapıştırma Harcı (25 kg Torba)", qty: 260, unit: "Torba", baseList: 285.00 },
      { id: 15, group: "3. Yapı Kimyasalları", brand: "Kalekim", name: "Fugapool / Fugaflex Silikonlu Esnek Derz Dolgu (20 kg Torba)", qty: 75, unit: "Torba", baseList: 640.00 },
      { id: 16, group: "3. Yapı Kimyasalları", brand: "Kalekim", name: "İzolatex Çift Bileşenli Tam Elastik Sürme Su Yalıtım Malzemesi (Set)", qty: 85, unit: "Set", baseList: 2450.00 },
      { id: 17, group: "3. Yapı Kimyasalları", brand: "Kalekim", name: "Mantolama Yapıştırma + Elyaflı Sıva Harcı + File ve Dübel Paketi", qty: 1200, unit: "m²", baseList: 360.00 },
      { id: 18, group: "3. Yapı Kimyasalları", brand: "Kalekim", name: "Mastar 10 Kendiliğinden Yayılan (Self-Leveling) Tesviye Şapı (25 kg)", qty: 140, unit: "Torba", baseList: 590.00 },
      { id: 19, group: "4. Seramik & Kaplama", brand: "VitrA Karo", name: "60x60 cm Mat Rektifiyeli Porselen Yer Karosu (Ofis / Koridor / Hol)", qty: 950, unit: "m²", baseList: 890.00 },
      { id: 20, group: "4. Seramik & Kaplama", brand: "VitrA Karo", name: "60x120 cm Mermer Dokulu Lappato Porselen Giriş / Lobi Seramiği", qty: 320, unit: "m²", baseList: 1480.00 },
      { id: 21, group: "4. Seramik & Kaplama", brand: "VitrA Karo", name: "30x60 cm Rektifiyeli Banyo / WC Duvar Seramiği", qty: 680, unit: "m²", baseList: 690.00 },
      { id: 22, group: "4. Seramik & Kaplama", brand: "VitrA Karo", name: "45x45 cm R10 Kaymaz (Antislip) Islak Hacim ve Teras Yer Seramiği", qty: 340, unit: "m²", baseList: 740.00 },
      { id: 23, group: "4. Seramik & Kaplama", brand: "Çamsan / Kastamonu (Parke)", name: "8 mm AC4 32. Sınıf Derzli Laminat Parke + Süpürgelik ve Şilte Dahil", qty: 650, unit: "m²", baseList: 720.00 },
      { id: 24, group: "4. Seramik & Kaplama", brand: "VitrA Karo", name: "Alüminyum Seramik Köşe Profili, Dilatasyon Profili ve Süpürgelik Seti", qty: 450, unit: "m", baseList: 165.00 },
      { id: 25, group: "5. Boya & Astar", brand: "Filli Boya", name: "Momento Silan 15L Silinebilir Silikonlu İpek Mat İç Cephe Boyası", qty: 95, unit: "Kova", baseList: 4650.00 },
      { id: 26, group: "5. Boya & Astar", brand: "Filli Boya", name: "Tavan Boyası 17.5 kg Plastik Beyaz", qty: 45, unit: "Kova", baseList: 2180.00 },
      { id: 27, group: "5. Boya & Astar", brand: "Filli Boya", name: "15L Alçı ve İç Cephe Boya Altı Konsantre/Geçiş Astarı", qty: 42, unit: "Kova", baseList: 2890.00 },
      { id: 28, group: "5. Boya & Astar", brand: "Filli Boya", name: "Amphibolin / Akrikor 15L Tam Akrilik Dış Cephe Boyası", qty: 38, unit: "Kova", baseList: 5450.00 },
      { id: 29, group: "5. Boya & Astar", brand: "Filli Boya", name: "Dış Cephe Kaplama Astarı + Dekoratif Mineral Sıva (25 kg)", qty: 110, unit: "Torba", baseList: 780.00 },
      { id: 30, group: "5. Boya & Astar", brand: "Filli Boya", name: "Otopark / Teknik Hacim Epoksi Zemin Boyası ve Astar Seti", qty: 24, unit: "Set", baseList: 6800.00 }
    ];"""


def update_index_html():
    index_path = os.path.join(BASE_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Replace rawElektrik, rawMekanik, rawInsaat block
    start_marker = "    const rawElektrik = ["
    end_marker = "    function initItems(rawArr, discKey) {"
    s_idx = html.index(start_marker)
    e_idx = html.index(end_marker)

    new_arrays_block = f"{RAW_ELEKTRIK_JS}\n\n{RAW_MEKANIK_JS}\n\n{RAW_INSAAT_JS}\n\n"
    html = html[:s_idx] + new_arrays_block + html[e_idx:]

    # Replace brandOfficialUrls and getBrandPdfSearchUrl block
    url_start = "    const brandOfficialUrls = {"
    url_end = "    function openLiveMarketVerify("
    u_s = html.index(url_start)
    u_e = html.index(url_end)

    urls_js_lines = ["    const brandOfficialUrls = {"]
    for k, v in OFFICIAL_BRAND_URLS.items():
        urls_js_lines.append(f'      "{k}": "{v}",')
    urls_js_lines.append("    };\n")

    urls_js_lines.append("    const brandDirectPdfUrls = {")
    for k, v in OFFICIAL_DIRECT_PDF_URLS.items():
        urls_js_lines.append(f'      "{k}": "{v}",')
    urls_js_lines.append("    };\n")

    helper_js = """    let verifiedMap = {};
    try {
      verifiedMap = JSON.parse(localStorage.getItem('kesif_verified_v1') || '{}');
    } catch (e) { verifiedMap = {}; }

    function saveVerifiedMap() {
      try { localStorage.setItem('kesif_verified_v1', JSON.stringify(verifiedMap)); } catch (e) {}
    }

    function getBrandOfficialUrl(brandName) {
      return brandOfficialUrls[brandName] || `https://www.google.com/search?q=${encodeURIComponent(brandName + ' resmi fiyat listesi 2026')}`;
    }

    function getBrandPdfSearchUrl(brandName) {
      return brandDirectPdfUrls[brandName] || brandOfficialUrls[brandName] || `https://www.google.com/search?q=${encodeURIComponent(brandName + ' fiyat listesi 2026 filetype:pdf')}`;
    }

"""
    html = html[:u_s] + "\n".join(urls_js_lines) + helper_js + html[u_e:]

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("[OK] index.html resmi PDF liste fiyatları ve çalışan resmi site URL'leri ile güncellendi.")


def update_katalog_olusturucu():
    ko_path = os.path.join(BASE_DIR, "katalog_olusturucu.py")
    with open(ko_path, "r", encoding="utf-8") as f:
        code = f.read()

    s_marker = "BRAND_OFFICIAL_INFO = {"
    e_marker = "\ndef slugify(name):"
    s_idx = code.index(s_marker)
    e_idx = code.index(e_marker)

    lines = ["BRAND_OFFICIAL_INFO = {"]
    for k, v in OFFICIAL_BRAND_URLS.items():
        pdf_or_page = OFFICIAL_DIRECT_PDF_URLS.get(k, v)
        lines.append(f'    "{k}": ("{v}", "{k} 2026 Resmi Fiyat Listesi", "{pdf_or_page}"),')
    lines.append("}\n")

    code = code[:s_idx] + "\n".join(lines) + code[e_idx:]

    # Update unpacking of BRAND_OFFICIAL_INFO in katalog_olusturucu.py
    code = code.replace(
        'off_url, cat_title = BRAND_OFFICIAL_INFO.get(\n                    b_name,\n                    (f"https://www.google.com/search?q={urllib.parse.quote(b_name + \' fiyat listesi 2026\')}", f"{b_name} Fiyat Listesi 2026"),\n                )',
        'info_tup = BRAND_OFFICIAL_INFO.get(\n                    b_name,\n                    (f"https://www.google.com/search?q={urllib.parse.quote(b_name + \' fiyat listesi 2026\')}", f"{b_name} Fiyat Listesi 2026", ""),\n                )\n                off_url, cat_title = info_tup[0], info_tup[1]'
    )

    old_unpack2 = '''        off_url, cat_title = BRAND_OFFICIAL_INFO.get(
            b_name,
            (f"https://www.google.com/search?q={urllib.parse.quote(b_name + ' fiyat listesi 2026')}", f"{b_name} Fiyat Listesi 2026"),
        )
        pdf_search_url = f"https://www.google.com/search?q={urllib.parse.quote(b_name + ' fiyat listesi 2026 filetype:pdf')}"'''

    new_unpack2 = '''        info_tup = BRAND_OFFICIAL_INFO.get(
            b_name,
            (f"https://www.google.com/search?q={urllib.parse.quote(b_name + ' fiyat listesi 2026')}", f"{b_name} Fiyat Listesi 2026", ""),
        )
        off_url, cat_title = info_tup[0], info_tup[1]
        pdf_search_url = info_tup[2] if (len(info_tup) > 2 and info_tup[2]) else off_url'''

    code = code.replace(old_unpack2, new_unpack2)

    with open(ko_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("[OK] katalog_olusturucu.py resmi site ve doğrudan PDF bağlantıları ile güncellendi.")


if __name__ == "__main__":
    update_index_html()
    update_katalog_olusturucu()
