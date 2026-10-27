#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elektrik - Mekanik - İnşaat Keşif & Çoklu Marka Liste Fiyatı / Teklif Oluşturma Aracı
55+ Marka Havuzu + Elektrik (50 Kalem), Mekanik (50 Kalem), İnşaat (30 Kalem) CSV & JSON Üretici
"""

import csv
import json
import os
from datetime import datetime
from typing import Dict, List, Any


MARKA_HAVUZU: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
    "ELEKTRIK": {
        "1. Pano & Kutu": [
            {"marka": "Legrand", "carpan": 1.00, "iskonto": 70},
            {"marka": "Schneider Electric", "carpan": 1.04, "iskonto": 68},
            {"marka": "Siemens", "carpan": 1.02, "iskonto": 68},
            {"marka": "ABB", "carpan": 0.98, "iskonto": 67},
            {"marka": "EAE Pano", "carpan": 0.88, "iskonto": 62},
            {"marka": "Viko (Panasonic)", "carpan": 0.76, "iskonto": 60},
            {"marka": "Mutlusan", "carpan": 0.68, "iskonto": 58},
        ],
        "2. Şalt & Sigorta": [
            {"marka": "Legrand", "carpan": 1.00, "iskonto": 70},
            {"marka": "Schneider Electric", "carpan": 1.05, "iskonto": 68},
            {"marka": "Siemens", "carpan": 1.03, "iskonto": 68},
            {"marka": "ABB", "carpan": 0.99, "iskonto": 67},
            {"marka": "Eaton (Moeller)", "carpan": 0.95, "iskonto": 65},
            {"marka": "Sigma Elektrik", "carpan": 0.72, "iskonto": 60},
            {"marka": "Chint", "carpan": 0.65, "iskonto": 58},
        ],
        "3. KA Kablo": [
            {"marka": "Prysmian", "carpan": 1.00, "iskonto": 58},
            {"marka": "Nexans", "carpan": 0.99, "iskonto": 58},
            {"marka": "Öznur Kablo", "carpan": 0.94, "iskonto": 60},
            {"marka": "Hes Kablo", "carpan": 0.95, "iskonto": 59},
            {"marka": "Borsan Kablo", "carpan": 0.90, "iskonto": 60},
            {"marka": "Vatan Kablo", "carpan": 0.91, "iskonto": 60},
            {"marka": "Pamukkale Kablo", "carpan": 0.92, "iskonto": 59},
        ],
        "4. ZA Kablo": [
            {"marka": "Prysmian (Draka)", "carpan": 1.00, "iskonto": 58},
            {"marka": "Erse Kablo (Ervital)", "carpan": 0.92, "iskonto": 62},
            {"marka": "Reçber Kablo", "carpan": 0.90, "iskonto": 62},
            {"marka": "ETK Kablo", "carpan": 0.89, "iskonto": 60},
            {"marka": "HCS (Kablo/Data)", "carpan": 0.96, "iskonto": 55},
            {"marka": "Legrand (LCS³)", "carpan": 1.05, "iskonto": 68},
            {"marka": "Nexans", "carpan": 0.98, "iskonto": 58},
        ],
        "5. Kanal & Priz": [
            {"marka": "Legrand", "carpan": 1.00, "iskonto": 70},
            {"marka": "Viko (Panasonic)", "carpan": 0.82, "iskonto": 62},
            {"marka": "Schneider (Günsan/Asfora)", "carpan": 0.86, "iskonto": 64},
            {"marka": "EAE (Kablo Tavası)", "carpan": 0.92, "iskonto": 60},
            {"marka": "Mutlusan (Kanal/Boru)", "carpan": 0.74, "iskonto": 60},
            {"marka": "Ovivo / Makel", "carpan": 0.70, "iskonto": 60},
        ],
    },
    "MEKANIK": {
        "1. Sıhhi & Pis Su Boru": [
            {"marka": "Fırat Boru", "carpan": 1.00, "iskonto": 55},
            {"marka": "Kalde", "carpan": 0.96, "iskonto": 56},
            {"marka": "GF Hakan Plastik", "carpan": 0.98, "iskonto": 55},
            {"marka": "Wavin Pilsa", "carpan": 0.97, "iskonto": 54},
            {"marka": "Dizayn Boru", "carpan": 0.91, "iskonto": 57},
            {"marka": "Vesbo", "carpan": 0.93, "iskonto": 56},
        ],
        "2. Isıtma & Radyatör": [
            {"marka": "E.C.A.", "carpan": 1.00, "iskonto": 45},
            {"marka": "DemirDöküm", "carpan": 0.98, "iskonto": 44},
            {"marka": "Buderus", "carpan": 1.12, "iskonto": 42},
            {"marka": "Vaillant", "carpan": 1.15, "iskonto": 40},
            {"marka": "Viessmann", "carpan": 1.10, "iskonto": 42},
            {"marka": "Baymak", "carpan": 0.92, "iskonto": 46},
            {"marka": "Alarko", "carpan": 0.96, "iskonto": 44},
        ],
        "3. Pompa & Vana": [
            {"marka": "Wilo", "carpan": 1.00, "iskonto": 38},
            {"marka": "Grundfos", "carpan": 1.04, "iskonto": 38},
            {"marka": "Mas Daf", "carpan": 0.88, "iskonto": 42},
            {"marka": "Standart Pompa", "carpan": 0.86, "iskonto": 42},
            {"marka": "E.C.A. (Valf)", "carpan": 0.95, "iskonto": 45},
            {"marka": "FAF Vana", "carpan": 0.90, "iskonto": 50},
            {"marka": "Ayvaz", "carpan": 0.92, "iskonto": 48},
        ],
        "4. Yangın & İzolasyon": [
            {"marka": "Duyar Vana", "carpan": 1.00, "iskonto": 50},
            {"marka": "FAF Vana", "carpan": 0.96, "iskonto": 50},
            {"marka": "Ayvaz Yangın", "carpan": 0.98, "iskonto": 48},
            {"marka": "Ode Yalıtım", "carpan": 1.00, "iskonto": 42},
            {"marka": "Oneflex", "carpan": 0.94, "iskonto": 44},
            {"marka": "Armacell (ArmaFlex)", "carpan": 1.12, "iskonto": 38},
        ],
        "5. Vitrifiye & Armatür": [
            {"marka": "VitrA / Artema", "carpan": 1.00, "iskonto": 42},
            {"marka": "E.C.A. / Serel", "carpan": 0.94, "iskonto": 45},
            {"marka": "Kale Banyo", "carpan": 0.95, "iskonto": 44},
            {"marka": "Creavit", "carpan": 0.84, "iskonto": 46},
            {"marka": "Geberit / Grohe", "carpan": 1.28, "iskonto": 36},
            {"marka": "Bien Banyo", "carpan": 0.86, "iskonto": 45},
        ],
    },
    "INSAAT": {
        "1. Alçıpan & Tavan": [
            {"marka": "Knauf", "carpan": 1.00, "iskonto": 35},
            {"marka": "Dalsan Alçı", "carpan": 0.96, "iskonto": 36},
            {"marka": "Saint-Gobain Rigips", "carpan": 0.99, "iskonto": 35},
            {"marka": "ABS Alçı", "carpan": 0.92, "iskonto": 38},
            {"marka": "Aspen (Asma Tavan)", "carpan": 1.02, "iskonto": 34},
        ],
        "2. Yalıtım": [
            {"marka": "İzocam", "carpan": 1.00, "iskonto": 40},
            {"marka": "Bonus (Eryap) Yalıtım", "carpan": 0.93, "iskonto": 42},
            {"marka": "Filli Boya Dalmaçyalı", "carpan": 0.98, "iskonto": 38},
            {"marka": "BTM Yalıtım", "carpan": 0.95, "iskonto": 40},
            {"marka": "Ravaber / Knauf Insulation", "carpan": 0.96, "iskonto": 40},
        ],
        "3. Yapı Kimyasalları": [
            {"marka": "Kalekim", "carpan": 1.00, "iskonto": 38},
            {"marka": "Weber (Saint-Gobain)", "carpan": 0.99, "iskonto": 38},
            {"marka": "Sika", "carpan": 1.06, "iskonto": 36},
            {"marka": "Ceresit (Henkel)", "carpan": 0.96, "iskonto": 39},
            {"marka": "Mapei", "carpan": 1.04, "iskonto": 36},
            {"marka": "BASF MasterBuilders", "carpan": 1.05, "iskonto": 36},
        ],
        "4. Seramik & Kaplama": [
            {"marka": "VitrA Karo", "carpan": 1.00, "iskonto": 40},
            {"marka": "Kaleseramik (Çanakkale)", "carpan": 0.98, "iskonto": 40},
            {"marka": "Bien Seramik", "carpan": 0.89, "iskonto": 42},
            {"marka": "Ege Seramik", "carpan": 0.90, "iskonto": 42},
            {"marka": "Kütahya Seramik", "carpan": 0.92, "iskonto": 41},
            {"marka": "Çamsan / Kastamonu (Parke)", "carpan": 0.94, "iskonto": 38},
        ],
        "5. Boya & Astar": [
            {"marka": "Filli Boya", "carpan": 1.00, "iskonto": 35},
            {"marka": "Jotun", "carpan": 1.08, "iskonto": 32},
            {"marka": "Marshall", "carpan": 0.95, "iskonto": 36},
            {"marka": "Dyo", "carpan": 0.94, "iskonto": 36},
            {"marka": "Polisan", "carpan": 0.92, "iskonto": 37},
        ],
    },
}


MEKANIK_50_KALEM: List[Dict[str, Any]] = [
    {"sira": 1, "bolum": "1. Sıhhi & Pis Su Boru", "marka": "Fırat Boru", "aciklama": "PPRC Ø20 mm PN20 Temiz Su Borusu (Soğuk/Sıcak Su)", "miktar": 1400, "birim": "m", "liste_fiyati": 92.0, "iskonto": 55.0},
    {"sira": 2, "bolum": "1. Sıhhi & Pis Su Boru", "marka": "Fırat Boru", "aciklama": "PPRC Ø25 mm PN20 Kompozit (Folyo/Cam Elyaf) Temiz Su Borusu", "miktar": 950, "birim": "m", "liste_fiyati": 158.0, "iskonto": 55.0},
    {"sira": 3, "bolum": "1. Sıhhi & Pis Su Boru", "marka": "Fırat Boru", "aciklama": "PPRC Ø32 mm PN20 Kompozit Kolon Temiz Su Borusu", "miktar": 420, "birim": "m", "liste_fiyati": 265.0, "iskonto": 55.0},
    {"sira": 4, "bolum": "1. Sıhhi & Pis Su Boru", "marka": "Fırat Boru", "aciklama": "PPRC Ø40 mm PN20 Kompozit Ana Kolon Temiz Su Borusu", "miktar": 210, "birim": "m", "liste_fiyati": 410.0, "iskonto": 55.0},
    {"sira": 5, "bolum": "1. Sıhhi & Pis Su Boru", "marka": "Fırat Boru", "aciklama": "PPRC Ø50 mm PN20 Kompozit Hidrofor Çıkış / Ana Dağıtım Borusu", "miktar": 120, "birim": "m", "liste_fiyati": 640.0, "iskonto": 55.0},
    {"sira": 6, "bolum": "1. Sıhhi & Pis Su Boru", "marka": "Fırat Boru", "aciklama": "PPRC Ek Parça Paketi (Dirsek, Te, Manşon, İstavroz, Rakor - Ø20-50mm)", "miktar": 1, "birim": "Set", "liste_fiyati": 85000.0, "iskonto": 55.0},
    {"sira": 7, "bolum": "1. Sıhhi & Pis Su Boru", "marka": "Fırat Boru", "aciklama": "PVC Ø50 mm (3.2mm) Conta Yuvalı Pis Su Borusu", "miktar": 650, "birim": "m", "liste_fiyati": 148.0, "iskonto": 55.0},
    {"sira": 8, "bolum": "1. Sıhhi & Pis Su Boru", "marka": "Fırat Boru", "aciklama": "PVC Ø75 mm (3.2mm) Conta Yuvalı Pis Su Borusu", "miktar": 320, "birim": "m", "liste_fiyati": 235.0, "iskonto": 55.0},
    {"sira": 9, "bolum": "1. Sıhhi & Pis Su Boru", "marka": "Fırat Boru", "aciklama": "Sessiz Boru (Silence) Ø110 mm Bina İçi Atık Su / Pis Su Kolon Borusu", "miktar": 480, "birim": "m", "liste_fiyati": 520.0, "iskonto": 55.0},
    {"sira": 10, "bolum": "1. Sıhhi & Pis Su Boru", "marka": "Fırat Boru", "aciklama": "PVC Ø160 mm Bina Altı / Yatay Ana Pis Su Toplayıcı Boru", "miktar": 140, "birim": "m", "liste_fiyati": 890.0, "iskonto": 55.0},
    {"sira": 11, "bolum": "1. Sıhhi & Pis Su Boru", "marka": "Fırat Boru", "aciklama": "PVC Atık Su Ek Parçaları (45°/87° Dirsek, Çatal, Temizleme Parçası)", "miktar": 1, "birim": "Set", "liste_fiyati": 64000.0, "iskonto": 55.0},
    {"sira": 12, "bolum": "1. Sıhhi & Pis Su Boru", "marka": "Fırat Boru", "aciklama": "Paslanmaz Izgaralı Koku Fermalı Yer Süzgeci ve Balkon/Teras Süzgeçleri", "miktar": 65, "birim": "Adet", "liste_fiyati": 680.0, "iskonto": 55.0},
    {"sira": 13, "bolum": "2. Isıtma & Radyatör", "marka": "E.C.A.", "aciklama": "28 kW Tam Yoğuşmalı Kombi (Baca Seti Dahil)", "miktar": 12, "birim": "Adet", "liste_fiyati": 46800.0, "iskonto": 45.0},
    {"sira": 14, "bolum": "2. Isıtma & Radyatör", "marka": "E.C.A.", "aciklama": "100 kW Duvar Tipi Yoğuşmalı Kaskad Kazan Ünitesi", "miktar": 2, "birim": "Adet", "liste_fiyati": 168000.0, "iskonto": 45.0},
    {"sira": 15, "bolum": "2. Isıtma & Radyatör", "marka": "E.C.A.", "aciklama": "PKKP Tip 22 (600 mm Yükseklik) Çelik Panel Radyatör (Toplam Metraj)", "miktar": 96, "birim": "m", "liste_fiyati": 4850.0, "iskonto": 45.0},
    {"sira": 16, "bolum": "2. Isıtma & Radyatör", "marka": "E.C.A.", "aciklama": "500x1000 mm Beyaz/Krom Banyo Havlupan Radyatör", "miktar": 24, "birim": "Adet", "liste_fiyati": 3450.0, "iskonto": 45.0},
    {"sira": 17, "bolum": "2. Isıtma & Radyatör", "marka": "E.C.A.", "aciklama": "1/2\" Köşe Tipi Termostatik Radyatör Valfi + Dönüş Valfi Takımı", "miktar": 85, "birim": "Takım", "liste_fiyati": 1380.0, "iskonto": 45.0},
    {"sira": 18, "bolum": "2. Isıtma & Radyatör", "marka": "E.C.A.", "aciklama": "1\" Debi Ayarlı / Dengeleme Valfli Isıtma Kollektörü (8 Çıkışlı + Dolap)", "miktar": 14, "birim": "Set", "liste_fiyati": 9200.0, "iskonto": 45.0},
    {"sira": 19, "bolum": "2. Isıtma & Radyatör", "marka": "E.C.A.", "aciklama": "PEX-b Ø16x2.0 mm Oksijen Bariyerli Kılıflı Mobil / Yerden Isıtma Borusu", "miktar": 3600, "birim": "m", "liste_fiyati": 54.0, "iskonto": 45.0},
    {"sira": 20, "bolum": "2. Isıtma & Radyatör", "marka": "E.C.A.", "aciklama": "Kapalı Genleşme Tankı 200 Litre (10 Bar) + Hava Ayırıcı ve Tortu Tutucu", "miktar": 2, "birim": "Set", "liste_fiyati": 28500.0, "iskonto": 45.0},
    {"sira": 21, "bolum": "2. Isıtma & Radyatör", "marka": "E.C.A.", "aciklama": "Boyler 500 Litre Çift Serpantinli Emaye Sıcak Su Hazırlayıcı", "miktar": 1, "birim": "Adet", "liste_fiyati": 64000.0, "iskonto": 45.0},
    {"sira": 22, "bolum": "2. Isıtma & Radyatör", "marka": "E.C.A.", "aciklama": "Oda Termostatı (Kablosuz Dijital Programlanabilir Modülasyonlu)", "miktar": 12, "birim": "Adet", "liste_fiyati": 3850.0, "iskonto": 45.0},
    {"sira": 23, "bolum": "3. Pompa & Vana", "marka": "Wilo", "aciklama": "İki Pompalı Frekans Konvertörlü Paket Hidrofor Seti", "miktar": 1, "birim": "Set", "liste_fiyati": 195000.0, "iskonto": 38.0},
    {"sira": 24, "bolum": "3. Pompa & Vana", "marka": "Wilo", "aciklama": "25/1-6 Islak Rotorlu Frekans Konvertörlü Sirkülasyon Pompası", "miktar": 4, "birim": "Adet", "liste_fiyati": 12400.0, "iskonto": 38.0},
    {"sira": 25, "bolum": "3. Pompa & Vana", "marka": "Wilo", "aciklama": "40/0.5-12 Flanşlı Yüksek Verimli Ana Isıtma Sirkülasyon Pompası", "miktar": 2, "birim": "Adet", "liste_fiyati": 54800.0, "iskonto": 38.0},
    {"sira": 26, "bolum": "3. Pompa & Vana", "marka": "Wilo", "aciklama": "Flatörlü Pis Su / Drenaj Dalgıç Pompası", "miktar": 2, "birim": "Adet", "liste_fiyati": 14200.0, "iskonto": 38.0},
    {"sira": 27, "bolum": "3. Pompa & Vana", "marka": "E.C.A. (Valf)", "aciklama": "1/2\" ve 3/4\" Tam Geçişli Pirinç Küresel Vana (PN25 - Ortalama)", "miktar": 95, "birim": "Adet", "liste_fiyati": 513.0, "iskonto": 45.0},
    {"sira": 28, "bolum": "3. Pompa & Vana", "marka": "E.C.A. (Valf)", "aciklama": "1\" ve 1 1/4\" Tam Geçişli Pirinç Küresel Vana (Kolon Kesme Vanaları)", "miktar": 36, "birim": "Adet", "liste_fiyati": 1216.0, "iskonto": 45.0},
    {"sira": 29, "bolum": "3. Pompa & Vana", "marka": "FAF Vana", "aciklama": "DN65 / DN80 Wafer Tipi EPDM Contalı Kelebek Vana (Kollu)", "miktar": 14, "birim": "Adet", "liste_fiyati": 2565.0, "iskonto": 50.0},
    {"sira": 30, "bolum": "3. Pompa & Vana", "marka": "FAF Vana", "aciklama": "DN50 / DN65 Flanşlı Pislik Tutucu + Çalpara/Wafer Çekvalf Seti", "miktar": 10, "birim": "Set", "liste_fiyati": 4140.0, "iskonto": 50.0},
    {"sira": 31, "bolum": "3. Pompa & Vana", "marka": "Ayvaz", "aciklama": "DN65 / DN80 Kauçuk Kompansatör + Basınç Düşürücü Vana Grubu", "miktar": 6, "birim": "Set", "liste_fiyati": 6348.0, "iskonto": 48.0},
    {"sira": 32, "bolum": "3. Pompa & Vana", "marka": "E.C.A. (Valf)", "aciklama": "Otomatik Hava Purjörü 1/2\" + Manometre (0-10 Bar) + Termometre Seti", "miktar": 18, "birim": "Set", "liste_fiyati": 1092.5, "iskonto": 45.0},
    {"sira": 33, "bolum": "4. Yangın & İzolasyon", "marka": "Duyar Vana", "aciklama": "Sıva Altı / Üstü Tüplü Yangın Dolabı (1\" 30m Kauçuk Hortumlu + 6kg KKT)", "miktar": 8, "birim": "Adet", "liste_fiyati": 14500.0, "iskonto": 50.0},
    {"sira": 34, "bolum": "4. Yangın & İzolasyon", "marka": "Duyar Vana", "aciklama": "UL/FM Onaylı 1/2\" K=80 68°C Sarkık/Dik Tip Sprinkler Başlığı + Rozet", "miktar": 160, "birim": "Adet", "liste_fiyati": 380.0, "iskonto": 50.0},
    {"sira": 35, "bolum": "4. Yangın & İzolasyon", "marka": "Duyar Vana", "aciklama": "1\"x1/2\" Paslanmaz Esnek (Flex) Sprinkler Bağlantı Hortumu (100 cm)", "miktar": 160, "birim": "Adet", "liste_fiyati": 740.0, "iskonto": 50.0},
    {"sira": 36, "bolum": "4. Yangın & İzolasyon", "marka": "Duyar Vana", "aciklama": "Kat Kontrol Vana Grubu (İzleme Anahtarlı Kelebek Vana + Akış Anahtarı)", "miktar": 4, "birim": "Set", "liste_fiyati": 16800.0, "iskonto": 50.0},
    {"sira": 37, "bolum": "4. Yangın & İzolasyon", "marka": "Duyar Vana", "aciklama": "Islak Alarm Vana İstasyonu DN100 + İtfaiye Su Verme Ağzı (Siyam İkizi)", "miktar": 1, "birim": "Set", "liste_fiyati": 44000.0, "iskonto": 50.0},
    {"sira": 38, "bolum": "4. Yangın & İzolasyon", "marka": "Ode Yalıtım", "aciklama": "9mm / 13mm Elastomerik Kauçuk Köpüğü Boru İzolasyonu (Ø20-Ø63 Ortalama)", "miktar": 2400, "birim": "m", "liste_fiyati": 78.0, "iskonto": 42.0},
    {"sira": 39, "bolum": "4. Yangın & İzolasyon", "marka": "Ode Yalıtım", "aciklama": "Alüminyum Folyo Kaplı Camyünü Havalandırma Kanal İzolasyonu (25mm)", "miktar": 450, "birim": "m²", "liste_fiyati": 245.0, "iskonto": 42.0},
    {"sira": 40, "bolum": "4. Yangın & İzolasyon", "marka": "Ode Yalıtım", "aciklama": "Galvaniz Sac Hava Kanalı + Menfez / Anemostad + Ses İzolasyonlu Flex Kanal", "miktar": 320, "birim": "m²", "liste_fiyati": 1180.0, "iskonto": 42.0},
    {"sira": 41, "bolum": "4. Yangın & İzolasyon", "marka": "Ode Yalıtım", "aciklama": "Split / VRF Klima Bakır Borulama Çifti (İzoleli) + Drenaj Hattı", "miktar": 380, "birim": "m", "liste_fiyati": 890.0, "iskonto": 42.0},
    {"sira": 42, "bolum": "5. Vitrifiye & Armatür", "marka": "VitrA / Artema", "aciklama": "Kanalsız (Rim-ex) Asma Klozet + Yavaş Kapanır Klozet Kapağı", "miktar": 24, "birim": "Takım", "liste_fiyati": 8950.0, "iskonto": 42.0},
    {"sira": 43, "bolum": "5. Vitrifiye & Armatür", "marka": "VitrA / Artema", "aciklama": "8 cm / 12 cm Tuğla/Alçıpan Duvar Tipi Gömme Rezervuar + Krom Kumanda Paneli", "miktar": 24, "birim": "Set", "liste_fiyati": 6400.0, "iskonto": 42.0},
    {"sira": 44, "bolum": "5. Vitrifiye & Armatür", "marka": "VitrA / Artema", "aciklama": "60 cm Tezgah Üstü / Yarı Gömme Porselen Lavabo", "miktar": 28, "birim": "Adet", "liste_fiyati": 4200.0, "iskonto": 42.0},
    {"sira": 45, "bolum": "5. Vitrifiye & Armatür", "marka": "VitrA / Artema", "aciklama": "Fotoselli / Yıkama Valfli Pisuar + Ara Bölme Seti", "miktar": 8, "birim": "Takım", "liste_fiyati": 9800.0, "iskonto": 42.0},
    {"sira": 46, "bolum": "5. Vitrifiye & Armatür", "marka": "E.C.A. / Serel", "aciklama": "Krom Lavabo Bataryası (Perlatörlü, Çelik Flex Bağlantılı)", "miktar": 28, "birim": "Adet", "liste_fiyati": 3901.0, "iskonto": 45.0},
    {"sira": 47, "bolum": "5. Vitrifiye & Armatür", "marka": "E.C.A. / Serel", "aciklama": "Döner Borulu Mutfak / Ofis Eviye Bataryası", "miktar": 14, "birim": "Adet", "liste_fiyati": 4559.0, "iskonto": 45.0},
    {"sira": 48, "bolum": "5. Vitrifiye & Armatür", "marka": "E.C.A. / Serel", "aciklama": "Banyo Bataryası + Sürgülü El Duşu Takımı", "miktar": 12, "birim": "Set", "liste_fiyati": 6486.0, "iskonto": 45.0},
    {"sira": 49, "bolum": "5. Vitrifiye & Armatür", "marka": "E.C.A. / Serel", "aciklama": "1/2\" Filtreli Krom Ara Musluk + Taharet Musluğu", "miktar": 96, "birim": "Adet", "liste_fiyati": 648.6, "iskonto": 45.0},
    {"sira": 50, "bolum": "5. Vitrifiye & Armatür", "marka": "VitrA / Artema", "aciklama": "Bedensel Engelli WC Tutunma Barları + Engelli Klozet ve Lavabo Seti", "miktar": 2, "birim": "Set", "liste_fiyati": 26500.0, "iskonto": 42.0},
]


def csv_yaz(dosya_yolu: str, disiplin: str, satirlar: List[Dict[str, Any]]) -> None:
    with open(dosya_yolu, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([
            "No", "Disiplin", "Grup", "Secilen Marka", "Malzeme Aciklamasi",
            "Miktar", "Birim", "Liste Fiyati (TL)", "Iskonto (%)",
            "Net Birim Fiyat (TL)", "Toplam Tutar (TL)"
        ])
        for idx, k in enumerate(satirlar, start=2):
            writer.writerow([
                k["sira"],
                disiplin,
                k["bolum"],
                k["marka"],
                k["aciklama"],
                k["miktar"],
                k["birim"],
                f"{k['liste_fiyati']:.2f}".replace(".", ","),
                f"{k['iskonto']:.1f}".replace(".", ","),
                f"=H{idx}*(1-I{idx}/100)",
                f"=F{idx}*J{idx}",
            ])


if __name__ == "__main__":
    klasor = os.path.dirname(os.path.abspath(__file__))
    csv_yaz(os.path.join(klasor, "Mekanik_Kesif_Teklif_50_Kalem.csv"), "MEKANIK", MEKANIK_50_KALEM)
    with open(os.path.join(klasor, "marka_fiyat_havuzu.json"), "w", encoding="utf-8") as jf:
        json.dump(
            {
                "guncelleme": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "marka_havuzu": MARKA_HAVUZU,
            },
            jf,
            ensure_ascii=False,
            indent=2,
        )
    print("[OK] Mekanik_Kesif_Teklif_50_Kalem.csv ve marka_fiyat_havuzu.json olusturuldu.")
