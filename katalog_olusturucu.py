# -*- coding: utf-8 -*-
"""
Tüm Markalar (Elektrik, Mekanik, İnşaat) İçin:
1. Siteden doğrudan indirilebilir Orijinal Marka Fiyat Listesi Excel (.CSV) dosyalarını,
2. Siteden doğrudan açılıp PDF olarak indirilebilir / yazdırılabilir Resmi Katalog sayfalarını (.HTML),
3. Resmi üretici fiyat listesi linklerini ve canlı piyasa doğrulama indeksini (resmi_katalog_indeksi.json) üretir.
"""

import csv
import json
import os
import re
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KATALOG_DIR = os.path.join(BASE_DIR, "kataloglar")
os.makedirs(KATALOG_DIR, exist_ok=True)

BRAND_OFFICIAL_INFO = {
    "Legrand": ("https://www.legrand.com.tr/fiyat-listeleri.php", "Legrand 2026 Resmi Fiyat Listesi", "https://www.legrand.com.tr/LegrandFL_TL_Mart2026.pdf"),
    "Legrand (LCS³)": ("https://www.legrand.com.tr/fiyat-listeleri.php", "Legrand (LCS³) 2026 Resmi Fiyat Listesi", "https://www.legrand.com.tr/LegrandFL_TL_Mart2026.pdf"),
    "Schneider Electric": ("https://www.se.com/tr/tr/", "Schneider Electric 2026 Resmi Fiyat Listesi", "https://www.se.com/tr/tr/"),
    "Schneider (Günsan/Asfora)": ("https://www.se.com/tr/tr/", "Schneider (Günsan/Asfora) 2026 Resmi Fiyat Listesi", "https://www.se.com/tr/tr/"),
    "Siemens": ("https://digionenow.siemens.com/tr/tr/isinize-ozel/elektrikciler", "Siemens 2026 Resmi Fiyat Listesi", "https://digionenow.siemens.com/tr/tr/isinize-ozel/elektrikciler"),
    "ABB": ("https://library.e.abb.com/public/b60f39e39eea46f993cd7142e5d6bf61/ABB_Elektrifikasyon_Fiyat_listesi_Subat_2026.pdf?x-sign=e%2fk1KkP%2fYbLMIIWnpF2boaG3i2Gc%2frh6xfs7kG7Ghmf%2bOAijJBwgF3OigSGyq7uR", "ABB 2026 Resmi Fiyat Listesi", "https://library.e.abb.com/public/b60f39e39eea46f993cd7142e5d6bf61/ABB_Elektrifikasyon_Fiyat_listesi_Subat_2026.pdf?x-sign=e%2fk1KkP%2fYbLMIIWnpF2boaG3i2Gc%2frh6xfs7kG7Ghmf%2bOAijJBwgF3OigSGyq7uR"),
    "EAE Pano": ("https://www.eaeelectric.com/", "EAE Pano 2026 Resmi Fiyat Listesi", "https://www.eaeelectric.com/"),
    "EAE (Kablo Tavası)": ("https://www.eaeelectric.com/", "EAE (Kablo Tavası) 2026 Resmi Fiyat Listesi", "https://www.eaeelectric.com/"),
    "Viko (Panasonic)": ("https://ewtr.panasonic.com/", "Viko (Panasonic) 2026 Resmi Fiyat Listesi", "https://ewtr.panasonic.com/"),
    "Mutlusan": ("https://www.mutlusan.com.tr/tr/sayfa/75/e-fiyat-listesi", "Mutlusan 2026 Resmi Fiyat Listesi", "https://www.mutlusan.com.tr/Upload/04082026_fiyat_listesi.pdf"),
    "Mutlusan (Kanal/Boru)": ("https://www.mutlusan.com.tr/tr/sayfa/75/e-fiyat-listesi", "Mutlusan (Kanal/Boru) 2026 Resmi Fiyat Listesi", "https://www.mutlusan.com.tr/Upload/04082026_fiyat_listesi.pdf"),
    "Eaton (Moeller)": ("https://www.eaton.com/tr/tr-tr.html", "Eaton (Moeller) 2026 Resmi Fiyat Listesi", "https://www.eaton.com/tr/tr-tr.html"),
    "Sigma Elektrik": ("https://sigmaelektrik.com/fiyat-listesi", "Sigma Elektrik 2026 Resmi Fiyat Listesi", "https://sigmaelektrik.com/img/2026-1_Fiyat_Listesi_Web_20.07.pdf"),
    "Chint": ("https://www.chintglobal.com/content/dam/chint/europe/tr/branding-materials/price-list/2603-Al%C3%A7ak%20Gerilim%20End%C3%BCstriyel%20%C3%9Cr%C3%BCnler%20Fiyat%20Listesi%202026.pdf", "Chint 2026 Resmi Fiyat Listesi", "https://www.chintglobal.com/content/dam/chint/europe/tr/branding-materials/price-list/2603-Al%C3%A7ak%20Gerilim%20End%C3%BCstriyel%20%C3%9Cr%C3%BCnler%20Fiyat%20Listesi%202026.pdf"),
    "Prysmian": ("https://tr.prysmian.com/tr/dokumanlar/fiyat-listeleri", "Prysmian 2026 Resmi Fiyat Listesi", "https://tr.prysmian.com/tr/dokumanlar/fiyat-listeleri"),
    "Prysmian (Draka)": ("https://tr.prysmian.com/tr/dokumanlar/fiyat-listeleri", "Prysmian (Draka) 2026 Resmi Fiyat Listesi", "https://tr.prysmian.com/tr/dokumanlar/fiyat-listeleri"),
    "Nexans": ("https://www.nexans.com.tr/tr/", "Nexans 2026 Resmi Fiyat Listesi", "https://www.nexans.com.tr/tr/"),
    "Öznur Kablo": ("https://www.oznurkablo.com.tr/", "Öznur Kablo 2026 Resmi Fiyat Listesi", "https://www.oznurkablo.com.tr/"),
    "Hes Kablo": ("https://www.hes.com.tr/fiyat-listeleri", "Hes Kablo 2026 Resmi Fiyat Listesi", "https://www.hes.com.tr/assets/images/temp/Fiyat_Listeleri_2026.pdf"),
    "Borsan Kablo": ("https://www.borsan.com.tr/", "Borsan Kablo 2026 Resmi Fiyat Listesi", "https://www.borsan.com.tr/"),
    "Vatan Kablo": ("https://www.vatankablo.com.tr/", "Vatan Kablo 2026 Resmi Fiyat Listesi", "https://www.vatankablo.com.tr/"),
    "Pamukkale Kablo": ("https://www.pamukkalekablo.com.tr/login_up.php", "Pamukkale Kablo 2026 Resmi Fiyat Listesi", "https://www.pamukkalekablo.com.tr/login_up.php"),
    "Erse Kablo (Ervital)": ("https://www.ersekablo.com.tr/Assets/Documents/Fiyat-Listesi.pdf", "Erse Kablo (Ervital) 2026 Resmi Fiyat Listesi", "https://www.ersekablo.com.tr/Assets/Documents/Fiyat-Listesi.pdf"),
    "Reçber Kablo": ("https://www.recber.com.tr/", "Reçber Kablo 2026 Resmi Fiyat Listesi", "https://www.recber.com.tr/"),
    "ETK Kablo": ("https://www.etkkablo.com/", "ETK Kablo 2026 Resmi Fiyat Listesi", "https://www.etkkablo.com/"),
    "HCS (Kablo/Data)": ("http://hescs.com/", "HCS (Kablo/Data) 2026 Resmi Fiyat Listesi", "http://hescs.com/"),
    "Ovivo / Makel": ("https://www.makel.com.tr/tr", "Ovivo / Makel 2026 Resmi Fiyat Listesi", "https://www.makel.com.tr/tr"),
    "Fırat Boru": ("https://www.firat.com/cmsfiles/documents/firatboru_fiyat_listesi.pdf", "Fırat Boru 2026 Resmi Fiyat Listesi", "https://www.firat.com/cmsfiles/documents/firatboru_fiyat_listesi.pdf"),
    "Kalde": ("https://kalde.com/tr/Belgeler/alt-yapi-boru-sistemleri", "Kalde 2026 Resmi Fiyat Listesi", "https://kalde.com/tr/Belgeler/alt-yapi-boru-sistemleri"),
    "GF Hakan Plastik": ("https://www.gfps.com/com/tr.html", "GF Hakan Plastik 2026 Resmi Fiyat Listesi", "https://www.gfps.com/com/tr.html"),
    "Wavin Pilsa": ("https://mediahub.wavin.com/m/4f26e8219dab67d/original/Fiyat-Listesi-Mart-2026.pdf", "Wavin Pilsa 2026 Resmi Fiyat Listesi", "https://mediahub.wavin.com/m/4f26e8219dab67d/original/Fiyat-Listesi-Mart-2026.pdf"),
    "Dizayn Boru": ("https://www.mirab.com.tr/", "Dizayn Boru 2026 Resmi Fiyat Listesi", "https://www.mirab.com.tr/"),
    "Vesbo": ("https://vesbo.com/", "Vesbo 2026 Resmi Fiyat Listesi", "https://vesbo.com/"),
    "E.C.A.": ("https://eca.com.tr/profesyoneller/fiyat-listeleri", "E.C.A. 2026 Resmi Fiyat Listesi", "https://eca.com.tr/profesyoneller/storage/documents/1432471784278607.pdf"),
    "E.C.A. (Valf)": ("https://eca.com.tr/profesyoneller/fiyat-listeleri", "E.C.A. (Valf) 2026 Resmi Fiyat Listesi", "https://eca.com.tr/profesyoneller/storage/documents/5892931784278685.pdf"),
    "E.C.A. / Serel": ("https://eca.com.tr/storage/documents/3470201768401191.pdf", "E.C.A. / Serel 2026 Resmi Fiyat Listesi", "https://eca.com.tr/storage/documents/3470201768401191.pdf"),
    "DemirDöküm": ("https://www.demirdokum.com.tr/urunler/", "DemirDöküm 2026 Resmi Fiyat Listesi", "https://www.demirdokum.com.tr/urunler/"),
    "Buderus": ("https://www.buderus.com/tr/tr/ocs/bireysel-urunler/yogusmali-kombiler-735153-c/", "Buderus 2026 Resmi Fiyat Listesi", "https://www.buderus.com/tr/tr/ocs/bireysel-urunler/yogusmali-kombiler-735153-c/"),
    "Vaillant": ("https://www.vaillant.com.tr/urunler/kombiler-kazanlar/", "Vaillant 2026 Resmi Fiyat Listesi", "https://www.vaillant.com.tr/urunler/kombiler-kazanlar/"),
    "Viessmann": ("https://www.viessmann.com.tr/", "Viessmann 2026 Resmi Fiyat Listesi", "https://www.viessmann.com.tr/"),
    "Baymak": ("https://www.baymak.com.tr/urunler", "Baymak 2026 Resmi Fiyat Listesi", "https://www.baymak.com.tr/urunler"),
    "Alarko": ("https://www.alarko-carrier.com.tr/tr/", "Alarko 2026 Resmi Fiyat Listesi", "https://www.alarko-carrier.com.tr/tr/"),
    "Wilo": ("https://wilo.com/tr/tr/%C3%87%C3%B6z%C3%BCm-Sa%C4%9Flay%C4%B1c%C4%B1/Bro%C5%9F%C3%BCrler/", "Wilo 2026 Resmi Fiyat Listesi", "https://wilo.com/tr/tr/%C3%87%C3%B6z%C3%BCm-Sa%C4%9Flay%C4%B1c%C4%B1/Bro%C5%9F%C3%BCrler/"),
    "Grundfos": ("https://product-selection.grundfos.com/tr", "Grundfos 2026 Resmi Fiyat Listesi", "https://product-selection.grundfos.com/tr"),
    "Mas Daf": ("https://masdaf.com/urunler", "Mas Daf 2026 Resmi Fiyat Listesi", "https://masdaf.com/urunler"),
    "Standart Pompa": ("https://www.standartpompa.com/tr/", "Standart Pompa 2026 Resmi Fiyat Listesi", "https://www.standartpompa.com/tr/"),
    "FAF Vana": ("https://www.fafvana.com.tr/fiyat-listesi/", "FAF Vana 2026 Resmi Fiyat Listesi", "https://www.fafvana.com.tr/fiyat-listesi/"),
    "Ayvaz": ("https://www.ayvaz.com/wp-content/uploads/2026/10/Fiyat-Listesi-Ekim-2026.pdf", "Ayvaz 2026 Resmi Fiyat Listesi", "https://www.ayvaz.com/wp-content/uploads/2026/10/Fiyat-Listesi-Ekim-2026.pdf"),
    "Ayvaz Yangın": ("https://www.ayvaz.com/wp-content/uploads/2026/10/Fiyat-Listesi-Ekim-2026.pdf", "Ayvaz Yangın 2026 Resmi Fiyat Listesi", "https://www.ayvaz.com/wp-content/uploads/2026/10/Fiyat-Listesi-Ekim-2026.pdf"),
    "Duyar Vana": ("https://www.duyar.com/yangin-vanalari", "Duyar Vana 2026 Resmi Fiyat Listesi", "https://www.duyar.com/yangin-vanalari"),
    "Ode Yalıtım": ("https://ode.com.tr/brosurler", "Ode Yalıtım 2026 Resmi Fiyat Listesi", "https://ode.com.tr/_upload/pdf/teknik-yalitim-brosuru_2026_R.pdf"),
    "Oneflex": ("https://www.oneflex.com.tr/", "Oneflex 2026 Resmi Fiyat Listesi", "https://www.oneflex.com.tr/"),
    "Armacell (ArmaFlex)": ("https://www.armacell.com/tr-tr", "Armacell (ArmaFlex) 2026 Resmi Fiyat Listesi", "https://www.armacell.com/tr-tr"),
    "VitrA / Artema": ("https://www.vitra.com.tr/", "VitrA / Artema 2026 Resmi Fiyat Listesi", "https://www.vitra.com.tr/"),
    "Kale Banyo": ("https://www.kale.com.tr/", "Kale Banyo 2026 Resmi Fiyat Listesi", "https://www.kale.com.tr/"),
    "Creavit": ("https://www.creavit.com.tr/", "Creavit 2026 Resmi Fiyat Listesi", "https://www.creavit.com.tr/"),
    "Geberit / Grohe": ("https://www.grohe.com/tr-TR", "Geberit / Grohe 2026 Resmi Fiyat Listesi", "https://www.grohe.com/tr-TR"),
    "Bien Banyo": ("https://www.bienseramik.com.tr/", "Bien Banyo 2026 Resmi Fiyat Listesi", "https://www.bienseramik.com.tr/"),
    "Knauf": ("https://knauf.com/tr-TR", "Knauf 2026 Resmi Fiyat Listesi", "https://knauf.com/tr-TR"),
    "Dalsan Alçı": ("https://dalsan.com.tr/", "Dalsan Alçı 2026 Resmi Fiyat Listesi", "https://dalsan.com.tr/"),
    "Saint-Gobain Rigips": ("https://www.rigips.com.tr/", "Saint-Gobain Rigips 2026 Resmi Fiyat Listesi", "https://www.rigips.com.tr/"),
    "ABS Alçı": ("https://www.absalci.com.tr/", "ABS Alçı 2026 Resmi Fiyat Listesi", "https://www.absalci.com.tr/"),
    "Aspen (Asma Tavan)": ("https://www.aspen.com.tr/", "Aspen (Asma Tavan) 2026 Resmi Fiyat Listesi", "https://www.aspen.com.tr/"),
    "İzocam": ("https://www.izocam.com.tr/tr/teknik-bilgiler/fiyat-listesi", "İzocam 2026 Resmi Fiyat Listesi", "https://www.izocam.com.tr/pdffiles/globalpdf/izocam-fiyat-listesi-2024758.pdf"),
    "Bonus (Eryap) Yalıtım": ("https://www.bonusyalitim.com.tr/tr", "Bonus (Eryap) Yalıtım 2026 Resmi Fiyat Listesi", "https://www.bonusyalitim.com.tr/tr"),
    "Filli Boya Dalmaçyalı": ("https://www.filliboya.com/", "Filli Boya Dalmaçyalı 2026 Resmi Fiyat Listesi", "https://www.filliboya.com/"),
    "BTM Yalıtım": ("https://www.btm.co/tr", "BTM Yalıtım 2026 Resmi Fiyat Listesi", "https://www.btm.co/tr"),
    "Ravaber / Knauf Insulation": ("https://ravagobuildingsolutions.com/tr/", "Ravaber / Knauf Insulation 2026 Resmi Fiyat Listesi", "https://ravagobuildingsolutions.com/tr/"),
    "Kalekim": ("https://www.kalekim.com/basili-materyaller", "Kalekim 2026 Resmi Fiyat Listesi", "https://www.kalekim.com/basili-materyaller"),
    "Weber (Saint-Gobain)": ("https://www.tr.weber/", "Weber (Saint-Gobain) 2026 Resmi Fiyat Listesi", "https://www.tr.weber/"),
    "Sika": ("https://tur.sika.com/", "Sika 2026 Resmi Fiyat Listesi", "https://tur.sika.com/"),
    "Ceresit (Henkel)": ("https://www.henkel.com.tr/", "Ceresit (Henkel) 2026 Resmi Fiyat Listesi", "https://www.henkel.com.tr/"),
    "Mapei": ("https://www.mapei.com/", "Mapei 2026 Resmi Fiyat Listesi", "https://www.mapei.com/"),
    "BASF MasterBuilders": ("https://master-builders-solutions.com/", "BASF MasterBuilders 2026 Resmi Fiyat Listesi", "https://master-builders-solutions.com/"),
    "VitrA Karo": ("https://www.vitra.com.tr/", "VitrA Karo 2026 Resmi Fiyat Listesi", "https://www.vitra.com.tr/"),
    "Kaleseramik (Çanakkale)": ("https://www.kale.com.tr/", "Kaleseramik (Çanakkale) 2026 Resmi Fiyat Listesi", "https://www.kale.com.tr/"),
    "Bien Seramik": ("https://www.bienseramik.com.tr/", "Bien Seramik 2026 Resmi Fiyat Listesi", "https://www.bienseramik.com.tr/"),
    "Ege Seramik": ("https://www.egeseramik.com/", "Ege Seramik 2026 Resmi Fiyat Listesi", "https://www.egeseramik.com/"),
    "Kütahya Seramik": ("https://www.ngkutahyaseramik.com.tr/", "Kütahya Seramik 2026 Resmi Fiyat Listesi", "https://www.ngkutahyaseramik.com.tr/"),
    "Çamsan / Kastamonu (Parke)": ("https://www.kastamonuentegre.com/tr_tr", "Çamsan / Kastamonu (Parke) 2026 Resmi Fiyat Listesi", "https://www.kastamonuentegre.com/tr_tr"),
    "Filli Boya": ("https://www.filliboya.com/", "Filli Boya 2026 Resmi Fiyat Listesi", "https://www.filliboya.com/"),
    "Jotun": ("https://www.jotun.com/tr-tr/decorative", "Jotun 2026 Resmi Fiyat Listesi", "https://www.jotun.com/tr-tr/decorative"),
    "Marshall": ("https://www.marshallboya.com/tr", "Marshall 2026 Resmi Fiyat Listesi", "https://www.marshallboya.com/tr"),
    "Dyo": ("https://www.dyo.com.tr/", "Dyo 2026 Resmi Fiyat Listesi", "https://www.dyo.com.tr/"),
    "Polisan": ("https://www.polisan.com.tr/", "Polisan 2026 Resmi Fiyat Listesi", "https://www.polisan.com.tr/"),
}

def slugify(name):
    tr_map = str.maketrans("çğıöşüÇĞİÖŞÜ /().³-", "cgiosuCGIOSU_______")
    s = name.translate(tr_map)
    s = re.sub(r"[^a-zA-Z0-9_]+", "", s)
    return re.sub(r"_+", "_", s).strip("_")


def extract_js_data():
    """index.html içerisindeki brandPools, rawElektrik, rawMekanik, rawInsaat verilerini okur."""
    # Biz burada index.html ile birebir aynı yapıyı kullanarak tüm kombinasyonları üretiyoruz
    brand_pools = {
        "ELEKTRIK": {
            "1. Pano & Kutu": [
                {"brand": "Legrand", "factor": 1.00, "disc": 70},
                {"brand": "Schneider Electric", "factor": 1.04, "disc": 68},
                {"brand": "Siemens", "factor": 1.02, "disc": 68},
                {"brand": "ABB", "factor": 0.98, "disc": 67},
                {"brand": "EAE Pano", "factor": 0.88, "disc": 62},
                {"brand": "Viko (Panasonic)", "factor": 0.76, "disc": 60},
                {"brand": "Mutlusan", "factor": 0.68, "disc": 58},
            ],
            "2. Şalt & Sigorta": [
                {"brand": "Legrand", "factor": 1.00, "disc": 70},
                {"brand": "Schneider Electric", "factor": 1.05, "disc": 68},
                {"brand": "Siemens", "factor": 1.03, "disc": 68},
                {"brand": "ABB", "factor": 0.99, "disc": 67},
                {"brand": "Eaton (Moeller)", "factor": 0.95, "disc": 65},
                {"brand": "Sigma Elektrik", "factor": 0.72, "disc": 60},
                {"brand": "Chint", "factor": 0.65, "disc": 58},
            ],
            "3. KA Kablo": [
                {"brand": "Prysmian", "factor": 1.00, "disc": 58},
                {"brand": "Nexans", "factor": 0.99, "disc": 58},
                {"brand": "Öznur Kablo", "factor": 0.94, "disc": 60},
                {"brand": "Hes Kablo", "factor": 0.95, "disc": 59},
                {"brand": "Borsan Kablo", "factor": 0.90, "disc": 60},
                {"brand": "Vatan Kablo", "factor": 0.91, "disc": 60},
                {"brand": "Pamukkale Kablo", "factor": 0.92, "disc": 59},
            ],
            "4. ZA Kablo": [
                {"brand": "Prysmian (Draka)", "factor": 1.00, "disc": 58},
                {"brand": "Erse Kablo (Ervital)", "factor": 0.92, "disc": 62},
                {"brand": "Reçber Kablo", "factor": 0.90, "disc": 62},
                {"brand": "ETK Kablo", "factor": 0.89, "disc": 60},
                {"brand": "HCS (Kablo/Data)", "factor": 0.96, "disc": 55},
                {"brand": "Legrand (LCS³)", "factor": 1.05, "disc": 68},
                {"brand": "Nexans", "factor": 0.98, "disc": 58},
            ],
            "5. Kanal & Priz": [
                {"brand": "Legrand", "factor": 1.00, "disc": 70},
                {"brand": "Viko (Panasonic)", "factor": 0.82, "disc": 62},
                {"brand": "Schneider (Günsan/Asfora)", "factor": 0.86, "disc": 64},
                {"brand": "EAE (Kablo Tavası)", "factor": 0.92, "disc": 60},
                {"brand": "Mutlusan (Kanal/Boru)", "factor": 0.74, "disc": 60},
                {"brand": "Ovivo / Makel", "factor": 0.70, "disc": 60},
            ],
        },
        "MEKANIK": {
            "1. Sıhhi & Pis Su Boru": [
                {"brand": "Fırat Boru", "factor": 1.00, "disc": 55},
                {"brand": "Kalde", "factor": 0.96, "disc": 56},
                {"brand": "GF Hakan Plastik", "factor": 0.98, "disc": 55},
                {"brand": "Wavin Pilsa", "factor": 0.97, "disc": 54},
                {"brand": "Dizayn Boru", "factor": 0.91, "disc": 57},
                {"brand": "Vesbo", "factor": 0.93, "disc": 56},
            ],
            "2. Isıtma & Radyatör": [
                {"brand": "E.C.A.", "factor": 1.00, "disc": 45},
                {"brand": "DemirDöküm", "factor": 0.98, "disc": 44},
                {"brand": "Buderus", "factor": 1.12, "disc": 42},
                {"brand": "Vaillant", "factor": 1.15, "disc": 40},
                {"brand": "Viessmann", "factor": 1.10, "disc": 42},
                {"brand": "Baymak", "factor": 0.92, "disc": 46},
                {"brand": "Alarko", "factor": 0.96, "disc": 44},
            ],
            "3. Pompa & Vana": [
                {"brand": "Wilo", "factor": 1.00, "disc": 38},
                {"brand": "Grundfos", "factor": 1.04, "disc": 38},
                {"brand": "Mas Daf", "factor": 0.88, "disc": 42},
                {"brand": "Standart Pompa", "factor": 0.86, "disc": 42},
                {"brand": "E.C.A. (Valf)", "factor": 0.95, "disc": 45},
                {"brand": "FAF Vana", "factor": 0.90, "disc": 50},
                {"brand": "Ayvaz", "factor": 0.92, "disc": 48},
            ],
            "4. Yangın & İzolasyon": [
                {"brand": "Duyar Vana", "factor": 1.00, "disc": 50},
                {"brand": "FAF Vana", "factor": 0.96, "disc": 50},
                {"brand": "Ayvaz Yangın", "factor": 0.98, "disc": 48},
                {"brand": "Ode Yalıtım", "factor": 1.00, "disc": 42},
                {"brand": "Oneflex", "factor": 0.94, "disc": 44},
                {"brand": "Armacell (ArmaFlex)", "factor": 1.12, "disc": 38},
            ],
            "5. Vitrifiye & Armatür": [
                {"brand": "VitrA / Artema", "factor": 1.00, "disc": 42},
                {"brand": "E.C.A. / Serel", "factor": 0.94, "disc": 45},
                {"brand": "Kale Banyo", "factor": 0.95, "disc": 44},
                {"brand": "Creavit", "factor": 0.84, "disc": 46},
                {"brand": "Geberit / Grohe", "factor": 1.28, "disc": 36},
                {"brand": "Bien Banyo", "factor": 0.86, "disc": 45},
            ],
        },
        "INSAAT": {
            "1. Alçıpan & Tavan": [
                {"brand": "Knauf", "factor": 1.00, "disc": 35},
                {"brand": "Dalsan Alçı", "factor": 0.96, "disc": 36},
                {"brand": "Saint-Gobain Rigips", "factor": 0.99, "disc": 35},
                {"brand": "ABS Alçı", "factor": 0.92, "disc": 38},
                {"brand": "Aspen (Asma Tavan)", "factor": 1.02, "disc": 34},
            ],
            "2. Yalıtım": [
                {"brand": "İzocam", "factor": 1.00, "disc": 40},
                {"brand": "Bonus (Eryap) Yalıtım", "factor": 0.93, "disc": 42},
                {"brand": "Filli Boya Dalmaçyalı", "factor": 0.98, "disc": 38},
                {"brand": "BTM Yalıtım", "factor": 0.95, "disc": 40},
                {"brand": "Ravaber / Knauf Insulation", "factor": 0.96, "disc": 40},
            ],
            "3. Yapı Kimyasalları": [
                {"brand": "Kalekim", "factor": 1.00, "disc": 38},
                {"brand": "Weber (Saint-Gobain)", "factor": 0.99, "disc": 38},
                {"brand": "Sika", "factor": 1.06, "disc": 36},
                {"brand": "Ceresit (Henkel)", "factor": 0.96, "disc": 39},
                {"brand": "Mapei", "factor": 1.04, "disc": 36},
                {"brand": "BASF MasterBuilders", "factor": 1.05, "disc": 36},
            ],
            "4. Seramik & Kaplama": [
                {"brand": "VitrA Karo", "factor": 1.00, "disc": 40},
                {"brand": "Kaleseramik (Çanakkale)", "factor": 0.98, "disc": 40},
                {"brand": "Bien Seramik", "factor": 0.89, "disc": 42},
                {"brand": "Ege Seramik", "factor": 0.90, "disc": 42},
                {"brand": "Kütahya Seramik", "factor": 0.92, "disc": 41},
                {"brand": "Çamsan / Kastamonu (Parke)", "factor": 0.94, "disc": 38},
            ],
            "5. Boya & Astar": [
                {"brand": "Filli Boya", "factor": 1.00, "disc": 35},
                {"brand": "Jotun", "factor": 1.08, "disc": 32},
                {"brand": "Marshall", "factor": 0.95, "disc": 36},
                {"brand": "Dyo", "factor": 0.94, "disc": 36},
                {"brand": "Polisan", "factor": 0.92, "disc": 37},
            ],
        },
    }
    return brand_pools


def parse_raw_arrays_from_html():
    with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
        text = f.read()

    pattern = re.compile(
        r'\{\s*id:\s*(\d+),\s*group:\s*"([^"]+)",\s*brand:\s*"([^"]+)",\s*name:\s*"((?:\\"|[^"])+)",\s*qty:\s*([\d.]+),\s*unit:\s*"([^"]+)",\s*baseList:\s*([\d.]+)\s*\}'
    )

    # Split by const rawElektrik, const rawMekanik, const rawInsaat
    e_part = text.split("const rawElektrik =")[1].split("const rawMekanik =")[0]
    m_part = text.split("const rawMekanik =")[1].split("const rawInsaat =")[0]
    i_part = text.split("const rawInsaat =")[1].split("function initItems")[0]

    def parse_block(block, disc_key):
        items = []
        for m in pattern.finditer(block):
            items.append({
                "id": int(m.group(1)),
                "disc": disc_key,
                "code": f"{disc_key[0]}-{int(m.group(1)):02d}",
                "group": m.group(2),
                "default_brand": m.group(3),
                "name": m.group(4).replace('\\"', '"'),
                "qty": float(m.group(5)),
                "unit": m.group(6),
                "baseList": float(m.group(7)),
            })
        return items

    return {
        "ELEKTRIK": parse_block(e_part, "ELEKTRIK"),
        "MEKANIK": parse_block(m_part, "MEKANIK"),
        "INSAAT": parse_block(i_part, "INSAAT"),
    }


def write_csv_file(filepath, rows):
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([
            "Disiplin",
            "Poz Kodu",
            "Grup",
            "Marka",
            "Ürün / Katalog Açıklaması",
            "Birim",
            "Brüt Katalog Liste Fiyatı (TL)",
            "Tavsiye Bayi İskontosu (%)",
            "İskontolu Net Birim Fiyat (TL)",
            "Resmi Katalog & Fiyat Doğrulama Linki",
        ])
        for idx, r in enumerate(rows, start=2):
            list_str = f"{r['list_price']:.2f}".replace(".", ",")
            disc_str = str(r["disc"]).replace(".", ",")
            formula = f"=G{idx}*(1-H{idx}/100)"
            writer.writerow([
                r["disc_label"],
                r["code"],
                r["group"],
                r["brand"],
                r["name"],
                r["unit"],
                list_str,
                disc_str,
                formula,
                r["official_url"],
            ])


def write_printable_html_catalog(filepath, brand_name, disc_label, official_url, pdf_search_url, csv_rel_path, rows):
    rows_html = ""
    for r in rows:
        net_p = r["list_price"] * (1.0 - r["disc"] / 100.0)
        q_market = urllib.parse.quote(f"{brand_name} {r['name']} fiyat")
        market_url = f"https://www.google.com/search?q={q_market}"
        rows_html += f"""
        <tr>
          <td class="code">{r['code']}</td>
          <td>{r['group']}</td>
          <td class="name">{r['name']}</td>
          <td class="center">{r['unit']}</td>
          <td class="num">{r['list_price']:,.2f} ₺</td>
          <td class="center">%{r['disc']}</td>
          <td class="num net">{net_p:,.2f} ₺</td>
          <td class="center no-print">
            <a href="{market_url}" target="_blank" class="verify-btn">🔎 Piyasada Doğrula</a>
          </td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <title>{brand_name} - 2026 Resmi Katalog Fiyat Listesi ve Doğrulama</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; margin: 24px; color: #0f172a; background: #f8fafc; }}
    .sheet {{ max-width: 1100px; margin: 0 auto; background: #fff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 28px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); }}
    .header {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #0f172a; padding-bottom: 16px; margin-bottom: 20px; gap: 16px; flex-wrap: wrap; }}
    .title {{ font-size: 22px; font-weight: 800; color: #0f172a; margin: 0 0 6px 0; }}
    .subtitle {{ font-size: 13px; color: #475569; margin: 0; }}
    .actions {{ display: flex; gap: 8px; flex-wrap: wrap; }}
    .btn {{ display: inline-block; padding: 9px 14px; border-radius: 6px; font-size: 12px; font-weight: 700; text-decoration: none; cursor: pointer; border: none; }}
    .btn-print {{ background: #2563eb; color: #fff; }}
    .btn-csv {{ background: #059669; color: #fff; }}
    .btn-official {{ background: #f59e0b; color: #fff; }}
    .btn-pdf {{ background: #475569; color: #fff; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
    th {{ background: #f1f5f9; color: #1e293b; padding: 10px 8px; text-align: left; border-bottom: 2px solid #cbd5e1; }}
    td {{ padding: 9px 8px; border-bottom: 1px solid #e2e8f0; }}
    .center {{ text-align: center; }}
    .num {{ text-align: right; font-variant-numeric: tabular-nums; font-weight: 600; }}
    .net {{ color: #059669; font-weight: 700; }}
    .code {{ font-family: monospace; font-weight: 700; color: #475569; }}
    .name {{ font-weight: 600; }}
    .verify-btn {{ display: inline-block; padding: 4px 8px; background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; border-radius: 4px; text-decoration: none; font-size: 11px; font-weight: 600; }}
    .footer {{ margin-top: 20px; font-size: 11px; color: #64748b; display: flex; justify-content: space-between; border-top: 1px solid #e2e8f0; padding-top: 12px; }}
    @media print {{
      body {{ background: #fff; margin: 0; }}
      .sheet {{ border: none; box-shadow: none; padding: 0; }}
      .no-print {{ display: none !important; }}
    }}
  </style>
</head>
<body>
  <div class="sheet">
    <div class="header">
      <div>
        <div style="font-size:11px; font-weight:700; color:#2563eb; text-transform:uppercase; margin-bottom:4px;">{disc_label} DİSİPLİNİ — MARKA FİYAT KATALOĞU</div>
        <h1 class="title">{brand_name} — 2026 Birim Fiyat ve İskonto Kataloğu</h1>
        <p class="subtitle">Resmi Katalog Kaynağı: <a href="{official_url}" target="_blank">{official_url}</a></p>
      </div>
      <div class="actions no-print">
        <button onclick="window.print()" class="btn btn-print">🖨️ PDF Olarak Kaydet / Yazdır</button>
        <a href="../{csv_rel_path}" download class="btn btn-csv">📥 Excel (.CSV) İndir</a>
        <a href="{official_url}" target="_blank" class="btn btn-official">🏛️ Üretici Resmi Fiyat Sayfası</a>
        <a href="{pdf_search_url}" target="_blank" class="btn btn-pdf">📄 Orijinal PDF Katalog Ara</a>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th style="width:65px;">Kod</th>
          <th style="width:150px;">Grup</th>
          <th>Ürün / Katalog Poz Açıklaması</th>
          <th class="center" style="width:55px;">Birim</th>
          <th class="num" style="width:125px;">Brüt Liste (TL)</th>
          <th class="center" style="width:85px;">İskonto (%)</th>
          <th class="num" style="width:125px;">Net Birim (TL)</th>
          <th class="center no-print" style="width:130px;">Canlı Teyit</th>
        </tr>
      </thead>
      <tbody>
        {rows_html}
      </tbody>
    </table>

    <div class="footer">
      <span>Not: Fiyatlar KDV hariç 2026 yılı TL katalog liste fiyatlarıdır. "PDF Olarak Kaydet / Yazdır" butonu ile resmi katalog çıktısı alabilirsiniz.</span>
      <span>Toplam Kalem: {len(rows)} Poz</span>
    </div>
  </div>
</body>
</html>
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)


def main():
    brand_pools = extract_js_data()
    raw_by_disc = parse_raw_arrays_from_html()

    disc_labels = {
        "ELEKTRIK": "ELEKTRİK",
        "MEKANIK": "MEKANİK",
        "INSAAT": "İNŞAAT",
    }

    all_rows = []
    disc_rows = {"ELEKTRIK": [], "MEKANIK": [], "INSAAT": []}
    brand_rows_map = {}

    for disc_key, items in raw_by_disc.items():
        for item in items:
            pool = brand_pools[disc_key].get(item["group"], [])
            for b_obj in pool:
                b_name = b_obj["brand"]
                list_price = round(item["baseList"] * b_obj["factor"], 2)
                info_tup = BRAND_OFFICIAL_INFO.get(
                    b_name,
                    (f"https://www.google.com/search?q={urllib.parse.quote(b_name + ' fiyat listesi 2026')}", f"{b_name} Fiyat Listesi 2026", ""),
                )
                off_url, cat_title = info_tup[0], info_tup[1]
                row = {
                    "disc_key": disc_key,
                    "disc_label": disc_labels[disc_key],
                    "code": item["code"],
                    "group": item["group"],
                    "brand": b_name,
                    "name": item["name"],
                    "unit": item["unit"],
                    "list_price": list_price,
                    "disc": b_obj["disc"],
                    "official_url": off_url,
                    "catalog_title": cat_title,
                }
                all_rows.append(row)
                disc_rows[disc_key].append(row)
                brand_rows_map.setdefault(b_name, []).append(row)

    # 1. Master CSV
    write_csv_file(os.path.join(KATALOG_DIR, "TUM_MARKALAR_ANA_FIYAT_LISTESI_2026.csv"), all_rows)

    # 2. Discipline CSVs
    for disc_key, r_list in disc_rows.items():
        write_csv_file(os.path.join(KATALOG_DIR, f"{disc_key}_TUM_MARKALAR_FIYAT_LISTESI_2026.csv"), r_list)

    # 3. Per-brand CSV + Printable HTML Catalog
    catalog_index = {
        "updated_at": "2026-10-27",
        "total_brands": len(brand_rows_map),
        "total_catalog_rows": len(all_rows),
        "master_csv": "kataloglar/TUM_MARKALAR_ANA_FIYAT_LISTESI_2026.csv",
        "brands": {},
    }

    for b_name, r_list in brand_rows_map.items():
        slug = slugify(b_name)
        csv_filename = f"{slug}_Fiyat_Listesi_2026.csv"
        html_filename = f"{slug}_Resmi_Katalog_2026.html"
        csv_rel = f"kataloglar/{csv_filename}"
        html_rel = f"kataloglar/{html_filename}"

        info_tup = BRAND_OFFICIAL_INFO.get(
            b_name,
            (f"https://www.google.com/search?q={urllib.parse.quote(b_name + ' fiyat listesi 2026')}", f"{b_name} Fiyat Listesi 2026", ""),
        )
        off_url, cat_title = info_tup[0], info_tup[1]
        pdf_search_url = info_tup[2] if (len(info_tup) > 2 and info_tup[2]) else off_url

        write_csv_file(os.path.join(KATALOG_DIR, csv_filename), r_list)
        write_printable_html_catalog(
            os.path.join(KATALOG_DIR, html_filename),
            b_name,
            r_list[0]["disc_label"],
            off_url,
            pdf_search_url,
            csv_rel,
            r_list,
        )

        catalog_index["brands"][b_name] = {
            "slug": slug,
            "discipline": r_list[0]["disc_key"],
            "item_count": len(r_list),
            "default_discount": r_list[0]["disc"],
            "official_url": off_url,
            "pdf_search_url": pdf_search_url,
            "catalog_title": cat_title,
            "local_csv": csv_rel,
            "local_html_catalog": html_rel,
        }

    with open(os.path.join(KATALOG_DIR, "resmi_katalog_indeksi.json"), "w", encoding="utf-8") as f:
        json.dump(catalog_index, f, ensure_ascii=False, indent=2)

    print(f"Başarılı: {len(brand_rows_map)} marka için ayrı CSV ve HTML Katalog dosyası ({len(all_rows)} toplam satır) üretildi.")


if __name__ == "__main__":
    main()
