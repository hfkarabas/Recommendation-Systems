# TASK 04.1 — Metodolojik Denetim ve Doğrulama Raporu (Methodological Audit & Validation Report)

**Proje:** Öneri Algoritmaları Projesi (MovieLens 32M Benchmark)  
**Tarih:** 1 Kasım 2026  
**İncelenen Çalışma Defteri:** `notebooks/02_data_preparation_and_temporal_split.ipynb`  
**Orijinal Veri Seti Konumu:** `C:\ml-32m` (Salt Okunur / Read-Only)  
**Doğrulama Ortamı:** Python 3.14.7 Virtual Environment (`.venv`), Jupyter Kernel `recommendation-systems-project`

---

## 1. Denetim Durum Sınıflandırması ve Gereksinim Kontrol Listesi (Audit Checklist)

TASK 04.1 kapsamında belirlenen tüm gereksinimlerin denetim durumu 4 seviyeli şema ile aşağıda sınıflandırılmıştır:

| Denetim Bileşeni / Alt Görev | Durum | Doğrulama Yöntemi / Gerekçe |
| :--- | :--- | :--- |
| **1.1. Değerlendirilebilir Kullanıcı Kapsamı** | **COMPLETED AND VERIFIED** | 3 zamansal alternatif için kullanıcı kümeleri ($U_{\text{train-only}}, U_{\text{test-only}}, U_{\text{eval}}, U_{\text{neither}}$) bağımsız hesaplandı; toplam $200,948$ sağlaması yapıldı. |
| **1.2. Kullanıcı Yaşam Döngüsü Analizi** | **COMPLETED AND VERIFIED** | $t_{\min}(u)$ ve $t_{\max}(u)$ dağılımları, persentil tablosu (0-100) çıkarıldı; %3.89 oranının veri yapısından kaynaklandığı kanıtlandı. |
| **2.1. k-core Algoritmik Yapı Tespiti** | **COMPLETED AND VERIFIED** | Kod satır satır denetlendi; döngüsel derecelendirme ve filtreleme ile **Gerçek Yinelemeli İki Parçalı (True Iterative Bipartite k-core)** olduğu teyit edildi. |
| **2.2. k-core Yakınsama ve Kayıp İstatistiği** | **COMPLETED AND VERIFIED** | 5, 10 ve 20-core için iterasyon sayıları (2, 3, 4), her adımda elenen kullanıcı/film/etkileşim ve son minimum dereceler doğrulandı. |
| **2.3. k-core'un Değerlendirilebilir Kullanıcıya Etkisi** | **COMPLETED AND VERIFIED** | 3 kesme noktası altında k-core filtrelerinin $U_{\text{eval}}$ havuzunu neredeyse hiç değiştirmediği (fark < %0.2) ispatlandı. |
| **3.1. Aday Havuzu Tanımları ve Sınırları** | **COMPLETED AND VERIFIED** | 3 aday evreni (A: 87,585, B: 84,432, C: 59,952) tanımlandı; 3,153 oylanmamış filmin etkisi ve model ailelerinin kapsama kapasitesi analiz edildi. |
| **3.2. Eğitim-Test Madde Örtüşmesi (Overlap)** | **COMPLETED AND VERIFIED** | $I_{\text{train}} \cap I_{\text{test}} = 45,472$ film; $I_{\text{test}} \setminus I_{\text{train}} = 24,480$ yeni film tespit edildi; saf CF için test etkileşim tavanı (%82.69) çıkarıldı. |
| **3.3. Görülmüş Öğe Dışlama Politikası ($C(u)$)** | **COMPLETED AND VERIFIED** | Veri setinde tekil kullanıcı-film çiftleri denetlendi (`duplicates = 0`), $I_{\text{train}}(u) \cap I_{\text{test}}(u) = \emptyset$ olduğu ve test hedeflerinin dışlanmadığı kanıtlandı. |
| **4.1. Zamansal Ayrım Bağımsız Yeniden Hesaplama** | **COMPLETED AND VERIFIED** | Bağımsız betik ile 32,000,204 satır taranarak 3 alternatif yeniden hesaplandı; `temporal_split_comparison.csv` ile %100 mutabakat sağlandı. |
| **4.2. Eşit Zaman Damgası (Tie Handling) ve Sızıntı** | **COMPLETED AND VERIFIED** | Kesme anındaki zaman damgası çakışmaları incelendi (3 alternatifte de tam kesme saniyesinde 0 etkileşim); `max_train < min_test` katı eşitsizliği doğrulandı. |
| **5.1. Orijinal Veri Bütünlüğü (MD5 Checksums)** | **COMPLETED AND VERIFIED** | `links.csv`, `movies.csv`, `ratings.csv`, `tags.csv` dosyalarının MD5 özetleri hesaplandı ve orijinal değerlerle birebir eşleşti (PASS). |
| **5.2. Çalışma Defteri Yürütme Bütünlüğü** | **COMPLETED AND VERIFIED** | `notebooks/02_data_preparation_and_temporal_split.ipynb` defterindeki tüm hücrelerin (execution count 1-10) hatasız çalıştığı doğrulandı. |
| **6.1. Nihai Metodolojik Kararlar** | **COMPLETED AND VERIFIED** | TASK 04.2 kapsamında Alternatif 1 kesmesi (1577836800), No k-core, 84,432 oylanan film aday evreni ve görülenlerin elenmesi kesinleştirildi ve `config.yaml` içine işlendi. |

---

## 2. Dört Boyutlu Çalışma Ayrımı (Four-Way Work Delineation)

1. **Önceden Tamamlanmış ve Doğrulanmış Çalışmalar (Previously Completed & Verified):**
   - Orijinal veri setinin bütünlüğü (`C:\ml-32m` MD5 sağlama toplamları).
   - TASK 04 çalışma defteri (`notebooks/02_data_preparation_and_temporal_split.ipynb`) mimarisi ve ilk yürütülmesi.
   - `results/temporal_split_comparison.csv` ve `results/kcore_alternatives_comparison.csv` veri tablolarının oluşturulması.
2. **Önceden Tamamlanmış Ancak Yeni Doğrulanan Çalışmalar (Previously Completed but Newly Verified):**
   - Değerlendirilebilir kullanıcı sayısının ($7,817$) matematiksel olarak $U_{\text{train}} \cap U_{\text{test}}$ kesişimine tam eşitliği.
   - Zaman damgası çakışma (timestamp tie) analizi: Her üç kesme saniyesinde de etkileşim sayısının 0 olduğu ve eğitim ile test arasında net saniye tamponlarının (Alt 1: 41 sn, Alt 2: 18 sn, Alt 3: 5 sn) bulunduğu.
   - Veri setinde hiçbir mükerrer $(u, i)$ etkileşimi bulunmadığı ve görülmüş öğe dışlama politikasının test hedeflerini asla yok etmediği.
3. **Yeni Tamamlanan Çalışmalar (Newly Completed Work):**
   - Kullanıcı yaşam döngüsü ($t_{\max} - t_{\min}$) tam persentil dağılım tablosunun (0, 10, 25, 50, 75, 90, 95, 99, 100) çıkarılması.
   - Kullanıcı ilk ($t_{\min}$) ve son ($t_{\max}$) oy tarihlerinin takvimsel dağılım analizi.
   - Yinelemeli iki parçalı k-core algoritmasının tüm iterasyon adımlarının ve yakınsama parametrelerinin kanıtlanması.
   - 3 alternatif kesme altında k-core filtrelerinin değerlendirilebilir kullanıcı havuzuna etkisinin kapsamlı karşılaştırması.
   - Aday havuzu evrenleri (A, B, C) arasındaki teorik ve pratik model uyumluluk sınırlarının tespiti.
4. **TASK 04.2 İle Kesinleştirilen Metodolojik Kararlar (Finalized Decisions):**
   - **Zamansal Kesme:** Alternatif 1 (`2020-01-01 00:00:00 UTC`, $T = 1577836800$).
   - **k-core:** Filtresiz (No filtering / $k=0$), 32,000,204 orijinal etkileşimin tamamı korunmuştur.
   - **Aday Evreni:** Orijinal veri setinde en az 1 oy almış **84,432 film** ($I_{\text{rated}}$).
   - **Görülmüş Öğe Dışlama:** Kullanıcı bazında eğitimde puanlanan filmlerin aday listesinden çıkarılması ($C(u) = I_{\text{rated}} \setminus I_{\text{train}}(u)$).
   - **Değerlendirilebilir Kullanıcılar:** En az 1 eğitim ve en az 1 test etkileşimi bulunan **7,817 kullanıcı** ($U_{\text{eval}}$).
   - **Ortak Değerlendirme:** Tüm modeller (Adjusted Popularity Baseline, Content-Based TF-IDF, Latent Factor Model SVD) aynı $7,817$ kullanıcı ve ortak aday evreni üzerinde değerlendirilecektir.
   - **Şeffaf Madde Kapsamı Raporlaması:** Test etkileşimlerinin %17.31'inin ($152,122$ etkileşim / $24,480$ yeni film) eğitim kümesinde yer almadığı soğuk başlangıç kısıtı açıkça raporlanacaktır.
   - **Veri Bütünlüğü:** Orijinal veriye kalıcı filtreleme yapılmayacaktır. Kararlar `config.yaml` dosyasına işlenmiştir.

---

## 3. Bölüm 1: Değerlendirilebilir Kullanıcı (Evaluable Users) Derinlemesine İncelemesi

### 3.1. ~%3.9 Oranının Matematiksel ve Davranışsal Açıklaması
Global kronolojik kesme uygulandığında yalnızca ~%3.89 - %3.97 oranında kullanıcının değerlendirilebilir çıkması, MovieLens platformunun doğasından kaynaklanmaktadır:

- **28.75 Yıllık Veri Toplama Penceresi:** 1995 ile 2023 yılları arasında toplanan 32 milyon etkileşimde kullanıcılar homojen bir şekilde var olmamaktadır.
- **Kısa Kullanıcı Yaşam Süresi (Short User Lifespan):** Kullanıcıların büyük kısmı platforma belirli bir dönemde (örneğin 2000 veya 2016 yıllarındaki zirvelerde) katılmış, değerlendirmelerini kısa bir zaman aralığında yapmış ve platformu terk etmiştir (churn).

### 3.2. Kullanıcı Yaşam Süresi Dağılımı (User Lifespan Percentiles)
Her kullanıcının ilk etkileşimi ($t_{\min}(u)$) ile son etkileşimi ($t_{\max}(u)$) arasındaki fark hesaplanmıştır:

$$\Delta t(u) = t_{\max}(u) - t_{\min}(u)$$

| Persentil (Quantile) | Yaşam Süresi (Saniye) | Yaşam Süresi (Gün) | Eşdeğer Takvimsel Süre | Açıklama ve Davranışsal Anlamı |
| :--- | :--- | :--- | :--- | :--- |
| **%0 (Min)** | 0 s | 0.000 gün | Anlık | Tek bir saniyede oy vermiş kullanıcılar |
| **%10** | 418 s | 0.005 gün | ~7.0 dakika | Tek bir oturumda hızlıca oy veren kullanıcılar |
| **%25** | 970 s | 0.011 gün | ~16.2 dakika | Kısa tek oturumlu kullanıcılar |
| **%50 (Medyan)** | **5,641 s** | **0.065 gün** | **~1.57 saat** | **Kullanıcıların yarısı 1.5 saat içinde platformdaki tüm oylarını tamamlamıştır!** |
| **%75** | 4,585,719 s | 53.075 gün | ~1.74 ay | Birkaç hafta/ay boyunca aktif kalan kullanıcılar |
| **%90** | 61,256,021 s | 708.982 gün | ~1.94 yıl | Uzun dönemli sadık kullanıcılar |
| **%95** | 138,053,535 s | 1,597.842 gün | ~4.38 yıl | Çok yıllık platform kullanıcıları |
| **%99** | 383,160,008 s | 4,434.722 gün | ~12.15 yıl | On yılı aşkın süredir oylama yapan kıdemli kullanıcılar |
| **%100 (Maks)** | 822,108,133 s | 9,515.140 gün | ~26.07 yıl | 1996'dan 2023'e kadar aktif olan uç kullanıcılar |

**Kümülatif Yaşam Süresi Oranları:**
- **< 1 gün aktif olanlar:** $118,129$ kullanıcı (**%58.79**)
- **< 30 gün aktif olanlar:** $145,706$ kullanıcı (**%72.51**)
- **< 365 gün (1 yıl) aktif olanlar:** $172,373$ kullanıcı (**%85.78**)
- **$\ge$ 1 yıl aktif olanlar:** $28,575$ kullanıcı (**%14.22**)

### 3.3. Kullanıcıların İlk ve Son Etkileşim Zaman Damgası Dağılımları

| Persentil | İlk Etkileşim Zamanı ($t_{\min}$) UTC | Son Etkileşim Zamanı ($t_{\max}$) UTC |
| :--- | :--- | :--- |
| **Min (%0)** | 1995-01-09 11:46:44 (789652004) | 1996-02-23 12:56:00 (825080160) |
| **%10** | 1996-10-23 12:26:42 (846073602) | 1996-11-15 14:03:41 (848066621) |
| **%25** | 2000-05-28 20:23:36 (959545416) | 2000-10-02 04:11:49 (970459909) |
| **%50 (Medyan)** | 2008-04-16 09:50:56 (1208339456) | 2009-02-21 01:57:09 (1235181429) |
| **%75** | 2016-05-21 14:12:40 (1463839960) | 2017-03-16 19:30:54 (1489692654) |
| **%90** | 2020-03-20 07:05:08 (1584687908) | 2021-02-01 20:21:56 (1612210916) |
| **%95** | 2021-06-02 18:40:33 (1622659233) | 2022-10-16 02:37:08 (1665887828) |
| **%99** | 2023-04-25 17:10:59 (1682442659) | 2023-09-23 15:19:01 (1695482341) |
| **Maks (%100)** | 2023-10-13 00:57:40 (1697158660) | 2023-10-13 02:29:07 (1697164147) |

Kullanıcıların %75'i platformdaki son oylarını Mart 2017'den önce vermiştir! Dolayısıyla 2020-01-01 gibi modern bir tarihte kesme yapıldığında kullanıcıların %85'inin tüm geçmişinin kesme öncesinde kalması kaçınılmazdır.

### 3.4. Üç Zamansal Ayrım Alternatifi İçin Kullanıcı Bölünmesi

| Metrik / Kullanıcı Kümesi | Alternatif 1: 2020-01-01 UTC (~85.5 / 14.5) | Alternatif 2: 2021-01-01 UTC (~90.8 / 9.2) | Alternatif 3: %80 Kümülatif (2018-10-03 UTC) |
| :--- | :--- | :--- | :--- |
| **Toplam Tekil Kullanıcı** | 200,948 (%100.0) | 200,948 (%100.0) | 200,948 (%100.0) |
| **Yalnızca Eğitimde Olan ($U_{\text{train-only}}$)** | 171,602 (%85.40) | 179,978 (%89.56) | 162,676 (%80.95) |
| **Yalnızca Testte Olan ($U_{\text{test-only}}$)** | 21,529 (%10.71) | 12,998 (%6.47) | 30,457 (%15.16) |
| **Her İki Dönemde Olan ($U_{\text{eval}}$)** | **7,817 (%3.89)** | **7,972 (%3.97)** | **7,815 (%3.89)** |
| **Hiçbir Dönemde Olmayan (Neither)** | **0 (%0.00)** | **0 (%0.00)** | **0 (%0.00)** |
| **Tüm Geçmişi Kesme Öncesinde Kalanlar** | 171,602 (%85.40) | 179,978 (%89.56) | 162,676 (%80.95) |
| **Tüm Geçmişi Kesme Sonrasında Kalanlar** | 21,529 (%10.71) | 12,998 (%6.47) | 30,457 (%15.16) |
| **Toplam Doğrulama Sağlaması** | $171,602 + 21,529 + 7,817 = 200,948$ | $179,978 + 12,998 + 7,972 = 200,948$ | $162,676 + 30,457 + 7,815 = 200,948$ |

*Kesişim Teyidi:* $U_{\text{eval}} = U_{\text{train}} \cap U_{\text{test}}$ formülü her üç alternatifte de tam sayısal eşitlikle doğrulanmıştır.

---

## 4. Bölüm 2: k-core Algoritması Denetimi (k-core Algorithm Audit)

### 4.1. Algoritmik Sınıflandırma
`notebooks/02_data_preparation_and_temporal_split.ipynb` dosyasındaki `compute_kcore` fonksiyonu denetlenmiştir:
- Algoritma, her iterasyonda kullanıcı etkileşim sayılarını (`u_counts`) ve film etkileşim sayılarını (`m_counts`) yeniden hesaplamaktadır.
- Derecesi $k$ eşiğinin altında kalan düğümler iki taraftan da eşzamanlı filtrelenmekte ve veri kümesi boyutu bir önceki adımla aynı olana kadar (`len(filtered) == len(curr_df)`) döngü yinelenmektedir.
- **Kesin Teyit:** Uygulanan yöntem **Gerçek Yinelemeli İki Parçalı k-core (True Iterative Bipartite k-core)** algoritmasıdır.

### 4.2. İterasyon Adımları, Yakınsama ve Derece Denetimi

| Metrik / Eşik | 5-core ($k=5$) | 10-core ($k=10$) | 20-core ($k=20$) |
| :--- | :--- | :--- | :--- |
| **İterasyon Sayısı (Yakınsama)** | **2 İterasyon** | **3 İterasyon** | **4 İterasyon** |
| **1. İterasyon Kullanıcı Elenen** | 0 kullanıcı | 0 kullanıcı | 0 kullanıcı |
| **1. İterasyon Film Elenen** | 40,548 film | 52,471 film | 61,082 film |
| **1. İterasyon Etkileşim Elenen** | 78,737 etkileşim | 157,499 etkileşim | 274,284 etkileşim |
| **2. İterasyon Kullanıcı Elenen** | 0 kullanıcı (Yakınsadı) | 1 kullanıcı | 185 kullanıcı |
| **2. İterasyon Film Elenen** | 0 film | 0 film | 0 film |
| **2. İterasyon Etkileşim Elenen** | 0 (Döngü Bitti) | 9 etkileşim | 3,311 etkileşim |
| **3. İterasyon Kullanıcı Elenen** | - | 0 kullanıcı (Yakınsadı) | 0 kullanıcı |
| **3. İterasyon Film Elenen** | - | 0 film | 11 film |
| **3. İterasyon Etkileşim Elenen** | - | 0 (Döngü Bitti) | 209 etkileşim |
| **4. İterasyon Kullanıcı / Film / Satır**| - | - | 0 / 0 / 0 (Döngü Bitti) |
| **Kalan Tekil Kullanıcı** | 200,948 (%100.0) | 200,947 (%99.999) | 200,763 (%99.908) |
| **Kalan Tekil Film** | 43,884 (%51.98) | 31,961 (%37.85) | 23,339 (%27.64) |
| **Kalan Etkileşim Sayısı** | 31,921,467 (%99.75) | 31,842,696 (%99.51) | 31,722,400 (%99.13) |
| **Kayıp Etkileşim Sayısı** | 78,737 (%0.25) | 157,508 (%0.49) | 277,804 (%0.87) |
| **Minimum Kullanıcı Derecesi** | 15 ($\ge 5$, Sağlandı) | 15 ($\ge 10$, Sağlandı) | 20 ($\ge 20$, Sağlandı) |
| **Minimum Film Derecesi** | 5 ($\ge 5$, Sağlandı) | 10 ($\ge 10$, Sağlandı) | 20 ($\ge 20$, Sağlandı) |

### 4.3. Film Kataloğundaki Kayıp Oranları (Katalog Eliminasyonu)
- **Puan Alan Filmler (84,432 Film Üzerinden):**
  - 5-core: %48.02 elendi (40,548 film silindi).
  - 10-core: %62.15 elendi (52,471 film silindi).
  - 20-core: %72.36 elendi (61,093 film silindi).
- **Tüm Film Kataloğu (87,585 Film Üzerinden):**
  - 5-core: %46.29 elendi (+ 3,153 oylanmamış = %49.90 katalog dışı).
  - 10-core: %59.91 elendi (+ 3,153 oylanmamış = %63.51 katalog dışı).
  - 20-core: %69.75 elendi (+ 3,153 oylanmamış = %73.35 katalog dışı).

### 4.4. Farklı Kesme Noktalarında k-core'un Değerlendirilebilir Kullanıcıya Etkisi

| k-core Filtresi | Alternatif 1 (2020-01-01) | Alternatif 2 (2021-01-01) | Alternatif 3 (2018-10-03) |
| :--- | :--- | :--- | :--- |
| **Filtresiz (No k-core)** | 7,817 | 7,972 | 7,815 |
| **5-core** | 7,812 (-5 kullanıcı) | 7,970 (-2 kullanıcı) | 7,813 (-2 kullanıcı) |
| **10-core** | 7,811 (-6 kullanıcı) | 7,968 (-4 kullanıcı) | 7,811 (-4 kullanıcı) |
| **20-core** | 7,805 (-12 kullanıcı) | 7,959 (-13 kullanıcı) | 7,804 (-11 kullanıcı) |

**Neden k-core Değerlendirilebilir Kullanıcı Sayısını Değiştirmez?**  
Zamansal bir kesmenin hem öncesinde hem sonrasında aktif olan kullanıcılar ($U_{\text{eval}}$) doğası gereği platformda yıllarca aktif kalmış kıdemli ve yüksek aktiviteye sahip güç kullanıcılarıdır (power users). Bu kullanıcıların etkileşim derecesi zaten 20'nin çok üzerindedir. k-core filtresi yalnızca tekil oturumlarda birkaç niş filme oy veren pasif kullanıcıları eler. Dolayısıyla k-core filtresi değerlendirilebilir kullanıcı havuzunu genişletmediği gibi, kataloğun %72'sini yok ederek aşırı hayatta kalma yanlılığı (survivorship bias) üretir. Bu nedenle **orijinal verinin filtrelenmeden korunması kararı %100 isabetlidir.**

---

## 5. Bölüm 3: Aday Havuzu (Candidate Pool) ve Madde Popülasyonu Örtüşme Denetimi

### 5.1. Aday Evreni Alternatifleri ve Model Aileleri Uyumluluğu

| Aday Evreni Alternatifi | Boyut | Tanım ve Kapsam | Öneri Modellerinin Puanlama Yeteneği |
| :--- | :--- | :--- | :--- |
| **A. Tüm Film Kataloğu (Full Catalog)** | **87,585** | `movies.csv` içindeki tüm başlıklar | 3,153 film hiçbir etkileşim almamıştır. Saf işbirlikçi filtreleme (Item-KNN, MF) bu filmlere latent vektör veya benzerlik atayamaz. Sadece içerik tabanlı veya rastgele modeller önerebilir. |
| **B. Oylanan Film Popülasyonu (Rated Movies)** | **84,432** | `ratings.csv` içindeki tüm başlıklar | Tüm veri setinde en az 1 kez oylanmış filmlerdir. Ancak test periyodunda ilk kez sisteme giren 24,480 yeni film ($I_{\text{test}} \setminus I_{\text{train}}$) için eğitim geçmişi yoktur. |
| **C. Modele Açık Eğitim Filmleri ($I_{\text{train}}$)** | **59,952** | Yalnızca eğitim kümesinde bulunan filmler | Tüm model ailelerinin (Popülerlik, Öğe Tabanlı CF, Matris Ayrıştırma) gömmelerini tam olarak öğrenebildiği kapalı dünya (closed-world) kümesidir. |

### 5.2. Oylanmamış Filmlerin (3,153 Film) Değerlendirmeye Etkisi
`movies.csv` dosyasında olup `ratings.csv` dosyasında hiç bulunmayan 3,153 film:
- Test kümesinde asla yer alamaz ($Y_{\text{test}} \cap I_{\text{unrated}} = \emptyset$).
- Eğer bir model bu filmleri öneri listesine (Top-K) alırsa, yer gerçeği (ground truth) karşılığı olmadığı için kesinlikle bir Yanlış Pozitif (False Positive) sayılacak ve Precision@K / Recall@K metriklerini düşürecektir.
- Saf işbirlikçi filtreleme modelleri hiçbir zaman bu filmleri öğrenemeyeceğinden, aday havuzunda bulunmaları CF modellerine haksız ceza vermez ancak değerlendirme matrisini gereksiz yere %3.6 oranında büyütür.

### 5.3. Eğitim ve Test Kümeleri Arasındaki Madde Örtüşmesi (Item Overlap)
Alternatif 1 (2020-01-01) kesmesi altında test kümesinde $70,027$ tekil film yer almaktadır:
- **Eğitim ve Test Kesişimi ($I_{\text{train}} \cap I_{\text{test}}$):** **45,472 film**.
- **Yalnızca Testte Olan Yeni Filmler ($I_{\text{test}} \setminus I_{\text{train}}$):** **24,480 film (%34.96)**. (Madde soğuk başlangıcı / Item cold-start).
- **Yalnızca Eğitimde Olan Eski Filmler ($I_{\text{train}} \setminus I_{\text{test}}$):** **14,480 film (%24.15)**. (Test döneminde hiç oylanmamış filmler).

### 5.4. Test Hedeflerinin Kapsamı ve Soğuk Başlangıç Tavanı (Recall Ceiling)
Değerlendirilebilir $7,817$ kullanıcının test dönemindeki $879,024$ etkileşimi analiz edildiğinde:
- **$726,902$ etkileşim (%82.69):** Eğitim kümesinde mevcut olan filmlere ($I_{\text{train}}$) aittir.
- **$152,122$ etkileşim (%17.31):** İlk kez 2020 sonrasında vizyona girmiş veya oy almış yeni filmlere ($I_{\text{test}} \setminus I_{\text{train}}$) aittir.
- **Kritik Metodolojik Sonuç:** Eğer aday havuzu olarak B (84,432 film) seçilirse, saf matris ayrıştırma ve komşuluk tabanlı modeller yeni filmleri öğrenemeyeceği için bu modellerin erişebileceği **teorik maksimum Recall tavanı %82.69** olacaktır. Aday havuzu olarak C seçilirse ($I_{\text{train}}$), hedef küme yalnızca eğitimde bilinen öğelerle sınırlandırılarak modeller kapalı dünyada %100 teorik tavan üzerinden adilce yarışabilir.

### 5.5. Görülmüş Öğe Dışlama Politikası ($C(u) = I \setminus I_{\text{train}}(u)$) Denetimi
- Veri setinde hiçbir mükerrer $(u, i)$ çifti bulunmamaktadır (`dup_count = 0`).
- Dolayısıyla her kullanıcı için eğitimdeki filmler kümesi ile testteki filmler kümesi kesin olarak ayrıktır:
  $$I_{\text{train}}(u) \cap I_{\text{test}}(u) = \emptyset$$
- **Kesin Sonuç:** Bir kullanıcı için eğitimde gördüğü filmleri aday havuzundan çıkarmak, **kullanıcının testteki hiçbir yer gerçeği (ground truth) filmini aday havuzundan silmez**. Bu politika adil, gerçekçi ve sızıntısızdır.

### 5.6. Üç Model Ailesinin Aynı Aday Evrenini Kullanabilirliği
- **Popülerlik Tabanlı Temel Model (Popularity Baseline):** Eğitimdeki en popüler filmleri sıralar; $C(u)$ aday havuzunu tam olarak destekler.
- **Komşuluk Tabanlı İşbirlikçi Filtreleme (Item-KNN / User-KNN):** Eğitim etkileşimleri üzerinden kosinüs benzerliği kurar; $C(u)$ aday havuzunu tam olarak destekler.
- **Örtük Faktör / Matris Ayrıştırma (SVD / BiasedMF / ALS):** Kullanıcı ve madde latent vektörlerini ($p_u, q_i$) eğitimde öğrenir; $C(u)$ aday havuzunu tam olarak destekler.
- **Öneri:** Her 3 model ailesi de kapalı dünya değerlendirmesi için kullanıcı bazlı görülenlerin çıkarıldığı eğitim filmleri evrenini ($C(u) = I_{\text{train}} \setminus I_{\text{train}}(u)$) ortak ve standart olarak kullanabilir.

---

## 6. Bölüm 4: Zamansal Ayrım Bağımsız Yeniden Hesaplama ve Eşitlik (Tie) Denetimi

Tüm hesaplamalar bağımsız bir Python betiği ile orijinal `ratings.csv` üzerinden teyit edilmiştir:

1. **Zaman Damgası Eşitliği ve Sınır Analizi (Timestamp Tie Handling):**
   - **Alternatif 1 ($T = 1577836800$):**
     - $t = 1577836800$ saniyesinde gerçekleşen etkileşim sayısı: **0**.
     - Son eğitim etkileşimi: $1577836786$ (2019-12-31 23:59:46 UTC).
     - İlk test etkileşimi: $1577836827$ (2020-01-01 00:00:27 UTC).
     - **Güvenlik Aralığı:** Eğitim ve test arasında **41 saniyelik net boşluk** vardır. Hiçbir etkileşim sınırda sıkışmamıştır.
   - **Alternatif 2 ($T = 1609459200$):**
     - $t = 1609459200$ saniyesinde etkileşim sayısı: **0**.
     - Son eğitim: $1609459190$ (23:59:50 UTC) | İlk test: $1609459208$ (00:00:08 UTC).
     - **Güvenlik Aralığı:** **18 saniyelik net boşluk**.
   - **Alternatif 3 ($T = 1538551302$):**
     - $t = 1538551302$ saniyesinde etkileşim sayısı: **0**.
     - Son eğitim: $1538551300$ (07:21:40 UTC) | İlk test: $1538551305$ (07:21:45 UTC).
     - **Güvenlik Aralığı:** **5 saniyelik net boşluk**.
2. **Katı Kronolojik Eşitsizlik (Zero Temporal Leakage):**
   - Her üç alternatif için de:
     $$\max(T_{\text{train}}) < \min(T_{\text{test}})$$
     koşulu `%100` sağlanmış, eğitim kümesinin geleceğe dair hiçbir bilgi içermediği matematiksel olarak ispatlanmıştır.
3. **Veri Kümesi Boyut Eşitliği:**
   - Her üç alternatifte de $N_{\text{train}} + N_{\text{test}} = 32,000,204$ satır eşitliği tam olarak sağlanmıştır.

---

## 7. Bölüm 5: Orijinal Veri Bütünlüğü ve Çalışma Defteri Doğrulaması

### 7.1. Orijinal Veri Seti MD5 Sağlama Toplamları (`C:\ml-32m`)

| Dosya Adı | Beklenen Resmi MD5 | Hesaplanan Yerel MD5 | Doğrulama Sonucu |
| :--- | :--- | :--- | :--- |
| `links.csv` | `8f033867bcb4e6be8792b21468b4fa6e` | `8f033867bcb4e6be8792b21468b4fa6e` | **GEÇTİ (PASS)** |
| `movies.csv` | `0df90835c19151f9d819d0822e190797` | `0df90835c19151f9d819d0822e190797` | **GEÇTİ (PASS)** |
| `ratings.csv` | `cf12b74f9ad4b94a011f079e26d4270a` | `cf12b74f9ad4b94a011f079e26d4270a` | **GEÇTİ (PASS)** |
| `tags.csv` | `963bf4fa4de6b8901868fddd3eb54567` | `963bf4fa4de6b8901868fddd3eb54567` | **GEÇTİ (PASS)** |

Orijinal veri setindeki tek bir bayt dahi değiştirilmemiştir.

### 7.2. Çalışma Defteri Yürütme Denetimi (`notebooks/02_data_preparation_and_temporal_split.ipynb`)
- Çalışma defteri baştan sona temiz bir çekirdek ile yürütülmüştür.
- Toplam **21 hücrenin** (10 kod hücresi, 11 markdown hücresi) tamamı başarıyla tamamlanmıştır.
- Tüm kod hücreleri sıralı olarak `execution_count` 1'den 10'a kadar yürütülmüş, **0 hata** üretmiştir.
- Üretilen grafikler (`results/figures/*.png`) 300 DPI çözünürlükte diske kaydedilmiştir.

---

## 8. Bölüm 6: Kesinleştirilen Metodolojik Kararlar ve Değerlendirme Yapılandırması (TASK 04.2)

TASK 04.1 denetim bulguları doğrultusunda TASK 04.2 kapsamında aşağıdaki metodolojik kararlar kesinleştirilmiş ve projenin merkezi yapılandırma dosyası olan `config.yaml` içine işlenmiştir:

1. **Zamansal Kesme Noktası (Temporal Cutoff):**
   - **Karar:** **Alternatif 1 (`2020-01-01 00:00:00 UTC`, Timestamp: $1577836800$)**.
   - **Gerekçe:** $7,817$ değerlendirilebilir kullanıcı ve $879,024$ test etkileşimi ile yüksek istatistiksel geçerlilik sağlar; eğitim ve test arasında 41 saniyelik net tamponla sıfır zamansal sızıntı garantilenmiştir.
2. **k-core Filtreleme Stratejisi:**
   - **Karar:** **Filtresiz (No k-core / Orijinal Veri Bütünlüğü, $k=0$)**.
   - **Gerekçe:** MovieLens 32M veri setinin 32,000,204 etkileşiminin tamamı ve doğal seyrekliği korunmuştur; aşırı hayatta kalma yanlılığı (survivorship bias) engellenmiştir.
3. **Zorunlu Model Aileleri:**
   - **Adjusted Popularity Baseline** (Düzeltilmiş popülerlik temel modeli).
   - **Content-Based TF-IDF + Cosine Similarity** (İçerik tabanlı TF-IDF ve kosinüs benzerliği).
   - **Latent Factor Model (SVD)** (Örtük faktör modeli / Matris ayrıştırma).
4. **Aday Evreni (Candidate Universe):**
   - **Karar:** MovieLens 32M veri setinde en az 1 oy almış **84,432 film** ($I_{\text{rated}}$).
5. **Kullanıcı Bazlı Görülmüş Öğe Dışlama (Per-User Seen-Item Exclusion):**
   - **Karar:** Kullanıcının eğitim kümesinde puanladığı filmler aday havuzundan çıkarılır:
     $$C(u) = I_{\text{rated}} \setminus I_{\text{train}}(u)$$
   - Veri setinde mükerrer kayıt bulunmadığı için testteki hiçbir yer gerçeği hedefi bu dışlama ile elenmez.
6. **Değerlendirilebilir Kullanıcılar (Evaluable Users):**
   - **Karar:** En az 1 eğitim ve en az 1 test etkileşimi bulunan **7,817 kullanıcı** ($U_{\text{eval}} = U_{\text{train}} \cap U_{\text{test}}$).
7. **Ortak Değerlendirme Protokolü (Common Benchmark Protocol):**
   - Tüm modeller aynı $7,817$ değerlendirilebilir kullanıcı ve kullanıcı bazında filtrelenmiş ortak aday evreni üzerinde değerlendirilecektir.
8. **Şeffaf Madde Kapsamı ve Soğuk Madde Kısıtı Raporlaması:**
   - Test etkileşimlerinin %17.31'inin ($152,122$ etkileşim / $24,480$ yeni film) eğitim kümesinde yer almadığı soğuk başlangıç kısıtı tüm model değerlendirme raporlarında açıkça belirtilecek ve gizlenmeyecektir.
9. **Veri Bütünlüğü Güvencesi:**
   - Orijinal veri dosyaları (`C:\ml-32m`) üzerinde hiçbir kalıcı değişiklik yapılmayacaktır.
