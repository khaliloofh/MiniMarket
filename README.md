===== Mini Market Sistemi ===== ( username: enver password: 1106 )

Bu layihe - DB olmadan Python dilinde, butun melumatlari fayl formatinda saxlayan bir magaza sistemidir. Sitem normal marketde olan sebete elave etme, favoritlere elave etme, kateqoryaya uygun mehsullarn siralanmasi ve tarixceni gormek kimi ozelliklere sahibdir.

===== Muellimin teleb etdiyi *Test Ssenarileri* =====

Test ssenariləri (minimum) ( Checklist ✅ )
1. Login limiti: 3 səhv → 10s cooldown → sonra doğru şifrə ilə giriş. ✅
2. Səbət axını: Geyimlərdən T-Shirt ×2 Səbətə əlavə et → balans dəyişməməlidir. ✅
3. Checkout uğurlu: Səbətdəki cəmi hesabla → balans kifayət edirsə Checkout et → balansdan çıx → purchases-a yaz. ✅
4. Checkout uğursuz: Səbətə balansdan çox məbləğlik elementlər yığ → checkout → rədd (səbət dəyişməz qalır). ✅
5. Favorit → Səbət: Favoritə əlavə et → Favoritdən Səbətə at → Checkout et. ✅
6. Şifrə dəyişmə: Köhnə şifrəni təsdiq et → yenisini təyin et → çıxış → yeni şifrə ilə giriş. ✅
7. Tarixçə: Yuxarıdakı bütün hadisələr logda ardıcıllıqla görünsün. ✅
8. Persistensiya: Proqram bağlanıb-açıldıqdan sonra səbət, favoritlər, purchases, balans qorunsun. ✅

- Butun testlerden kecmisdir

===== *Layihede istifade olunan esas anlayislar* =====

JSON (JavaScript Object Notation): Məlumatları "açar-dəyər" (key-value) cütlüyü şəklində saxlayan yüngül məlumat formatıdır. Bizim proqramda Python lüğətlərini (dictionary) faylda saxlamaq üçün istifadə olunur.

File I/O (Input/Output): Fayla məlumat yazılması və fayldan məlumat oxunması prosesidir.

Data Persistence (Məlumatın Davamlılığı): Proqram bağlansa belə, məlumatların itməməsi xüsusiyyətidir. Məlumatlar diskdəki fayllarda saxlandığı üçün növbəti dəfə proqram açıldıqda hər şey yerində qalır.

Cooldown (Gözləmə Müddəti): Təhlükəsizlik funksiyasıdır. Ardıcıl olaraq 3 dəfə səhv şifrə daxil edildikdə, sistemin müvəqqəti olaraq (10 saniyə) girişi bloklamasıdır.

Timestamp (Zaman Damğası): Hər hansı bir hadisənin (məs: login və ya alış-veriş) tam olaraq hansı saniyədə baş verdiyini göstərən vaxt qeydi.

UTF-8: Fayllarda Azərbaycan hərflərinin (ə, ö, ü, ç, ş, ğ) düzgün oxunması və yazılması üçün istifadə olunan kodlaşdırma standartı.

===== *Layihə bütün məlumatları data/ qovluğunda saxlayır:* =====

users.json: İstifadəçi adları, şifrələr, balans və bloklanma məlumatlarını saxlayır.

products.json: Mağazadakı kateqoriyaları və hər kateqoriyaya aid məhsul siyahısını (ad, qiymət, ID) saxlayır.

basket_<user>.json: Hər bir istifadəçinin özünə aid, hələ pulları ödənilməmiş (gözləyən) məhsullar siyahısı.

favorites_<user>.json: İstifadəçinin sonradan almaq üçün bəyəndiyi məhsullar.

history_<user>.log: İstifadəçinin bütün hərəkətlərini (uğurlu/uğursuz login, alışlar) sətir-sətir saxlayan jurnal faylı.

purchases_<user>.json: Tamamlanmış (pulu ödənilmiş) alış-verişlərin arxivi.

===== *Kod daxilindəki əsas funksiyaların vəzifələri:* =====

Məlumat İdarəetmə Funksiyaları
load_json(path, default): Göstərilən yoldakı faylı açır və Python formatına çevirir. Əgər fayl yoxdursa, proqramın dayanmaması üçün boş bir siyahı və ya lüğət qaytarır.

save_json(path, data): Proqramda yenilənmiş məlumatları JSON formatında fayla yazır. indent=2 parametri sayəsində fayl Notepad ilə açıldıqda insan tərəfindən rahat oxunur.

init_data(): Proqram ilk dəfə işə düşəndə lazım olan qovluğu və standart istifadəçi/məhsul fayllarını yaradır.

İstifadəçi Əməliyyatları
login(): Giriş prosesini idarə edir. İstifadəçini tapır, bloklanıb-bloklanmadığını yoxlayır və şifrəni təsdiqləyir.

change_password(user): İstifadəçinin köhnə şifrəsini təsdiqləyərək yeni şifrə təyin etməsini təmin edir (Minimum 4 simvol tələbi ilə).

log_event(username, message): Hər bir mühüm addımı zaman damğası ilə log faylına əlavə edir.

Market və Alış-veriş Məntiqi
browse_products(user): Məhsul kataloqunu göstərir. İstifadəçiyə miqdar daxil etməklə məhsulu səbətə (B) və ya favoritə (F) atmaq imkanı verir.

manage_basket(user): Səbəti idarə edir. Burada list, qty (say dəyişmə), remove (silmə) və checkout (ödəniş) əmrləri icra olunur.

manage_favorites(user): Favoritləri siyahılayır və oradakı məhsulu birbaşa səbətə köçürür.

show_history(username): İstifadəçinin log faylından son 20 hərəkətini oxuyub ekranda göstərir.



QEYD: Kodu yazarken Suni intellekten "copy-paste" etmeden komek almisam, lazm olan terminleri funksiyalari arasdirib oyrenmisem.

  
