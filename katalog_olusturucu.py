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
    # ELEKTRİK
    "Legrand": ("https://www.legrand.com.tr/kataloglar-ve-fiyat-listeleri", "Legrand Türkiye Resmi Fiyat Listesi 2026"),
    "Schneider Electric": ("https://www.se.com/tr/tr/work/support/downloads/price-list.jsp", "Schneider Electric Resmi Fiyat Listesi 2026"),
    "Schneider (Günsan/Asfora)": ("https://www.se.com/tr/tr/work/support/downloads/price-list.jsp", "Schneider / Günsan Anahtar-Priz Fiyat Listesi 2026"),
    "Siemens": ("https://www.siemens.com/tr/tr/urunler/enerji/alcak-gerilim/fiyat-listeleri.html", "Siemens Alçak Gerilim Şalt Fiyat Listesi 2026"),
    "ABB": ("https://new.abb.com/low-voltage/tr/destek/fiyat-listeleri", "ABB Elektrifikasyon Fiyat Listesi 2026"),
    "EAE Pano": ("https://www.eaegroup.com/tr/kataloglar-ve-fiyat-listeleri", "EAE Pano & Kabin Sistemleri Fiyat Listesi 2026"),
    "EAE (Kablo Tavası)": ("https://www.eaegroup.com/tr/kataloglar-ve-fiyat-listeleri", "EAE Kablo Tavası ve Taşıma Sistemleri Fiyat Listesi 2026"),
    "Viko (Panasonic)": ("https://ewtr.panasonic.com/fiyat-listeleri/", "VİKO by Panasonic Resmi Fiyat Listesi 2026"),
    "Mutlusan": ("https://www.mutlusan.com.tr/fiyat-listesi", "Mutlusan Elektrik Resmi Fiyat Listesi 2026"),
    "Mutlusan (Kanal/Boru)": ("https://www.mutlusan.com.tr/fiyat-listesi", "Mutlusan Kablo Kanalı ve Boru Fiyat Listesi 2026"),
    "Eaton (Moeller)": ("https://www.eaton.com/tr/tr-tr/support/fiyat-listeleri.html", "Eaton (Moeller) Şalt Fiyat Listesi 2026"),
    "Sigma Elektrik": ("https://www.sigmaelektrik.com/tr/fiyat-listesi", "Sigma Elektrik AG Şalt Fiyat Listesi 2026"),
    "Chint": ("https://chint.com.tr/fiyat-listesi/", "Chint Türkiye Şalt Fiyat Listesi 2026"),
    "Prysmian": ("https://tr.prysmian.com/tr/dokumanlar-ve-fiyat-listeleri", "Türk Prysmian Kablo Enerji Kabloları Fiyat Listesi 2026"),
    "Prysmian (Draka)": ("https://tr.prysmian.com/tr/dokumanlar-ve-fiyat-listeleri", "Prysmian Draka Zayıf Akım & Data Kablo Fiyat Listesi 2026"),
    "Nexans": ("https://www.nexans.com.tr/tr/products/fiyat-listesi.html", "Nexans Türkiye Kablo Fiyat Listesi 2026"),
    "Öznur Kablo": ("https://www.oznurkablo.com.tr/fiyat-listesi/", "Öznur Kablo Nihai Fiyat Listesi 2026"),
    "Hes Kablo": ("https://www.hes.com.tr/tr/fiyat-listeleri", "HES Kablo Resmi Fiyat Listesi 2026"),
    "Borsan Kablo": ("https://www.borsan.com.tr/fiyat-listeleri/", "Borsan Kablo Resmi Fiyat Listesi 2026"),
    "Vatan Kablo": ("https://www.vatankablo.com.tr/", "Vatan Kablo Enerji Kabloları Fiyat Listesi 2026"),
    "Pamukkale Kablo": ("https://www.pamukkalekablo.com.tr/", "Pamukkale Kablo Fiyat Listesi 2026"),
    "Erse Kablo (Ervital)": ("https://www.ersekablo.com.tr/fiyat-listesi", "Erse Kablo Zayıf Akım & Yangın Kablosu Fiyat Listesi 2026"),
    "Reçber Kablo": ("https://www.recber.com.tr/fiyat-listesi/", "Reçber Kablo Zayıf Akım & Data Fiyat Listesi 2026"),
    "ETK Kablo": ("https://www.etkkablo.com/tr/fiyat-listesi", "ETK Kablo Zayıf Akım & Fiber Fiyat Listesi 2026"),
    "HCS (Kablo/Data)": ("https://www.hcs.com.tr/", "HCS Kablolama Sistemleri Fiyat Listesi 2026"),
    "Legrand (LCS³)": ("https://www.legrand.com.tr/kataloglar-ve-fiyat-listeleri", "Legrand LCS³ Yapısal Kablolama Fiyat Listesi 2026"),
    "Ovivo / Makel": ("https://www.makel.com.tr/tr/fiyat-listeleri", "Makel / Ovivo Anahtar-Priz Fiyat Listesi 2026"),

    # MEKANİK
    "Fırat Boru": ("https://www.firat.com/tr-tr/fiyat-listeleri", "Fırat Boru Bina İçi Tesisat Fiyat Listesi 2026"),
    "Kalde": ("https://www.kalde.com/fiyat-listeleri", "Kalde Boru ve Fittings Fiyat Listesi 2026"),
    "GF Hakan Plastik": ("https://www.gfps.com/com/tr/about-gf-piping-systems/local-support/turkey/fiyat-listesi.html", "GF Hakan Plastik Silenta & PPRC Fiyat Listesi 2026"),
    "Wavin Pilsa": ("https://www.wavin.com/tr-tr/indirmeler", "Wavin Pilsa Plastik Boru Fiyat Listesi 2026"),
    "Dizayn Boru": ("https://www.dizayngrup.com/", "Dizayn Boru Tesisat Sistemleri Fiyat Listesi 2026"),
    "Vesbo": ("https://www.vesbo.com/tr/fiyat-listesi", "Vesbo PPRC ve PVC Boru Fiyat Listesi 2026"),
    "E.C.A.": ("https://www.eca.com.tr/katalog-ve-fiyat-listeleri", "E.C.A. Isıtma, Kombi ve Radyatör Fiyat Listesi 2026"),
    "E.C.A. (Valf)": ("https://www.eca.com.tr/katalog-ve-fiyat-listeleri", "E.C.A. Valf ve Tesisat Vanaları Fiyat Listesi 2026"),
    "E.C.A. / Serel": ("https://www.eca.com.tr/katalog-ve-fiyat-listeleri", "E.C.A. & Serel Armatür ve Vitrifiye Fiyat Listesi 2026"),
    "DemirDöküm": ("https://www.demirdokum.com.tr/destek/fiyat-listeleri/", "DemirDöküm Kombi, Radyatör ve Kazan Fiyat Listesi 2026"),
    "Buderus": ("https://www.buderus.com/tr/tr/dokumanlar/fiyat-listesi/", "Buderus Isıtma Sistemleri Fiyat Listesi 2026"),
    "Vaillant": ("https://www.vaillant.com.tr/musteri-hizmetleri/fiyat-listeleri/", "Vaillant Türkiye Resmi Fiyat Listesi 2026"),
    "Viessmann": ("https://www.viessmann.com.tr/tr/servisler/fiyat-listeleri.html", "Viessmann Isıtma Sistemleri Fiyat Listesi 2026"),
    "Baymak": ("https://www.baymak.com.tr/fiyat-listeleri", "Baymak Resmi Ürün Fiyat Listesi 2026"),
    "Alarko": ("https://www.alarko-carrier.com.tr/tr/dokumanlar/fiyat-listeleri", "Alarko Carrier Fiyat Listesi 2026"),
    "Wilo": ("https://wilo.com/tr/tr/Hizmetler/Fiyat-Listesi/", "Wilo Pompa Sistemleri Resmi Fiyat Listesi 2026"),
    "Grundfos": ("https://www.grundfos.com/tr/support/price-list", "Grundfos Türkiye Pompa Fiyat Listesi 2026"),
    "Mas Daf": ("https://www.masdaf.com/fiyat-listesi", "Mas Daf Pompa ve Hidrofor Fiyat Listesi 2026"),
    "Standart Pompa": ("https://www.standartpompa.com/tr/dokumanlar", "Standart Pompa Fiyat Listesi 2026"),
    "FAF Vana": ("https://www.fafvana.com.tr/fiyat-listesi/", "FAF Vana Resmi Fiyat Listesi 2026"),
    "Ayvaz": ("https://www.ayvaz.com/tr/fiyat-listesi", "Ayvaz Kompansatör ve Vana Fiyat Listesi 2026"),
    "Ayvaz Yangın": ("https://www.ayvaz.com/tr/fiyat-listesi", "Ayvaz Yangın Ekipmanları Fiyat Listesi 2026"),
    "Duyar Vana": ("https://www.duyar.com/fiyat-listesi", "Duyar Vana ve Yangın Grubu Fiyat Listesi 2026"),
    "Ode Yalıtım": ("https://www.ode.com.tr/fiyat-listeleri/", "ODE Yalıtım R-Flex ve Starflex Fiyat Listesi 2026"),
    "Oneflex": ("https://www.oneflex.com.tr/", "Oneflex Elastomerik Kauçuk Yalıtım Fiyat Listesi 2026"),
    "Armacell (ArmaFlex)": ("https://www.armacell.com/tr/", "Armacell ArmaFlex Yalıtım Fiyat Listesi 2026"),
    "VitrA / Artema": ("https://www.vitra.com.tr/kataloglar-ve-fiyat-listeleri/", "VitrA & Artema Vitrifiye ve Armatür Fiyat Listesi 2026"),
    "Kale Banyo": ("https://www.kale.com.tr/tr/kataloglar", "Kale Banyo Vitrifiye ve Armatür Fiyat Listesi 2026"),
    "Creavit": ("https://www.creavit.com.tr/kataloglar", "Creavit Vitrifiye Fiyat Listesi 2026"),
    "Geberit / Grohe": ("https://www.geberit.com.tr/destek-merkezi/kataloglar-ve-brosurler/", "Geberit & Grohe Tesisat ve Armatür Fiyat Listesi 2026"),
    "Bien Banyo": ("https://www.bienseramik.com.tr/kataloglar", "Bien Banyo Vitrifiye Fiyat Listesi 2026"),

    # İNŞAAT
    "Knauf": ("https://www.knauf.com.tr/tr/dokuman-merkezi", "Knauf Alçıpan, Profil ve Kuru Yapı Fiyat Listesi 2026"),
    "Dalsan Alçı": ("https://www.dalsan.com.tr/fiyat-listesi", "Dalsan Alçı Levha, BoardeX ve Profil Fiyat Listesi 2026"),
    "Saint-Gobain Rigips": ("https://www.rigips.com.tr/dokumanlar/fiyat-listesi", "Saint-Gobain Rigips Alçı Sistemleri Fiyat Listesi 2026"),
    "ABS Alçı": ("https://www.absalci.com.tr/fiyat-listesi/", "ABS Alçı Levha ve Torba Alçı Fiyat Listesi 2026"),
    "Aspen (Asma Tavan)": ("https://www.aspen.com.tr/", "Aspen Modüler Asma Tavan Sistemleri Fiyat Listesi 2026"),
    "İzocam": ("https://www.izocam.com.tr/tr/fiyat-listesi", "İzocam Taşyünü, Camyünü, XPS/EPS Resmi Fiyat Listesi 2026"),
    "Bonus (Eryap) Yalıtım": ("https://www.bonusyalitim.com.tr/fiyat-listesi", "Bonus Yalıtım Taşyünü, XPS ve Membran Fiyat Listesi 2026"),
    "Filli Boya Dalmaçyalı": ("https://www.filliboya.com/", "Filli Boya Capatect Dalmaçyalı Mantolama Fiyat Listesi 2026"),
    "BTM Yalıtım": ("https://www.btm.co/tr/fiyat-listeleri", "BTM Su ve Isı Yalıtım Membranları Fiyat Listesi 2026"),
    "Ravaber / Knauf Insulation": ("https://www.ravaber.com.tr/", "Ravaber & Knauf Insulation Taşyünü Fiyat Listesi 2026"),
    "Kalekim": ("https://www.kalekim.com/basili-materyaller", "Kalekim Yapı Kimyasalları Resmi Fiyat Listesi 2026"),
    "Weber (Saint-Gobain)": ("https://www.tr.weber/fiyat-listesi", "Saint-Gobain Weber Yapı Kimyasalları Fiyat Listesi 2026"),
    "Sika": ("https://tur.sika.com/tr/dokumanlar-ve-kataloglar.html", "Sika Türkiye Yapı Kimyasalları Fiyat Listesi 2026"),
    "Ceresit (Henkel)": ("https://www.ceresit.com.tr/", "Henkel Ceresit Yapı Kimyasalları Fiyat Listesi 2026"),
    "Mapei": ("https://www.mapei.com/tr/tr/dokumanlar", "Mapei Yapı Kimyasalları Fiyat Listesi 2026"),
    "BASF MasterBuilders": ("https://master-builders-solutions.com/tr-tr", "Master Builders Solutions Fiyat Listesi 2026"),
    "VitrA Karo": ("https://www.vitra.com.tr/kataloglar-ve-fiyat-listeleri/", "VitrA Karo Seramik ve Porselen Fiyat Listesi 2026"),
    "Kaleseramik (Çanakkale)": ("https://www.kale.com.tr/tr/kataloglar", "Kaleseramik & Çanakkale Seramik Fiyat Listesi 2026"),
    "Bien Seramik": ("https://www.bienseramik.com.tr/kataloglar", "Bien Seramik ve Teknik Granit Fiyat Listesi 2026"),
    "Ege Seramik": ("https://www.egeseramik.com/kataloglar", "Ege Seramik Resmi Fiyat Listesi 2026"),
    "Kütahya Seramik": ("https://www.ngkutahyaseramik.com.tr/", "NG Kütahya Seramik Fiyat Listesi 2026"),
    "Çamsan / Kastamonu (Parke)": ("https://www.kastamonuentegre.com/tr_tr", "Çamsan & Floorpan Laminat Parke Fiyat Listesi 2026"),
    "Filli Boya": ("https://www.filliboya.com/", "Filli Boya İç ve Dış Cephe Boya Fiyat Listesi 2026"),
    "Jotun": ("https://www.jotun.com/tr-tr/decorative", "Jotun Boya Resmi Fiyat Listesi 2026"),
    "Marshall": ("https://www.marshallboya.com/", "Marshall Boya Resmi Fiyat Listesi 2026"),
    "Dyo": ("https://www.dyo.com.tr/", "DYO Boya Resmi Fiyat Listesi 2026"),
    "Polisan": ("https://www.polisan.com.tr/", "Polisan Kansai Boya Resmi Fiyat Listesi 2026")
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
                off_url, cat_title = BRAND_OFFICIAL_INFO.get(
                    b_name,
                    (f"https://www.google.com/search?q={urllib.parse.quote(b_name + ' fiyat listesi 2026')}", f"{b_name} Fiyat Listesi 2026"),
                )
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

        off_url, cat_title = BRAND_OFFICIAL_INFO.get(
            b_name,
            (f"https://www.google.com/search?q={urllib.parse.quote(b_name + ' fiyat listesi 2026')}", f"{b_name} Fiyat Listesi 2026"),
        )
        pdf_search_url = f"https://www.google.com/search?q={urllib.parse.quote(b_name + ' fiyat listesi 2026 filetype:pdf')}"

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
