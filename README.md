# ⚡🔧🏗️ Elektrik - Mekanik - İnşaat Keşif & Marka Fiyat Listesi Teklif Sistemi

Markaların yayınladığı **birim liste fiyatlarını** otomatik eşleştirip, **marka veya grup bazlı bayi iskonto oranlarını** girerek hızlı ve hatasız keşif/teklif oluşturma aracı.

## Özellikler
- **3 Ana Disiplin Sekmesi:**
  - ⚡ **Elektrik Keşfi (50 Kalem):** Pano, Sigorta Kutusu, Şalt/Sigorta, Kuvvetli Akım (KA) Kablo, Zayıf Akım (ZA) Kablo & Data, Kanal/Tava/Boru & Anahtar-Priz.
  - 🔧 **Mekanik Tesisat Keşfi (50 Kalem):** Sıhhi & Pis Su Borulama, Isıtma & Radyatör, Pompa/Hidrofor & Vana Grubu, Yangın Tesisatı & İzolasyon, Vitrifiye & Armatür.
  - 🏗️ **İnşaat & Mimari Keşfi (30 Kalem):** Alçıpan & Asma Tavan, Isı/Ses/Su Yalıtımı, Yapı Kimyasalları, Seramik & Kaplama, Boya & Astar.
- **55+ Marka Seçeneği (Grup veya Satır Bazlı):**
  - **Elektrik:** Prysmian, Nexans, Öznur Kablo, Hes Kablo, Erse Kablo, Reçber, Legrand, Schneider Electric, Siemens, ABB, Eaton, Sigma, Chint, Viko (Panasonic), EAE, Mutlusan.
  - **Mekanik:** Fırat Boru, Kalde, GF Hakan Plastik, Wavin Pilsa, Dizayn, E.C.A., DemirDöküm, Buderus, Vaillant, Viessmann, Wilo, Grundfos, Mas Daf, Duyar Vana, FAF Vana, Ayvaz, VitrA, Kale, Ode, Armacell.
  - **İnşaat:** Knauf, Dalsan, Rigips, İzocam, Bonus Yalıtım, BTM, Kalekim, Weber, Sika, Ceresit, VitrA Karo, Kaleseramik, Bien, Filli Boya, Jotun, Marshall, Dyo.
- **📚 Tüm Marka Fiyat Listeleri (Katalog Havuzu):** Tüm alternatif markaların liste fiyatlarını, piyasa iskontolarını ve net birim fiyatlarını yan yana karşılaştırma.
- **📥 Formüllü Excel (.CSV) Çıktısı:** Tek tıkla Excel formülleri (`=H2*(1-I2/100)`) gömülü olarak indirme.

## Çalıştırma

### 1. Doğrudan Tarayıcıda Açma
`index.html` dosyasını çift tıklayarak veya yerel sunucu ile açabilirsiniz:
```bash
python3 -m http.server 8080
```
Tarayıcıda `http://localhost:8080` adresine gidin.

### 2. Python Fiyat Çekici & CSV/JSON Üretici
```bash
python3 fiyat_cekici_ve_kesif.py
```
