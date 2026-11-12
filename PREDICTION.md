# Prediksi sebelum refactor EquipmentUnavailable

> ? DRAF ? tulis ulang dengan kata sendiri

Tanggal 2026-11-12, basis 5f8fc29. File ini tidak boleh diubah sesudah implementasi.
Saya memilih Result<Loan> untuk equipment yang sedang dipinjam. Ini outcome normal
untuk katalog bersama; runner bisa mencatat penolakan dan melanjutkan baris berikutnya.
Seed memanggil borrow tiga kali per bahasa, runner sekali per bahasa; test juga memanggilnya.
UnknownAssetTag, mismatch case, reservasi dan kuota tetap exception bertipe ke app.

Penghitungan nyata scripts/count_callsites.sh sebelum perubahan menghasilkan 48 ekspresi
panggilan dalam produksi dan test, tersimpan docs/evidence/pre_result_callsites.txt.
Ada delapan call site produksi (enam seed, dua runner). Prediksi saya delapan itu perlu
penanganan Result secara eksplisit. Saya memprediksi 20 dari 48 ekspresi perlu perubahan
teks; sisanya test untuk exception lain yang masih melempar. Ini perkiraan, bukan hasil.
Runner menjadi lebih sederhana untuk outcome unavailable: cabang if, tanpa catch khusus.
Kontrak campuran return/throw tetap perlu dijelaskan; Result tidak menghapus semua exception.
