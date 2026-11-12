# Progres Modul 3

Tanggal: 2026-11-12. Spesifikasi tunggal: prompt pengguna, bukan PDF/TXT.
Pembaruan eksekusi: setup WSL cc85467. Python tetap 3.14.4.
- [x] ASan native: docs/evidence/05_asan_instructor_errors.txt.
- [x] Rekonstruksi: branch baseline/reconstructed, baseline 6ca6c7b.
- [x] Defect A: test merah 0c004e1, hijau 0f0ccad; Defect B 67780d9.
- [x] Bukti asli disimpan docs/evidence/reconstructed/ (bukan starter asli).
- [x] Dua node, validator/paritas, return bersuara dan atomic writer diterapkan.
- [x] Dependency gate negatif 12 arah dan graf nyata; gate/full test hijau.
- [x] Hasil terakhir: 32 C++ dan 98 Python, docs/evidence/parity-review.log.
- [ ] Refactor Result belum dimulai; PREDICTION harus commit terlebih dahulu.

Checklist historis di bawah merekam keadaan awal, bukan status terbaru.


## D0
- [x] Periksa status dan log; branch lab/modul3, tag m3-as-received = aa83fec.
- [x] T1 telah diperbaiki pada ab23da4 sebelum sesi ini; tidak direkayasa ulang.
- [x] Venv WSL dibuat dengan python3 -m venv .venv; requirements terpasang.
- [x] Baseline WSL hijau: docs/evidence/03_wsl_baseline.txt.
- [ ] Python 3.12: belum tersedia; yang diuji 3.14.4. Jangan klaim paritas versi.
- [ ] Probe native ASan dan baseline merah T1 dari tag pada salinan terisolasi.
- [ ] Branch baseline/reconstructed dan god file berlabel direkonstruksi.
- [ ] Commit penutupan D0; hash dicatat pada pembaruan berikutnya agar tidak sirkular.

## D1-D2
- [ ] Lab 1.1 peta handler terstruktur dan rekonstruksi.
- [ ] Lab 1.2 mode kegagalan; Lab 1.3 golden tambahan setelah pesan final.
- [ ] Lab 1.4 riset Ariane dan refleksi DRAF.
- [ ] Lab 2.1 dua node dengan handler pemakai data.
- [ ] Lab 2.3 atomic writer, T3/T4/T7 dan pengujian.
- [ ] Defect A test-merah dahulu; Defect B ASan sebelum/sesudah.

## D3-D4-E-F
- [ ] Commit PREDICTION sebelum implementasi Result (Lab 2.2/3.1).
- [ ] Dependency gate negatif, graf, matriks strategi dan cleanup.
- [ ] README, clone bersih dan checklist rekan.
