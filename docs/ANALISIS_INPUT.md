# Analisis Input PinjamLab

Ekspor faktual Indonesia berdasarkan pembacaan dan eksekusi sesi sekarang. Dossier untracked sebelumnya dibaca sebelum diganti. Tidak commit/push/checkout/modifikasi sumber. Artefak baru hanya dossier dan ignored bin/analisis-export; tidak menulis di luar repo,generator stdin tidak disimpan. Tidak mengisi refleksi pribadi/lab hilang.

Sanitasi path home pengguna menjadi ~,email [EMAIL DIHAPUS],hostname [HOST DIHAPUS];hash/tanggal/PID/alamat memori/exit dipertahankan. Output fenced aktual kecuali sanitasi. cat/nl ekspor sumber dibaca ulang saat ini,nl nomor fisik. Arsip bukan run ulang. Cwd akar repo WSL. Timing command-*.txt perf_counter sekitar subprocess.run,bukan benchmark. CLI_EXIT berbeda shell exit validasi. Test env TMPDIR=$PWD/bin/analisis-export,PYTHONDONTWRITEBYTECODE=1,PYTEST_ADDOPTS="--basetemp=$PWD/bin/analisis-export/pytest-tmp -p no:cacheprovider". Output panjang40awal/40akhir+total/path;sumber wajib/diff relevan/ASan penuh.

## §0 Metadata & peta repo

Status awal sesi ini: dossier sudah untracked.

Probe ASan native memakai test yang sudah ada, bukan program probe baru; sukses probe tidak menggantikan pembuktian leak Defect B.

Perintah: `date --iso-8601=seconds; date +%Z; uname -srmo; pwd; git --version; g++ --version; python3 --version; .venv/bin/python --version; .venv/bin/python -m pytest --version`

`````text
STDOUT:
2026-11-12T14:44:14+07:00
WIB
Linux 6.18.33.2-microsoft-standard-WSL2 x86_64 GNU/Linux
~/loanbench
git version 2.53.0
g++ (Ubuntu 15.2.0-16ubuntu1) 15.2.0
Copyright (C) 2025 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Python 3.14.4
Python 3.14.4
pytest 9.2.0

STDERR:

exit=0; durasi_detik=0.233
`````

Perintah: `git ls-files -z | xargs -0 sha256sum`

`````text
7eaae6fbdddfcf88524df07f4041d5ea16c690fca1978ee7a422147bd0a739a7  .gitattributes
682665e3a07c8ec86d5c69f3642e1d80927dd49ac7c84ecca463975841313f90  .gitignore
893b669f680840bca5ab837bcf31e9598fe09c164b33f8e8e4d3ca713b6fccaf  PREDICTION.md
a14a21d979d34318d49c2414581249df94430d633bc3c1726af0f6cf5f5c2111  README.md
5e834d538c80ec0d905d8d0fdbbf29ba0f52f249c865314c6b5ee2381eacc833  cpp/app/main.cpp
21e4664d197054b76f1c07635e2b3ce50ab34073de6514cbb5dd9dae2f8cdd10  cpp/include/pinjamlab/app/runner.hpp
daafd004b5e2de622eb4b2598c66901297fd6b3dd2d800666827fc70e4617b38  cpp/include/pinjamlab/app/seed.hpp
097670d34b20b38e0d8038f078f2815e6cb91718229e39e15f0c614c42d214b7  cpp/include/pinjamlab/domain/equipment.hpp
58d637a4d6b3b6e562cf6dfb2a550f3255d5c74572f0deae05ac89af77673ef7  cpp/include/pinjamlab/domain/loan.hpp
95cf215323568f9a1e14d23fc46b5db82c4d66cc3e5a2a728282b0b929e2fadf  cpp/include/pinjamlab/domain/loan_error.hpp
e09509ff1ad533be70480f6bbf945fcef419305382964a2fac2ea4fcd66b90cc  cpp/include/pinjamlab/domain/member.hpp
187631d7015e8a4b79f294b51481765381d56fcf05962b03fbee8a38ae984782  cpp/include/pinjamlab/domain/result.hpp
5ee0982bc90e585352e57d703f34b654d54df9c25f6d675c03f7aa8981823089  cpp/include/pinjamlab/io/csv_reader.hpp
a33b4febba4172a20d4ec31341605ccecd66213c6db51aebb06cc8fa408c0af2  cpp/include/pinjamlab/io/report_writer.hpp
e5a13c09e382370ded2159714aa46ecfd3f887ed0c20dec105567b83e5f06390  cpp/include/pinjamlab/io/validator.hpp
4457a82a70be7a7a91efbe0668245c31d70f60d8cf8d8bbd2df46175911fc0fa  cpp/include/pinjamlab/service/database.hpp
e12d58c3193eb1cda9ba9816c33b58b771a38f86b999f421904de4e8747330ff  cpp/include/pinjamlab/service/loan_service.hpp
72e9a55d32c4143974a36f35004295f8e20307ccb92d311e4ce818007c176769  cpp/include/pinjamlab/service/txn_guard.hpp
4ded6d7be833c3829e704116c4a5f0056620cb639b463c0b3b12f3ccf8758230  cpp/tests/mini_catch.hpp
c57d25e3bd1000ce59748c38a02460a3f3c8611f9b5c23f1d7e922871d898cc0  cpp/tests/test_app.cpp
ac6b11aaa2b7bbd52b68a7d79fc2c7d946c3d90297b523e823dbf890923ab8f3  cpp/tests/test_errors.cpp
1c823df323a8a7c722cadb668667547014b404dbe0bd1446b8d574aeaf38e3e8  cpp/tests/test_raii.cpp
4fe71b0bfeaaf0542d8d1df9350f6f75849dc56673a1474f8f7ebeda29670b6b  cpp/tests/test_result.cpp
ca7ac9842013bebf2bb3af5d210b6553265522ac98a1383f02536a73b4f5baa6  cpp/tests/test_robustness.cpp
11c1ad51dd372626c58491582fdd5ad31064162c2c19f0cf4ed186e0374fbdc9  docs/PROGRESS.md
503427789fd2a642f9c6ab878628e4223744bf987c6529037c97185f75998c85  docs/SERAH_TERIMA.md
f6923fda7d76352b03c1662b9bc9962faf2174fefcee2d360862c1679c18a377  docs/decisions.md
c73d3d488567f84395b9059ca24314e3dc9bbe3a969a9fbc022a4f618b030ac8  docs/env.md
b1cde1d90e344b641f2d94f5afbe5dd1bb9f96652cb53a023c06af89728d51c0  docs/evidence/00_baseline_run.txt
f6b3ab06d7417644753d3f0ac2e5263b86916eb41f2e9d2136c54740530ab5f4  docs/evidence/01_t1_line_ending_proof.txt
e5a31873465302618126102cecd03dba3aae1e147e0482d3aac80dbf898ecde7  docs/evidence/02_run_with_venv.txt
fb34e162e93e92139b88e5a768a3727c812e2c9baa95caaeb78ea25bb6c4da09  docs/evidence/03_wsl_baseline.txt
9cdd670d064da5d7dd0a9c159c234636edfd8b8725f95f9e4b449c17add8dff3  docs/evidence/04_wsl_setup_green.txt
6321945c2ee7f5116100b1e02f5499b49fad00599874c94c1a77378d33b122d9  docs/evidence/05_asan_instructor_errors.txt
ef2b171112cd4d622853061a4a200fa4183de603e19b4fd4b1b9e53cf02acadb  docs/evidence/borrow-callsites.log
870ca4845e176fd0a98a8269e400fb8d338f0997064655523629d3cd427a4e16  docs/evidence/dependency-full-run.log
f1845c9872538bf90b5cd062444d5179b70dff01a18b9e675f3aca02c0ef81ca  docs/evidence/dependency-graphs.log
eae3e0baa60fedd2232b0ecc42b3eb00783452760cea7bbbe886dbe5dbcbaf3b  docs/evidence/dependency-negative-tests.log
8ab060b954bd58f9e3d9cccd715f16eda5cb3986ac479effed7e60df75853b94  docs/evidence/parity-review.log
7ac7a4d1f7d3cace3d3e7e16ce9038e110e286824a75610bda92d2f35e480e42  docs/evidence/pre_result_callsites.txt
9cdd670d064da5d7dd0a9c159c234636edfd8b8725f95f9e4b449c17add8dff3  docs/evidence/prediction_precommit_green.log
e857b0fe9e962a504d981f5554d4da953bc9d3bc31991eeb826339e913d89a65  docs/evidence/reconstructed/00-inherited-original.log
532e64f425d7bf7f41d40986b0c900589991c4b416fe2d0917028db7288a7ec1  docs/evidence/reconstructed/01-baseline-inherited.log
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  docs/evidence/reconstructed/01-build.log
d9e08144cab8b02bbd3b66ac4140e74592a6d88e198ae9f80a79956d95172b59  docs/evidence/reconstructed/01-commit.log
be01797502a9d3e7f4eb16cef8e256204d9d8f3da7617f1b91fca3ce28ef9d17  docs/evidence/reconstructed/01-precommit-diff.patch
70641fef3822ed7394ac1cbe7bb281d2cbd97b7703cb9e9f18a05bd2557fc349  docs/evidence/reconstructed/01-precommit-log.txt
e4eda06c9e6f3c224286a9d7ef9374262188d4509ad6b2b9cdb0071daecb899e  docs/evidence/reconstructed/01-precommit-status.txt
10514163282082acc5d34589faa04898fd0e3230922ee6ca2284902ac469f505  docs/evidence/reconstructed/02-commit.log
2f248878da213b837fed60a5de3f9dee603938975585bef4c7a988f138c9e752  docs/evidence/reconstructed/02-defect-A-red.log
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  docs/evidence/reconstructed/02-precommit-diff.patch
a9f369ae52d2c5231b1dcba73463c5c3b827dd9238f22b3207d645bca1ccee57  docs/evidence/reconstructed/02-precommit-log.txt
af54c5cfe2a2ec4c54459e6392b0c898a31b015415883ec6f39ee2b80162dcc1  docs/evidence/reconstructed/02-precommit-status.txt
5d17077d3f8afa85fce12f5761f6e77c90bda8ff11d65313bd1a74bac6062b50  docs/evidence/reconstructed/03-commit.log
2c46a18871e426acdc6f62105d5933da91e2e97d67197dd4da937d68cd62086e  docs/evidence/reconstructed/03-defect-A-green.log
b56ab88ae6f1d0a42061147e15cfc07f3b05108d3399ad12443d89313e233db9  docs/evidence/reconstructed/03-inherited.log
55147a5bc2398e9c40464661734f271df47badcde45ae88d5eb83af53e78dc37  docs/evidence/reconstructed/03-precommit-diff.patch
e6efd2c2dbb8b414d1103a121baf69e3c68805e9cd59c2fa423d40f9f57f6fbb  docs/evidence/reconstructed/03-precommit-log.txt
88171805f3c917029bc174ae1d7cf712e3c17479bcc08d77f914c2fc7f600276  docs/evidence/reconstructed/03-precommit-status.txt
10b39cfdf65bd435fd3081d8e242c61658b750113c25e5e3dfe836da30f8a72c  docs/evidence/reconstructed/04-asan-before-status.txt
3ee372d977c9c5412d40a163b79f27a7cddf2e3a2ef0307d8f129715be24368d  docs/evidence/reconstructed/04-asan-before.stderr
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  docs/evidence/reconstructed/04-asan-before.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  docs/evidence/reconstructed/04-asan-build.log
cf205dbb8cea84897b488abcc281bf96698d5e94b1096b16657b4caba9082a22  docs/evidence/reconstructed/05-asan-after-status.txt
39a9c241b44ee1f708ed3359864ba75b2144c74f88c70f20d6bd62ae780790ae  docs/evidence/reconstructed/05-asan-after.stderr
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  docs/evidence/reconstructed/05-asan-after.stdout
f9a58c1e7949805ef77ef51115fd7a486dc5a42c435f796d1c31d01b5fe08f70  docs/evidence/reconstructed/05-asan-green.log
67c06c98ffa95250312f9ce75219b081d0e6164fbf2b054a6def4fa4c91e2ddd  docs/evidence/reconstructed/05-commit.log
68984f450ce70f3c1fb13409f9bc62b70ef752dfc6d67f076e688c3c80da42d1  docs/evidence/reconstructed/05-inherited.log
c9a1066f22a45df682a029addb69f019344374b1fd57e5d76de3e1929fc8b330  docs/evidence/reconstructed/05-monolith-green.log
aa8f7fdf95dc5e532f932093b25955b2d13b99c98c1b1d84234f40b357041cc3  docs/evidence/reconstructed/05-precommit-diff.patch
dbcb9abea7f3a5ed5978958e40df75cf083c415616dbb2c4a44dc59e3d7153e0  docs/evidence/reconstructed/05-precommit-log.txt
dbfdb9f793c487d329ad5f593718345985b7e57244b23cd1883d9e3445670def  docs/evidence/reconstructed/05-precommit-status.txt
c0648da9c7f7ac901abc9b3d441a11357398c6316506500996052cf55bcaec79  docs/evidence/reconstructed/06-commit.log
58418aea7a6f6efc00536d8ce2ee3cfe5632db38732293a0d819cd630c0ccbee  docs/evidence/reconstructed/06-docs-inherited.log
ffb6bb9c9c24d709b801a2057cf693517ddeaf7c542f26fbe203b7e6967f382e  docs/evidence/reconstructed/06-precommit-diff.patch
11321d5456ff0745b2c67cff8b76b2291ec833f70594737be25d6734836e6540  docs/evidence/reconstructed/06-precommit-log.txt
99823ec956ca3a77abf0f504421136918022e2fa01d91034d6f49f23c5293caa  docs/evidence/reconstructed/06-precommit-status.txt
7cce9726e5341742709c119baf9849830a19357924deaa3877125b37b38de797  docs/evidence/reconstructed/SUMMARY.txt
424a899870a7a8386f80e8e7f0693af27d5f901990373b8de2916c6cdc978caa  docs/evidence/reconstructed/commits.txt
006af72a29bab8fb8afcb169c3ceec5028570ca626ce2654c49878656993fadd  docs/evidence/reconstructed/final-change-stat.txt
0512a381ecb06f1e7907ad5fa26614f531c3390a4361a381e87ae737ba242750  docs/evidence/reconstructed/isolation-verification.txt
f1bf47695877bab35bbbc5847e628e8b97a12d746cef8a6c50a55d0e5219df17  docs/evidence/reconstructed/main-diff-after.patch
f1bf47695877bab35bbbc5847e628e8b97a12d746cef8a6c50a55d0e5219df17  docs/evidence/reconstructed/main-diff-before.patch
597881f5dbcd516992be617cb9d8f4eb2f10a9d9299082fd1423b1dfd3127218  docs/evidence/reconstructed/main-head-after.txt
597881f5dbcd516992be617cb9d8f4eb2f10a9d9299082fd1423b1dfd3127218  docs/evidence/reconstructed/main-head-before.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  docs/evidence/reconstructed/main-index-after.patch
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  docs/evidence/reconstructed/main-index-before.patch
cd6e53730dc1ab913b18bdcea76c67f4a5b80440476f47757deab3c6f2942e0f  docs/evidence/reconstructed/main-status-after.txt
cd6e53730dc1ab913b18bdcea76c67f4a5b80440476f47757deab3c6f2942e0f  docs/evidence/reconstructed/main-status-before.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  docs/evidence/reconstructed/production-diff.patch
aab02797021693596c8ff8b7008bc6899bed7491e66e573d48763b3dbf9d8abe  docs/evidence/reconstructed/quota.csv
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  docs/evidence/reconstructed/worktree-final-status.txt
6388d85966e5a7fc3baf3f1a7bd9ed39d51f698fca99ea1d3020d28421116aa0  docs/evidence/result_asan.txt
b6c2fc66d7b66d0dec155aa103fb3984c3740def781d1b40289b0a74182f4a1f  docs/evidence/result_callsites.txt
c921f281ee9b511db4d6eed7e7cc792daa867ce3baaf416368799d8fdb97916d  docs/evidence/result_changed_callsites.txt
c969d30ffca841a4d3f01b21da4983176ff7deadd56d344a7c7e04d59948b41f  docs/evidence/result_diff.patch
1a4cd4bb62155c839ad8d71d67c386c6976c0cd9cb1b7a29f7736f225fcef29e  docs/evidence/result_diff_stat.txt
376dbd788edfad15999758648912be3492dd61f55634ca10aa30d59c1fb81c0b  docs/evidence/result_full_run.txt
3854e4b1e8d7db56771926cdcadc2996ffa6fa4f5d7556cc26863c2265cc8d18  docs/evidence/result_golden_generation.txt
96806101d270f6580f780f25cf5f328644b68032ee76e6d3daf699961b049f70  docs/evidence/result_new_files.patch
cfde87d776ca69b76c4613d56cb259690e3fb1127481de7456aa78133aade642  docs/evidence/result_production_callsites.txt
13a9ac786bc9aa3605896bd0a4109406c011a2e956373b93a6c0daed32a8b47b  docs/evidence/result_status.txt
55f71472053a86a6674aac9b0c1c4cf2110934bd60d3d3f0886e82cc04484ca2  docs/graphs/after-cpp-layers.mmd
388b7eb60797e3b48e13a44decb4ea1f1620ed4436fb7ec00446d6ac0d81a42e  docs/graphs/after-cpp.mmd
55f71472053a86a6674aac9b0c1c4cf2110934bd60d3d3f0886e82cc04484ca2  docs/graphs/after-py-layers.mmd
76235c9d96ecf72891259d0d0d505030d3d10127997f54e964c823c6904563e6  docs/graphs/after-py.mmd
9f762b384104b7d565799e3cebf5e6eb51d69da597a6270c8a163a038d7e169e  docs/graphs/before-cpp.mmd
8174c788a1e6c8146e653b22ffab99a6b0d72bd1d2485353bc94ffb7655735bb  docs/graphs/before-py.mmd
cbb5437bd6907995db4a09d2b936cf2c18b3324ce31fded5e4bab18d7f6a537a  docs/lab2_result_refactor.md
bf7cc630cfc5ecf4f4e7bcf082a7dde83400281ee2be3e1069c226f9362f4fd6  docs/prediction_outcome.md
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  py/pinjamlab/__init__.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  py/pinjamlab/app/__init__.py
0a76cbd4b63222861d15581756d06b6071048100e247b4852d4ae8971ef618f3  py/pinjamlab/app/main.py
6a8fbfbd7ac55b3c37fa3c1567af168150c2f8ccc2259d03fc11fc592a32ea81  py/pinjamlab/app/runner.py
fc2678294018a1918f2e8a75ee1f7676a14b4a819663e7d1347ee8016558eb77  py/pinjamlab/app/seed.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  py/pinjamlab/domain/__init__.py
cb7e71729af0d34bd740cc02e0c4c5940e2610f281d040793f241ecfbe8258c6  py/pinjamlab/domain/equipment.py
13873a661b5e3f1b4368b4d1c22b7edd0fb1192d2d5dba57110d32ad5237d65e  py/pinjamlab/domain/loan.py
7a07d8ff9880f7ec1e1c32168950eb2e4ee48bd4189dd5311342126140d1512d  py/pinjamlab/domain/loan_error.py
9fb3524a92f889623b9c0fd84f689f45eb715700e5f3198e4bdd4d10f81e44a4  py/pinjamlab/domain/member.py
ca3ec018aceb437f2c5cf51859c217b65767a380a0785646cfc54e0f0f815f7b  py/pinjamlab/domain/result.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  py/pinjamlab/io/__init__.py
0f0942ac22a83e67869a46aba040a28d554485d4c99fd7ff83b6a5b9743db84c  py/pinjamlab/io/atomic_writer.py
54a79ee727525bfca718f05b1451e3f9464d60c125d543d5a1581644427aa077  py/pinjamlab/io/csv_reader.py
742cfaa630ffbe711157738775129ea40ede3a526bd9eae1108165ab22acb329  py/pinjamlab/io/report_writer.py
c39a76b90eae7fd075d6728416b09410e4b61fa5cd962569bbe48ab290c832e1  py/pinjamlab/io/validator.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  py/pinjamlab/service/__init__.py
df08efe1bbe9bb3b8fc42f50e2333d5129a9933f009f12c675516fd02d09bbeb  py/pinjamlab/service/database.py
4a238f99428fc7486e19e00c823b554d3c0453f3923bc9b3f7d6a66de053edc5  py/pinjamlab/service/loan_service.py
e9ffdd03f3e3df300e5d4586ec3f755e32d9cba83784acdedd7da5846ef39c12  py/pinjamlab/service/txn_guard.py
35da9587ddcdf2f12064f3acbf4ea353246673441e3dc5f4f0af92968ed2248a  py/requirements.txt
2531d996e5fe8f65c18f0f6aa9b93db4c93e562be2adc1ba538435314b98982f  py/tests/test_app.py
848255d4b5a44d5271fc4407b70f6f07ca25245807e96354bcc4ddbcbbde77f3  py/tests/test_cleanup.py
4c7a1c714b0c16684576baab7512639931efb289ced82e0fc675f960024125a4  py/tests/test_dependency_gate.py
7f6f69727e984124cbe9fc0d8e5e0301811b1a4ed8cbd6e80babb2229ff2a29c  py/tests/test_errors.py
2ae1a57d838490b18826583154d3caf13c1fd29893f5550684fc98e25b3c6eab  py/tests/test_result.py
d952efecea7600dfba967e2a6d71f7e825cf418ac8649a1740b8ee9db021cdfd  py/tests/test_robustness.py
0d043a1301675902b6df1d5361c1795f75f909f1b43119e861d2637f174d1596  run_tests.sh
8010b40371a505068b46b0eafd31e4790d0042e7018b0fdb25b6879b05f30219  sample-data/bad-requests.csv
7e16a06b3b97c416adb5d4f375cd3d6260e90f718fe6ab85468409b485b59a6b  sample-data/expected-output.txt
87387ba9a28f37a731fdf18d7abf2a7bab25bde48ac9eaf0b61cae435fb1a2c5  sample-data/my-bad-requests.csv
0e34893622a5fa7bc9debf6d07681418669a543b3919c54223d815e364055a09  sample-data/my-expected-output.txt
c0f5bbd6c0052df7648a4040997fd61238e3cd475b3f6ed10343c6462145c171  scripts/audit_result_calls.py
086dfb11e08af9422be579d6e8f22d53dd62752e5cec59f19d8a014a777e27aa  scripts/check_dependencies.py
ea2f3bebfa4a1a5307ef0b53cbb8dbbc6ca0e22f97db87f141c2d1784c7999c5  scripts/count_callsites.py
f7adcd8c908c6804797cdfda8e90962b784db499944291937499b1709690e196  scripts/count_callsites.sh
2ab4efd2488baa1706e03d074cbdeec3ab1be843260ba4ca2b039e58a8162e1b  scripts/gen_graphs.py
8b26699c2b2030995153a5031d2a49ad97c727eafd8851fb1672ad80f72652fd  scripts/run_result_asan.sh
37df8cd56395c085bf1b4451c842764831a71e5a83893d0f15b67f371f2ee854  tests/limits_demo.cpp
4cc80e7b38458bcef51bd9415c7578909449b605c963402a61ba5ba863cc993a  tests/limits_demo.py

STDERR:

exit=0
`````

Perintah: `find cpp py/pinjamlab py/tests tests scripts sample-data docs -type f ! -path "*/__pycache__/*" ! -name ANALISIS_INPUT.md | sort`

`````text
STDOUT:
cpp/app/main.cpp
cpp/include/pinjamlab/app/runner.hpp
cpp/include/pinjamlab/app/seed.hpp
cpp/include/pinjamlab/domain/equipment.hpp
cpp/include/pinjamlab/domain/loan.hpp
cpp/include/pinjamlab/domain/loan_error.hpp
cpp/include/pinjamlab/domain/member.hpp
cpp/include/pinjamlab/domain/result.hpp
cpp/include/pinjamlab/io/csv_reader.hpp
cpp/include/pinjamlab/io/report_writer.hpp
cpp/include/pinjamlab/io/validator.hpp
cpp/include/pinjamlab/service/database.hpp
cpp/include/pinjamlab/service/loan_service.hpp
cpp/include/pinjamlab/service/txn_guard.hpp
cpp/tests/mini_catch.hpp
cpp/tests/test_app.cpp
cpp/tests/test_errors.cpp
cpp/tests/test_raii.cpp
cpp/tests/test_result.cpp
cpp/tests/test_robustness.cpp
docs/PROGRESS.md
docs/SERAH_TERIMA.md
docs/decisions.md
docs/env.md
docs/evidence/00_baseline_run.txt
docs/evidence/01_t1_line_ending_proof.txt
docs/evidence/02_run_with_venv.txt
docs/evidence/03_wsl_baseline.txt
docs/evidence/04_wsl_setup_green.txt
docs/evidence/05_asan_instructor_errors.txt
docs/evidence/borrow-callsites.log
docs/evidence/dependency-full-run.log
docs/evidence/dependency-graphs.log
docs/evidence/dependency-negative-tests.log
docs/evidence/parity-review.log
docs/evidence/pre_result_callsites.txt
docs/evidence/prediction_precommit_green.log
docs/evidence/reconstructed/00-inherited-original.log
docs/evidence/reconstructed/01-baseline-inherited.log
[... total 150 baris; lengkap bin/analisis-export/command-004.txt ...]
py/pinjamlab/app/main.py
py/pinjamlab/app/runner.py
py/pinjamlab/app/seed.py
py/pinjamlab/domain/__init__.py
py/pinjamlab/domain/equipment.py
py/pinjamlab/domain/loan.py
py/pinjamlab/domain/loan_error.py
py/pinjamlab/domain/member.py
py/pinjamlab/domain/result.py
py/pinjamlab/io/__init__.py
py/pinjamlab/io/atomic_writer.py
py/pinjamlab/io/csv_reader.py
py/pinjamlab/io/report_writer.py
py/pinjamlab/io/validator.py
py/pinjamlab/service/__init__.py
py/pinjamlab/service/database.py
py/pinjamlab/service/loan_service.py
py/pinjamlab/service/txn_guard.py
py/tests/test_app.py
py/tests/test_cleanup.py
py/tests/test_dependency_gate.py
py/tests/test_errors.py
py/tests/test_result.py
py/tests/test_robustness.py
sample-data/bad-requests.csv
sample-data/expected-output.txt
sample-data/my-bad-requests.csv
sample-data/my-expected-output.txt
scripts/audit_result_calls.py
scripts/check_dependencies.py
scripts/count_callsites.py
scripts/count_callsites.sh
scripts/gen_graphs.py
scripts/run_result_asan.sh
tests/limits_demo.cpp
tests/limits_demo.py

STDERR:

exit=0; durasi_detik=0.009
`````

Perintah: `g++ -std=c++20 -Wall -Wextra -Werror -g -O1 -fno-omit-frame-pointer -fsanitize=address -fno-pie -no-pie -Icpp/include -Icpp/tests cpp/tests/test_errors.cpp -o bin/analisis-export/asan-probe && ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 bin/analisis-export/asan-probe`

`````text
STDOUT:
===============================================================================
Running test suite (8 test cases)...
===============================================================================
PASSED: UnknownAssetTag: unknown tag, carries the tag
PASSED: UnknownMember: unknown member, carries the id
PASSED: InvalidLoanDuration: business-rule maximum, not the format check
PASSED: EquipmentUnavailable: already on loan returns the same message
PASSED: QuotaExceeded: over quota, carries active and limit
PASSED: Remaining thrown service errors are catchable as LoanError
PASSED: Catch order: most-specific handler runs when listed first
PASSED: A successful borrow raises nothing and updates both entities
===============================================================================
All tests finished: 8 passed, 0 failed.
===============================================================================

STDERR:

exit=0; durasi_detik=5.444
`````

Perintah: `git rev-parse HEAD; git branch -avv; git tag -n; git log --all --date=iso-strict --format="%H %ad %cd %s"; git status --porcelain=v1 --untracked-files=all; git diff --stat; git diff --cached --stat; git diff --shortstat m3-as-received...HEAD; git diff --shortstat baseline/reconstructed...HEAD`

`````text
ce8bec3c830cfb1c8880453ff084a3aa62c6ac84
+ baseline/reconstructed                33c2ad5 (~/loanbench/bin/reconstructed) [origin/baseline/reconstructed] docs: clarify observed fixture and Python path exceptions
* lab/modul3                            ce8bec3 [origin/lab/modul3] docs: add Module 3 documentation and lab materials for exception handling and modularity
  main                                  aa83fec [origin/main] chore: import instructor code as received
  remotes/origin/HEAD                   -> origin/main
  remotes/origin/baseline/reconstructed 33c2ad5 docs: clarify observed fixture and Python path exceptions
  remotes/origin/lab/modul3             ce8bec3 docs: add Module 3 documentation and lab materials for exception handling and modularity
  remotes/origin/main                   aa83fec chore: import instructor code as received
m3-as-received  chore: import instructor code as received
ce8bec3c830cfb1c8880453ff084a3aa62c6ac84 2026-11-12T14:02:31+07:00 2026-11-12T14:02:31+07:00 docs: add Module 3 documentation and lab materials for exception handling and modularity
5b26936d962f281a4925d9bc2ff3068ac5b5cf54 2026-11-12T13:26:06+07:00 2026-11-12T13:26:06+07:00 docs: predict Result refactor before implementation
5f8fc2991faeba364fa00a17db982dff2855da05 2026-11-12T13:25:18+07:00 2026-11-12T13:25:18+07:00 feat: add typed failures and robust boundary cleanup
33c2ad53232eff8eb7006dca64e1e00d2e998fd0 2026-11-12T13:02:58+07:00 2026-11-12T13:02:58+07:00 docs: clarify observed fixture and Python path exceptions
67780d98515464f510ba10d04d40e48b7ef4be03 2026-11-12T13:02:14+07:00 2026-11-12T13:02:14+07:00 fix: own Loan with unique_ptr across quota exceptions
0f0ccadbaf32930cf46b531cd76715edd9b6751b 2026-11-12T13:00:50+07:00 2026-11-12T13:00:50+07:00 fix: report application errors and return nonzero
0c004e1dbb9cc6f9e581d635e5fe91f1db343368 2026-11-12T12:57:29+07:00 2026-11-12T12:57:29+07:00 test: failing test exposes swallowed errors
6ca6c7b0fc01bf58087ec740859ed7d20f06d02e 2026-11-12T12:55:56+07:00 2026-11-12T12:55:56+07:00 chore: reconstruct deliberately defective teaching baseline
cc854672524058c02ff3496ee9b82305053fdc32 2026-11-12T12:40:13+07:00 2026-11-12T12:40:13+07:00 chore: verify WSL baseline and persist module progress
5cc26e629ec8b1f0f25f917de54975b1474754cd 2026-11-12T11:45:41+07:00 2026-11-12T11:45:41+07:00 docs: add env.md and evidence for T1 fix and venv run
ab23da412a9aa0671792557395f18860a7f8c151 2026-11-12T11:45:41+07:00 2026-11-12T11:45:41+07:00 fix: normalize golden-file line endings
299cec02e93ac55f5a4b691d5ee2f4dcc3657eed 2026-11-12T11:43:14+07:00 2026-11-12T11:43:14+07:00 chore: untrack build artifacts (bin/, __pycache__) now covered by .gitignore
aa83fec0ea1d8a145a2681d71e4d46f104d15d1c 2026-11-12T11:42:58+07:00 2026-11-12T11:42:58+07:00 chore: import instructor code as received
a0aececdada5d7f4a7622f462ae5d6700f2c8bc7 2026-11-12T11:41:08+07:00 2026-11-12T11:41:08+07:00 feat: initialize loanbench project with C++ and Python implementations
?? docs/ANALISIS_INPUT.md
 155 files changed, 7698 insertions(+), 243 deletions(-)
 155 files changed, 7698 insertions(+), 243 deletions(-)

STDERR:

exit=0
`````

## §1 Status pekerjaan & penyimpangan

| Tahap | Status faktual saat ekspor | Penyimpangan/batas |
|---|---|---|
| D0 | Setup Git/WSL, baseline rekonstruksi dan ASan terverifikasi | Python 3.12 belum diverifikasi; m3-start asli TIDAK ADA; T1 merah asli tidak direproduksi |
| D1 | Lab 1 belum lengkap | Dokumen lab1 dan riset Ariane TIDAK ADA; fixture/CLI tersedia (§3) |
| D2 | Implementasi Lab 2 tersedia | Node, Result, cleanup dan defect diuji; bukan refleksi pribadi selesai |
| D3 | Lab 3 sebagian: prediction, gate dan graf tersedia | Matriks mandiri dan reproduksi rekan belum tersedia (§5) |
| D4 | Analisis belum selesai | Trace tangan TIDAK DILAKUKAN; pembelaan pribadi/viva belum ada |
| E | Laporan PDF TIDAK ADA | Dossier ini bukan laporan PDF; pengujian §7 bukan tahap E |
| F | Belum lengkap | Refleksi, viva, konfirmasi dosen dan hasil rekan belum tersedia |

Pemetaan formal modul C1-C6 dan P1-P5: TIDAK DIKETAHUI dari prompt ini. Nomor tidak dipasangkan ke kelas/fungsi berdasarkan dugaan. Status hijau teknis bukan klaim semua praktikum selesai.

Perintah: `cat docs/PROGRESS.md`

`````text
# Progres Modul 3

Tanggal: 2026-11-12. Spesifikasi tunggal: prompt pengguna, bukan PDF/TXT.
Commit fitur sebelum Result: 5f8fc29. PREDICTION ditulis sekarang sebelum implementasi.

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
`````

## §2 Keputusan desain final

Node #1 yang nyata adalah `AssetTagCaseMismatch : UnknownAssetTag`, membawa given/tag dan suggestion. Node #2 `ReservationConflict : LoanError`, membawa tag dan reservedFor. Case mismatch dicari hanya sesudah lookup tag eksak gagal, dengan pelipatan ASCII; reservasi disimpan pada Equipment dan diperiksa sebelum kuota. Unknown tag/member, durasi, reservasi, kuota tetap exception. EquipmentUnavailable saja menjadi failure Result saat borrow; kelas exception tetap ada untuk pesan/adapter dan jalur domain lain. Validator mengembalikan Result untuk input format. Duplikasi alat adalah logic_error/ValueError (bug/setup), bukan penolakan baris biasa. I/O pembukaan CSV dan kegagalan tak dikenal diteruskan ke boundary proses.

Data bertipe lebih kaya daripada string: catch AssetTagCaseMismatch memakai given/suggestion; Python juga memiliki catch ReservationConflict memakai tag/reserved_for, sedangkan C++ reservasi memakai handler LoanError generik. Ini perbedaan nyata, bukan paritas handler penuh. Alasan pribadi mahasiswa untuk memilih exception pada A3 belum diisi (§14).

Perintah: `cat docs/decisions.md`

`````text
# Keputusan

- Prompt pengguna adalah spesifikasi tunggal; Modul 3.txt tidak dipakai sebagai syarat tambahan.
- Pertahankan branch lab/modul3 dan tag m3-as-received yang sudah ada; jangan tulis ulang sejarah.
- Dua berkas evidence lama yang sudah berubah tidak disentuh atau di-stage.
- Python WSL 3.14.4 dipakai sementara agar pekerjaan tidak terhenti; verifikasi 3.12 tetap belum terpenuhi.
- Default desain B tetap berlaku; EquipmentUnavailable tidak diubah sebelum commit PREDICTION.
- Clone sementara dan seluruh keluaran kerja harus berada di dalam repo, bukan /tmp atau home lain.
- core.autocrlf tidak diubah karena instruksi lingkungan melarang perubahan git config.
- Riwayat commit lama tidak memuat footer atribusi. Footer baru menggunakan identitas agen
  Co-authored-by: OpenAI ChatGPT <[EMAIL DIHAPUS]>; ini atribusi AI, bukan identitas mahasiswa.
`````

## §3 Lab 1

Dokumen terpisah Lab 1.1 peta handler, Lab 1.2 mode kegagalan, Lab 1.4 Ariane/refleksi: TIDAK ADA. Sumber Ariane yang diverifikasi pada sesi ini: TIDAK ADA; tidak ada klaim faktual kecelakaan atau sumber web buatan. Peta handler yang dapat diturunkan dari sumber tersedia di §4 dan §11, bukan artefak mahasiswa lama.

Fixture tambahan mempunyai tepat lima baris data (header tidak dihitung): blank tag, blank member, overflow int32, mismatch case, konflik reservasi. Bukti historis generasi golden berasal dari berkas berikut; sesi ini hanya memverifikasi ulang dan tidak menimpa fixture.

Perintah: `cat sample-data/bad-requests.csv`

`````text
tag,member_id,days
,M-101,7
LP-001,,7
LP-001,M-101,abc
LP-001,M-101,-3
LP-001,M-101,0
LP-999,M-101,7
LP-001,M-404,7
LP-002,M-101,7
LP-003,M-102,7
LP-001,M-101,400
`````

Perintah: `cat sample-data/expected-output.txt`

`````text
row 1: tag is empty
row 2: memberId is empty
row 3: days is not a number: abc
row 4: days must be positive, got -3
row 5: days must be positive, got 0
row 6: Unknown asset tag: LP-999
row 7: Unknown member: M-404
row 8: Equipment already on loan: LP-002
row 9: Loan quota exceeded: 2 active, limit 2
row 10: Loan duration exceeds maximum: 400 > 90
`````

Perintah: `cat sample-data/my-bad-requests.csv`

`````text
tag,member_id,days
   ,M-101,7
LP-001,   ,7
LP-001,M-101,2147483648
lp-001,M-101,7
LP-004,M-101,7
`````

Perintah: `cat sample-data/my-expected-output.txt`

`````text
row 1: tag is blank
row 2: memberId is blank
row 3: days is out of range: 2147483648
row 4: Unknown asset tag: lp-001 (did you mean LP-001?)
row 5: Equipment reserved: LP-004 for M-103
`````

Perintah: `g++ -std=c++20 -Wall -Wextra -Werror -Icpp/include cpp/app/main.cpp -o bin/analisis-export/cli`

`````text
STDOUT:

STDERR:

exit=0; durasi_detik=1.616
`````

Perintah: `bin/analisis-export/cli sample-data/bad-requests.csv >bin/analisis-export/cpp.stdout 2>bin/analisis-export/cpp.stderr; rc=$?; cat bin/analisis-export/cpp.stdout; cat bin/analisis-export/cpp.stderr >&2; echo CLI_EXIT=$rc; diff -u sample-data/expected-output.txt bin/analisis-export/cpp.stderr; diff_rc=$?; echo DIFF_EXIT=$diff_rc; test "$rc" -eq 1 && test "$diff_rc" -eq 0`

`````text
STDOUT:
Processed 10 rows.
0 loans created, 10 rejected.
CLI_EXIT=1
DIFF_EXIT=0

STDERR:
row 1: tag is empty
row 2: memberId is empty
row 3: days is not a number: abc
row 4: days must be positive, got -3
row 5: days must be positive, got 0
row 6: Unknown asset tag: LP-999
row 7: Unknown member: M-404
row 8: Equipment already on loan: LP-002
row 9: Loan quota exceeded: 2 active, limit 2
row 10: Loan duration exceeds maximum: 400 > 90

exit=0; durasi_detik=0.015
`````

Perintah: `env PYTHONPATH=py .venv/bin/python -m pinjamlab.app.main sample-data/bad-requests.csv >bin/analisis-export/py.stdout 2>bin/analisis-export/py.stderr; rc=$?; cat bin/analisis-export/py.stdout; cat bin/analisis-export/py.stderr >&2; echo CLI_EXIT=$rc; diff -u sample-data/expected-output.txt bin/analisis-export/py.stderr; diff_rc=$?; echo DIFF_EXIT=$diff_rc; test "$rc" -eq 1 && test "$diff_rc" -eq 0`

`````text
STDOUT:
Processed 10 rows.
0 loans created, 10 rejected.
CLI_EXIT=1
DIFF_EXIT=0

STDERR:
row 1: tag is empty
row 2: memberId is empty
row 3: days is not a number: abc
row 4: days must be positive, got -3
row 5: days must be positive, got 0
row 6: Unknown asset tag: LP-999
row 7: Unknown member: M-404
row 8: Equipment already on loan: LP-002
row 9: Loan quota exceeded: 2 active, limit 2
row 10: Loan duration exceeds maximum: 400 > 90

exit=0; durasi_detik=0.064
`````

Perintah: `bin/analisis-export/cli sample-data/my-bad-requests.csv >bin/analisis-export/my-cpp.stdout 2>bin/analisis-export/my-cpp.stderr; rc=$?; cat bin/analisis-export/my-cpp.stdout; cat bin/analisis-export/my-cpp.stderr >&2; echo CLI_EXIT=$rc; diff -u sample-data/my-expected-output.txt bin/analisis-export/my-cpp.stderr; diff_rc=$?; echo DIFF_EXIT=$diff_rc; test "$rc" -eq 1 && test "$diff_rc" -eq 0`

`````text
STDOUT:
Processed 5 rows.
0 loans created, 5 rejected.
CLI_EXIT=1
DIFF_EXIT=0

STDERR:
row 1: tag is blank
row 2: memberId is blank
row 3: days is out of range: 2147483648
row 4: Unknown asset tag: lp-001 (did you mean LP-001?)
row 5: Equipment reserved: LP-004 for M-103

exit=0; durasi_detik=0.015
`````

Perintah: `env PYTHONPATH=py .venv/bin/python -m pinjamlab.app.main sample-data/my-bad-requests.csv >bin/analisis-export/my-py.stdout 2>bin/analisis-export/my-py.stderr; rc=$?; cat bin/analisis-export/my-py.stdout; cat bin/analisis-export/my-py.stderr >&2; echo CLI_EXIT=$rc; diff -u sample-data/my-expected-output.txt bin/analisis-export/my-py.stderr; diff_rc=$?; echo DIFF_EXIT=$diff_rc; test "$rc" -eq 1 && test "$diff_rc" -eq 0`

`````text
STDOUT:
Processed 5 rows.
0 loans created, 5 rejected.
CLI_EXIT=1
DIFF_EXIT=0

STDERR:
row 1: tag is blank
row 2: memberId is blank
row 3: days is out of range: 2147483648
row 4: Unknown asset tag: lp-001 (did you mean LP-001?)
row 5: Equipment reserved: LP-004 for M-103

exit=0; durasi_detik=0.068
`````

## §4 Lab 2

Hierarki lengkap berasal dari dua berkas kelas di bawah: LoanError berakar runtime_error (C++) / Exception (Python); UnknownAssetTag mempunyai turunan AssetTagCaseMismatch; UnknownMember, InvalidLoanDuration, EquipmentUnavailable, QuotaExceeded, ReservationConflict langsung menuruni LoanError. Kode lengkap berikut adalah bukti kontrak dan field, bukan bagan perkiraan.

Catch spesifik mismatch mendahului LoanError pada runner. Kompensasi lokal markLoaned/mark_loaned melakukan undo jumlah pinjaman lalu rethrow; bukan log-and-swallow. TxnGuard hanya menjaga ledger, bukan seluruh state. Kuota gagal sebelum TxnGuard dibuat. Batas exception safety: kegagalan alokasi pada stage/commit, pencatatan owners, atau konstruksi Loan setelah commit tidak dibuktikan strong guarantee; jangan menyimpulkan rollback seluruh objek. Python txn_guard menangkap Exception, bukan BaseException, sehingga cleanup KeyboardInterrupt pada guard transaksi tidak terbukti (atomic_writer berbeda karena finally).

Cleanup Lab 2.3 dibuktikan oleh throw di wilayah guard dan assertion ledger kosong/pending nol; ini bukan T7 (tes forgetting-with tautologis). Guard report destructor C++ noexcept mengabaikan kegagalan close, remove memakai error_code; ini bukan jaminan pembersihan selalu berhasil ketika filesystem menolak. Rename/replace atomik pada filesystem sama tidak sama dengan durability: tidak ada fsync. mkstemp lalu close/reopen memberi celah penggantian path; tidak diklaim aman terhadap penyerang lokal. API C++ memakai unistd/mkstemp sehingga portabilitas Windows native tidak diverifikasi.

Diff relevan commit Result: seluruh diff pada produksi, pengujian, fixture, runner, sanitizer dan laporan Result berikut diekspor penuh. Berkas evidence besar lain tidak disalin sebagai diff agar tidak menduplikasi log. Judul commit ce8bec3 berupa dokumentasi tetapi muatannya termasuk implementasi; jangan menganggap judul sebagai bukti tidak ada perubahan kode.

Ekuivalensi: wrapper uji memanggil implementasi borrow yang sama lalu menerjemahkan failure ke EquipmentUnavailable. Ada 12 kombinasi input, pengecekan tipe/pesan, field Loan, availability/reservation, jumlah pinjaman, committed/pending dan return pemilik. Ini bukti konsistensi adapter dan state pada kasus tersebut, bukan oracle independen untuk algoritme pra-refactor. Kode test lengkap ada §7.

Defect A/B adalah baseline DIREKONSTRUKSI, bukan starter dosen asli. Tanggal/hash berikut berasal Git, bukan waktu pembuatan ulang pada sesi ini.

Defect A arsip merah: 10 failed, 2 passed; hijau: 12 passed. Sesi ini tidak mengklaim menjalankan kembali commit merah dahulu atau membuat ulang urutan commit. Diff fix A juga memuat perubahan anotasi Python `str` menjadi `st` yang bukan inti penanganan error; ini penyimpangan riil yang perlu dicermati, bukan disembunyikan.

Laporan ASan arsip mentah sebelum dan sesudah diekspor penuh (termasuk stdout kosong dan status). Keduanya arsip eksekusi lampau; pembuktian baru terisolasi menyusul.

Interpretasi ASan: sebelum fix ownership diharapkan exit 23 karena leak; sesudah fix exit 1 tetap benar karena semua baris ditolak. Tidak menyamakan exit aplikasi 1 dengan kegagalan sanitizer. Laporan sesi ini di atas memperlihatkan hasil aktual beserta seluruh stderr.

Perintah: `nl -ba cpp/include/pinjamlab/domain/loan_error.hpp`

`````text
1: #ifndef PINJAMLAB_DOMAIN_LOAN_ERROR_HPP
2: #define PINJAMLAB_DOMAIN_LOAN_ERROR_HPP
3: #include <stdexcept>
4: #include <string>
5: #include <utility>
6: namespace pinjamlab {
7: class LoanError : public std::runtime_error {
8: public:
9:     explicit LoanError(const std::string& msg) : std::runtime_error(msg) {}
10: };
11: class UnknownAssetTag : public LoanError {
12:     std::string tag_;
13: protected:
14:     UnknownAssetTag(std::string tag, const std::string& message)
15:         : LoanError(message), tag_(std::move(tag)) {}
16: public:
17:     explicit UnknownAssetTag(std::string tag)
18:         : LoanError("Unknown asset tag: " + tag), tag_(std::move(tag)) {}
19:     [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
20: };
21: class AssetTagCaseMismatch : public UnknownAssetTag {
22:     std::string suggestion_;
23: public:
24:     AssetTagCaseMismatch(std::string given, std::string suggestion)
25:         : UnknownAssetTag(given, "Unknown asset tag: " + given +
26:                           " (did you mean " + suggestion + "?)"),
27:           suggestion_(std::move(suggestion)) {}
28:     [[nodiscard]] const std::string& given() const noexcept { return tag(); }
29:     [[nodiscard]] const std::string& suggestion() const noexcept { return suggestion_; }
30: };
31: class ReservationConflict : public LoanError {
32:     std::string tag_, reservedFor_;
33: public:
34:     ReservationConflict(std::string tag, std::string reservedFor)
35:         : LoanError("Equipment reserved: " + tag + " for " + reservedFor),
36:           tag_(std::move(tag)), reservedFor_(std::move(reservedFor)) {}
37:     [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
38:     [[nodiscard]] const std::string& reservedFor() const noexcept { return reservedFor_; }
39: };
40: class UnknownMember : public LoanError {
41:     std::string memberId_;
42: public:
43:     explicit UnknownMember(std::string memberId)
44:         : LoanError("Unknown member: " + memberId), memberId_(std::move(memberId)) {}
45:     [[nodiscard]] const std::string& memberId() const noexcept { return memberId_; }
46: };
47: class InvalidLoanDuration : public LoanError {
48:     int days_, maxDays_;
49: public:
50:     InvalidLoanDuration(int days, int maxDays)
51:         : LoanError("Loan duration exceeds maximum: " + std::to_string(days) + " > " + std::to_string(maxDays)),
52:           days_(days), maxDays_(maxDays) {}
53:     [[nodiscard]] int days() const noexcept { return days_; }
54:     [[nodiscard]] int maxDays() const noexcept { return maxDays_; }
55: };
56: class EquipmentUnavailable : public LoanError {
57:     std::string tag_;
58: public:
59:     explicit EquipmentUnavailable(std::string tag)
60:         : LoanError("Equipment already on loan: " + tag), tag_(std::move(tag)) {}
61:     [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
62: };
63: class QuotaExceeded : public LoanError {
64:     int active_, limit_;
65: public:
66:     QuotaExceeded(int active, int limit)
67:         : LoanError("Loan quota exceeded: " + std::to_string(active) + " active, limit " + std::to_string(limit)),
68:           active_(active), limit_(limit) {}
69:     [[nodiscard]] int active() const noexcept { return active_; }
70:     [[nodiscard]] int limit() const noexcept { return limit_; }
71: };
72: }  // namespace pinjamlab
73: #endif
`````

Perintah: `nl -ba py/pinjamlab/domain/loan_error.py`

`````text
1: """Pure domain module: no console output, no file streams, no text formats.
2: 
3: The dependency-rule check in run_tests.sh greps this package for exactly
4: those things (module-level file or console access) and fails the build if
5: it finds one outside a comment.
6: """
7: 
8: 
9: class LoanError(Exception):
10:     """Base for every PinjamLab loan failure."""
11: 
12: 
13: class UnknownAssetTag(LoanError):
14:     def __init__(self, tag: str) -> None:
15:         super().__init__(f"Unknown asset tag: {tag}")
16:         self.tag = tag
17: 
18: 
19: class AssetTagCaseMismatch(UnknownAssetTag):
20:     def __init__(self, given: str, suggestion: str) -> None:
21:         super().__init__(given)
22:         self.given = given
23:         self.suggestion = suggestion
24:         self.args = (f"Unknown asset tag: {given} (did you mean {suggestion}?)",)
25: 
26: 
27: class ReservationConflict(LoanError):
28:     def __init__(self, tag: str, reserved_for: str) -> None:
29:         super().__init__(f"Equipment reserved: {tag} for {reserved_for}")
30:         self.tag = tag
31:         self.reserved_for = reserved_for
32: 
33: 
34: class UnknownMember(LoanError):
35:     def __init__(self, member_id: str) -> None:
36:         super().__init__(f"Unknown member: {member_id}")
37:         self.member_id = member_id
38: 
39: 
40: class InvalidLoanDuration(LoanError):
41:     """A business-rule violation on duration (exceeds the policy maximum).
42: 
43:     Distinct from the io-layer's "days is not a number" / "days must be
44:     positive" checks, which are format failures returned as a Result before
45:     a request ever reaches the domain layer.
46:     """
47: 
48:     def __init__(self, days: int, max_days: int) -> None:
49:         super().__init__(f"Loan duration exceeds maximum: {days} > {max_days}")
50:         self.days = days
51:         self.max_days = max_days
52: 
53: 
54: class EquipmentUnavailable(LoanError):
55:     """Guard 3 of the failure cascade: an ORDINARY, expected outcome."""
56: 
57:     def __init__(self, tag: str) -> None:
58:         super().__init__(f"Equipment already on loan: {tag}")
59:         self.tag = tag
60: 
61: 
62: class QuotaExceeded(LoanError):
63:     def __init__(self, active: int, limit: int) -> None:
64:         super().__init__(f"Loan quota exceeded: {active} active, limit {limit}")
65:         self.active = active
66:         self.limit = limit
`````

Perintah: `nl -ba cpp/include/pinjamlab/domain/result.hpp`

`````text
1: #ifndef PINJAMLAB_DOMAIN_RESULT_HPP
2: #define PINJAMLAB_DOMAIN_RESULT_HPP
3: 
4: // Handmade tagged storage: failure never constructs T (Loan has no default).
5: 
6: #include <stdexcept>
7: #include <string>
8: #include <utility>
9: #include <new>
10: #include <type_traits>
11: 
12: namespace pinjamlab {
13: 
14: template <typename T>
15: class [[nodiscard]] Result {  // [[nodiscard]]: ignoring the return value warns
16:     bool ok_;
17:     union Storage {
18:         T value;
19:         Storage() noexcept {}
20:         ~Storage() noexcept {}
21:     } storage_;
22:     std::string error_;
23: 
24:     explicit Result(std::string e) : ok_(false), error_(std::move(e)) {}
25:     Result(T v, bool) : ok_(false) {
26:         new (&storage_.value) T(std::move(v));
27:         ok_ = true;
28:     }
29: 
30: public:
31:     static Result success(T v) { return Result(std::move(v), true); }
32:     static Result failure(std::string e) { return Result(std::move(e)); }
33: 
34:     Result(const Result& other) : ok_(false), error_(other.error_) {
35:         if (other.ok_) {
36:             new (&storage_.value) T(other.storage_.value);
37:             ok_ = true;
38:         }
39:     }
40:     Result(Result&& other) noexcept(std::is_nothrow_move_constructible_v<T>)
41:         : ok_(false), error_(std::move(other.error_)) {
42:         if (other.ok_) {
43:             new (&storage_.value) T(std::move(other.storage_.value));
44:             ok_ = true;
45:         }
46:     }
47:     Result& operator=(const Result& other) {
48:         if (this == &other) return *this;
49:         error_ = other.error_;
50:         if (ok_) { storage_.value.~T(); ok_ = false; }
51:         // Publish the tag only after construction, even when T's copy throws.
52:         if (other.ok_) {
53:             new (&storage_.value) T(other.storage_.value);
54:             ok_ = true;
55:         }
56:         return *this;
57:     }
58:     Result& operator=(Result&& other) noexcept(std::is_nothrow_move_constructible_v<T>) {
59:         if (this == &other) return *this;
60:         error_ = std::move(other.error_);
61:         if (ok_) { storage_.value.~T(); ok_ = false; }
62:         if (other.ok_) {
63:             new (&storage_.value) T(std::move(other.storage_.value));
64:             ok_ = true;
65:         }
66:         return *this;
67:     }
68:     ~Result() { if (ok_) storage_.value.~T(); }
69: 
70:     [[nodiscard]] bool ok() const noexcept { return ok_; }
71:     [[nodiscard]] const std::string& error() const noexcept { return error_; }
72: 
73:     // Reading the value of a failed Result is a PROGRAMMING error (the caller
74:     // skipped ok()), not a runtime one -- so it throws rather than returning
75:     // a default-constructed T that looks like real data.
76:     [[nodiscard]] const T& value() const {
77:         if (!ok_) throw std::logic_error("value() on a failed Result: " + error_);
78:         return storage_.value;
79:     }
80: };
81: 
82: }  // namespace pinjamlab
83: 
84: #endif  // PINJAMLAB_DOMAIN_RESULT_HPP
`````

Perintah: `nl -ba py/pinjamlab/domain/result.py`

`````text
1: """Result[T]: a small frozen dataclass. Pure domain module."""
2: from __future__ import annotations
3: 
4: from dataclasses import dataclass
5: from typing import Generic, TypeVar
6: 
7: T = TypeVar("T")
8: 
9: 
10: @dataclass(frozen=True, slots=True)
11: class Result(Generic[T]):
12:     ok: bool
13:     _value: T | None = None
14:     error: str = ""
15: 
16:     @staticmethod
17:     def success(value: T) -> "Result[T]":
18:         return Result(True, value, "")
19: 
20:     @staticmethod
21:     def failure(error: str) -> "Result[T]":
22:         return Result(False, None, error)
23: 
24:     @property
25:     def value(self) -> T:
26:         if not self.ok:
27:             raise RuntimeError(f"value on a failed Result: {self.error}")
28:         return self._value  # type: ignore[return-value]
`````

Perintah: `nl -ba cpp/include/pinjamlab/service/loan_service.hpp`

`````text
1: #ifndef PINJAMLAB_SERVICE_LOAN_SERVICE_HPP
2: #define PINJAMLAB_SERVICE_LOAN_SERVICE_HPP
3: 
4: // Orchestration only: LoanService coordinates domain objects and raises the
5: // domain's own typed exceptions. It contains no CSV parsing, no console
6: // output, and no formatting -- those belong to io/ and app/.
7: 
8: #include "pinjamlab/domain/equipment.hpp"
9: #include "pinjamlab/domain/loan.hpp"
10: #include "pinjamlab/domain/loan_error.hpp"
11: #include "pinjamlab/domain/member.hpp"
12: #include "pinjamlab/domain/result.hpp"
13: #include "pinjamlab/service/database.hpp"
14: #include "pinjamlab/service/txn_guard.hpp"
15: 
16: #include <string>
17: #include <unordered_map>
18: 
19: namespace pinjamlab {
20: 
21: class LoanService {
22: public:
23:     static constexpr int kMaxLoanDays = 90;
24: 
25:     void addEquipment(Equipment eq) {
26:         const std::string tag = eq.tag();
27:         if (!catalog_.emplace(tag, std::move(eq)).second)
28:             throw std::logic_error("Duplicate equipment: " + tag);
29:     }
30:     void addMember(Member m) {
31:         roster_.emplace(m.id(), std::move(m));
32:     }
33: 
34:     [[nodiscard]] Equipment* findEquipment(const std::string& tag) {
35:         auto it = catalog_.find(tag);
36:         return it == catalog_.end() ? nullptr : &it->second;
37:     }
38:     [[nodiscard]] Member* findMember(const std::string& id) {
39:         auto it = roster_.find(id);
40:         return it == roster_.end() ? nullptr : &it->second;
41:     }
42: 
43:     // The failure cascade, guard by guard. Every check below happens BEFORE
44:     // any mutation, so no rollback is ever needed for the current guard set
45:     // -- the TxnGuard exists for the mutation step itself, to keep the
46:     // pattern honest for the day a guard is added AFTER a mutation begins
47:     // (Module 5's database transactions are exactly that day).
48:     // Only unavailability returns failure; all other guards still throw.
49:     [[nodiscard]] Result<Loan> borrow(const std::string& tag, const std::string& memberId, int days) {
50:         auto eqIt = catalog_.find(tag);
51:         if (eqIt == catalog_.end()) {
52:             for (const auto& [known, equipment] : catalog_) {
53:                 (void)equipment;
54:                 if (known.size() != tag.size()) continue;
55:                 bool matches = true;
56:                 for (std::size_t i = 0; i < tag.size(); ++i) {
57:                     const auto fold = [](unsigned char c) { return c >= 'a' && c <= 'z' ? c - 'a' + 'A' : c; };
58:                     if (fold(tag[i]) != fold(known[i])) { matches = false; break; }
59:                 }
60:                 if (matches) throw AssetTagCaseMismatch(tag, known);
61:             }
62:             throw UnknownAssetTag(tag);
63:         }
64: 
65:         auto memIt = roster_.find(memberId);
66:         if (memIt == roster_.end()) throw UnknownMember(memberId);
67: 
68:         if (days <= 0 || days > kMaxLoanDays) throw InvalidLoanDuration(days, kMaxLoanDays);
69: 
70:         Equipment& eq = eqIt->second;
71:         Member& mem = memIt->second;
72: 
73:         if (!eq.isAvailable()) return Result<Loan>::failure(EquipmentUnavailable(tag).what());
74:         if (!eq.reservedFor().empty() && eq.reservedFor() != memberId)
75:             throw ReservationConflict(tag, eq.reservedFor());
76:         if (!mem.canBorrow()) throw QuotaExceeded(mem.activeLoans(), mem.maxLoans());
77: 
78:         TxnGuard txn(db_);
79:         mem.recordLoan();
80:         db_.stage("loan:" + memberId + ":" + tag);
81:         try {
82:             eq.markLoaned();
83:         } catch (...) {
84:             mem.undoRecordLoan();  // manual compensation: txn.commit() was
85:             throw;                 // never called, so the guard still rolls
86:         }                          // back the LEDGER on the way out.
87:         db_.stage("equipment:" + tag + ":loaned");
88:         txn.commit();
89: 
90:         owners_[tag] = memberId;
91:         return Result<Loan>::success(Loan("L-" + tag + "-" + memberId, tag, memberId, days));
92:     }
93: 
94:     void returnItem(const std::string& loanTag, const std::string& memberId) {
95:         auto eqIt = catalog_.find(loanTag);
96:         if (eqIt == catalog_.end()) throw UnknownAssetTag(loanTag);
97:         auto memIt = roster_.find(memberId);
98:         if (memIt == roster_.end()) throw UnknownMember(memberId);
99:         auto ownerIt = owners_.find(loanTag);
100:         if (ownerIt == owners_.end())
101:             throw LoanError("Equipment is not on loan: " + loanTag);
102:         if (ownerIt->second != memberId)
103:             throw LoanError("Equipment not loaned to member: " + loanTag + " for " + memberId);
104:         eqIt->second.markReturned();
105:         memIt->second.recordReturn();
106:         owners_.erase(ownerIt);
107:     }
108: 
109:     [[nodiscard]] const Database& ledger() const noexcept { return db_; }
110: 
111: private:
112:     std::unordered_map<std::string, Equipment> catalog_;
113:     std::unordered_map<std::string, Member> roster_;
114:     std::unordered_map<std::string, std::string> owners_;
115:     Database db_;
116: };
117: 
118: }  // namespace pinjamlab
119: 
120: #endif  // PINJAMLAB_SERVICE_LOAN_SERVICE_HPP
`````

Perintah: `nl -ba py/pinjamlab/service/loan_service.py`

`````text
1: """Orchestration only: LoanService coordinates domain objects and raises the
2: domain's own typed exceptions. No CSV parsing, no console output here.
3: """
4: from __future__ import annotations
5: 
6: from ..domain.equipment import Equipment
7: from ..domain.loan import Loan
8: from ..domain.loan_error import (
9:     AssetTagCaseMismatch,
10:     LoanError,
11:     ReservationConflict,
12:     EquipmentUnavailable,
13:     InvalidLoanDuration,
14:     QuotaExceeded,
15:     UnknownAssetTag,
16:     UnknownMember,
17: )
18: from ..domain.member import Member
19: from ..domain.result import Result
20: from .database import Database
21: from .txn_guard import txn_guard
22: 
23: MAX_LOAN_DAYS = 90
24: _ASCII_UPPER = str.maketrans(
25:     "abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
26: )
27: 
28: 
29: class LoanService:
30:     def __init__(self) -> None:
31:         self._catalog: dict[str, Equipment] = {}
32:         self._roster: dict[str, Member] = {}
33:         self._owners: dict[str, str] = {}
34:         self._db = Database()
35: 
36:     def add_equipment(self, equipment: Equipment) -> None:
37:         if equipment.tag in self._catalog:
38:             raise ValueError(f"Duplicate equipment: {equipment.tag}")
39:         self._catalog[equipment.tag] = equipment
40: 
41:     def reserve(self, tag: str, member_id: str) -> None:
42:         if tag not in self._catalog:
43:             raise UnknownAssetTag(tag)
44:         if member_id not in self._roster:
45:             raise UnknownMember(member_id)
46:         self._catalog[tag].reserved_for = member_id
47: 
48:     def add_member(self, member: Member) -> None:
49:         self._roster[member.member_id] = member
50: 
51:     def find_equipment(self, tag: str) -> Equipment | None:
52:         return self._catalog.get(tag)
53: 
54:     def find_member(self, member_id: str) -> Member | None:
55:         return self._roster.get(member_id)
56: 
57:     @property
58:     def ledger(self) -> Database:
59:         return self._db
60: 
61:     def borrow(self, tag: str, member_id: str, days: int) -> Result[Loan]:
62:         # Only unavailability returns failure; other guards still raise.
63:         equipment = self._catalog.get(tag)
64:         if equipment is None:
65:             for known_tag in self._catalog:
66:                 if known_tag.translate(_ASCII_UPPER) == tag.translate(_ASCII_UPPER):
67:                     raise AssetTagCaseMismatch(tag, known_tag)
68:             raise UnknownAssetTag(tag)
69: 
70:         member = self._roster.get(member_id)
71:         if member is None:
72:             raise UnknownMember(member_id)
73: 
74:         if days <= 0 or days > MAX_LOAN_DAYS:
75:             raise InvalidLoanDuration(days, MAX_LOAN_DAYS)
76: 
77:         # Checked before any mutation, same order as the C++ side:
78:         # availability, reservation, then quota.
79:         if not equipment.is_available():
80:             return Result.failure(str(EquipmentUnavailable(tag)))
81:         reserved_for = equipment.reserved_for
82:         if reserved_for and reserved_for != member_id:
83:             raise ReservationConflict(tag, reserved_for)
84:         if not member.can_borrow():
85:             raise QuotaExceeded(member.active_loans, member.max_loans)
86: 
87:         with txn_guard(self._db) as db:
88:             member.record_loan()
89:             db.stage(f"loan:{member_id}:{tag}")
90:             try:
91:                 equipment.mark_loaned()
92:             except Exception:
93:                 member.undo_record_loan()
94:                 raise
95:             db.stage(f"equipment:{tag}:loaned")
96: 
97:         self._owners[tag] = member_id
98:         return Result.success(Loan(f"L-{tag}-{member_id}", tag, member_id, days))
99: 
100:     def return_item(self, tag: str, member_id: str) -> None:
101:         equipment = self._catalog.get(tag)
102:         member = self._roster.get(member_id)
103:         if equipment is None:
104:             raise UnknownAssetTag(tag)
105:         if member is None:
106:             raise UnknownMember(member_id)
107:         if tag not in self._owners:
108:             raise LoanError(f"Equipment is not on loan: {tag}")
109:         if self._owners[tag] != member_id:
110:             raise LoanError(f"Equipment not loaned to member: {tag} for {member_id}")
111:         equipment.mark_returned()
112:         member.record_return()
113:         del self._owners[tag]
`````

Perintah: `nl -ba cpp/include/pinjamlab/app/runner.hpp`

`````text
1: #ifndef PINJAMLAB_APP_RUNNER_HPP
2: #define PINJAMLAB_APP_RUNNER_HPP
3: 
4: // app layer: the top-level handler. This is the ONE place in the codebase
5: // allowed to catch `const LoanError&` and turn it into a message a human
6: // reads, and the ONE place that decides the process exit code. It contains
7: // no business rules of its own.
8: 
9: #include "pinjamlab/domain/loan_error.hpp"
10: #include "pinjamlab/io/csv_reader.hpp"
11: #include "pinjamlab/io/report_writer.hpp"
12: #include "pinjamlab/io/validator.hpp"
13: #include "pinjamlab/service/loan_service.hpp"
14: 
15: #include <string>
16: #include <vector>
17: 
18: namespace pinjamlab {
19: 
20: struct RunResult {
21:     std::vector<std::string> rejectedLines;  // exactly what expected-output.txt holds
22:     int total = 0;
23:     int created = 0;
24:     int rejected = 0;
25:     [[nodiscard]] int exitCode() const noexcept { return rejected == 0 ? 0 : 1; }
26: };
27: 
28: // Pure of console I/O on purpose: returns the lines instead of printing them,
29: // so both the CLI (main.cpp) and the tests (test_app.cpp) can drive the same
30: // code path -- one prints to stderr, the other diffs against a golden file.
31: [[nodiscard]] inline RunResult runCatalogue(LoanService& svc, const std::string& csvPath) {
32:     CsvReader reader;
33:     Validator validator;
34:     RunResult result;
35: 
36:     const auto rows = reader.read(csvPath);
37:     result.total = static_cast<int>(rows.size());
38: 
39:     for (const auto& row : rows) {
40:         const auto validated = validator.validate(row);
41:         if (!validated.ok()) {
42:             ++result.rejected;
43:             result.rejectedLines.push_back(
44:                 ReportWriter::rejectedLine(row.lineNumber, validated.error()));
45:             continue;
46:         }
47:         const auto& req = validated.value();
48:         try {
49:             const auto borrowed = svc.borrow(req.tag, req.memberId, req.days);
50:             if (!borrowed.ok()) {
51:                 ++result.rejected;
52:                 result.rejectedLines.push_back(
53:                     ReportWriter::rejectedLine(row.lineNumber, borrowed.error()));
54:                 continue;
55:             }
56:             ++result.created;
57:         } catch (const AssetTagCaseMismatch& e) {
58:             ++result.rejected;
59:             result.rejectedLines.push_back(ReportWriter::rejectedLine(
60:                 row.lineNumber, "Unknown asset tag: " + e.given() +
61:                 " (did you mean " + e.suggestion() + "?)"));
62:         } catch (const LoanError& e) {  // the family we understand
63:             ++result.rejected;
64:             result.rejectedLines.push_back(
65:                 ReportWriter::rejectedLine(row.lineNumber, e.what()));
66:         }
67:         // Anything that is NOT a LoanError is left to travel: we do not know
68:         // what it is, so we are not entitled to decide it is unimportant.
69:     }
70:     return result;
71: }
72: 
73: }  // namespace pinjamlab
74: 
75: #endif  // PINJAMLAB_APP_RUNNER_HPP
`````

Perintah: `nl -ba py/pinjamlab/app/runner.py`

`````text
1: """app layer: the top-level handler. This is the ONE place allowed to catch
2: `LoanError` and turn it into a message a human reads, and the ONE place that
3: decides the process exit code.
4: """
5: from __future__ import annotations
6: 
7: from dataclasses import dataclass, field
8: 
9: from ..domain.loan_error import (
10:     AssetTagCaseMismatch, LoanError, ReservationConflict,
11: )
12: from ..io.csv_reader import CsvReader
13: from ..io.report_writer import ReportWriter
14: from ..io.validator import Validator
15: from ..service.loan_service import LoanService
16: 
17: 
18: @dataclass
19: class RunResult:
20:     rejected_lines: list[str] = field(default_factory=list)
21:     total: int = 0
22:     created: int = 0
23:     rejected: int = 0
24: 
25:     @property
26:     def exit_code(self) -> int:
27:         return 0 if self.rejected == 0 else 1
28: 
29: 
30: def run_catalogue(svc: LoanService, csv_path: str) -> RunResult:
31:     reader = CsvReader()
32:     validator = Validator()
33:     result = RunResult()
34: 
35:     rows = reader.read(csv_path)
36:     result.total = len(rows)
37: 
38:     for row in rows:
39:         validated = validator.validate(row)
40:         if not validated.ok:
41:             result.rejected += 1
42:             result.rejected_lines.append(
43:                 ReportWriter.rejected_line(row.line_number, validated.error))
44:             continue
45:         req = validated.value
46:         try:
47:             borrowed = svc.borrow(req.tag, req.member_id, req.days)
48:             if not borrowed.ok:
49:                 result.rejected += 1
50:                 result.rejected_lines.append(
51:                     ReportWriter.rejected_line(row.line_number, borrowed.error))
52:                 continue
53:             result.created += 1
54:         except AssetTagCaseMismatch as e:
55:             result.rejected += 1
56:             result.rejected_lines.append(ReportWriter.rejected_line(
57:                 row.line_number,
58:                 f"Unknown asset tag: {e.given} (did you mean {e.suggestion}?)"))
59:         except ReservationConflict as e:
60:             result.rejected += 1
61:             result.rejected_lines.append(ReportWriter.rejected_line(
62:                 row.line_number,
63:                 f"Equipment reserved: {e.tag} for {e.reserved_for}"))
64:         except LoanError as e:  # the family we understand
65:             result.rejected += 1
66:             result.rejected_lines.append(
67:                 ReportWriter.rejected_line(row.line_number, str(e)))
68:         # Anything that is NOT a LoanError is left to travel.
69: 
70:     return result
`````

Perintah: `nl -ba cpp/include/pinjamlab/service/txn_guard.hpp`

`````text
1: #ifndef PINJAMLAB_SERVICE_TXN_GUARD_HPP
2: #define PINJAMLAB_SERVICE_TXN_GUARD_HPP
3: 
4: // From-scratch primitive: an RAII transaction guard. The constructor
5: // acquires (begin()); the destructor releases (rollback()) UNLESS commit()
6: // was called first. That pairing is RAII, and it is what makes borrow()
7: // exception-safe with zero try/catch of its own -- Figure "Stack Unwinding"
8: // is doing the actual work; this class only wires it to a resource.
9: 
10: #include "pinjamlab/service/database.hpp"
11: 
12: #include <iostream>
13: 
14: namespace pinjamlab {
15: 
16: class TxnGuard {
17:     Database& db_;
18:     bool committed_ = false;
19: 
20: public:
21:     explicit TxnGuard(Database& db) : db_(db) { db_.begin(); }  // acquire
22: 
23:     // Rule of Five: a guard must not be copied -- two guards, one transaction.
24:     TxnGuard(const TxnGuard&) = delete;
25:     TxnGuard& operator=(const TxnGuard&) = delete;
26:     TxnGuard(TxnGuard&&) = delete;
27:     TxnGuard& operator=(TxnGuard&&) = delete;
28: 
29:     void commit() {
30:         db_.commit();
31:         committed_ = true;
32:     }
33: 
34:     ~TxnGuard() noexcept {  // noexcept: destructors must NOT throw
35:         if (committed_) return;
36:         try {
37:             db_.rollback();  // released on EVERY path that did not commit
38:         } catch (...) {
39:             // Swallowing is correct HERE and almost nowhere else: throwing
40:             // from a destructor during unwinding calls std::terminate().
41:             std::cerr << "rollback failed during unwind\n";
42:         }
43:     }
44: };
45: 
46: }  // namespace pinjamlab
47: 
48: #endif  // PINJAMLAB_SERVICE_TXN_GUARD_HPP
`````

Perintah: `nl -ba py/pinjamlab/service/txn_guard.py`

`````text
1: """The @contextmanager equivalent of service/txn_guard.hpp's RAII guard.
2: 
3: Everything before `yield` is acquisition; everything after is release. The
4: `raise` in the except clause is essential -- without it this would silently
5: swallow every exception from the body, which is the defect Lab 2 asks you
6: to find in the wild.
7: """
8: from __future__ import annotations
9: 
10: import sys
11: from collections.abc import Iterator
12: from contextlib import contextmanager
13: 
14: from .database import Database
15: 
16: 
17: @contextmanager
18: def txn_guard(db: Database) -> Iterator[Database]:
19:     db.begin()  # acquire
20:     try:
21:         yield db  # the body of the `with` runs here
22:     except Exception:
23:         try:
24:             db.rollback()  # released on the exception path
25:         except Exception:
26:             # Swallowing here is correct, and almost nowhere else: an
27:             # exception escaping __exit__ during unwinding would replace
28:             # the original exception instead of adding to it.
29:             print("rollback failed during unwind", file=sys.stderr)
30:         raise  # ...and the error keeps travelling
31:     else:
32:         db.commit()  # released on the success path
`````

Perintah: `nl -ba cpp/include/pinjamlab/service/database.hpp`

`````text
1: #ifndef PINJAMLAB_SERVICE_DATABASE_HPP
2: #define PINJAMLAB_SERVICE_DATABASE_HPP
3: 
4: // A minimal in-memory stand-in for persistence. Real durability (SQLite)
5: // arrives in Module 5; here "the database" is just enough state -- a staged
6: // list and a committed list -- to demonstrate begin/commit/rollback
7: // honestly, and to give TxnGuard something real to guard.
8: 
9: #include <string>
10: #include <vector>
11: 
12: namespace pinjamlab {
13: 
14: class Database {
15:     std::vector<std::string> committed_;
16:     std::vector<std::string> pending_;
17: 
18: public:
19:     void begin() { pending_.clear(); }
20:     void stage(std::string record) { pending_.push_back(std::move(record)); }
21: 
22:     void commit() {
23:         for (auto& r : pending_) committed_.push_back(std::move(r));
24:         pending_.clear();
25:     }
26: 
27:     void rollback() { pending_.clear(); }
28: 
29:     [[nodiscard]] const std::vector<std::string>& committed() const noexcept { return committed_; }
30:     [[nodiscard]] std::size_t pendingCount() const noexcept { return pending_.size(); }
31: };
32: 
33: }  // namespace pinjamlab
34: 
35: #endif  // PINJAMLAB_SERVICE_DATABASE_HPP
`````

Perintah: `nl -ba py/pinjamlab/service/database.py`

`````text
1: """A minimal in-memory stand-in for persistence -- the Python twin of
2: service/database.hpp. Real durability (SQLite) arrives in Module 5.
3: """
4: from __future__ import annotations
5: 
6: 
7: class Database:
8:     def __init__(self) -> None:
9:         self._committed: list[str] = []
10:         self._pending: list[str] = []
11: 
12:     def begin(self) -> None:
13:         self._pending.clear()
14: 
15:     def stage(self, record: str) -> None:
16:         self._pending.append(record)
17: 
18:     def commit(self) -> None:
19:         self._committed.extend(self._pending)
20:         self._pending.clear()
21: 
22:     def rollback(self) -> None:
23:         self._pending.clear()
24: 
25:     @property
26:     def committed(self) -> list[str]:
27:         return list(self._committed)
28: 
29:     @property
30:     def pending_count(self) -> int:
31:         return len(self._pending)
`````

Perintah: `nl -ba cpp/include/pinjamlab/io/report_writer.hpp`

`````text
1: #ifndef PINJAMLAB_IO_REPORT_WRITER_HPP
2: #define PINJAMLAB_IO_REPORT_WRITER_HPP
3: 
4: // io layer: the ONLY place that knows what a report line looks like. app/
5: // calls these formatters instead of building strings itself, so the exact
6: // wording (which expected-output.txt pins byte-for-byte) lives in one place.
7: 
8: #include <sstream>
9: #include <filesystem>
10: #include <fstream>
11: #include <cstdlib>
12: #include <stdexcept>
13: #include <utility>
14: #include <vector>
15: #include <unistd.h>
16: #include <string>
17: 
18: namespace pinjamlab {
19: 
20: // The destination is untouched until commit; the temporary lives beside it
21: // so the rename is atomic on the destination filesystem.
22: class ScopedReportFile {
23:     std::filesystem::path destination_, temporary_;
24:     std::ofstream output_;
25:     bool committed_ = false;
26: public:
27:     explicit ScopedReportFile(std::filesystem::path destination)
28:         : destination_(std::move(destination)) {
29:         const auto pattern = destination_.string() + ".tmp.XXXXXX";
30:         std::vector<char> name(pattern.begin(), pattern.end());
31:         name.push_back('\0');
32:         const int fd = ::mkstemp(name.data());
33:         if (fd == -1) throw std::runtime_error("cannot create report temporary: " + destination_.string());
34:         ::close(fd);
35:         try {
36:             temporary_ = name.data();
37:             output_.exceptions(std::ios::failbit | std::ios::badbit);
38:             output_.open(temporary_, std::ios::binary | std::ios::trunc);
39:         } catch (...) {
40:             std::error_code ignored;
41:             std::filesystem::remove(name.data(), ignored);
42:             throw;
43:         }
44:     }
45:     ScopedReportFile(const ScopedReportFile&) = delete;
46:     ScopedReportFile& operator=(const ScopedReportFile&) = delete;
47:     ~ScopedReportFile() noexcept {
48:         try { if (output_.is_open()) output_.close(); } catch (...) {}
49:         if (!committed_) {
50:             std::error_code ignored;
51:             std::filesystem::remove(temporary_, ignored);
52:         }
53:     }
54:     [[nodiscard]] std::ostream& stream() noexcept { return output_; }
55:     [[nodiscard]] const std::filesystem::path& temporaryPath() const noexcept { return temporary_; }
56:     void commit() {
57:         if (committed_) throw std::logic_error("report already committed");
58:         output_.flush();
59:         output_.close();
60:         std::filesystem::rename(temporary_, destination_);
61:         committed_ = true;
62:     }
63: };
64: 
65: class ReportWriter {
66: public:
67:     [[nodiscard]] static std::string rejectedLine(int rowNumber, const std::string& message) {
68:         std::ostringstream os;
69:         os << "row " << rowNumber << ": " << message;
70:         return os.str();
71:     }
72: 
73:     [[nodiscard]] static std::string summary(int total, int created, int rejected) {
74:         std::ostringstream os;
75:         os << "Processed " << total << " rows.\n"
76:            << created << " loans created, " << rejected << " rejected.";
77:         return os.str();
78:     }
79: };
80: 
81: }  // namespace pinjamlab
82: 
83: #endif  // PINJAMLAB_IO_REPORT_WRITER_HPP
`````

Perintah: `nl -ba py/pinjamlab/io/atomic_writer.py`

`````text
1: """Publish a text file only after its guarded write succeeds."""
2: from collections.abc import Iterator
3: from contextlib import contextmanager
4: import os
5: from pathlib import Path
6: import tempfile
7: from typing import TextIO
8: 
9: 
10: @contextmanager
11: def atomic_writer(path: str | Path) -> Iterator[TextIO]:
12:     destination = Path(path)
13:     temporary = None
14:     try:
15:         with tempfile.NamedTemporaryFile(
16:             mode="w", encoding="utf-8", newline="",
17:             dir=destination.parent, prefix=f".{destination.name}.",
18:             suffix=".tmp", delete=False,
19:         ) as handle:
20:             temporary = Path(handle.name)
21:             yield handle
22:         os.replace(temporary, destination)
23:     finally:
24:         if temporary is not None:
25:             temporary.unlink(missing_ok=True)
`````

Perintah: `nl -ba py/pinjamlab/io/report_writer.py`

`````text
1: """io layer: the ONLY place that knows what a report line looks like."""
2: from __future__ import annotations
3: 
4: 
5: class ReportWriter:
6:     @staticmethod
7:     def rejected_line(row_number: int, message: str) -> str:
8:         return f"row {row_number}: {message}"
9: 
10:     @staticmethod
11:     def summary(total: int, created: int, rejected: int) -> str:
12:         return f"Processed {total} rows.\n{created} loans created, {rejected} rejected."
`````

Perintah: `cat docs/evidence/reconstructed/03-defect-A-green.log`

`````text
............                                                             [100%]
12 passed in 4.46s
`````

Perintah: `cat docs/evidence/reconstructed/04-asan-before-status.txt`

`````text
exit=23
`````

Perintah: `cat docs/evidence/reconstructed/04-asan-before.stdout`

`````text

`````

Perintah: `cat docs/evidence/reconstructed/04-asan-before.stderr`

`````text
row 1: Loan quota exceeded: 2 active, limit 2

=================================================================
==57877==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 72 byte(s) in 1 object(s) allocated from:
    #0 0x76419a72c73f in operator new(unsigned long) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:109
    #1 0x000000406ba0 in rules(Request const&, std::map<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, bool, std::less<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::allocator<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const, bool> > >&, std::map<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, Member, std::less<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::allocator<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const, Member> > >&) ~/loanbench/bin/reconstructed/pinjamlab.cpp:53
    #2 0x000000407d17 in main ~/loanbench/bin/reconstructed/pinjamlab.cpp:67
    #3 0x764199e2a600  (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a600) (BuildId: 066527e430a32768d82741e00b81eebb1a872294)
    #4 0x764199e2a717 in __libc_start_main (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a717) (BuildId: 066527e430a32768d82741e00b81eebb1a872294)
    #5 0x000000405c34 in _start (~/loanbench/bin/reconstructed/bin/reconstructed_asan+0x405c34) (BuildId: d4076c717018ec3d9f652ed1c6b5e83cc3f660e3)

SUMMARY: AddressSanitizer: 72 byte(s) leaked in 1 allocation(s).
`````

Perintah: `cat docs/evidence/reconstructed/05-asan-after-status.txt`

`````text
exit=1
`````

Perintah: `cat docs/evidence/reconstructed/05-asan-after.stdout`

`````text

`````

Perintah: `cat docs/evidence/reconstructed/05-asan-after.stderr`

`````text
row 1: Loan quota exceeded: 2 active, limit 2
`````

Perintah: `git log --all --date=iso-strict --format="%H %ad %cd %s" -- cpp/include/pinjamlab/domain/result.hpp cpp/include/pinjamlab/service/loan_service.hpp; git diff 5b26936 ce8bec3 -- cpp/include/pinjamlab/domain/result.hpp cpp/include/pinjamlab/service/loan_service.hpp cpp/include/pinjamlab/app/runner.hpp cpp/include/pinjamlab/app/seed.hpp py/pinjamlab/service/loan_service.py py/pinjamlab/app/runner.py py/pinjamlab/app/seed.py`

`````text
STDOUT:
ce8bec3c830cfb1c8880453ff084a3aa62c6ac84 2026-11-12T14:02:31+07:00 2026-11-12T14:02:31+07:00 docs: add Module 3 documentation and lab materials for exception handling and modularity
5f8fc2991faeba364fa00a17db982dff2855da05 2026-11-12T13:25:18+07:00 2026-11-12T13:25:18+07:00 feat: add typed failures and robust boundary cleanup
a0aececdada5d7f4a7622f462ae5d6700f2c8bc7 2026-11-12T11:41:08+07:00 2026-11-12T11:41:08+07:00 feat: initialize loanbench project with C++ and Python implementations
diff --git a/cpp/include/pinjamlab/app/runner.hpp b/cpp/include/pinjamlab/app/runner.hpp
index 73c0512..fffe4a7 100644
--- a/cpp/include/pinjamlab/app/runner.hpp
+++ b/cpp/include/pinjamlab/app/runner.hpp
@@ -46,7 +46,13 @@ struct RunResult {
         }
         const auto& req = validated.value();
         try {
-            (void)svc.borrow(req.tag, req.memberId, req.days);
+            const auto borrowed = svc.borrow(req.tag, req.memberId, req.days);
+            if (!borrowed.ok()) {
+                ++result.rejected;
+                result.rejectedLines.push_back(
+                    ReportWriter::rejectedLine(row.lineNumber, borrowed.error()));
+                continue;
+            }
             ++result.created;
         } catch (const AssetTagCaseMismatch& e) {
             ++result.rejected;
diff --git a/cpp/include/pinjamlab/app/seed.hpp b/cpp/include/pinjamlab/app/seed.hpp
index 7bfd648..e30a123 100644
--- a/cpp/include/pinjamlab/app/seed.hpp
+++ b/cpp/include/pinjamlab/app/seed.hpp
@@ -35,9 +35,12 @@ inline void seedPinjamLab(LoanService& svc) {
 
     // Sequenced through the real borrow() path rather than poked directly,
     // so the seed itself exercises the same invariants the CSV rows do.
-    (void)svc.borrow("LP-002", "M-103", 5);   // LP-002 -> Loaned; M-103 -> 1 active
-    (void)svc.borrow("SEED-01", "M-102", 5);  // M-102 -> 1 active
-    (void)svc.borrow("SEED-02", "M-102", 5);  // M-102 -> 2 active == limit
+    if (const auto r = svc.borrow("LP-002", "M-103", 5); !r.ok())
+        throw std::logic_error(r.error());
+    if (const auto r = svc.borrow("SEED-01", "M-102", 5); !r.ok())
+        throw std::logic_error(r.error());
+    if (const auto r = svc.borrow("SEED-02", "M-102", 5); !r.ok())
+        throw std::logic_error(r.error());
 }
 
 }  // namespace pinjamlab
diff --git a/cpp/include/pinjamlab/domain/result.hpp b/cpp/include/pinjamlab/domain/result.hpp
index 7907c9d..ffb5478 100644
--- a/cpp/include/pinjamlab/domain/result.hpp
+++ b/cpp/include/pinjamlab/domain/result.hpp
@@ -1,27 +1,71 @@
 #ifndef PINJAMLAB_DOMAIN_RESULT_HPP
 #define PINJAMLAB_DOMAIN_RESULT_HPP
 
-// From-scratch primitive (~15 lines of actual logic): no std::optional,
-// no std::expected, no library type. Pure domain header.
+// Handmade tagged storage: failure never constructs T (Loan has no default).
 
 #include <stdexcept>
 #include <string>
 #include <utility>
+#include <new>
+#include <type_traits>
 
 namespace pinjamlab {
 
 template <typename T>
 class [[nodiscard]] Result {  // [[nodiscard]]: ignoring the return value warns
     bool ok_;
-    T value_{};
+    union Storage {
+        T value;
+        Storage() noexcept {}
+        ~Storage() noexcept {}
+    } storage_;
     std::string error_;
 
-    Result(bool ok, T v, std::string e)
-        : ok_(ok), value_(std::move(v)), error_(std::move(e)) {}
+    explicit Result(std::string e) : ok_(false), error_(std::move(e)) {}
+    Result(T v, bool) : ok_(false) {
+        new (&storage_.value) T(std::move(v));
+        ok_ = true;
+    }
 
 public:
-    static Result success(T v) { return Result(true, std::move(v), ""); }
-    static Result failure(std::string e) { return Result(false, T{}, std::move(e)); }
+    static Result success(T v) { return Result(std::move(v), true); }
+    static Result failure(std::string e) { return Result(std::move(e)); }
+
+    Result(const Result& other) : ok_(false), error_(other.error_) {
+        if (other.ok_) {
+            new (&storage_.value) T(other.storage_.value);
+            ok_ = true;
+        }
+    }
+    Result(Result&& other) noexcept(std::is_nothrow_move_constructible_v<T>)
+        : ok_(false), error_(std::move(other.error_)) {
+        if (other.ok_) {
+            new (&storage_.value) T(std::move(other.storage_.value));
+            ok_ = true;
+        }
+    }
+    Result& operator=(const Result& other) {
+        if (this == &other) return *this;
+        error_ = other.error_;
+        if (ok_) { storage_.value.~T(); ok_ = false; }
+        // Publish the tag only after construction, even when T's copy throws.
+        if (other.ok_) {
+            new (&storage_.value) T(other.storage_.value);
+            ok_ = true;
+        }
+        return *this;
+    }
+    Result& operator=(Result&& other) noexcept(std::is_nothrow_move_constructible_v<T>) {
+        if (this == &other) return *this;
+        error_ = std::move(other.error_);
+        if (ok_) { storage_.value.~T(); ok_ = false; }
+        if (other.ok_) {
+            new (&storage_.value) T(std::move(other.storage_.value));
+            ok_ = true;
+        }
+        return *this;
+    }
+    ~Result() { if (ok_) storage_.value.~T(); }
 
     [[nodiscard]] bool ok() const noexcept { return ok_; }
     [[nodiscard]] const std::string& error() const noexcept { return error_; }
@@ -31,7 +75,7 @@ public:
     // a default-constructed T that looks like real data.
     [[nodiscard]] const T& value() const {
         if (!ok_) throw std::logic_error("value() on a failed Result: " + error_);
-        return value_;
+        return storage_.value;
     }
 };
 
diff --git a/cpp/include/pinjamlab/service/loan_service.hpp b/cpp/include/pinjamlab/service/loan_service.hpp
index ddcc852..6e18bfa 100644
--- a/cpp/include/pinjamlab/service/loan_service.hpp
+++ b/cpp/include/pinjamlab/service/loan_service.hpp
@@ -9,6 +9,7 @@
 #include "pinjamlab/domain/loan.hpp"
 #include "pinjamlab/domain/loan_error.hpp"
 #include "pinjamlab/domain/member.hpp"
+#include "pinjamlab/domain/result.hpp"
 #include "pinjamlab/service/database.hpp"
 #include "pinjamlab/service/txn_guard.hpp"
 
@@ -44,7 +45,8 @@ public:
     // -- the TxnGuard exists for the mutation step itself, to keep the
     // pattern honest for the day a guard is added AFTER a mutation begins
     // (Module 5's database transactions are exactly that day).
-    [[nodiscard]] Loan borrow(const std::string& tag, const std::string& memberId, int days) {
+    // Only unavailability returns failure; all other guards still throw.
+    [[nodiscard]] Result<Loan> borrow(const std::string& tag, const std::string& memberId, int days) {
         auto eqIt = catalog_.find(tag);
         if (eqIt == catalog_.end()) {
             for (const auto& [known, equipment] : catalog_) {
@@ -68,7 +70,7 @@ public:
         Equipment& eq = eqIt->second;
         Member& mem = memIt->second;
 
-        if (!eq.isAvailable()) throw EquipmentUnavailable(tag);
+        if (!eq.isAvailable()) return Result<Loan>::failure(EquipmentUnavailable(tag).what());
         if (!eq.reservedFor().empty() && eq.reservedFor() != memberId)
             throw ReservationConflict(tag, eq.reservedFor());
         if (!mem.canBorrow()) throw QuotaExceeded(mem.activeLoans(), mem.maxLoans());
@@ -86,7 +88,7 @@ public:
         txn.commit();
 
         owners_[tag] = memberId;
-        return Loan("L-" + tag + "-" + memberId, tag, memberId, days);
+        return Result<Loan>::success(Loan("L-" + tag + "-" + memberId, tag, memberId, days));
     }
 
     void returnItem(const std::string& loanTag, const std::string& memberId) {
diff --git a/py/pinjamlab/app/runner.py b/py/pinjamlab/app/runner.py
index 0ea036b..1a1e875 100644
--- a/py/pinjamlab/app/runner.py
+++ b/py/pinjamlab/app/runner.py
@@ -44,7 +44,12 @@ def run_catalogue(svc: LoanService, csv_path: str) -> RunResult:
             continue
         req = validated.value
         try:
-            svc.borrow(req.tag, req.member_id, req.days)
+            borrowed = svc.borrow(req.tag, req.member_id, req.days)
+            if not borrowed.ok:
+                result.rejected += 1
+                result.rejected_lines.append(
+                    ReportWriter.rejected_line(row.line_number, borrowed.error))
+                continue
             result.created += 1
         except AssetTagCaseMismatch as e:
             result.rejected += 1
diff --git a/py/pinjamlab/app/seed.py b/py/pinjamlab/app/seed.py
index 5207424..2762702 100644
--- a/py/pinjamlab/app/seed.py
+++ b/py/pinjamlab/app/seed.py
@@ -21,6 +21,9 @@ def seed_pinjamlab(svc: LoanService) -> None:
     svc.add_member(Member("M-102", "Budi Santoso", Role.STUDENT))
     svc.add_member(Member("M-103", "Citra Dewi", Role.STUDENT))
 
-    svc.borrow("LP-002", "M-103", 5)   # LP-002 -> Loaned; M-103 -> 1 active
-    svc.borrow("SEED-01", "M-102", 5)  # M-102 -> 1 active
-    svc.borrow("SEED-02", "M-102", 5)  # M-102 -> 2 active == limit
+    if not (result := svc.borrow("LP-002", "M-103", 5)).ok:
+        raise RuntimeError(result.error)
+    if not (result := svc.borrow("SEED-01", "M-102", 5)).ok:
+        raise RuntimeError(result.error)
+    if not (result := svc.borrow("SEED-02", "M-102", 5)).ok:
+        raise RuntimeError(result.error)
diff --git a/py/pinjamlab/service/loan_service.py b/py/pinjamlab/service/loan_service.py
index 446e8f4..4747443 100644
--- a/py/pinjamlab/service/loan_service.py
+++ b/py/pinjamlab/service/loan_service.py
@@ -16,6 +16,7 @@ from ..domain.loan_error import (
     UnknownMember,
 )
 from ..domain.member import Member
+from ..domain.result import Result
 from .database import Database
 from .txn_guard import txn_guard
 
@@ -57,7 +58,8 @@ class LoanService:
     def ledger(self) -> Database:
         return self._db
 
-    def borrow(self, tag: str, member_id: str, days: int) -> Loan:
+    def borrow(self, tag: str, member_id: str, days: int) -> Result[Loan]:
+        # Only unavailability returns failure; other guards still raise.
         equipment = self._catalog.get(tag)
         if equipment is None:
             for known_tag in self._catalog:
@@ -75,7 +77,7 @@ class LoanService:
         # Checked before any mutation, same order as the C++ side:
         # availability, reservation, then quota.
         if not equipment.is_available():
-            raise EquipmentUnavailable(tag)
+            return Result.failure(str(EquipmentUnavailable(tag)))
         reserved_for = equipment.reserved_for
         if reserved_for and reserved_for != member_id:
             raise ReservationConflict(tag, reserved_for)
@@ -93,7 +95,7 @@ class LoanService:
             db.stage(f"equipment:{tag}:loaned")
 
         self._owners[tag] = member_id
-        return Loan(f"L-{tag}-{member_id}", tag, member_id, days)
+        return Result.success(Loan(f"L-{tag}-{member_id}", tag, member_id, days))
 
     def return_item(self, tag: str, member_id: str) -> None:
         equipment = self._catalog.get(tag)

STDERR:

exit=0; durasi_detik=0.012
`````

Perintah: `git log --all --date=iso-strict --format="%H %ad %cd %s" -- pinjamlab.cpp pinjamlab.py test_reconstructed.py RECONSTRUCTION.md; git diff 0c004e1 0f0ccad -- pinjamlab.cpp pinjamlab.py; git diff 0f0ccad 67780d9 -- pinjamlab.cpp`

`````text
STDOUT:
33c2ad53232eff8eb7006dca64e1e00d2e998fd0 2026-11-12T13:02:58+07:00 2026-11-12T13:02:58+07:00 docs: clarify observed fixture and Python path exceptions
67780d98515464f510ba10d04d40e48b7ef4be03 2026-11-12T13:02:14+07:00 2026-11-12T13:02:14+07:00 fix: own Loan with unique_ptr across quota exceptions
0f0ccadbaf32930cf46b531cd76715edd9b6751b 2026-11-12T13:00:50+07:00 2026-11-12T13:00:50+07:00 fix: report application errors and return nonzero
0c004e1dbb9cc6f9e581d635e5fe91f1db343368 2026-11-12T12:57:29+07:00 2026-11-12T12:57:29+07:00 test: failing test exposes swallowed errors
6ca6c7b0fc01bf58087ec740859ed7d20f06d02e 2026-11-12T12:55:56+07:00 2026-11-12T12:55:56+07:00 chore: reconstruct deliberately defective teaching baseline
diff --git a/pinjamlab.cpp b/pinjamlab.cpp
index 52fbd67..cdebddb 100644
--- a/pinjamlab.cpp
+++ b/pinjamlab.cpp
@@ -60,13 +60,20 @@ int main(int argc, char** argv) {
     if (argc != 2) { std::cerr << "usage: pinjamlab INPUT.csv\n"; return 2; }
     std::map<std::string, bool> equipment{{"LP-001", true}, {"LP-002", false}, {"LP-003", true}};
     std::map<std::string, Member> members{{"M-101", {0}}, {"M-102", {2}}, {"M-103", {1}}};
+    bool failed = false;
     try {
         for (const auto& r : parse(argv[1])) {
             try {
                 rules(r, equipment, members);
                 print(r);
-            } catch (...) {} // Deliberately defective teaching baseline A.
+            } catch (const std::exception& error) {
+                std::cerr << "row " << r.row << ": " << error.what() << '\n';
+                failed = true;
+            }
         }
-    } catch (...) {} // Deliberately defective teaching baseline A.
-    return 0;
+    } catch (const std::exception& error) {
+        std::cerr << error.what() << '\n';
+        failed = true;
+    }
+    return failed ? 1 : 0;
 }
diff --git a/pinjamlab.py b/pinjamlab.py
index 3f3ca95..2de6221 100644
--- a/pinjamlab.py
+++ b/pinjamlab.py
@@ -6,8 +6,8 @@ import sys
 
 @dataclass
 class Loan:
-    tag: str
-    member: str
+    tag: st
+    member: st
     days: int
 
 @dataclass
@@ -62,15 +62,19 @@ def main(argv):
         return 2
     equipment = {"LP-001": True, "LP-002": False, "LP-003": True}
     members = {"M-101": Member(0), "M-102": Member(2), "M-103": Member(1)}
+    failed = False
     try:
         for row, fields in parse(argv[1]):
             try:
                 print_loan(row, rules(fields, equipment, members))
-            except:  # Deliberately defective teaching baseline A.
-                pass
-    except:  # Deliberately defective teaching baseline A.
-        pass
-    return 0
+            except Exception as error:
+                print(f"row {row}: {error}", file=sys.stderr)
+                failed = True
+    except Exception as error:
+        message = f"cannot open input: {argv[1]}" if isinstance(error, OSError) else str(error)
+        print(message, file=sys.stderr)
+        failed = True
+    return 1 if failed else 0
 
 if __name__ == "__main__":
     sys.exit(main(sys.argv))
diff --git a/pinjamlab.cpp b/pinjamlab.cpp
index cdebddb..1891bff 100644
--- a/pinjamlab.cpp
+++ b/pinjamlab.cpp
@@ -2,6 +2,7 @@
 #include <fstream>
 #include <iostream>
 #include <map>
+#include <memory>
 #include <regex>
 #include <sstream>
 #include <stdexcept>
@@ -49,11 +50,10 @@ void rules(const Request& r, std::map<std::string, bool>& equipment, std::map<st
     if (!members.count(r.member)) throw std::runtime_error("Unknown member: " + r.member);
     if (days > 90) throw std::runtime_error("Loan duration exceeds maximum: " + std::to_string(days) + " > 90");
     if (!equipment.at(r.tag)) throw std::runtime_error("Equipment already on loan: " + r.tag);
-    // Deliberately defective teaching baseline B: quota throws before delete.
-    Loan* loan = new Loan{r.tag, r.member, days};
+    // Scoped ownership releases the Loan when recordLoan throws quota.
+    auto loan = std::make_unique<Loan>(Loan{r.tag, r.member, days});
     members.at(r.member).recordLoan();
     equipment.at(r.tag) = false;
-    delete loan;
 }
 void print(const Request& r) { std::cout << "row " << r.row << ": loan created: " << r.tag << '\n'; }
 int main(int argc, char** argv) {

STDERR:

exit=0; durasi_detik=0.014
`````

Perintah: `.venv/bin/python -m pytest bin/analisis-export/red/test_reconstructed.py -v --import-mode=importlib`

`````text
STDOUT:
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.2.0, pluggy-1.7.0 -- ~/loanbench/.venv/bin/python
rootdir: ~/loanbench
collecting ... collected 12 items

bin/analisis-export/red/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[cpp-LP-999,M-101,7-Unknown asset tag: LP-999] FAILED [  8%]
bin/analisis-export/red/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[cpp-LP-003,M-102,7-Loan quota exceeded: 2 active, limit 2] FAILED [ 16%]
bin/analisis-export/red/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[cpp-LP-001,M-101,abc-days is not a number: abc] FAILED [ 25%]
bin/analisis-export/red/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[python-LP-999,M-101,7-Unknown asset tag: LP-999] FAILED [ 33%]
bin/analisis-export/red/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[python-LP-003,M-102,7-Loan quota exceeded: 2 active, limit 2] FAILED [ 41%]
bin/analisis-export/red/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[python-LP-001,M-101,abc-days is not a number: abc] FAILED [ 50%]
bin/analisis-export/red/test_reconstructed.py::test_missing_input_exact_message_and_nonzero[cpp] FAILED [ 58%]
bin/analisis-export/red/test_reconstructed.py::test_missing_input_exact_message_and_nonzero[python] FAILED [ 66%]
bin/analisis-export/red/test_reconstructed.py::test_valid_request[cpp] PASSED [ 75%]
bin/analisis-export/red/test_reconstructed.py::test_valid_request[python] PASSED [ 83%]
bin/analisis-export/red/test_reconstructed.py::test_ten_errors_match_main_golden[cpp] FAILED [ 91%]
bin/analisis-export/red/test_reconstructed.py::test_ten_errors_match_main_golden[python] FAILED [100%]

=================================== FAILURES ===================================
_ test_rejected_row_exact_message_and_nonzero[cpp-LP-999,M-101,7-Unknown asset tag: LP-999] _

command = ['~/loanbench/bin/analisis-export/red/bin/reconstructed_cli']
tmp_path = PosixPath('~/loanbench/bin/analisis-export/pytest-tmp/test_rejected_row_exact_messag0')
fields = 'LP-999,M-101,7', message = 'Unknown asset tag: LP-999'

    @pytest.mark.parametrize("fields,message", [
        ("LP-999,M-101,7", "Unknown asset tag: LP-999"),
        ("LP-003,M-102,7", "Loan quota exceeded: 2 active, limit 2"),
        ("LP-001,M-101,abc", "days is not a number: abc"),
    ])
    def test_rejected_row_exact_message_and_nonzero(command, tmp_path, fields, message):
        source = tmp_path / "request.csv"
        source.write_text("tag,memberId,days\n" + fields + "\n")
        result = subprocess.run(command + [str(source)], capture_output=True, text=True)
>       assert (result.stderr, result.returncode, result.stdout) == (f"row 1: {message}\n", 1, "")
E       AssertionError: assert ('', 0, '') == ('row 1: Unkn...999\n', 1, '')
E         
E         At index 0 diff: '' != 'row 1: Unknown asset tag: LP-999\n'
E         
[... total 286 baris; lengkap bin/analisis-export/command-014.txt ...]
E         
E         ...Full output truncated, use '-vv' to show

bin/analisis-export/red/test_reconstructed.py:44: AssertionError
__________________ test_ten_errors_match_main_golden[python] ___________________

command = ['~/loanbench/.venv/bin/python', '~/loanbench/bin/analisis-export/red/pinjamlab.py']

    def test_ten_errors_match_main_golden(command):
        result = subprocess.run(command + [str(ROOT / "sample-data/bad-requests.csv")], capture_output=True, text=True)
        expected = Path("~/loanbench/sample-data/expected-output.txt").read_text()
>       assert (result.stderr, result.returncode, result.stdout) == (expected, 1, "")
E       AssertionError: assert ('', 0, '') == ('row 1: tag ... 90\n', 1, '')
E         
E         At index 0 diff: '' != 'row 1: tag is empty\nrow 2: memberId is empty\nrow 3: days is not a number: abc\nrow 4: days must be positive, got -3\nrow 5: days must be positive, got 0\nrow 6: Unknown asset tag: LP-999\nrow 7: Unknown member: M-404\nrow 8: Equipment already on loan: LP-002\nrow 9: Loan quota exceeded: 2 active, limit 2\nrow 10: Loan duration exceeds maximum: 400 > 90\n'
E         
E         Full diff: (-: missing in left side, +: extra in left side)
E           (
E         +     '',
E         -     'row 1: tag is empty\n'...
E         
E         ...Full output truncated, use '-vv' to show

bin/analisis-export/red/test_reconstructed.py:44: AssertionError
=========================== short test summary info ============================
FAILED bin/analisis-export/red/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[cpp-LP-999,M-101,7-Unknown asset tag: LP-999]
FAILED bin/analisis-export/red/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[cpp-LP-003,M-102,7-Loan quota exceeded: 2 active, limit 2]
FAILED bin/analisis-export/red/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[cpp-LP-001,M-101,abc-days is not a number: abc]
FAILED bin/analisis-export/red/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[python-LP-999,M-101,7-Unknown asset tag: LP-999]
FAILED bin/analisis-export/red/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[python-LP-003,M-102,7-Loan quota exceeded: 2 active, limit 2]
FAILED bin/analisis-export/red/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[python-LP-001,M-101,abc-days is not a number: abc]
FAILED bin/analisis-export/red/test_reconstructed.py::test_missing_input_exact_message_and_nonzero[cpp]
FAILED bin/analisis-export/red/test_reconstructed.py::test_missing_input_exact_message_and_nonzero[python]
FAILED bin/analisis-export/red/test_reconstructed.py::test_ten_errors_match_main_golden[cpp]
FAILED bin/analisis-export/red/test_reconstructed.py::test_ten_errors_match_main_golden[python]
========================= 10 failed, 2 passed in 3.71s =========================

STDERR:

exit=1; durasi_detik=4.018
`````

Perintah: `.venv/bin/python -m pytest bin/analisis-export/green/test_reconstructed.py -v --import-mode=importlib`

`````text
STDOUT:
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.2.0, pluggy-1.7.0 -- ~/loanbench/.venv/bin/python
rootdir: ~/loanbench
collecting ... collected 12 items

bin/analisis-export/green/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[cpp-LP-999,M-101,7-Unknown asset tag: LP-999] PASSED [  8%]
bin/analisis-export/green/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[cpp-LP-003,M-102,7-Loan quota exceeded: 2 active, limit 2] PASSED [ 16%]
bin/analisis-export/green/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[cpp-LP-001,M-101,abc-days is not a number: abc] PASSED [ 25%]
bin/analisis-export/green/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[python-LP-999,M-101,7-Unknown asset tag: LP-999] PASSED [ 33%]
bin/analisis-export/green/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[python-LP-003,M-102,7-Loan quota exceeded: 2 active, limit 2] PASSED [ 41%]
bin/analisis-export/green/test_reconstructed.py::test_rejected_row_exact_message_and_nonzero[python-LP-001,M-101,abc-days is not a number: abc] PASSED [ 50%]
bin/analisis-export/green/test_reconstructed.py::test_missing_input_exact_message_and_nonzero[cpp] PASSED [ 58%]
bin/analisis-export/green/test_reconstructed.py::test_missing_input_exact_message_and_nonzero[python] PASSED [ 66%]
bin/analisis-export/green/test_reconstructed.py::test_valid_request[cpp] PASSED [ 75%]
bin/analisis-export/green/test_reconstructed.py::test_valid_request[python] PASSED [ 83%]
bin/analisis-export/green/test_reconstructed.py::test_ten_errors_match_main_golden[cpp] PASSED [ 91%]
bin/analisis-export/green/test_reconstructed.py::test_ten_errors_match_main_golden[python] PASSED [100%]

============================== 12 passed in 3.74s ==============================

STDERR:

exit=0; durasi_detik=4.061
`````

Run ulang A: salinan otomatis git show 0c004e1/0f0ccad/67780d9 dari pinjamlab.cpp,pinjamlab.py,test_reconstructed.py,sample-data/bad-requests.csv tanpa edit ke bin/analisis-export/red/green/fixed-b,subdir bin. Test golden absolut historis bukan cleanclone. quota.csv literal header tag,memberId,days dan LP-003,M-102,7. ASan awal-O1-Werror gagal headerregexGCC log016/018,run127017/019 binarybelumada,bukan leak. Ulang-O0:

Perintah: `g++ -std=c++20 -Wall -Wextra -Werror -g -O0 -fno-omit-frame-pointer -fsanitize=address -fno-pie -no-pie bin/analisis-export/green/pinjamlab.cpp -o bin/analisis-export/green/bin/asan`

`````text
STDOUT:

STDERR:

exit=0; durasi_detik=5.024
`````

Perintah: `ASAN_OPTIONS=detect_leaks=1:halt_on_error=1:exitcode=23 bin/analisis-export/green/bin/asan bin/analisis-export/quota.csv`

`````text
STDOUT:

STDERR:
row 1: Loan quota exceeded: 2 active, limit 2

=================================================================
==106032==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 72 byte(s) in 1 object(s) allocated from:
    #0 0x77c4dbd2c73f in operator new(unsigned long) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:109
    #1 0x000000406ba0 in rules(Request const&, std::map<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, bool, std::less<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::allocator<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const, bool> > >&, std::map<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, Member, std::less<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::allocator<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const, Member> > >&) bin/analisis-export/green/pinjamlab.cpp:53
    #2 0x000000407d17 in main bin/analisis-export/green/pinjamlab.cpp:67
    #3 0x77c4db42a600  (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a600) (BuildId: 066527e430a32768d82741e00b81eebb1a872294)
    #4 0x77c4db42a717 in __libc_start_main (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a717) (BuildId: 066527e430a32768d82741e00b81eebb1a872294)
    #5 0x000000405c34 in _start (~/loanbench/bin/analisis-export/green/bin/asan+0x405c34) (BuildId: 5df05007edde02e05a6cc415d2e5330ecb6e09f2)

SUMMARY: AddressSanitizer: 72 byte(s) leaked in 1 allocation(s).

exit=23; durasi_detik=0.042
`````

Perintah: `g++ -std=c++20 -Wall -Wextra -Werror -g -O0 -fno-omit-frame-pointer -fsanitize=address -fno-pie -no-pie bin/analisis-export/fixed-b/pinjamlab.cpp -o bin/analisis-export/fixed-b/bin/asan`

`````text
STDOUT:

STDERR:

exit=0; durasi_detik=4.942
`````

Perintah: `ASAN_OPTIONS=detect_leaks=1:halt_on_error=1:exitcode=23 bin/analisis-export/fixed-b/bin/asan bin/analisis-export/quota.csv`

`````text
STDOUT:

STDERR:
row 1: Loan quota exceeded: 2 active, limit 2

exit=1; durasi_detik=0.020
`````

Perintah: `git show 0c004e1:test_reconstructed.py`

`````text
"""Subprocess contracts shared by both standalone reconstructions."""
from pathlib import Path
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parent

@pytest.fixture(scope="session")
def cpp():
    target = ROOT / "bin" / "reconstructed_cli"
    subprocess.run(["g++", "-std=c++20", "-Wall", "-Wextra", "-Werror", str(ROOT / "pinjamlab.cpp"), "-o", str(target)], check=True)
    return [str(target)]

@pytest.fixture(params=["cpp", "python"])
def command(request, cpp):
    return cpp if request.param == "cpp" else [sys.executable, str(ROOT / "pinjamlab.py")]

@pytest.mark.parametrize("fields,message", [
    ("LP-999,M-101,7", "Unknown asset tag: LP-999"),
    ("LP-003,M-102,7", "Loan quota exceeded: 2 active, limit 2"),
    ("LP-001,M-101,abc", "days is not a number: abc"),
])
def test_rejected_row_exact_message_and_nonzero(command, tmp_path, fields, message):
    source = tmp_path / "request.csv"
    source.write_text("tag,memberId,days\n" + fields + "\n")
    result = subprocess.run(command + [str(source)], capture_output=True, text=True)
    assert (result.stderr, result.returncode, result.stdout) == (f"row 1: {message}\n", 1, "")

def test_missing_input_exact_message_and_nonzero(command, tmp_path):
    path = str(tmp_path / "missing.csv")
    result = subprocess.run(command + [path], capture_output=True, text=True)
    assert (result.stderr, result.returncode, result.stdout) == (f"cannot open input: {path}\n", 1, "")

def test_valid_request(command, tmp_path):
    source = tmp_path / "valid.csv"
    source.write_text("tag,memberId,days\nLP-001,M-101,7\n")
    result = subprocess.run(command + [str(source)], capture_output=True, text=True)
    assert (result.stdout, result.stderr, result.returncode) == ("row 1: loan created: LP-001\n", "", 0)

def test_ten_errors_match_main_golden(command):
    result = subprocess.run(command + [str(ROOT / "sample-data/bad-requests.csv")], capture_output=True, text=True)
    expected = Path("~/loanbench/sample-data/expected-output.txt").read_text()
    assert (result.stderr, result.returncode, result.stdout) == (expected, 1, "")
`````

Perintah: `git show 0f0ccad:pinjamlab.cpp`

`````text
// Reconstructed teaching baseline, not the missing original m3-start.
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
struct Request { int row; std::string tag, member, days; };
struct Loan { std::string tag, member; int days; };
struct Member {
    int active;
    void recordLoan() {
        if (active >= 2) throw std::runtime_error("Loan quota exceeded: " + std::to_string(active) + " active, limit 2");
        ++active;
    }
};
std::vector<Request> parse(const std::string& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open input: " + path);
    std::vector<Request> rows;
    std::string line;
    std::getline(input, line);
    int row = 0;
    while (std::getline(input, line)) {
        ++row;
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (line.empty()) continue;
        std::istringstream fields(line);
        Request r{row, {}, {}, {}};
        std::getline(fields, r.tag, ',');
        std::getline(fields, r.member, ',');
        std::getline(fields, r.days, ',');
        rows.push_back(r);
    }
    return rows;
}
void rules(const Request& r, std::map<std::string, bool>& equipment, std::map<std::string, Member>& members) {
    if (r.tag.empty()) throw std::runtime_error("tag is empty");
    if (r.member.empty()) throw std::runtime_error("memberId is empty");
    int days;
    try {
        if (!std::regex_match(r.days, std::regex("[+-]?[0-9]+"))) throw std::invalid_argument("integer");
        days = std::stoi(r.days);
    } catch (const std::exception&) { throw std::runtime_error("days is not a number: " + r.days); }
    if (days <= 0) throw std::runtime_error("days must be positive, got " + std::to_string(days));
    if (!equipment.count(r.tag)) throw std::runtime_error("Unknown asset tag: " + r.tag);
    if (!members.count(r.member)) throw std::runtime_error("Unknown member: " + r.member);
    if (days > 90) throw std::runtime_error("Loan duration exceeds maximum: " + std::to_string(days) + " > 90");
    if (!equipment.at(r.tag)) throw std::runtime_error("Equipment already on loan: " + r.tag);
    // Deliberately defective teaching baseline B: quota throws before delete.
    Loan* loan = new Loan{r.tag, r.member, days};
    members.at(r.member).recordLoan();
    equipment.at(r.tag) = false;
    delete loan;
}
void print(const Request& r) { std::cout << "row " << r.row << ": loan created: " << r.tag << '\n'; }
int main(int argc, char** argv) {
    if (argc != 2) { std::cerr << "usage: pinjamlab INPUT.csv\n"; return 2; }
    std::map<std::string, bool> equipment{{"LP-001", true}, {"LP-002", false}, {"LP-003", true}};
    std::map<std::string, Member> members{{"M-101", {0}}, {"M-102", {2}}, {"M-103", {1}}};
    bool failed = false;
    try {
        for (const auto& r : parse(argv[1])) {
            try {
                rules(r, equipment, members);
                print(r);
            } catch (const std::exception& error) {
                std::cerr << "row " << r.row << ": " << error.what() << '\n';
                failed = true;
            }
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        failed = true;
    }
    return failed ? 1 : 0;
}
`````

Perintah: `git show 67780d9:pinjamlab.cpp`

`````text
// Reconstructed teaching baseline, not the missing original m3-start.
#include <fstream>
#include <iostream>
#include <map>
#include <memory>
#include <regex>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
struct Request { int row; std::string tag, member, days; };
struct Loan { std::string tag, member; int days; };
struct Member {
    int active;
    void recordLoan() {
        if (active >= 2) throw std::runtime_error("Loan quota exceeded: " + std::to_string(active) + " active, limit 2");
        ++active;
    }
};
std::vector<Request> parse(const std::string& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open input: " + path);
    std::vector<Request> rows;
    std::string line;
    std::getline(input, line);
    int row = 0;
    while (std::getline(input, line)) {
        ++row;
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (line.empty()) continue;
        std::istringstream fields(line);
        Request r{row, {}, {}, {}};
        std::getline(fields, r.tag, ',');
        std::getline(fields, r.member, ',');
        std::getline(fields, r.days, ',');
        rows.push_back(r);
    }
    return rows;
}
void rules(const Request& r, std::map<std::string, bool>& equipment, std::map<std::string, Member>& members) {
    if (r.tag.empty()) throw std::runtime_error("tag is empty");
    if (r.member.empty()) throw std::runtime_error("memberId is empty");
    int days;
    try {
        if (!std::regex_match(r.days, std::regex("[+-]?[0-9]+"))) throw std::invalid_argument("integer");
        days = std::stoi(r.days);
    } catch (const std::exception&) { throw std::runtime_error("days is not a number: " + r.days); }
    if (days <= 0) throw std::runtime_error("days must be positive, got " + std::to_string(days));
    if (!equipment.count(r.tag)) throw std::runtime_error("Unknown asset tag: " + r.tag);
    if (!members.count(r.member)) throw std::runtime_error("Unknown member: " + r.member);
    if (days > 90) throw std::runtime_error("Loan duration exceeds maximum: " + std::to_string(days) + " > 90");
    if (!equipment.at(r.tag)) throw std::runtime_error("Equipment already on loan: " + r.tag);
    // Scoped ownership releases the Loan when recordLoan throws quota.
    auto loan = std::make_unique<Loan>(Loan{r.tag, r.member, days});
    members.at(r.member).recordLoan();
    equipment.at(r.tag) = false;
}
void print(const Request& r) { std::cout << "row " << r.row << ": loan created: " << r.tag << '\n'; }
int main(int argc, char** argv) {
    if (argc != 2) { std::cerr << "usage: pinjamlab INPUT.csv\n"; return 2; }
    std::map<std::string, bool> equipment{{"LP-001", true}, {"LP-002", false}, {"LP-003", true}};
    std::map<std::string, Member> members{{"M-101", {0}}, {"M-102", {2}}, {"M-103", {1}}};
    bool failed = false;
    try {
        for (const auto& r : parse(argv[1])) {
            try {
                rules(r, equipment, members);
                print(r);
            } catch (const std::exception& error) {
                std::cerr << "row " << r.row << ": " << error.what() << '\n';
                failed = true;
            }
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        failed = true;
    }
    return failed ? 1 : 0;
}
`````

## §5 Lab 3

Provenans: 5b26936 menyimpan prediction dan merupakan ancestor HEAD ce8bec3; implementasi Result yang dibandingkan ada di commit sesudahnya. Ini mendukung urutan rekaman Git, bukan bukti independen siapa yang menulis atau waktu ketikan sebenarnya. Tidak ada identitas mahasiswa yang dikarang, dan tidak ada commit prediction baru pada sesi ini.

Graf before berlabel baseline standalone DIREKONSTRUKSI, tidak menyatakan struktur starter asli. Graf after berasal dependency include/import lokal, bukan runtime call graph. Daftar edge aktual berikut dihitung dari sumber HEAD, bukan hanya salinan gambar.

| Strategi | Pemakaian nyata | Cleanup / konsekuensi |
|---|---|---|
| Result | Validator dan unavailable borrow | Pemanggil harus cek ok; tidak unwind otomatis |
| Exception bertipe | Lookup, durasi, reservasi, kuota | Handler family di runner; field spesifik bila perlu |
| RAII C++ | TxnGuard, ScopedReportFile | Destruktor saat keluar scope; rollback ledger / hapus temporary |
| with Python | txn_guard, atomic_writer | Commit normal; rollback Exception untuk txn; finally untuk atomic |
| Boundary fatal | CLI menangkap kegagalan proses | stderr dan exit nonzero, bukan sukses palsu |

Matriks di atas analisis dossier, bukan deliverable mandiri. `docs/strategy_matrix.md`, `docs/cleanup_matrix.md` dan `docs/peer_reproduction_checklist.md`: TIDAK ADA; nama path matriks ini label pemeriksaan, bukan klaim nama wajib rubrik. Cleanup assert rinci §7. Clone bersih sesi ini TIDAK DILAKUKAN; hasil checklist rekan TIDAK ADA. Reproduksi yang benar-benar dilakukan adalah runner pada worktree saat ini. README penuh berikut dipertahankan apa adanya, tidak ditulis ulang menjadi klaim mahasiswa; angka test, Windows/Python 3.12, ketiadaan node/fixture dan ASan di README sudah kedaluwarsa untuk HEAD/WSL saat ini.

Perintah: `cat PREDICTION.md`

`````text
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
`````

Perintah: `cat docs/prediction_outcome.md`

`````text
# Prediction Outcome

> DRAF: evidence-backed implementation notes, not a claim of independently authored student reflection. Rewrite the personal interpretation in your own words before submission. PREDICTION.md remains frozen.

Comparison base: commit `5b26936`. The prediction was 20 changed call-site expressions out of 48, including all 8 production sites. The measured result is **23 changed enclosing call-site source lines out of the original 48**, including **all 8 production sites**. Thus the usage-change prediction was low by 3, while the production prediction was exact.

## Counting Method

Run `python3 scripts/audit_result_calls.py`. It reads baseline sources with `git show 5b26936:<path>`, identifies Python attribute-call AST nodes and cleaned C++ `.borrow(` occurrences, and compares exact enclosing source lines with the working tree using SequenceMatcher. Each original expression contributes once. The complete per-call inventory is `docs/evidence/result_changed_callsites.txt`.

This is a usage-change metric, not an argument-change metric: strictly counting only the text of the `svc.borrow(...)` invocation gives **0 changed invocations**. Calls now sit inside assignments, explicit checks, or value extraction instead. This distinction matters because the prediction used the ambiguous phrase "expressions need text changes." No count is inflated by newly added tests.

| Scope | Original calls | Changed enclosing usage |
| --- | ---: | ---: |
| C++ production | 4 | 4 |
| Python production | 4 | 4 |
| C++ tests | 21 | 7 |
| Python tests | 19 | 8 |
| Total | 48 | 23 |

The unchanged 25 call-site lines test errors which still throw. Two of those unchanged calls are loops whose unavailable case was removed from the input table; the surrounding test behavior changed without changing its call expression. Those are deliberately not counted as changed call-site lines.

All six seed calls changed text and explicitly check success; none are merely asserted away or left ignored. Both runner calls also check the Result before counting a created loan. Seed unavailability raises a programming/setup error; runner unavailability produces the existing rejection message and continues.

## Current Inventory

`bash scripts/count_callsites.sh` now reports 52 expressions in cpp/py: 48 originals plus four new calls in test-only wrappers and equivalence tests. `docs/evidence/result_callsites.txt` captures that inventory; `result_production_callsites.txt` separately records the 8 production calls. Root limits demos contain no service borrow calls and do not affect the comparison.

## Observed Outcome

Unavailability is an ordinary branch at the runner; it no longer needs to travel by exception. However the runner already caught the entire LoanError family before this refactor, so there was no dedicated EquipmentUnavailable catch to remove. The runner actually grows an explicit branch. The benefit is visible expected-outcome handling, not fewer lines or the disappearance of exception handling. Unknown tag/member, case mismatch, duration, reservation and quota remain typed exceptions.

The old fixed ten-row CSV and golden are unchanged. The new CSV has one header and exactly five data rows; both CLI implementations match the C++-generated new golden and exit 1. Full test names and results are in `result_full_run.txt`; all C++ suites and error paths pass sanitizers in `result_asan.txt`. These runs used Python 3.14.4 in the existing venv, not Python 3.12; no 3.12 run is claimed.
`````

Perintah: `cat scripts/check_dependencies.py`

`````text
#!/usr/bin/env python3
"""Check inward layer dependencies and domain I/O purity without importing code."""
import argparse
import ast
import posixpath
import re
from pathlib import Path

LAYERS = ("domain", "io", "service", "app")
FORBIDDEN = {"domain": {"io", "service", "app"}, "io": {"service", "app"},
             "service": {"app"}, "app": set()}
CPP_SUFFIXES = {".h", ".hpp", ".hh", ".hxx", ".cpp", ".cc", ".cxx"}
CPP_IO = {"fstream", "iostream", "sstream", "cstdio", "stdio.h", "filesystem", "unistd.h"}
PY_IO = {"csv", "sys", "io", "os", "pathlib", "tempfile", "socket", "subprocess", "shutil"}

def cpp_clean(text, strings=False):
    # Preserve newlines so diagnostics and callsite locations remain physical lines.
    pattern = r'R"([^ ()\\\t\r\n]*)\([\s\S]*?\)\1"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/'
    return re.sub(pattern, lambda m: re.sub(r"[^\n]", " ", m[0])
                  if strings or m[0].startswith(("//", "/*")) else m[0], text)

def python_imports(tree, module, package=False):
    parent = module.split(".") if package else module.split(".")[:-1]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield node.lineno, alias.name
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                base = ".".join(parent[:len(parent) - node.level + 1] + ([base] if base else []))
            for alias in node.names:
                yield node.lineno, base + ("." + alias.name if alias.name != "*" else "")

def source_files(root):
    for base, language in ((root / "cpp/include/pinjamlab", "cpp"),
                           (root / "cpp/app", "cpp"), (root / "py/pinjamlab", "py")):
        if not base.is_dir():
            raise ValueError(f"missing source directory: {base}")
        for path in sorted(base.rglob("*")):
            if path.is_file() and path.suffix in (CPP_SUFFIXES if language == "cpp" else {".py"}):
                yield language, path

def inspect(root):
    edges, violations = [], []
    for language, path in source_files(root):
        relative = path.relative_to(root).as_posix()
        parts = relative.split("/")
        source_layer = "app" if relative.startswith("cpp/app/") else parts[3 if language == "cpp" else 2]
        if source_layer not in LAYERS:
            continue
        text = path.read_text(encoding="utf-8")
        dependencies = []
        if language == "py":
            module_parts = list(path.relative_to(root / "py").with_suffix("").parts)
            package = module_parts[-1] == "__init__"
            if package:
                module_parts.pop()
            try:
                tree = ast.parse(text, filename=relative)
            except SyntaxError as error:
                violations.append(f"{relative}:{error.lineno}: invalid Python: {error.msg}")
                continue
            imports = list(python_imports(tree, ".".join(module_parts), package))
            for line, name in imports:
                bits = name.split(".")
                if len(bits) > 1 and bits[0] == "pinjamlab" and bits[1] in LAYERS:
                    dependencies.append((line, bits[1], name))
                elif source_layer == "domain" and bits[0] in PY_IO:
                    violations.append(f"{relative}:{line}: domain I/O import: {name}")
            if source_layer == "domain":
                aliases = {}
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        aliases.update((a.asname or a.name, a.name) for a in node.names)
                    elif isinstance(node, ast.ImportFrom):
                        aliases.update((a.asname or a.name, (node.module or "") + "." + a.name) for a in node.names)
                for node in ast.walk(tree):
                    if not isinstance(node, ast.Call):
                        continue
                    name = ast.unparse(node.func)
                    head, _, tail = name.partition(".")
                    name = aliases.get(head, head) + ("." + tail if tail else "")
                    if name in {"print", "open", "input", "builtins.print", "builtins.open", "builtins.input"} or name.rsplit(".", 1)[-1] in {"open", "read_text", "write_text", "read_bytes", "write_bytes"}:
                        violations.append(f"{relative}:{node.lineno}: domain I/O call: {name}")
        else:
            clean = cpp_clean(text)
            for match in re.finditer(r'^\s*#\s*include\s*[<"]([^>"\n]+)[>"]', clean, re.MULTILINE):
                name = match[1]
                line = clean.count("\n", 0, match.start(1)) + 1
                if name.startswith("pinjamlab/"):
                    target = name.split("/")
                elif (path.parent / name).is_file() or name.startswith(("../", "./", "domain/", "io/", "service/", "app/")):
                    target = posixpath.normpath(posixpath.join(posixpath.dirname(relative), name)).split("/")
                    target = target[target.index("pinjamlab"):] if "pinjamlab" in target else []
                else:
                    target = []
                if len(target) > 1 and target[1] in LAYERS:
                    dependencies.append((line, target[1], name))
                if source_layer == "domain" and (name in CPP_IO or "csv" in name.lower()):
                    violations.append(f"{relative}:{line}: domain I/O include: {name}")
            if source_layer == "domain":
                for match in re.finditer(r'\bstd\s*::\s*(?:cout|cerr|clog|cin|wcout|wcerr|wclog|wcin)\b|\b(?:printf|fprintf|fopen|freopen|puts|scanf)\s*\(|\bcsv\b', cpp_clean(text, strings=True), re.IGNORECASE):
                    violations.append(f"{relative}:{text.count(chr(10), 0, match.start()) + 1}: domain I/O: {match[0]}")
        for line, target, name in dependencies:
            edges.append((language, relative, source_layer, target, name, line))
            if target in FORBIDDEN[source_layer]:
                violations.append(f"{relative}:{line}: forbidden {source_layer} -> {target}: {name}")
    return sorted(set(edges)), sorted(set(violations))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        edges, violations = inspect(args.root.resolve())
    except (OSError, ValueError) as error:
        print(f"Dependency gate error: {error}")
        return 2
    if violations:
        print("\n".join(violations))
        print(f"FAIL: {len(violations)} dependency/purity violation(s)")
        return 1
    print(f"PASS: dependency directions and domain I/O purity ({len(edges)} local dependencies)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
`````

Perintah: `cat py/tests/test_dependency_gate.py`

`````text
"""Exercise the real gate against isolated source copies, never live sources."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "scripts/check_dependencies.py"
DIRECTIONS = [("domain", "io"), ("domain", "service"), ("domain", "app"),
              ("io", "service"), ("io", "app"), ("service", "app")]

@pytest.fixture
def source_copy():
    (ROOT / "bin").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dependency-gate-", dir=ROOT / "bin") as directory:
        root = Path(directory)
        for source in ("cpp/include/pinjamlab", "cpp/app", "py/pinjamlab"):
            shutil.copytree(ROOT / source, root / source, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        yield root

def run_gate(root):
    return subprocess.run([sys.executable, str(GATE), str(root)], capture_output=True, text=True)

def test_real_sources_pass():
    result = run_gate(ROOT)
    assert result.returncode == 0, result.stdout + result.stderr

@pytest.mark.parametrize("source,target", DIRECTIONS)
@pytest.mark.parametrize("language", ["cpp", "py"])
def test_each_forbidden_direction(source_copy, source, target, language):
    if language == "cpp":
        path = source_copy / "cpp/include/pinjamlab" / source / "gate_probe.hpp"
        text = f'#include "pinjamlab/{target}/gate_probe.hpp"\n'
    else:
        path = source_copy / "py/pinjamlab" / source / "gate_probe.py"
        text = f"from ..{target} import gate_probe\n"
    path.write_text(text, encoding="utf-8")
    result = run_gate(source_copy)
    assert result.returncode == 1, result.stdout + result.stderr
    assert f"forbidden {source} -> {target}" in result.stdout
    print(f"REJECTED {language} {source} -> {target}: {result.stdout.strip()}")

@pytest.mark.parametrize("language,text", [
    ("py", "def hidden():\n    import csv as c\n"),
    ("py", "from builtins import open as op\nop('file')\n"),
    ("py", "print('forbidden')\n"),
    ("cpp", "#include <fstream>\n"),
    ("cpp", "void probe() { std::cout << 1; }\n"),
])
def test_domain_io_rejected(source_copy, language, text):
    base = "py/pinjamlab/domain" if language == "py" else "cpp/include/pinjamlab/domain"
    path = source_copy / base / ("gate_probe.py" if language == "py" else "gate_probe.hpp")
    path.write_text(text, encoding="utf-8")
    result = run_gate(source_copy)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "domain I/O" in result.stdout

def test_comments_and_strings_are_not_dependencies(source_copy):
    (source_copy / "py/pinjamlab/domain/gate_probe.py").write_text(
        '# import csv\ntext = "print(open())"\n', encoding="utf-8")
    (source_copy / "cpp/include/pinjamlab/domain/gate_probe.hpp").write_text(
        '/* #include "pinjamlab/app/runner.hpp" */\n// std::cout\nconst char* text = "csv std::cout";\n', encoding="utf-8")
    result = run_gate(source_copy)
    assert result.returncode == 0, result.stdout + result.stderr
`````

Perintah: `cat docs/graphs/after-cpp-layers.mmd`

`````text
%% Actual cross-layer include/import dependencies
%% Arrow: source --> dependency
flowchart LR
    n0["app"]
    n1["domain"]
    n2["io"]
    n3["service"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n2 --> n1
    n3 --> n1
`````

Perintah: `cat docs/graphs/after-cpp.mmd`

`````text
%% Actual local include/import dependencies
%% Arrow: source --> dependency
flowchart LR
    n0["cpp/app/main.cpp"]
    n1["cpp/include/pinjamlab/app/runner.hpp"]
    n2["cpp/include/pinjamlab/app/seed.hpp"]
    n3["cpp/include/pinjamlab/domain/equipment.hpp"]
    n4["cpp/include/pinjamlab/domain/loan.hpp"]
    n5["cpp/include/pinjamlab/domain/loan_error.hpp"]
    n6["cpp/include/pinjamlab/domain/member.hpp"]
    n7["cpp/include/pinjamlab/domain/result.hpp"]
    n8["cpp/include/pinjamlab/io/csv_reader.hpp"]
    n9["cpp/include/pinjamlab/io/report_writer.hpp"]
    n10["cpp/include/pinjamlab/io/validator.hpp"]
    n11["cpp/include/pinjamlab/service/database.hpp"]
    n12["cpp/include/pinjamlab/service/loan_service.hpp"]
    n13["cpp/include/pinjamlab/service/txn_guard.hpp"]
    n0 --> n1
    n0 --> n2
    n1 --> n5
    n1 --> n8
    n1 --> n9
    n1 --> n10
    n1 --> n12
    n2 --> n3
    n2 --> n6
    n2 --> n12
    n3 --> n5
    n6 --> n5
    n10 --> n7
    n10 --> n8
    n12 --> n3
    n12 --> n4
    n12 --> n5
    n12 --> n6
    n12 --> n11
    n12 --> n13
    n13 --> n11
`````

Perintah: `cat docs/graphs/after-py-layers.mmd`

`````text
%% Actual cross-layer include/import dependencies
%% Arrow: source --> dependency
flowchart LR
    n0["app"]
    n1["domain"]
    n2["io"]
    n3["service"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n2 --> n1
    n3 --> n1
`````

Perintah: `cat docs/graphs/after-py.mmd`

`````text
%% Actual local include/import dependencies
%% Arrow: source --> dependency
flowchart LR
    n0["py/pinjamlab/app/main.py"]
    n1["py/pinjamlab/app/runner.py"]
    n2["py/pinjamlab/app/seed.py"]
    n3["py/pinjamlab/domain/equipment.py"]
    n4["py/pinjamlab/domain/loan.py"]
    n5["py/pinjamlab/domain/loan_error.py"]
    n6["py/pinjamlab/domain/member.py"]
    n7["py/pinjamlab/domain/result.py"]
    n8["py/pinjamlab/io/csv_reader.py"]
    n9["py/pinjamlab/io/report_writer.py"]
    n10["py/pinjamlab/io/validator.py"]
    n11["py/pinjamlab/service/database.py"]
    n12["py/pinjamlab/service/loan_service.py"]
    n13["py/pinjamlab/service/txn_guard.py"]
    n0 --> n1
    n0 --> n2
    n0 --> n9
    n0 --> n12
    n1 --> n5
    n1 --> n8
    n1 --> n9
    n1 --> n10
    n1 --> n12
    n2 --> n3
    n2 --> n6
    n2 --> n12
    n3 --> n5
    n6 --> n5
    n10 --> n7
    n10 --> n8
    n12 --> n3
    n12 --> n4
    n12 --> n5
    n12 --> n6
    n12 --> n11
    n12 --> n13
    n13 --> n11
`````

Perintah: `cat docs/graphs/before-cpp.mmd`

`````text
%% Measured standalone reconstructed baseline: bin/reconstructed/pinjamlab.cpp
%% Arrow: source --> dependency
flowchart LR
    n0["fstream"]
    n1["iostream"]
    n2["map"]
    n3["memory"]
    n4["pinjamlab.cpp"]
    n5["regex"]
    n6["sstream"]
    n7["stdexcept"]
    n8["string"]
    n9["vector"]
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n4 --> n9
`````

Perintah: `cat docs/graphs/before-py.mmd`

`````text
%% Measured standalone reconstructed baseline: bin/reconstructed/pinjamlab.py
%% Arrow: source --> dependency
flowchart LR
    n0["csv"]
    n1["dataclasses.dataclass"]
    n2["pinjamlab.py"]
    n3["re"]
    n4["sys"]
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
`````

Perintah: `cat README.md`

`````text
# PinjamLab Module 3 — Error Handling & Modular Programming

Part of **Laboratorium Pemrograman II** (`25MP7716G014`), S1 Informatika,
Universitas Muhammadiyah Surabaya. Extends the same repository as Modules 1–2.

## Unit verification table

| Unit / test file | Language | Concept verified | Outcome |
|---|---|---|---|
| `cpp/tests/test_errors.cpp` | C++20 | Every `LoanError` subclass, catch-order/precision, a successful borrow | **8 passed** |
| `cpp/tests/test_raii.cpp` | C++20 | `TxnGuard` commits, rolls back on normal exit, rolls back on the throwing path; wired into `LoanService` | **4 passed** |
| `cpp/tests/test_result.cpp` | C++20 | `Result<T>` factories, `value()` throws on failure, the from-scratch match against a throwing twin | **5 passed** |
| `cpp/tests/test_app.cpp` | C++20 | The full pipeline reproduces `expected-output.txt` byte for byte | **1 passed** |
| `py/tests/test_errors.py` | Python 3.12 | Same 5 failure modes, same catch-family guarantee | **8 passed** |
| `py/tests/test_cleanup.py` | Python 3.12 | `txn_guard` context manager releases on every exit path, incl. raising | **4 passed** |
| `py/tests/test_result.py` | Python 3.12 | `Result` + the from-scratch match | **7 passed** |
| `py/tests/test_app.py` | Python 3.12 | The full pipeline matches the SAME `expected-output.txt` as C++ | **1 passed** |

**18 C++ test cases + 20 Python tests.**

## One command

```bash
./run_tests.sh
```

Five steps, and **the script fails (non-zero exit) if any of them does**:

1. **The dependency-rule purity check** — greps `domain/` in both languages
   for io/console tokens outside a comment. `domain/` may not include,
   import, or name anything from `io`, `service` or `app`.
2. Build the C++ suites at `-Wall -Wextra -Werror`.
3. Run the C++ suites.
4. **Cross-language golden file** — run the compiled C++ CLI against
   `sample-data/bad-requests.csv` and diff its stderr against
   `sample-data/expected-output.txt`.
5. Run the Python suite (which independently re-checks the same golden file).

Unlike Module 1's script, this one (like Module 2's) treats a missing
toolchain, a failed diff, or a purity violation as a hard failure — never a
`[SUCCESS]` banner over a step that did not run.

## The ten rows, ten failures, one rule each

`sample-data/bad-requests.csv` is fixed and committed. Every row triggers
exactly one failure, and the two implementations must produce the identical
message, in order, on stderr, exit code 1:

| Row | CSV content | Rejected by | Message |
|---|---|---|---|
| 1 | `,M-101,7` | Validator (io) | `tag is empty` |
| 2 | `LP-001,,7` | Validator (io) | `memberId is empty` |
| 3 | `LP-001,M-101,abc` | Validator (io) | `days is not a number: abc` |
| 4 | `LP-001,M-101,-3` | Validator (io) | `days must be positive, got -3` |
| 5 | `LP-001,M-101,0` | Validator (io) | `days must be positive, got 0` |
| 6 | `LP-999,M-101,7` | domain | `Unknown asset tag: LP-999` |
| 7 | `LP-001,M-404,7` | domain | `Unknown member: M-404` |
| 8 | `LP-002,M-101,7` | domain | `Equipment already on loan: LP-002` |
| 9 | `LP-003,M-102,7` | domain | `Loan quota exceeded: 2 active, limit 2` |
| 10 | `LP-001,M-101,400` | domain | `Loan duration exceeds maximum: 400 > 90` |

Rows 1–5 never reach `domain` — the io-layer `Validator` returns a
`Result<LoanRequest>` and rejects them at the boundary. Rows 6–10 are
business-rule failures raised as typed `LoanError` subclasses and caught once,
centrally, in `app/runner.hpp`'s row loop.

**The seed state these rows depend on** (`app/seed.hpp` / `app/seed.py`),
because the failures for rows 8 and 9 require specific starting conditions:

| Entity | State before row 1 runs | Why |
|---|---|---|
| `LP-001` | Available | rows 7, 10 need it available so their OWN rule is what fails |
| `LP-002` | **Loaned** (to `M-103`) | row 8 expects `EquipmentUnavailable` |
| `LP-003` | Available | row 9's failure is quota, not availability |
| `M-101` | 0 / 2 active | rows 6, 8, 10 need quota to NOT be the failure |
| `M-102` | **2 / 2 active** (at quota) | row 9 expects `QuotaExceeded` |
| `M-103` | 1 / 2 active | holds `LP-002` |

The seed is built by calling the real `borrow()` path (against two
seed-only tags, `SEED-01`/`SEED-02`, that never appear in the CSV), so the
seed itself already exercises the same invariants the ten rows do.

## The dependency rule, enforced

`domain/` contains `LoanError`, `Result<T>`, `Member`, `Equipment`, `Loan` —
pure rules, in both languages. It does not include `<fstream>`, `<iostream>`,
or `<sstream>` in C++, and does not `import csv`/`sys` or call `print(`/`open(`
in Python. `run_tests.sh` step 1 greps for exactly those tokens (outside
comments) and fails the build on a hit — verified against both a clean run
and a deliberately injected violation during authoring.

## Verified

- **Environment:** Windows 11 · g++ (GCC) 15.2.0 · Python 3.12.13 · pytest 8.3.4
- **Date:** 2026-09-15
- **Result:** `./run_tests.sh` exits 0; all five steps pass; no warnings under
  `-Wall -Wextra -Werror`.

## Directory structure

```
Module3/
├── run_tests.sh                    # purity check, C++, golden file, Python -- all 5 fail loudly
├── cpp/
│   ├── include/pinjamlab/
│   │   ├── domain/                 # PURE: LoanError, Result<T>, Member, Equipment, Loan
│   │   ├── service/                # LoanService (orchestration), Database + TxnGuard (RAII)
│   │   ├── io/                     # CsvReader, Validator, ReportWriter
│   │   └── app/                    # seed.hpp, runner.hpp (pure of console I/O, returns lines)
│   ├── app/main.cpp                # the ONLY place with iostream + exit codes
│   └── tests/
├── py/pinjamlab/                   # domain/ service/ io/ app/ -- the same four
├── py/tests/
└── sample-data/
    ├── bad-requests.csv            # fixed, committed, 10 rows, one failure each
    └── expected-output.txt         # generated FROM the real C++ binary, not hand-typed
```

`my-bad-requests.csv` and the two original `LoanError` subclasses named in the
module (e.g. `ReservationConflict`, `FineCapReached`) are **deliberately
absent**: they are Lab 1.3's bring-your-own-input and Lab 2.1's original-work
deliverables respectively, not instructor-provided starter content.

## AddressSanitizer

This toolchain (WinLibs/MinGW g++ 15.2.0) does not ship `libasan`, so Lab
2.4's Defect B evidence (`-fsanitize=address`) cannot be captured here. Per
the fallback already established in Week 2's deck: accept a destructor-trace
print (a live-object counter that changes between the raw-pointer and
smart-pointer versions) as equivalent evidence when a student's own toolchain
also lacks ASan.
`````

Perintah: `git log --all --date=iso-strict --format="%H %ad %cd %s" -- PREDICTION.md docs/prediction_outcome.md; git diff --stat 5b26936 ce8bec3; .venv/bin/python scripts/audit_result_calls.py; bash scripts/count_callsites.sh`

`````text
STDOUT:
ce8bec3c830cfb1c8880453ff084a3aa62c6ac84 2026-11-12T14:02:31+07:00 2026-11-12T14:02:31+07:00 docs: add Module 3 documentation and lab materials for exception handling and modularity
5b26936d962f281a4925d9bc2ff3068ac5b5cf54 2026-11-12T13:26:06+07:00 2026-11-12T13:26:06+07:00 docs: predict Result refactor before implementation
 cpp/include/pinjamlab/app/runner.hpp           |   8 +-
 cpp/include/pinjamlab/app/seed.hpp             |   9 +-
 cpp/include/pinjamlab/domain/result.hpp        |  60 +-
 cpp/include/pinjamlab/service/loan_service.hpp |   8 +-
 cpp/tests/test_app.cpp                         |  13 +
 cpp/tests/test_errors.cpp                      |  21 +-
 cpp/tests/test_raii.cpp                        |   2 +-
 cpp/tests/test_result.cpp                      | 139 ++++
 cpp/tests/test_robustness.cpp                  |  14 +-
 docs/evidence/00_baseline_run.txt              |  88 +--
 docs/evidence/02_run_with_venv.txt             |  88 +--
 docs/evidence/result_asan.txt                  |  91 +++
 docs/evidence/result_callsites.txt             |  54 ++
 docs/evidence/result_changed_callsites.txt     |  51 ++
 docs/evidence/result_diff.patch                | 996 +++++++++++++++++++++++++
 docs/evidence/result_diff_stat.txt             |  21 +
 docs/evidence/result_full_run.txt              | 217 ++++++
 docs/evidence/result_golden_generation.txt     |   8 +
 docs/evidence/result_new_files.patch           | 315 ++++++++
 docs/evidence/result_production_callsites.txt  |  10 +
 docs/evidence/result_status.txt                |  42 ++
 docs/lab2_result_refactor.md                   |  80 ++
 docs/prediction_outcome.md                     |  33 +
 py/pinjamlab/app/runner.py                     |   7 +-
 py/pinjamlab/app/seed.py                       |   9 +-
 py/pinjamlab/service/loan_service.py           |   8 +-
 py/tests/test_app.py                           |  10 +
 py/tests/test_cleanup.py                       |   2 +-
 py/tests/test_errors.py                        |  24 +-
 py/tests/test_result.py                        |  62 ++
 py/tests/test_robustness.py                    |  12 +-
 run_tests.sh                                   |  12 +-
 sample-data/my-bad-requests.csv                |   6 +
 sample-data/my-expected-output.txt             |   5 +
 scripts/audit_result_calls.py                  |  38 +
 scripts/run_result_asan.sh                     |  29 +
 tests/limits_demo.cpp                          |  37 +
 tests/limits_demo.py                           |  39 +
 38 files changed, 2527 insertions(+), 141 deletions(-)
CHANGED cpp/include/pinjamlab/app/runner.hpp:49: (void)svc.borrow(req.tag, req.memberId, req.days);
CHANGED cpp/include/pinjamlab/app/seed.hpp:38: (void)svc.borrow("LP-002", "M-103", 5);   // LP-002 -> Loaned; M-103 -> 1 active
CHANGED cpp/include/pinjamlab/app/seed.hpp:39: (void)svc.borrow("SEED-01", "M-102", 5);  // M-102 -> 1 active
CHANGED cpp/include/pinjamlab/app/seed.hpp:40: (void)svc.borrow("SEED-02", "M-102", 5);  // M-102 -> 2 active == limit
same    cpp/tests/test_errors.cpp:19: (void)svc.borrow("LP-999", "M-101", 7);
same    cpp/tests/test_errors.cpp:30: (void)svc.borrow("LP-001", "M-404", 7);
same    cpp/tests/test_errors.cpp:40: (void)svc.borrow("LP-001", "M-101", 400);
CHANGED cpp/tests/test_errors.cpp:52: (void)svc.borrow("LP-002", "M-101", 7);
same    cpp/tests/test_errors.cpp:62: (void)svc.borrow("LP-003", "M-102", 7);
same    cpp/tests/test_errors.cpp:79: (void)svc.borrow(c.tag, c.member, c.days);
same    cpp/tests/test_errors.cpp:95: (void)svc.borrow("LP-003", "M-102", 7);
CHANGED cpp/tests/test_errors.cpp:107: const Loan loan = svc.borrow("LP-001", "M-101", 7);
CHANGED cpp/tests/test_raii.cpp:59: (void)svc.borrow("LP-001", "M-101", 7);
same    cpp/tests/test_robustness.cpp:31: (void)svc.borrow("lp-001", "M-101", 7);
same    cpp/tests/test_robustness.cpp:41: REQUIRE_THROWS_AS((void)svc.borrow("lp-001", "M-101", 7), UnknownAssetTag);
same    cpp/tests/test_robustness.cpp:42: REQUIRE_THROWS_AS((void)svc.borrow("lp-001", "M-101", 7), LoanError);
same    cpp/tests/test_robustness.cpp:52: (void)svc.borrow("LP-004", "M-101", 7);
same    cpp/tests/test_robustness.cpp:59: REQUIRE_THROWS_AS((void)svc.borrow("LP-004", "M-101", 7), LoanError);
CHANGED cpp/tests/test_robustness.cpp:61: REQUIRE(svc.borrow("LP-004", "M-103", 7).memberId() == "M-103");
same    cpp/tests/test_robustness.cpp:215: (void)svc.borrow("\xc3\xa4-lp", "M-101", 7);
same    cpp/tests/test_robustness.cpp:220: REQUIRE_THROWS_AS((void)svc.borrow("\xc3\x84-lp", "M-101", 7), AssetTagCaseMismatch);
CHANGED cpp/tests/test_robustness.cpp:243: (void)svc.borrow("LP-002", "M-101", 7);
same    cpp/tests/test_robustness.cpp:254: (void)svc.borrow("LP-001", "M-101", days);
CHANGED cpp/tests/test_robustness.cpp:265: REQUIRE(svc.borrow("LP-001", "M-101", 1).days() == 1);
CHANGED cpp/tests/test_robustness.cpp:267: REQUIRE(svc.borrow("LP-001", "M-101", 90).days() == 90);
CHANGED py/pinjamlab/app/runner.py:47: svc.borrow(req.tag, req.member_id, req.days)
CHANGED py/pinjamlab/app/seed.py:24: svc.borrow("LP-002", "M-103", 5)   # LP-002 -> Loaned; M-103 -> 1 active
CHANGED py/pinjamlab/app/seed.py:25: svc.borrow("SEED-01", "M-102", 5)  # M-102 -> 1 active
CHANGED py/pinjamlab/app/seed.py:26: svc.borrow("SEED-02", "M-102", 5)  # M-102 -> 2 active == limit
CHANGED py/tests/test_cleanup.py:58: svc.borrow("LP-001", "M-101", 7)
same    py/tests/test_errors.py:25: svc.borrow("LP-999", "M-101", 7)
same    py/tests/test_errors.py:33: svc.borrow("LP-001", "M-404", 7)
same    py/tests/test_errors.py:40: svc.borrow("LP-001", "M-101", 400)
CHANGED py/tests/test_errors.py:49: svc.borrow("LP-002", "M-101", 7)
same    py/tests/test_errors.py:56: svc.borrow("LP-003", "M-102", 7)
same    py/tests/test_errors.py:70: svc.borrow(tag, member, days)
CHANGED py/tests/test_errors.py:87: loan = svc.borrow("LP-001", "M-101", 7)
same    py/tests/test_errors.py:98: seeded().borrow("lp-001", "M-101", 7)
same    py/tests/test_errors.py:111: svc.borrow("LP-004", "M-101", 7)
CHANGED py/tests/test_errors.py:116: assert svc.borrow("LP-004", "M-103", 7).member_id == "M-103"
CHANGED py/tests/test_errors.py:155: svc.borrow("LP-002", "M-101", 7)
same    py/tests/test_robustness.py:22: svc.borrow("LP-001", "M-101", 7)
CHANGED py/tests/test_robustness.py:30: assert svc.borrow("LP-001", "M-101", 7).member_id == "M-101"
same    py/tests/test_robustness.py:39: svc.borrow("LP-001", "M-101", days)
CHANGED py/tests/test_robustness.py:45: assert svc.borrow("LP-001", "M-101", 1).days == 1
CHANGED py/tests/test_robustness.py:47: assert svc.borrow("LP-001", "M-101", 90).days == 90
same    py/tests/test_robustness.py:55: svc.borrow("\u00e4-lp", "M-101", 7)
same    py/tests/test_robustness.py:59: svc.borrow("\u00c4-lp", "M-101", 7)
Baseline expressions: 48; changed enclosing source lines: 23; production changed: 8
Method: baseline AST/C++ cleaned calls; exact-line diff matching. New calls excluded.
The borrow invocation arguments themselves are unchanged; enclosing usage is what changed.
path:line:count
cpp/include/pinjamlab/app/runner.hpp:49:1
cpp/include/pinjamlab/app/seed.hpp:38:1
cpp/include/pinjamlab/app/seed.hpp:40:1
cpp/include/pinjamlab/app/seed.hpp:42:1
cpp/tests/test_errors.cpp:19:1
cpp/tests/test_errors.cpp:30:1
cpp/tests/test_errors.cpp:40:1
cpp/tests/test_errors.cpp:51:1
cpp/tests/test_errors.cpp:59:1
cpp/tests/test_errors.cpp:76:1
cpp/tests/test_errors.cpp:92:1
cpp/tests/test_errors.cpp:104:1
cpp/tests/test_raii.cpp:59:1
cpp/tests/test_result.cpp:88:1
cpp/tests/test_result.cpp:112:1
cpp/tests/test_robustness.cpp:31:1
cpp/tests/test_robustness.cpp:41:1
cpp/tests/test_robustness.cpp:42:1
cpp/tests/test_robustness.cpp:52:1
cpp/tests/test_robustness.cpp:59:1
cpp/tests/test_robustness.cpp:61:1
cpp/tests/test_robustness.cpp:217:1
cpp/tests/test_robustness.cpp:222:1
cpp/tests/test_robustness.cpp:245:1
cpp/tests/test_robustness.cpp:256:1
cpp/tests/test_robustness.cpp:267:1
cpp/tests/test_robustness.cpp:271:1
py/pinjamlab/app/runner.py:47:1
py/pinjamlab/app/seed.py:24:1
py/pinjamlab/app/seed.py:26:1
py/pinjamlab/app/seed.py:28:1
py/tests/test_cleanup.py:58:1
py/tests/test_errors.py:25:1
py/tests/test_errors.py:33:1
py/tests/test_errors.py:40:1
py/tests/test_errors.py:48:1
py/tests/test_errors.py:56:1
py/tests/test_errors.py:70:1
py/tests/test_errors.py:87:1
py/tests/test_errors.py:100:1
py/tests/test_errors.py:113:1
py/tests/test_errors.py:118:1
py/tests/test_errors.py:159:1
py/tests/test_result.py:17:1
py/tests/test_result.py:38:1
py/tests/test_robustness.py:22:1
py/tests/test_robustness.py:30:1
py/tests/test_robustness.py:41:1
py/tests/test_robustness.py:47:1
py/tests/test_robustness.py:51:1
py/tests/test_robustness.py:61:1
py/tests/test_robustness.py:65:1
TOTAL: 52

STDERR:

exit=0; durasi_detik=0.331
`````

Perintah: `PYTHONPATH=py .venv/bin/python -m pytest py/tests/test_dependency_gate.py -v -s`

`````text
STDOUT:
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.2.0, pluggy-1.7.0 -- ~/loanbench/.venv/bin/python
rootdir: ~/loanbench
collecting ... collected 19 items

py/tests/test_dependency_gate.py::test_real_sources_pass PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[cpp-domain-io] REJECTED cpp domain -> io: cpp/include/pinjamlab/domain/gate_probe.hpp:1: forbidden domain -> io: pinjamlab/io/gate_probe.hpp
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[cpp-domain-service] REJECTED cpp domain -> service: cpp/include/pinjamlab/domain/gate_probe.hpp:1: forbidden domain -> service: pinjamlab/service/gate_probe.hpp
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[cpp-domain-app] REJECTED cpp domain -> app: cpp/include/pinjamlab/domain/gate_probe.hpp:1: forbidden domain -> app: pinjamlab/app/gate_probe.hpp
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[cpp-io-service] REJECTED cpp io -> service: cpp/include/pinjamlab/io/gate_probe.hpp:1: forbidden io -> service: pinjamlab/service/gate_probe.hpp
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[cpp-io-app] REJECTED cpp io -> app: cpp/include/pinjamlab/io/gate_probe.hpp:1: forbidden io -> app: pinjamlab/app/gate_probe.hpp
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[cpp-service-app] REJECTED cpp service -> app: cpp/include/pinjamlab/service/gate_probe.hpp:1: forbidden service -> app: pinjamlab/app/gate_probe.hpp
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[py-domain-io] REJECTED py domain -> io: py/pinjamlab/domain/gate_probe.py:1: forbidden domain -> io: pinjamlab.io.gate_probe
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[py-domain-service] REJECTED py domain -> service: py/pinjamlab/domain/gate_probe.py:1: forbidden domain -> service: pinjamlab.service.gate_probe
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[py-domain-app] REJECTED py domain -> app: py/pinjamlab/domain/gate_probe.py:1: forbidden domain -> app: pinjamlab.app.gate_probe
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[py-io-service] REJECTED py io -> service: py/pinjamlab/io/gate_probe.py:1: forbidden io -> service: pinjamlab.service.gate_probe
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[py-io-app] REJECTED py io -> app: py/pinjamlab/io/gate_probe.py:1: forbidden io -> app: pinjamlab.app.gate_probe
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[py-service-app] REJECTED py service -> app: py/pinjamlab/service/gate_probe.py:1: forbidden service -> app: pinjamlab.app.gate_probe
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_domain_io_rejected[py-def hidden():\n    import csv as c\n] PASSED
py/tests/test_dependency_gate.py::test_domain_io_rejected[py-from builtins import open as op\nop('file')\n] PASSED
py/tests/test_dependency_gate.py::test_domain_io_rejected[py-print('forbidden')\n] PASSED
py/tests/test_dependency_gate.py::test_domain_io_rejected[cpp-#include <fstream>\n] PASSED
py/tests/test_dependency_gate.py::test_domain_io_rejected[cpp-void probe() { std::cout << 1; }\n] PASSED
py/tests/test_dependency_gate.py::test_comments_and_strings_are_not_dependencies PASSED

============================== 19 passed in 1.98s ==============================

STDERR:

exit=0; durasi_detik=2.308
`````

Perintah: `PYTHONPATH=scripts .venv/bin/python -c 'from pathlib import Path; from check_dependencies import inspect; edges,violations=inspect(Path.cwd()); [print(*e,sep=" | ") for e in edges]; print("VIOLATIONS",violations)' `

`````text
STDOUT:
cpp | cpp/app/main.cpp | app | app | pinjamlab/app/runner.hpp | 5
cpp | cpp/app/main.cpp | app | app | pinjamlab/app/seed.hpp | 6
cpp | cpp/include/pinjamlab/app/runner.hpp | app | domain | pinjamlab/domain/loan_error.hpp | 9
cpp | cpp/include/pinjamlab/app/runner.hpp | app | io | pinjamlab/io/csv_reader.hpp | 10
cpp | cpp/include/pinjamlab/app/runner.hpp | app | io | pinjamlab/io/report_writer.hpp | 11
cpp | cpp/include/pinjamlab/app/runner.hpp | app | io | pinjamlab/io/validator.hpp | 12
cpp | cpp/include/pinjamlab/app/runner.hpp | app | service | pinjamlab/service/loan_service.hpp | 13
cpp | cpp/include/pinjamlab/app/seed.hpp | app | domain | pinjamlab/domain/equipment.hpp | 10
cpp | cpp/include/pinjamlab/app/seed.hpp | app | domain | pinjamlab/domain/member.hpp | 11
cpp | cpp/include/pinjamlab/app/seed.hpp | app | service | pinjamlab/service/loan_service.hpp | 12
cpp | cpp/include/pinjamlab/domain/equipment.hpp | domain | domain | pinjamlab/domain/loan_error.hpp | 8
cpp | cpp/include/pinjamlab/domain/member.hpp | domain | domain | pinjamlab/domain/loan_error.hpp | 8
cpp | cpp/include/pinjamlab/io/validator.hpp | io | domain | pinjamlab/domain/result.hpp | 3
cpp | cpp/include/pinjamlab/io/validator.hpp | io | io | pinjamlab/io/csv_reader.hpp | 4
cpp | cpp/include/pinjamlab/service/loan_service.hpp | service | domain | pinjamlab/domain/equipment.hpp | 8
cpp | cpp/include/pinjamlab/service/loan_service.hpp | service | domain | pinjamlab/domain/loan.hpp | 9
cpp | cpp/include/pinjamlab/service/loan_service.hpp | service | domain | pinjamlab/domain/loan_error.hpp | 10
cpp | cpp/include/pinjamlab/service/loan_service.hpp | service | domain | pinjamlab/domain/member.hpp | 11
cpp | cpp/include/pinjamlab/service/loan_service.hpp | service | domain | pinjamlab/domain/result.hpp | 12
cpp | cpp/include/pinjamlab/service/loan_service.hpp | service | service | pinjamlab/service/database.hpp | 13
cpp | cpp/include/pinjamlab/service/loan_service.hpp | service | service | pinjamlab/service/txn_guard.hpp | 14
cpp | cpp/include/pinjamlab/service/txn_guard.hpp | service | service | pinjamlab/service/database.hpp | 10
py | py/pinjamlab/app/main.py | app | app | pinjamlab.app.runner.run_catalogue | 10
py | py/pinjamlab/app/main.py | app | app | pinjamlab.app.seed.seed_pinjamlab | 11
py | py/pinjamlab/app/main.py | app | io | pinjamlab.io.report_writer.ReportWriter | 8
py | py/pinjamlab/app/main.py | app | service | pinjamlab.service.loan_service.LoanService | 9
py | py/pinjamlab/app/runner.py | app | domain | pinjamlab.domain.loan_error.AssetTagCaseMismatch | 9
py | py/pinjamlab/app/runner.py | app | domain | pinjamlab.domain.loan_error.LoanError | 9
py | py/pinjamlab/app/runner.py | app | domain | pinjamlab.domain.loan_error.ReservationConflict | 9
py | py/pinjamlab/app/runner.py | app | io | pinjamlab.io.csv_reader.CsvReader | 12
py | py/pinjamlab/app/runner.py | app | io | pinjamlab.io.report_writer.ReportWriter | 13
py | py/pinjamlab/app/runner.py | app | io | pinjamlab.io.validator.Validator | 14
py | py/pinjamlab/app/runner.py | app | service | pinjamlab.service.loan_service.LoanService | 15
py | py/pinjamlab/app/seed.py | app | domain | pinjamlab.domain.equipment.Equipment | 7
py | py/pinjamlab/app/seed.py | app | domain | pinjamlab.domain.member.Member | 8
py | py/pinjamlab/app/seed.py | app | domain | pinjamlab.domain.member.Role | 8
py | py/pinjamlab/app/seed.py | app | service | pinjamlab.service.loan_service.LoanService | 9
py | py/pinjamlab/domain/equipment.py | domain | domain | pinjamlab.domain.loan_error.EquipmentUnavailable | 6
py | py/pinjamlab/domain/member.py | domain | domain | pinjamlab.domain.loan_error.QuotaExceeded | 6
py | py/pinjamlab/io/validator.py | io | domain | pinjamlab.domain.result.Result | 9
py | py/pinjamlab/io/validator.py | io | io | pinjamlab.io.csv_reader.RawRow | 10
py | py/pinjamlab/service/loan_service.py | service | domain | pinjamlab.domain.equipment.Equipment | 6
py | py/pinjamlab/service/loan_service.py | service | domain | pinjamlab.domain.loan.Loan | 7
py | py/pinjamlab/service/loan_service.py | service | domain | pinjamlab.domain.loan_error.AssetTagCaseMismatch | 8
py | py/pinjamlab/service/loan_service.py | service | domain | pinjamlab.domain.loan_error.EquipmentUnavailable | 8
py | py/pinjamlab/service/loan_service.py | service | domain | pinjamlab.domain.loan_error.InvalidLoanDuration | 8
py | py/pinjamlab/service/loan_service.py | service | domain | pinjamlab.domain.loan_error.LoanError | 8
py | py/pinjamlab/service/loan_service.py | service | domain | pinjamlab.domain.loan_error.QuotaExceeded | 8
py | py/pinjamlab/service/loan_service.py | service | domain | pinjamlab.domain.loan_error.ReservationConflict | 8
py | py/pinjamlab/service/loan_service.py | service | domain | pinjamlab.domain.loan_error.UnknownAssetTag | 8
py | py/pinjamlab/service/loan_service.py | service | domain | pinjamlab.domain.loan_error.UnknownMember | 8
py | py/pinjamlab/service/loan_service.py | service | domain | pinjamlab.domain.member.Member | 18
py | py/pinjamlab/service/loan_service.py | service | domain | pinjamlab.domain.result.Result | 19
py | py/pinjamlab/service/loan_service.py | service | service | pinjamlab.service.database.Database | 20
py | py/pinjamlab/service/loan_service.py | service | service | pinjamlab.service.txn_guard.txn_guard | 21
py | py/pinjamlab/service/txn_guard.py | service | service | pinjamlab.service.database.Database | 14
VIOLATIONS []

STDERR:

exit=0; durasi_detik=0.050
`````

Perintah: `cat run_tests.sh`

`````text
#!/usr/bin/env bash
# ==============================================================================
# PinjamLab Module 3: one command -- build, C++ tests, Python tests, AND the
# dependency-rule purity check (Lab 3.2: "Add the purity check to run_tests.sh
# so a violation fails the build.").
#
# Like Module 2's script and unlike Module 1's, this one FAILS (non-zero exit)
# when a toolchain is missing or a check fails -- it never prints a success
# banner over a step that did not actually run.
# ==============================================================================
set -euo pipefail

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p bin

CXX="${CXX:-g++}"
# Prefer the WSL project venv; never select a Windows interpreter implicitly.
if [ -z "${PY:-}" ]; then
    if [ -x ".venv/bin/python" ]; then PY=".venv/bin/python"
    else PY="python3"; fi
fi
command -v "$CXX" >/dev/null || { echo "FATAL: no C++ compiler ($CXX) on PATH."; exit 2; }
command -v "$PY"  >/dev/null || { echo "FATAL: no Python interpreter ($PY) on PATH."; exit 2; }

echo "================================================================================"
echo " [PinjamLab M3] $("$CXX" --version | head -1)"
echo " [PinjamLab M3] $("$PY" --version 2>&1)"
echo "================================================================================"

# ---- 1/5: parsed layer directions and domain I/O purity ----------------------
echo ""
echo ">>> [1/5] Dependency gate (C++ includes and Python AST)"
"$PY" scripts/check_dependencies.py .

# ---- 2/5: build the C++ suites -----------------------------------------------
echo ""
echo ">>> [2/5] Building C++20 tests (-Wall -Wextra -Werror)"
for t in test_errors test_raii test_result test_app test_robustness; do
    "$CXX" -std=c++20 -Wall -Wextra -Werror \
           -Icpp/include -Icpp/tests "cpp/tests/$t.cpp" -o "bin/$t"
done
"$CXX" -std=c++20 -Wall -Wextra -Werror -Icpp/include cpp/app/main.cpp -o bin/pinjamlab_cli
"$CXX" -std=c++20 -Wall -Wextra -Werror -Icpp/include -Icpp/tests tests/limits_demo.cpp -o bin/limits_demo

# ---- 3/5: run the C++ suites --------------------------------------------------
echo ""
echo ">>> [3/5] Running C++20 test suites"
for t in test_errors test_raii test_result test_app test_robustness; do
    "./bin/$t"
done

# ---- 4/5: the cross-language golden-file check -------------------------------
./bin/limits_demo
PYTHONPATH=py "$PY" tests/limits_demo.py
echo ""
echo ">>> [4/5] Cross-language golden files and exact CLI exit codes"
expect_rejected() {
    local status=0
    "$@" || status=$?
    if [ "$status" -ne 1 ]; then
        echo "FATAL: CLI must exit 1 for bad requests, got $status: $*" >&2
        exit 1
    fi
}
# Line endings are normalised on BOTH sides (tr -d '\r'): the Windows CLI prints
# CRLF, Linux/macOS prints LF, and the golden file is stored as LF (.gitattributes).
# The message text must still match exactly; only the line terminator is ignored.
GOLDEN="${GOLDEN:-sample-data/expected-output.txt}"
expect_rejected ./bin/pinjamlab_cli sample-data/bad-requests.csv 2>bin/cpp_stderr.txt >/dev/null
expect_rejected env PYTHONPATH=py "$PY" -m pinjamlab.app.main sample-data/bad-requests.csv 2>bin/py_stderr.txt >/dev/null
for output in bin/cpp_stderr.txt bin/py_stderr.txt; do
    diff <(tr -d '\r' < "$output") <(tr -d '\r' < sample-data/expected-output.txt)
    if [ "$GOLDEN" != "sample-data/expected-output.txt" ]; then
        [ -f "$GOLDEN" ] || { echo "FATAL: golden file not found: $GOLDEN" >&2; exit 1; }
        diff <(tr -d '\r' < "$output") <(tr -d '\r' < "$GOLDEN")
    fi
    echo "  match: $output matches golden file(s), CLI exit 1"
done

expect_rejected ./bin/pinjamlab_cli sample-data/my-bad-requests.csv 2>bin/my_cpp_stderr.txt >/dev/null
expect_rejected env PYTHONPATH=py "$PY" -m pinjamlab.app.main sample-data/my-bad-requests.csv 2>bin/my_py_stderr.txt >/dev/null
for output in bin/my_cpp_stderr.txt bin/my_py_stderr.txt; do
    diff <(tr -d '\r' < "$output") <(tr -d '\r' < sample-data/my-expected-output.txt)
    echo "  match: $output matches C++ generated five-row golden, CLI exit 1"
done

# ---- 5/5: run the Python suite, including gate mutation tests ------------------
echo ""
echo ">>> [5/5] Running Python test suite (version reported above)"
PYTHONPATH=py "$PY" -m pytest py/tests -v

echo ""
echo "================================================================================"
echo " [SUCCESS] Purity check, C++ suites, golden file, and Python suite all passed."
echo "================================================================================"
`````

## §6 Bahan A1 (trace satu rute error — baris 9)

Baris data #9 ialah LP-003,M-102,7. CSV reader melewati header, lalu menomori posisi data; salinan satu baris karena itu melapor row 1, bukan row 9. Sumber service lengkap bernomor pada §4 menunjukkan quota check sebelum konstruksi TxnGuard/with txn_guard. Jalur ini tidak memasuki transaksi baru sehingga tidak membuktikan destructor rollback dari borrow. Seed sebelumnya memang memakai transaksi; jangan mencampurkannya dengan row 9. Urutan konseptual: main -> seed -> reader -> validator -> borrow -> quota throw -> handler LoanError -> rejectedLine -> stderr/exit 1. Trace instrumentasi aktual atau gambar tangan: TIDAK DILAKUKAN. Urutan konseptual di sini adalah pembacaan sumber, bukan trace eksekusi yang diklaim direkam.

Perintah: `nl -ba cpp/include/pinjamlab/app/seed.hpp`

`````text
1: #ifndef PINJAMLAB_APP_SEED_HPP
2: #define PINJAMLAB_APP_SEED_HPP
3: 
4: // app layer: the fixed starting roster and catalogue that bad-requests.csv
5: // is written against. A real deployment would load this from a database
6: // (Module 5); Module 3 has no persistence yet, so the app layer is the
7: // legitimate place to construct it -- domain and service take these objects
8: // as parameters and never manufacture their own test data.
9: 
10: #include "pinjamlab/domain/equipment.hpp"
11: #include "pinjamlab/domain/member.hpp"
12: #include "pinjamlab/service/loan_service.hpp"
13: 
14: namespace pinjamlab {
15: 
16: // Seeds exactly the state the ten committed rows in bad-requests.csv assume:
17: //   LP-001    available                 (rows 7, 10 touch it and expect this)
18: //   LP-002    ALREADY LOANED to M-103    (row 8 expects EquipmentUnavailable)
19: //   LP-003    available                 (row 9 touches it; its failure is quota, not this)
20: //   SEED-01/02 exist only to bring M-102 to quota without touching LP-00x
21: //   M-101     Student, 0 active / 2 max (rows 6, 8, 10)
22: //   M-102     Student, 2 active / 2 max (row 9 expects QuotaExceeded)
23: //   M-103     Student, 1 active / 2 max (holds LP-002)
24: inline void seedPinjamLab(LoanService& svc) {
25:     svc.addEquipment(Equipment("LP-001", "ThinkPad T14"));
26:     svc.addEquipment(Equipment("LP-002", "Latitude 5440"));
27:     svc.addEquipment(Equipment("LP-003", "ProBook 450"));
28:     svc.addEquipment(Equipment("LP-004", "Reserved laptop", "M-103"));
29:     svc.addEquipment(Equipment("SEED-01", "Seed placeholder A"));
30:     svc.addEquipment(Equipment("SEED-02", "Seed placeholder B"));
31: 
32:     svc.addMember(Member("M-101", "Ayu Lestari", Role::Student));
33:     svc.addMember(Member("M-102", "Budi Santoso", Role::Student));
34:     svc.addMember(Member("M-103", "Citra Dewi", Role::Student));
35: 
36:     // Sequenced through the real borrow() path rather than poked directly,
37:     // so the seed itself exercises the same invariants the CSV rows do.
38:     if (const auto r = svc.borrow("LP-002", "M-103", 5); !r.ok())
39:         throw std::logic_error(r.error());
40:     if (const auto r = svc.borrow("SEED-01", "M-102", 5); !r.ok())
41:         throw std::logic_error(r.error());
42:     if (const auto r = svc.borrow("SEED-02", "M-102", 5); !r.ok())
43:         throw std::logic_error(r.error());
44: }
45: 
46: }  // namespace pinjamlab
47: 
48: #endif  // PINJAMLAB_APP_SEED_HPP
`````

Perintah: `nl -ba py/pinjamlab/app/seed.py`

`````text
1: """app layer: the fixed starting roster and catalogue that bad-requests.csv
2: is written against. Mirrors cpp/include/pinjamlab/app/seed.hpp exactly --
3: see that file for why each seed step exists.
4: """
5: from __future__ import annotations
6: 
7: from ..domain.equipment import Equipment
8: from ..domain.member import Member, Role
9: from ..service.loan_service import LoanService
10: 
11: 
12: def seed_pinjamlab(svc: LoanService) -> None:
13:     svc.add_equipment(Equipment("LP-001", "ThinkPad T14"))
14:     svc.add_equipment(Equipment("LP-002", "Latitude 5440"))
15:     svc.add_equipment(Equipment("LP-003", "ProBook 450"))
16:     svc.add_equipment(Equipment("LP-004", "Reserved laptop", "M-103"))
17:     svc.add_equipment(Equipment("SEED-01", "Seed placeholder A"))
18:     svc.add_equipment(Equipment("SEED-02", "Seed placeholder B"))
19: 
20:     svc.add_member(Member("M-101", "Ayu Lestari", Role.STUDENT))
21:     svc.add_member(Member("M-102", "Budi Santoso", Role.STUDENT))
22:     svc.add_member(Member("M-103", "Citra Dewi", Role.STUDENT))
23: 
24:     if not (result := svc.borrow("LP-002", "M-103", 5)).ok:
25:         raise RuntimeError(result.error)
26:     if not (result := svc.borrow("SEED-01", "M-102", 5)).ok:
27:         raise RuntimeError(result.error)
28:     if not (result := svc.borrow("SEED-02", "M-102", 5)).ok:
29:         raise RuntimeError(result.error)
`````

Perintah: `nl -ba cpp/app/main.cpp`

`````text
1: // app layer entry point: argument parsing, top-level handler, exit codes.
2: // No business rule lives in this file; it wires io + service + domain
3: // together and reports what happened.
4: 
5: #include "pinjamlab/app/runner.hpp"
6: #include "pinjamlab/app/seed.hpp"
7: 
8: #include <iostream>
9: #include <string>
10: 
11: int main(int argc, char** argv) {
12:     const std::string path = (argc >= 2) ? argv[1] : "sample-data/bad-requests.csv";
13: 
14:     pinjamlab::LoanService svc;
15:     pinjamlab::seedPinjamLab(svc);
16: 
17:     const auto result = pinjamlab::runCatalogue(svc, path);
18: 
19:     for (const auto& line : result.rejectedLines) {
20:         std::cerr << line << "\n";
21:     }
22:     std::cout << pinjamlab::ReportWriter::summary(result.total, result.created, result.rejected)
23:               << "\n";
24: 
25:     return result.exitCode();
26: }
`````

Perintah: `nl -ba py/pinjamlab/app/main.py`

`````text
1: """app layer entry point: argument parsing, top-level handler, exit codes.
2: No business rule lives in this file.
3: """
4: from __future__ import annotations
5: 
6: import sys
7: 
8: from ..io.report_writer import ReportWriter
9: from ..service.loan_service import LoanService
10: from .runner import run_catalogue
11: from .seed import seed_pinjamlab
12: 
13: 
14: def main(argv: list[str]) -> int:
15:     path = argv[1] if len(argv) >= 2 else "sample-data/bad-requests.csv"
16: 
17:     svc = LoanService()
18:     seed_pinjamlab(svc)
19: 
20:     result = run_catalogue(svc, path)
21: 
22:     for line in result.rejected_lines:
23:         print(line, file=sys.stderr)
24:     print(ReportWriter.summary(result.total, result.created, result.rejected))
25: 
26:     return result.exit_code
27: 
28: 
29: if __name__ == "__main__":
30:     sys.exit(main(sys.argv))
`````

Perintah: `awk 'NR==1 || NR==10 {print NR ":" $0}' sample-data/bad-requests.csv; grep -n 'row 9:' bin/analisis-export/cpp.stderr bin/analisis-export/py.stderr`

`````text
STDOUT:
1:tag,member_id,days
10:LP-003,M-102,7
bin/analisis-export/cpp.stderr:9:row 9: Loan quota exceeded: 2 active, limit 2
bin/analisis-export/py.stderr:9:row 9: Loan quota exceeded: 2 active, limit 2

STDERR:

exit=0; durasi_detik=0.008
`````

## §7 Bahan A2

| Bukti assertion | Test/kode nyata | Batas klaim |
|---|---|---|
| Ledger commit normal | test_raii committed size=2,pending=0; test_cleanup len=2,pending=0 | Hanya kasus yang dijalankan |
| Rollback scope normal tanpa commit | test_raii committed empty,pending=0 | API Python normal exit justru commit |
| Throw di wilayah guard | test_raii caught=true,committed empty,pending=0; test_cleanup pytest.raises RuntimeError | Bukan row9 |
| Handle tanpa with | test_cleanup handle masih terbuka lalu finally close | Demonstrasi buruk yang dikendalikan |
| Atomic publish normal | file lama tetap sebelum commit, file baru sesudah, temp hilang | Tidak menguji crash listrik/fsync |
| Body/write/replace gagal | test_cleanup handle.closed, isi lama/list directory; test_robustness !exists(temp),old preserved | Cleanup filesystem gagal tidak disimulasikan |
| BaseException atomic | KeyboardInterrupt,handle.closed,direktori kosong | Tidak berlaku otomatis pada txn_guard |
| Result payload | Tracked::live==0 dan transisi/copy/move/throw assignment | Basic guarantee, bukan strong guarantee |

Uji node baru memeriksa field, keluarga catch, ASCII folding, konflik reservasi dan state. Verbose Python di atas menunjukkan nama dan hasil aktual; sumber test robustness lengkap yang relevan ada pada diff §4. Full test_result Python juga terdapat pada diff §4; tidak diduplikasi.

Perintah: `cat run_tests.sh`

`````text
#!/usr/bin/env bash
# ==============================================================================
# PinjamLab Module 3: one command -- build, C++ tests, Python tests, AND the
# dependency-rule purity check (Lab 3.2: "Add the purity check to run_tests.sh
# so a violation fails the build.").
#
# Like Module 2's script and unlike Module 1's, this one FAILS (non-zero exit)
# when a toolchain is missing or a check fails -- it never prints a success
# banner over a step that did not actually run.
# ==============================================================================
set -euo pipefail

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p bin

CXX="${CXX:-g++}"
# Prefer the WSL project venv; never select a Windows interpreter implicitly.
if [ -z "${PY:-}" ]; then
    if [ -x ".venv/bin/python" ]; then PY=".venv/bin/python"
    else PY="python3"; fi
fi
command -v "$CXX" >/dev/null || { echo "FATAL: no C++ compiler ($CXX) on PATH."; exit 2; }
command -v "$PY"  >/dev/null || { echo "FATAL: no Python interpreter ($PY) on PATH."; exit 2; }

echo "================================================================================"
echo " [PinjamLab M3] $("$CXX" --version | head -1)"
echo " [PinjamLab M3] $("$PY" --version 2>&1)"
echo "================================================================================"

# ---- 1/5: parsed layer directions and domain I/O purity ----------------------
echo ""
echo ">>> [1/5] Dependency gate (C++ includes and Python AST)"
"$PY" scripts/check_dependencies.py .

# ---- 2/5: build the C++ suites -----------------------------------------------
echo ""
echo ">>> [2/5] Building C++20 tests (-Wall -Wextra -Werror)"
for t in test_errors test_raii test_result test_app test_robustness; do
    "$CXX" -std=c++20 -Wall -Wextra -Werror \
           -Icpp/include -Icpp/tests "cpp/tests/$t.cpp" -o "bin/$t"
done
"$CXX" -std=c++20 -Wall -Wextra -Werror -Icpp/include cpp/app/main.cpp -o bin/pinjamlab_cli
"$CXX" -std=c++20 -Wall -Wextra -Werror -Icpp/include -Icpp/tests tests/limits_demo.cpp -o bin/limits_demo

# ---- 3/5: run the C++ suites --------------------------------------------------
echo ""
echo ">>> [3/5] Running C++20 test suites"
for t in test_errors test_raii test_result test_app test_robustness; do
    "./bin/$t"
done

# ---- 4/5: the cross-language golden-file check -------------------------------
./bin/limits_demo
PYTHONPATH=py "$PY" tests/limits_demo.py
echo ""
echo ">>> [4/5] Cross-language golden files and exact CLI exit codes"
expect_rejected() {
    local status=0
    "$@" || status=$?
    if [ "$status" -ne 1 ]; then
        echo "FATAL: CLI must exit 1 for bad requests, got $status: $*" >&2
        exit 1
    fi
}
# Line endings are normalised on BOTH sides (tr -d '\r'): the Windows CLI prints
# CRLF, Linux/macOS prints LF, and the golden file is stored as LF (.gitattributes).
# The message text must still match exactly; only the line terminator is ignored.
GOLDEN="${GOLDEN:-sample-data/expected-output.txt}"
expect_rejected ./bin/pinjamlab_cli sample-data/bad-requests.csv 2>bin/cpp_stderr.txt >/dev/null
expect_rejected env PYTHONPATH=py "$PY" -m pinjamlab.app.main sample-data/bad-requests.csv 2>bin/py_stderr.txt >/dev/null
for output in bin/cpp_stderr.txt bin/py_stderr.txt; do
    diff <(tr -d '\r' < "$output") <(tr -d '\r' < sample-data/expected-output.txt)
    if [ "$GOLDEN" != "sample-data/expected-output.txt" ]; then
        [ -f "$GOLDEN" ] || { echo "FATAL: golden file not found: $GOLDEN" >&2; exit 1; }
        diff <(tr -d '\r' < "$output") <(tr -d '\r' < "$GOLDEN")
    fi
    echo "  match: $output matches golden file(s), CLI exit 1"
done

expect_rejected ./bin/pinjamlab_cli sample-data/my-bad-requests.csv 2>bin/my_cpp_stderr.txt >/dev/null
expect_rejected env PYTHONPATH=py "$PY" -m pinjamlab.app.main sample-data/my-bad-requests.csv 2>bin/my_py_stderr.txt >/dev/null
for output in bin/my_cpp_stderr.txt bin/my_py_stderr.txt; do
    diff <(tr -d '\r' < "$output") <(tr -d '\r' < sample-data/my-expected-output.txt)
    echo "  match: $output matches C++ generated five-row golden, CLI exit 1"
done

# ---- 5/5: run the Python suite, including gate mutation tests ------------------
echo ""
echo ">>> [5/5] Running Python test suite (version reported above)"
PYTHONPATH=py "$PY" -m pytest py/tests -v

echo ""
echo "================================================================================"
echo " [SUCCESS] Purity check, C++ suites, golden file, and Python suite all passed."
echo "================================================================================"
`````

Perintah: `nl -ba cpp/tests/test_result.cpp`

`````text
1: // Result<T> from-scratch primitive: proves the two named factories are the
2: // only way to build one, proves value() throws on failure, and proves a
3: // throwing implementation and a Result-returning implementation of the SAME
4: // rule produce identical observable behaviour on the same inputs -- the
5: // "from-scratch match" Lab 2.2 requires.
6: 
7: #include "mini_catch.hpp"
8: #include "pinjamlab/domain/result.hpp"
9: #include "pinjamlab/io/validator.hpp"
10: #include "pinjamlab/app/seed.hpp"
11: #include <typeinfo>
12: 
13: #include <stdexcept>
14: #include <string>
15: 
16: using namespace pinjamlab;
17: 
18: TEST_CASE("Result::success carries a value and ok() is true") {
19:     auto r = Result<int>::success(42);
20:     REQUIRE(r.ok());
21:     REQUIRE(r.value() == 42);
22:     REQUIRE(r.error().empty());
23: }
24: 
25: TEST_CASE("Result::failure carries a message and ok() is false") {
26:     auto r = Result<int>::failure("days must be positive, got -3");
27:     REQUIRE(!r.ok());
28:     REQUIRE(r.error() == "days must be positive, got -3");
29: }
30: 
31: TEST_CASE("value() on a failed Result throws, rather than returning garbage") {
32:     auto r = Result<std::string>::failure("tag is empty");
33:     REQUIRE_THROWS_AS((void)r.value(), std::logic_error);
34: }
35: 
36: // ---- the from-scratch match: Validator (Result) vs a throwing equivalent ----
37: 
38: // A deliberately duplicated throwing version of the SAME rule Validator
39: // applies, so the two can be compared on the same inputs. Real code should
40: // never have both; this exists only to prove the refactor changes shape, not
41: // behaviour -- Lab 2.2's explicit requirement.
42: static int parseDaysOrThrow(const std::string& raw) {
43:     if (raw.empty()) throw std::invalid_argument("days is not a number: " + raw);
44:     std::size_t i = 0;
45:     bool neg = false;
46:     if (raw[0] == '+' || raw[0] == '-') { neg = (raw[0] == '-'); i = 1; }
47:     if (i == raw.size()) throw std::invalid_argument("days is not a number: " + raw);
48:     long long value = 0;
49:     for (; i < raw.size(); ++i) {
50:         if (raw[i] < '0' || raw[i] > '9') throw std::invalid_argument("days is not a number: " + raw);
51:         value = value * 10 + (raw[i] - '0');
52:     }
53:     const int days = static_cast<int>(neg ? -value : value);
54:     if (days <= 0) throw std::invalid_argument("days must be positive, got " + std::to_string(days));
55:     return days;
56: }
57: 
58: TEST_CASE("From-scratch match: Result and throwing agree on well-formed input") {
59:     Validator v;
60:     RawRow row{1, "LP-001", "M-101", "7"};
61:     const auto r = v.validate(row);
62:     REQUIRE(r.ok());
63:     REQUIRE(r.value().days == 7);
64:     REQUIRE(parseDaysOrThrow("7") == 7);  // identical outcome, different shape
65: }
66: 
67: TEST_CASE("From-scratch match: Result and throwing agree on every malformed input") {
68:     Validator v;
69:     const std::string malformed[] = {"abc", "-3", "0", ""};
70:     for (const auto& raw : malformed) {
71:         RawRow row{1, "LP-001", "M-101", raw};
72:         const auto r = v.validate(row);
73:         REQUIRE(!r.ok());  // Result: caller decides, cannot ignore ok()
74: 
75:         bool threw = false;
76:         try {
77:             (void)parseDaysOrThrow(raw);
78:         } catch (const std::invalid_argument&) {
79:             threw = true;  // throwing: caller who forgets try/catch still compiles
80:         }
81:         REQUIRE(threw);
82:     }
83: }
84: 
85: // Test-only adapter, not a second production implementation of the rules.
86: static Loan borrowOrThrow(LoanService& svc, const std::string& tag,
87:                           const std::string& member, int days) {
88:     const auto result = svc.borrow(tag, member, days);
89:     if (!result.ok()) throw EquipmentUnavailable(tag);
90:     return result.value();
91: }
92: 
93: TEST_CASE("Borrow Result and throwing twin: identical inputs, messages, types and state") {
94:     const struct { const char* tag; const char* member; int days; } cases[] = {
95:         {"LP-001", "M-101", 7}, {"LP-002", "M-101", 7},
96:         {"LP-999", "M-101", 7}, {"lp-001", "M-101", 7},
97:         {"LP-001", "M-404", 7}, {"LP-001", "M-101", 0},
98:         {"LP-001", "M-101", 91}, {"LP-004", "M-101", 7},
99:         {"LP-003", "M-102", 7},
100:         // Earlier guards must still win over unavailability.
101:         {"LP-002", "M-404", 7}, {"LP-002", "M-101", 0},
102:         {"LP-002", "M-102", 7},
103:     };
104:     for (const auto& c : cases) {
105:         LoanService resultSvc, throwingSvc;
106:         seedPinjamLab(resultSvc);
107:         seedPinjamLab(throwingSvc);
108:         const auto before = resultSvc.ledger().committed();
109:         std::string resultMessage, throwMessage, resultType, throwType;
110:         bool success = false;
111:         try {
112:             const auto result = resultSvc.borrow(c.tag, c.member, c.days);
113:             success = result.ok();
114:             if (success) {
115:                 REQUIRE(result.value().tag() == c.tag);
116:                 REQUIRE(result.value().memberId() == c.member);
117:                 REQUIRE(result.value().days() == c.days);
118:                 resultMessage = result.value().id();
119:             } else {
120:                 resultMessage = result.error();
121:                 resultType = typeid(EquipmentUnavailable).name();
122:                 REQUIRE_THROWS_AS((void)result.value(), std::logic_error);
123:             }
124:         } catch (const LoanError& error) {
125:             resultMessage = error.what();
126:             resultType = typeid(error).name();
127:         }
128:         bool twinSuccess = false;
129:         try {
130:             const auto loan = borrowOrThrow(throwingSvc, c.tag, c.member, c.days);
131:             twinSuccess = true;
132:             throwMessage = loan.id();
133:             REQUIRE(loan.tag() == c.tag);
134:             REQUIRE(loan.memberId() == c.member);
135:             REQUIRE(loan.days() == c.days);
136:         } catch (const LoanError& error) {
137:             throwMessage = error.what();
138:             throwType = typeid(error).name();
139:         }
140:         REQUIRE(success == twinSuccess);
141:         REQUIRE(resultMessage == throwMessage);
142:         REQUIRE(resultType == throwType);
143:         for (const auto* tag : {"LP-001", "LP-002", "LP-003", "LP-004", "SEED-01", "SEED-02"}) {
144:             REQUIRE(resultSvc.findEquipment(tag)->isAvailable() == throwingSvc.findEquipment(tag)->isAvailable());
145:             REQUIRE(resultSvc.findEquipment(tag)->reservedFor() == throwingSvc.findEquipment(tag)->reservedFor());
146:         }
147:         for (const auto* member : {"M-101", "M-102", "M-103"})
148:             REQUIRE(resultSvc.findMember(member)->activeLoans() == throwingSvc.findMember(member)->activeLoans());
149:         REQUIRE(resultSvc.ledger().committed() == throwingSvc.ledger().committed());
150:         REQUIRE(resultSvc.ledger().pendingCount() == 0);
151:         REQUIRE(throwingSvc.ledger().pendingCount() == 0);
152:         REQUIRE(resultSvc.ledger().committed().size() == (success ? 8 : 6));
153:         if (!success) {
154:             REQUIRE(resultSvc.ledger().committed() == before);
155:             REQUIRE(resultSvc.findMember("M-101")->activeLoans() == 0);
156:             REQUIRE(resultSvc.findMember("M-102")->activeLoans() == 2);
157:             REQUIRE(resultSvc.findMember("M-103")->activeLoans() == 1);
158:             REQUIRE(resultSvc.findEquipment("LP-001")->isAvailable());
159:             REQUIRE(!resultSvc.findEquipment("LP-002")->isAvailable());
160:             REQUIRE(resultSvc.findEquipment("LP-003")->isAvailable());
161:             REQUIRE(resultSvc.findEquipment("LP-004")->isAvailable());
162:         }
163:         // Returning the item observes the private owner mapping too.
164:         resultSvc.returnItem(success ? c.tag : "LP-002", success ? c.member : "M-103");
165:         throwingSvc.returnItem(success ? c.tag : "LP-002", success ? c.member : "M-103");
166:         REQUIRE(resultSvc.findEquipment(success ? c.tag : "LP-002")->isAvailable());
167:         REQUIRE(throwingSvc.findEquipment(success ? c.tag : "LP-002")->isAvailable());
168:     }
169: }
170: 
171: struct Tracked {
172:     inline static int live = 0;
173:     inline static bool fail = false;
174:     int n;
175:     explicit Tracked(int value) : n(value) { ++live; }
176:     Tracked(const Tracked& other) : n(other.n) {
177:         if (fail) throw std::runtime_error("copy failure");
178:         ++live;
179:     }
180:     Tracked(Tracked&& other) : n(other.n) {
181:         if (fail) throw std::runtime_error("move failure");
182:         ++live;
183:     }
184:     ~Tracked() { --live; }
185: };
186: 
187: TEST_CASE("Manual union owns nondefault payload across copies, moves and throwing assignments") {
188:     static_assert(!std::is_default_constructible_v<Loan>);
189:     {
190:         auto a = Result<Tracked>::success(Tracked(7));
191:         auto b = a;
192:         auto c = std::move(b);
193:         auto d = Result<Tracked>::failure("unavailable");
194:         d = a;
195:         REQUIRE(d.value().n == 7);
196:         d = Result<Tracked>::failure("no value");
197:         REQUIRE(!d.ok());
198:         d = std::move(c);
199:         a = a;
200:         auto* alias = &a;
201:         a = std::move(*alias);
202:         REQUIRE(a.value().n == 7);
203:         Tracked::fail = true;
204:         REQUIRE_THROWS_AS(d = a, std::runtime_error);
205:         REQUIRE(!d.ok());
206:         REQUIRE_THROWS_AS(d = std::move(a), std::runtime_error);
207:         REQUIRE(!d.ok());
208:         REQUIRE_THROWS_AS(Result<Tracked>(a), std::runtime_error);
209:         REQUIRE_THROWS_AS(Result<Tracked>(std::move(a)), std::runtime_error);
210:         Tracked::fail = false;
211:         d = a;
212:         REQUIRE(d.value().n == 7);
213:     }
214:     REQUIRE(Tracked::live == 0);
215:     auto failed = Result<Loan>::failure("busy");
216:     auto copy = failed;
217:     auto moved = std::move(copy);
218:     REQUIRE(!moved.ok());
219:     REQUIRE(moved.error() == "busy");
220: }
221: 
222: int main() { return test_runner::runAll(); }
`````

Perintah: `nl -ba cpp/tests/test_raii.cpp`

`````text
1: // Proves TxnGuard releases (rolls back) on EVERY exit path, including the
2: // throwing one -- Lab 2.3's explicit requirement: "a test that throws inside
3: // the guarded region and asserts the resource was released."
4: 
5: #include "mini_catch.hpp"
6: #include "pinjamlab/service/database.hpp"
7: #include "pinjamlab/service/loan_service.hpp"
8: #include "pinjamlab/service/txn_guard.hpp"
9: 
10: #include <stdexcept>
11: 
12: using namespace pinjamlab;
13: 
14: TEST_CASE("TxnGuard commits: staged records become committed") {
15:     Database db;
16:     {
17:         TxnGuard txn(db);
18:         db.stage("a");
19:         db.stage("b");
20:         txn.commit();
21:     }
22:     REQUIRE(db.committed().size() == 2);
23:     REQUIRE(db.pendingCount() == 0);
24: }
25: 
26: TEST_CASE("TxnGuard rolls back on normal scope exit without commit()") {
27:     Database db;
28:     {
29:         TxnGuard txn(db);
30:         db.stage("never committed");
31:         // txn destructs here WITHOUT commit() having been called.
32:     }
33:     REQUIRE(db.committed().empty());
34:     REQUIRE(db.pendingCount() == 0);  // rollback cleared the staged record
35: }
36: 
37: TEST_CASE("TxnGuard rolls back when an exception unwinds through it") {
38:     Database db;
39:     bool caught = false;
40:     try {
41:         TxnGuard txn(db);
42:         db.stage("about to be abandoned");
43:         throw std::runtime_error("simulated failure mid-transaction");
44:         txn.commit();  // unreachable; proves the guard, not this line, cleans up
45:     } catch (const std::runtime_error&) {
46:         caught = true;
47:     }
48:     REQUIRE(caught);
49:     REQUIRE(db.committed().empty());  // the throwing path released, exactly
50:     REQUIRE(db.pendingCount() == 0);  // like the normal exit path above
51: }
52: 
53: TEST_CASE("LoanService.borrow() commits the ledger on success") {
54:     // Integration: the guard is not just testable in isolation, it is wired
55:     // into the real orchestration.
56:     LoanService svc;
57:     svc.addEquipment(Equipment("LP-001", "ThinkPad T14"));
58:     svc.addMember(Member("M-101", "Ayu Lestari", Role::Student));
59:     REQUIRE(svc.borrow("LP-001", "M-101", 7).ok());
60:     REQUIRE(svc.ledger().committed().size() == 2);  // "loan:" and "equipment:" records
61: }
62: 
63: int main() { return test_runner::runAll(); }
`````

Perintah: `nl -ba py/tests/test_cleanup.py`

`````text
1: """Proves txn_guard releases (rolls back) on EVERY exit path, including the
2: raising one -- Lab 2.3's requirement: "a test that throws inside the guarded
3: region and asserts the resource was released."
4: """
5: import pytest
6: 
7: from pinjamlab.domain.equipment import Equipment
8: from pinjamlab.domain.member import Member, Role
9: from pinjamlab.service.database import Database
10: from pinjamlab.service.loan_service import LoanService
11: from pinjamlab.service.txn_guard import txn_guard
12: 
13: 
14: def test_txn_guard_commits_staged_records_become_committed():
15:     db = Database()
16:     with txn_guard(db) as txn:
17:         txn.stage("a")
18:         txn.stage("b")
19:     assert len(db.committed) == 2
20:     assert db.pending_count == 0
21: 
22: 
23: def test_txn_guard_rolls_back_when_an_exception_propagates_through_it():
24:     db = Database()
25:     with pytest.raises(RuntimeError):
26:         with txn_guard(db) as txn:
27:             txn.stage("about to be abandoned")
28:             raise RuntimeError("simulated failure mid-transaction")
29:     assert db.committed == []       # the raising path released, exactly
30:     assert db.pending_count == 0    # like the normal exit path above
31: 
32: 
33: def test_forgetting_with_retains_an_open_handle_until_manually_closed(tmp_path):
34:     handle = open(tmp_path / "unguarded.txt", "w", encoding="utf-8")
35:     try:
36:         with pytest.raises(RuntimeError):
37:             handle.write("partial")
38:             raise RuntimeError("no with statement owns this handle")
39:         assert not handle.closed
40:     finally:
41:         handle.close()
42:     assert handle.closed
43: 
44: 
45: def test_contextmanager_generator_is_lazy():
46:     from unittest.mock import Mock
47: 
48:     db = Mock(spec=Database)
49:     guard = txn_guard(db)
50:     db.begin.assert_not_called()
51:     del guard
52: 
53: 
54: def test_loan_service_borrow_commits_the_ledger_on_success():
55:     svc = LoanService()
56:     svc.add_equipment(Equipment("LP-001", "ThinkPad T14"))
57:     svc.add_member(Member("M-101", "Ayu Lestari", Role.STUDENT))
58:     assert svc.borrow("LP-001", "M-101", 7).ok
59:     assert len(svc.ledger.committed) == 2  # "loan:" and "equipment:" records
60: 
61: 
62: def test_atomic_writer_replaces_only_on_success(tmp_path):
63:     from pathlib import Path
64:     from pinjamlab.io.atomic_writer import atomic_writer
65: 
66:     target = tmp_path / "report.txt"
67:     target.write_text("old", encoding="utf-8")
68:     with atomic_writer(target) as handle:
69:         temporary = Path(handle.name)
70:         assert temporary.parent == target.parent
71:         handle.write("new")
72:         assert target.read_text(encoding="utf-8") == "old"
73:     assert handle.closed
74:     assert target.read_text(encoding="utf-8") == "new"
75:     assert not temporary.exists()
76:     assert list(tmp_path.iterdir()) == [target]
77: 
78: 
79: @pytest.mark.parametrize("existing", [False, True])
80: def test_atomic_writer_cleans_up_on_body_failure(tmp_path, existing):
81:     from pinjamlab.io.atomic_writer import atomic_writer
82: 
83:     target = tmp_path / "report.txt"
84:     if existing:
85:         target.write_text("old", encoding="utf-8")
86:     with pytest.raises(RuntimeError, match="body failed"):
87:         with atomic_writer(target) as handle:
88:             handle.write("partial")
89:             raise RuntimeError("body failed")
90:     assert handle.closed
91:     assert target.exists() == existing
92:     if existing:
93:         assert target.read_text(encoding="utf-8") == "old"
94:     assert list(tmp_path.iterdir()) == ([target] if existing else [])
95: 
96: 
97: def test_atomic_writer_cleans_up_on_replace_failure(tmp_path, monkeypatch):
98:     import importlib
99: 
100:     module = importlib.import_module("pinjamlab.io.atomic_writer")
101:     target = tmp_path / "report.txt"
102:     target.write_text("old", encoding="utf-8")
103: 
104:     def fail_replace(source, destination):
105:         raise OSError("replace failed")
106: 
107:     monkeypatch.setattr(module.os, "replace", fail_replace)
108:     with pytest.raises(OSError, match="replace failed"):
109:         with module.atomic_writer(target) as handle:
110:             handle.write("new")
111:     assert handle.closed
112:     assert target.read_text(encoding="utf-8") == "old"
113:     assert list(tmp_path.iterdir()) == [target]
114: 
115: 
116: def test_atomic_writer_uses_unique_temporary_files(tmp_path):
117:     from pinjamlab.io.atomic_writer import atomic_writer
118: 
119:     target = tmp_path / "report.txt"
120:     with atomic_writer(target) as first:
121:         with atomic_writer(target) as second:
122:             assert first.name != second.name
123:             second.write("second")
124:         first.write("first")
125:     assert target.read_text(encoding="utf-8") == "first"
126:     assert list(tmp_path.iterdir()) == [target]
127: 
128: 
129: def test_atomic_writer_cleans_up_on_write_failure(tmp_path):
130:     from pinjamlab.io.atomic_writer import atomic_writer
131: 
132:     target = tmp_path / "report.txt"
133:     with pytest.raises(TypeError):
134:         with atomic_writer(target) as handle:
135:             handle.write(b"not text")
136:     assert handle.closed
137:     assert list(tmp_path.iterdir()) == []
138: 
139: 
140: def test_atomic_writer_cleans_up_on_base_exception(tmp_path):
141:     from pinjamlab.io.atomic_writer import atomic_writer
142: 
143:     target = tmp_path / "report.txt"
144:     with pytest.raises(KeyboardInterrupt):
145:         with atomic_writer(target) as handle:
146:             handle.write("partial")
147:             raise KeyboardInterrupt()
148:     assert handle.closed
149:     assert list(tmp_path.iterdir()) == []
`````

Perintah: `cat scripts/run_result_asan.sh`

`````text
#!/usr/bin/env bash
# Entire C++ suite, limits demo, and real CLI rejection paths under sanitizers.
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p bin/result-asan
CXX="${CXX:-g++}"
export ASAN_OPTIONS=detect_leaks=1:halt_on_error=1
export UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1
flags=(-std=c++20 -Wall -Wextra -Werror -g -O1 -fno-omit-frame-pointer
       -fsanitize=address,undefined -fno-pie -no-pie -Icpp/include -Icpp/tests)
echo "Sanitizers: $ASAN_OPTIONS; $UBSAN_OPTIONS"
"$CXX" --version
for suite in test_errors test_raii test_result test_app test_robustness; do
    echo "ASan/UBSan build and run: $suite"
    "$CXX" "${flags[@]}" "cpp/tests/$suite.cpp" -o "bin/result-asan/$suite"
    "./bin/result-asan/$suite"
done
"$CXX" "${flags[@]}" tests/limits_demo.cpp -o bin/result-asan/limits_demo
./bin/result-asan/limits_demo
"$CXX" "${flags[@]}" cpp/app/main.cpp -o bin/result-asan/cli
for prefix in '' my-; do
    status=0
    ./bin/result-asan/cli "sample-data/${prefix}bad-requests.csv" \
        2>"bin/result-asan/${prefix}stderr.txt" || status=$?
    test "$status" -eq 1
    diff "sample-data/${prefix}expected-output.txt" "bin/result-asan/${prefix}stderr.txt"
    echo "ASan/UBSan CLI ${prefix}bad-requests.csv: golden exact, exit 1"
done
echo "PASS: all C++ suites, limits demo and both CLI error paths; no sanitizer diagnostics"
`````

Perintah: `./run_tests.sh`

`````text
STDOUT:

STDERR:
/bin/bash: line 1: ./run_tests.sh: Permission denied

exit=126; durasi_detik=0.002
`````

Perintah: `bin/test_result`

`````text
STDOUT:
===============================================================================
Running test suite (7 test cases)...
===============================================================================
PASSED: Result::success carries a value and ok() is true
PASSED: Result::failure carries a message and ok() is false
PASSED: value() on a failed Result throws, rather than returning garbage
PASSED: From-scratch match: Result and throwing agree on well-formed input
PASSED: From-scratch match: Result and throwing agree on every malformed input
PASSED: Borrow Result and throwing twin: identical inputs, messages, types and state
PASSED: Manual union owns nondefault payload across copies, moves and throwing assignments
===============================================================================
All tests finished: 7 passed, 0 failed.
===============================================================================

STDERR:

exit=0; durasi_detik=0.004
`````

Perintah: `bin/test_raii`

`````text
STDOUT:
===============================================================================
Running test suite (4 test cases)...
===============================================================================
PASSED: TxnGuard commits: staged records become committed
PASSED: TxnGuard rolls back on normal scope exit without commit()
PASSED: TxnGuard rolls back when an exception unwinds through it
PASSED: LoanService.borrow() commits the ledger on success
===============================================================================
All tests finished: 4 passed, 0 failed.
===============================================================================

STDERR:

exit=0; durasi_detik=0.003
`````

Perintah: `PYTHONPATH=py .venv/bin/python -m pytest py/tests/test_cleanup.py -v -s`

`````text
STDOUT:
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.2.0, pluggy-1.7.0 -- ~/loanbench/.venv/bin/python
rootdir: ~/loanbench
collecting ... collected 12 items

py/tests/test_cleanup.py::test_txn_guard_commits_staged_records_become_committed PASSED
py/tests/test_cleanup.py::test_txn_guard_rolls_back_when_an_exception_propagates_through_it PASSED
py/tests/test_cleanup.py::test_forgetting_with_retains_an_open_handle_until_manually_closed PASSED
py/tests/test_cleanup.py::test_contextmanager_generator_is_lazy PASSED
py/tests/test_cleanup.py::test_loan_service_borrow_commits_the_ledger_on_success PASSED
py/tests/test_cleanup.py::test_atomic_writer_replaces_only_on_success PASSED
py/tests/test_cleanup.py::test_atomic_writer_cleans_up_on_body_failure[False] PASSED
py/tests/test_cleanup.py::test_atomic_writer_cleans_up_on_body_failure[True] PASSED
py/tests/test_cleanup.py::test_atomic_writer_cleans_up_on_replace_failure PASSED
py/tests/test_cleanup.py::test_atomic_writer_uses_unique_temporary_files PASSED
py/tests/test_cleanup.py::test_atomic_writer_cleans_up_on_write_failure PASSED
py/tests/test_cleanup.py::test_atomic_writer_cleans_up_on_base_exception PASSED

============================== 12 passed in 0.06s ==============================

STDERR:

exit=0; durasi_detik=0.370
`````

Perintah: `PYTHONPATH=py .venv/bin/python -m pytest py/tests/test_result.py -v -s`

`````text
STDOUT:
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.2.0, pluggy-1.7.0 -- ~/loanbench/.venv/bin/python
rootdir: ~/loanbench
collecting ... collected 53 items

py/tests/test_result.py::test_borrow_result_throwing_twin_same_inputs_outcome_and_state[LP-001-M-101-7] PASSED
py/tests/test_result.py::test_borrow_result_throwing_twin_same_inputs_outcome_and_state[LP-002-M-101-7] PASSED
py/tests/test_result.py::test_borrow_result_throwing_twin_same_inputs_outcome_and_state[LP-999-M-101-7] PASSED
py/tests/test_result.py::test_borrow_result_throwing_twin_same_inputs_outcome_and_state[lp-001-M-101-7] PASSED
py/tests/test_result.py::test_borrow_result_throwing_twin_same_inputs_outcome_and_state[LP-001-M-404-7] PASSED
py/tests/test_result.py::test_borrow_result_throwing_twin_same_inputs_outcome_and_state[LP-001-M-101-0] PASSED
py/tests/test_result.py::test_borrow_result_throwing_twin_same_inputs_outcome_and_state[LP-001-M-101-91] PASSED
py/tests/test_result.py::test_borrow_result_throwing_twin_same_inputs_outcome_and_state[LP-004-M-101-7] PASSED
py/tests/test_result.py::test_borrow_result_throwing_twin_same_inputs_outcome_and_state[LP-003-M-102-7] PASSED
py/tests/test_result.py::test_borrow_result_throwing_twin_same_inputs_outcome_and_state[LP-002-M-404-7] PASSED
py/tests/test_result.py::test_borrow_result_throwing_twin_same_inputs_outcome_and_state[LP-002-M-101-0] PASSED
py/tests/test_result.py::test_borrow_result_throwing_twin_same_inputs_outcome_and_state[LP-002-M-102-7] PASSED
py/tests/test_result.py::test_success_carries_a_value_and_ok_is_true PASSED
py/tests/test_result.py::test_failure_carries_a_message_and_ok_is_false PASSED
py/tests/test_result.py::test_value_on_a_failed_result_raises_rather_than_returning_garbage PASSED
py/tests/test_result.py::test_from_scratch_match_agree_on_well_formed_input PASSED
py/tests/test_result.py::test_from_scratch_match_agree_on_every_malformed_input[abc] PASSED
py/tests/test_result.py::test_from_scratch_match_agree_on_every_malformed_input[-3] PASSED
py/tests/test_result.py::test_from_scratch_match_agree_on_every_malformed_input[0] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[7] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[+7] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[0007] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[+0007] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[2147483647] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[-2147483648] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[2147483648] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[-2147483649] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[+2147483648] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[0] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[-0] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[-3] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[+] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[-] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[ 7] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[7 ] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[7\n] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[1_0] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[1.0] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[++7] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[+-7] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[\u0667] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[\uff17] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[\u22127] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[raw25] PASSED
py/tests/test_result.py::test_strict_days_parsing_parity[raw26] PASSED
py/tests/test_result.py::test_empty_and_blank_fields_are_validator_results[-M-101-tag is empty] PASSED
py/tests/test_result.py::test_empty_and_blank_fields_are_validator_results[ \t-M-101-tag is blank] PASSED
py/tests/test_result.py::test_empty_and_blank_fields_are_validator_results[LP-001--memberId is empty] PASSED
py/tests/test_result.py::test_empty_and_blank_fields_are_validator_results[LP-001- \t-memberId is blank] PASSED
py/tests/test_result.py::test_out_of_range_message_preserves_raw_days[2147483648] PASSED
py/tests/test_result.py::test_out_of_range_message_preserves_raw_days[-2147483649] PASSED
py/tests/test_result.py::test_out_of_range_message_preserves_raw_days[+9999999999] PASSED

============================== 53 passed in 0.07s ==============================

STDERR:

exit=0; durasi_detik=0.384
`````

Hasil node/robustness tersedia di log ignored command-031.txt dan run Bash aktual di atas.


Eksekusi langsung ./run_tests.sh exit126 Permission denied; permission tidak diubah. Eksekusi eksplisit Bash berikut berhasil:35 testcase C++ utama (8+4+7+2+14),2 demo C++,111 Python.

Perintah: `bash ./run_tests.sh`

`````text
STDOUT:
================================================================================
 [PinjamLab M3] g++ (Ubuntu 15.2.0-16ubuntu1) 15.2.0
 [PinjamLab M3] Python 3.14.4
================================================================================

>>> [1/5] Dependency gate (C++ includes and Python AST)
PASS: dependency directions and domain I/O purity (56 local dependencies)

>>> [2/5] Building C++20 tests (-Wall -Wextra -Werror)

>>> [3/5] Running C++20 test suites
===============================================================================
Running test suite (8 test cases)...
===============================================================================
PASSED: UnknownAssetTag: unknown tag, carries the tag
PASSED: UnknownMember: unknown member, carries the id
PASSED: InvalidLoanDuration: business-rule maximum, not the format check
PASSED: EquipmentUnavailable: already on loan returns the same message
PASSED: QuotaExceeded: over quota, carries active and limit
PASSED: Remaining thrown service errors are catchable as LoanError
PASSED: Catch order: most-specific handler runs when listed first
PASSED: A successful borrow raises nothing and updates both entities
===============================================================================
All tests finished: 8 passed, 0 failed.
===============================================================================
===============================================================================
Running test suite (4 test cases)...
===============================================================================
PASSED: TxnGuard commits: staged records become committed
PASSED: TxnGuard rolls back on normal scope exit without commit()
PASSED: TxnGuard rolls back when an exception unwinds through it
PASSED: LoanService.borrow() commits the ledger on success
===============================================================================
All tests finished: 4 passed, 0 failed.
===============================================================================
===============================================================================
Running test suite (7 test cases)...
===============================================================================
PASSED: Result::success carries a value and ok() is true
[... total 221 baris; lengkap tersanitasi bin/analisis-export/full-tests-final.txt ...]
py/tests/test_result.py::test_strict_days_parsing_parity[-3] PASSED      [ 73%]
py/tests/test_result.py::test_strict_days_parsing_parity[] PASSED        [ 74%]
py/tests/test_result.py::test_strict_days_parsing_parity[+] PASSED       [ 75%]
py/tests/test_result.py::test_strict_days_parsing_parity[-] PASSED       [ 76%]
py/tests/test_result.py::test_strict_days_parsing_parity[ 7] PASSED      [ 77%]
py/tests/test_result.py::test_strict_days_parsing_parity[7 ] PASSED      [ 78%]
py/tests/test_result.py::test_strict_days_parsing_parity[7\n] PASSED     [ 79%]
py/tests/test_result.py::test_strict_days_parsing_parity[1_0] PASSED     [ 80%]
py/tests/test_result.py::test_strict_days_parsing_parity[1.0] PASSED     [ 81%]
py/tests/test_result.py::test_strict_days_parsing_parity[++7] PASSED     [ 81%]
py/tests/test_result.py::test_strict_days_parsing_parity[+-7] PASSED     [ 82%]
py/tests/test_result.py::test_strict_days_parsing_parity[\u0667] PASSED  [ 83%]
py/tests/test_result.py::test_strict_days_parsing_parity[\uff17] PASSED  [ 84%]
py/tests/test_result.py::test_strict_days_parsing_parity[\u22127] PASSED [ 85%]
py/tests/test_result.py::test_strict_days_parsing_parity[raw25] PASSED   [ 86%]
py/tests/test_result.py::test_strict_days_parsing_parity[raw26] PASSED   [ 87%]
py/tests/test_result.py::test_empty_and_blank_fields_are_validator_results[-M-101-tag is empty] PASSED [ 88%]
py/tests/test_result.py::test_empty_and_blank_fields_are_validator_results[ \t-M-101-tag is blank] PASSED [ 89%]
py/tests/test_result.py::test_empty_and_blank_fields_are_validator_results[LP-001--memberId is empty] PASSED [ 90%]
py/tests/test_result.py::test_empty_and_blank_fields_are_validator_results[LP-001- \t-memberId is blank] PASSED [ 90%]
py/tests/test_result.py::test_out_of_range_message_preserves_raw_days[2147483648] PASSED [ 91%]
py/tests/test_result.py::test_out_of_range_message_preserves_raw_days[-2147483649] PASSED [ 92%]
py/tests/test_result.py::test_out_of_range_message_preserves_raw_days[+9999999999] PASSED [ 93%]
py/tests/test_robustness.py::test_reservation_lives_on_equipment_and_reserve_updates_it PASSED [ 94%]
py/tests/test_robustness.py::test_direct_service_duration_bounds_preserve_error_and_state[0] PASSED [ 95%]
py/tests/test_robustness.py::test_direct_service_duration_bounds_preserve_error_and_state[-1] PASSED [ 96%]
py/tests/test_robustness.py::test_direct_service_duration_bounds_preserve_error_and_state[-2147483648] PASSED [ 97%]
py/tests/test_robustness.py::test_direct_service_duration_bounds_preserve_error_and_state[91] PASSED [ 98%]
py/tests/test_robustness.py::test_case_suggestions_fold_ascii_only PASSED [ 99%]
py/tests/test_robustness.py::test_wrong_owner_return_preserves_state_and_correct_owner_can_return PASSED [100%]

============================= 111 passed in 2.20s ==============================

================================================================================
 [SUCCESS] Purity check, C++ suites, golden file, and Python suite all passed.
================================================================================

STDERR:

exit=0; durasi_detik=15.825
`````

Perintah: `PYTHONPATH=py .venv/bin/python -m pytest py/tests/test_errors.py py/tests/test_robustness.py -v -s`

`````text
STDOUT:
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.2.0, pluggy-1.7.0 -- ~/loanbench/.venv/bin/python
rootdir: ~/loanbench
collecting ... collected 23 items

py/tests/test_errors.py::test_unknown_asset_tag_carries_the_tag PASSED
py/tests/test_errors.py::test_unknown_member_carries_the_id PASSED
py/tests/test_errors.py::test_invalid_loan_duration_is_the_business_rule_maximum PASSED
py/tests/test_errors.py::test_equipment_unavailable_returns_same_message PASSED
py/tests/test_errors.py::test_quota_exceeded_carries_active_and_limit PASSED
py/tests/test_errors.py::test_remaining_thrown_service_errors_are_catchable_as_loan_error PASSED
py/tests/test_errors.py::test_a_bare_except_would_also_catch_keyboard_interrupt_dont_write_one PASSED
py/tests/test_errors.py::test_a_successful_borrow_raises_nothing_and_updates_both_entities PASSED
py/tests/test_errors.py::test_case_mismatch_fields_message_and_family PASSED
py/tests/test_errors.py::test_reservation_fields_message_family_and_allowed_member PASSED
py/tests/test_errors.py::test_duplicate_equipment_preserves_original PASSED
py/tests/test_errors.py::test_invalid_returns_raise_without_mutation[LP-999-M-101-UnknownAssetTag-Unknown asset tag: LP-999] PASSED
py/tests/test_errors.py::test_invalid_returns_raise_without_mutation[LP-002-M-404-UnknownMember-Unknown member: M-404] PASSED
py/tests/test_errors.py::test_invalid_returns_raise_without_mutation[LP-001-M-101-LoanError-Equipment is not on loan: LP-001] PASSED
py/tests/test_errors.py::test_invalid_returns_raise_without_mutation[LP-002-M-101-LoanError-Equipment not loaned to member: LP-002 for M-101] PASSED
py/tests/test_errors.py::test_return_updates_owner_once_and_allows_reborrow PASSED
py/tests/test_robustness.py::test_reservation_lives_on_equipment_and_reserve_updates_it PASSED
py/tests/test_robustness.py::test_direct_service_duration_bounds_preserve_error_and_state[0] PASSED
py/tests/test_robustness.py::test_direct_service_duration_bounds_preserve_error_and_state[-1] PASSED
py/tests/test_robustness.py::test_direct_service_duration_bounds_preserve_error_and_state[-2147483648] PASSED
py/tests/test_robustness.py::test_direct_service_duration_bounds_preserve_error_and_state[91] PASSED
py/tests/test_robustness.py::test_case_suggestions_fold_ascii_only PASSED
py/tests/test_robustness.py::test_wrong_owner_return_preserves_state_and_correct_owner_can_return PASSED

============================== 23 passed in 0.04s ==============================

STDERR:

exit=0; durasi_detik=0.348
`````

## §8 Bahan A3 (pembelaan node #1)

Rujukan implementasi nyata: AssetTagCaseMismatch pada domain/loan_error dan pencarian fallback service; ReservationConflict pada domain/loan_error serta Equipment.reservedFor/reserved_for. Sumber bernomor §4 dan diff §4 memuat kode kedua node beserta pengujiannya. Saat tag tidak ditemukan dengan ejaan eksak tetapi sama setelah ASCII fold, node #1 memberi suggestion; ketika tag sudah dipinjam, unavailable diperiksa lebih dahulu daripada reservasi. Reservasi owner kosong berarti tidak ada reservasi, dan holder yang sama boleh borrow.

Eksperimen eksplorasi node baru yang mengubah desain: TIDAK DILAKUKAN. Eksperimen yang membutuhkan akses di luar repo: TIDAK DILAKUKAN karena batas lokasi kerja; tidak ada akses lokasi lain yang diada-adakan. Pengujian yang sudah ada dijalankan di §7, bukan dilabeli eksperimen baru. Alasan pribadi untuk node #1 sebagai error alih-alih Result tetap kosong di §14.

Perintah: `nl -ba cpp/include/pinjamlab/domain/equipment.hpp`

`````text
1: #ifndef PINJAMLAB_DOMAIN_EQUIPMENT_HPP
2: #define PINJAMLAB_DOMAIN_EQUIPMENT_HPP
3: 
4: // PURE domain header: entity carried forward from Modules 1-2. Module 3 does
5: // not need the polymorphic Equipment hierarchy (that lesson is done); this is
6: // the concrete shape LoanService actually holds in its catalogue.
7: 
8: #include "pinjamlab/domain/loan_error.hpp"
9: 
10: #include <string>
11: #include <utility>
12: 
13: namespace pinjamlab {
14: 
15: enum class EquipmentState { Available, Loaned };
16: 
17: class Equipment {
18:     std::string tag_;
19:     std::string model_;
20:     EquipmentState state_ = EquipmentState::Available;
21:     std::string reservedFor_;  // Empty means no reservation.
22: 
23: public:
24:     Equipment(std::string tag, std::string model, std::string reservedFor = "")
25:         : tag_(std::move(tag)), model_(std::move(model)),
26:           reservedFor_(std::move(reservedFor)) {}
27:     [[nodiscard]] const std::string& reservedFor() const noexcept { return reservedFor_; }
28: 
29:     [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
30:     [[nodiscard]] const std::string& model() const noexcept { return model_; }
31:     [[nodiscard]] EquipmentState state() const noexcept { return state_; }
32:     [[nodiscard]] bool isAvailable() const noexcept { return state_ == EquipmentState::Available; }
33: 
34:     void markLoaned() {
35:         if (!isAvailable()) throw EquipmentUnavailable(tag_);
36:         state_ = EquipmentState::Loaned;
37:     }
38: 
39:     void markReturned() { state_ = EquipmentState::Available; }
40: };
41: 
42: }  // namespace pinjamlab
43: 
44: #endif  // PINJAMLAB_DOMAIN_EQUIPMENT_HPP
`````

Perintah: `nl -ba py/pinjamlab/domain/equipment.py`

`````text
1: """Pure domain module: Equipment entity, carried forward from Modules 1-2."""
2: from __future__ import annotations
3: 
4: from enum import Enum, auto
5: 
6: from .loan_error import EquipmentUnavailable
7: 
8: 
9: class EquipmentState(Enum):
10:     AVAILABLE = auto()
11:     LOANED = auto()
12: 
13: 
14: class Equipment:
15:     def __init__(self, tag: str, model: str, reserved_for: str = "") -> None:
16:         self.tag = tag
17:         self.model = model
18:         self.reserved_for = reserved_for
19:         self._state = EquipmentState.AVAILABLE
20: 
21:     @property
22:     def state(self) -> EquipmentState:
23:         return self._state
24: 
25:     def is_available(self) -> bool:
26:         return self._state == EquipmentState.AVAILABLE
27: 
28:     def mark_loaned(self) -> None:
29:         if not self.is_available():
30:             raise EquipmentUnavailable(self.tag)
31:         self._state = EquipmentState.LOANED
32: 
33:     def mark_returned(self) -> None:
34:         self._state = EquipmentState.AVAILABLE
`````

## §9 Bahan A4 (keterbatasan Result<T>)

Keterbatasan terukur pertama: rantai 33 frame memerlukan penerusan failure eksplisit pada setiap frame; test juga memeriksa alternate success value 39. Kedua: signature callback void C++ tidak dapat mengembalikan Result sehingga perlu adapter throw; Python dapat membuang failure tanpa warning, diperagakan operation() yang tidak diperiksa lalu varian checked. nodiscard C++ hanya diagnostik compile dan dapat ditekan cast void, bukan jaminan pemakaian runtime. Kontrak borrow campuran Result dan exception juga membuat caller tetap perlu try/catch. Ini analisis teknis, bukan pendapat pribadi mahasiswa yang belum ditulis.

Perintah: `cat tests/limits_demo.cpp`

`````text
#include "mini_catch.hpp"
#include "pinjamlab/domain/result.hpp"
#include <functional>

using pinjamlab::Result;

static Result<int> deepChain(int depth, bool fail, int& visited) {
    ++visited;
    if (depth == 0)
        return fail ? Result<int>::failure("leaf unavailable") : Result<int>::success(7);
    const auto child = deepChain(depth - 1, fail, visited);
    if (!child.ok()) return Result<int>::failure(child.error());
    return Result<int>::success(child.value() + 1);
}

TEST_CASE("Limits demo: deep chain explicitly propagates failure through every frame") {
    int visited = 0;
    const auto failed = deepChain(32, true, visited);
    REQUIRE(visited == 33);
    REQUIRE(!failed.ok());
    REQUIRE(failed.error() == "leaf unavailable");
    visited = 0;
    const auto success = deepChain(32, false, visited);
    REQUIRE(success.ok());
    REQUIRE(success.value() == 39);
    REQUIRE(visited == 33);
}

TEST_CASE("Limits demo: fixed void callback cannot return Result and needs an adapter") {
    std::function<void()> callback = [] {
        const auto result = Result<int>::failure("callback unavailable");
        if (!result.ok()) throw std::runtime_error(result.error());
    };
    REQUIRE_THROWS_AS(callback(), std::runtime_error);
}

int main() { return test_runner::runAll(); }
`````

Perintah: `cat tests/limits_demo.py`

`````text
"""Runnable assertions illustrating Result's explicit propagation cost."""
from pinjamlab.domain.result import Result

def deep_chain(depth, fail, visited):
    visited.append(depth)
    if depth == 0:
        return Result.failure("leaf unavailable") if fail else Result.success(7)
    child = deep_chain(depth - 1, fail, visited)
    if not child.ok:
        return Result.failure(child.error)
    return Result.success(child.value + 1)

def main():
    visited = []
    failed = deep_chain(32, True, visited)
    assert len(visited) == 33
    assert not failed.ok and failed.error == "leaf unavailable"
    visited.clear()
    success = deep_chain(32, False, visited)
    assert success.ok and success.value == 39 and len(visited) == 33
    print("PASSED: limits_demo deep chain explicit propagation")

    calls = []

    def operation():
        calls.append("attempted")
        return Result.failure("ignored unavailable")

    operation()  # Python has no nodiscard warning: a failure can be ignored.
    assert calls == ["attempted"]
    checked = operation()
    assert not checked.ok and checked.error == "ignored unavailable"
    print("PASSED: limits_demo Python can silently ignore a failed Result")

if __name__ == "__main__":
    main()
`````

Perintah: `g++ -std=c++20 -Wall -Wextra -Werror -Icpp/include -Icpp/tests tests/limits_demo.cpp -o bin/analisis-export/limits_demo && bin/analisis-export/limits_demo`

`````text
STDOUT:
===============================================================================
Running test suite (2 test cases)...
===============================================================================
PASSED: Limits demo: deep chain explicitly propagates failure through every frame
PASSED: Limits demo: fixed void callback cannot return Result and needs an adapter
===============================================================================
All tests finished: 2 passed, 0 failed.
===============================================================================

STDERR:

exit=0; durasi_detik=1.004
`````

Perintah: `PYTHONPATH=py .venv/bin/python tests/limits_demo.py`

`````text
STDOUT:
PASSED: limits_demo deep chain explicit propagation
PASSED: limits_demo Python can silently ignore a failed Result

STDERR:

exit=0; durasi_detik=0.052
`````

## §10 Bahan A5 (viva)

Latihan viva dan catatan jawaban spontan: TIDAK ADA. Mutasi berikut hanya pada temporary directory dalam bin, dihapus setelah eksperimen. Tuple argumen aktual dan stdout/stderr/exit dicatat sehingga penolakan compiler/gate tidak disamarkan sebagai test produksi gagal.

Input mutasi yang dibuat otomatis persis: Python `import csv` dalam domain; C++ include pinjamlab/io/csv_reader.hpp dalam domain; program C++ main membuat LoanService lalu memanggil borrow tanpa memakai return. Dua probe pertama diharapkan gate exit 1; ketiga compiler exit 1 karena nodiscard dengan -Werror. Tidak ada mutasi CsvReader hidup, tidak ada perubahan test agar hijau palsu. Mutation suite yang lebih luas tercatat §5.

Perintah: `.venv/bin/python scripts/check_dependencies.py bin/analisis-export/mutation`

`````text
STDOUT:
cpp/include/pinjamlab/domain/csv_probe.hpp:1: domain I/O include: pinjamlab/io/csv_reader.hpp
cpp/include/pinjamlab/domain/csv_probe.hpp:1: forbidden domain -> io: pinjamlab/io/csv_reader.hpp
py/pinjamlab/domain/csv_probe.py:1: domain I/O import: csv
FAIL: 3 dependency/purity violation(s)

STDERR:

exit=1; durasi_detik=0.081
`````

Perintah: `g++ -std=c++20 -Wall -Wextra -Werror -Ibin/analisis-export/mutation/cpp/include -fsyntax-only bin/analisis-export/mutation/csv_probe.cpp`

`````text
STDOUT:

STDERR:

exit=0; durasi_detik=0.466
`````

Perintah: `g++ -std=c++20 -Wall -Wextra -Werror -Ibin/analisis-export/mutation/cpp/include -fsyntax-only bin/analisis-export/mutation/ignored_result.cpp`

`````text
STDOUT:

STDERR:
bin/analisis-export/mutation/ignored_result.cpp: In function ‘int main()’:
bin/analisis-export/mutation/ignored_result.cpp:2:52: error: ignoring return value of ‘pinjamlab::Result<pinjamlab::Loan> pinjamlab::LoanService::borrow(const std::string&, const std::string&, int)’, declared with attribute ‘nodiscard’ [-Werror=unused-result]
    2 | int main() { pinjamlab::LoanService svc; svc.borrow("LP-001", "M-101", 7); }
      |                                          ~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~
In file included from bin/analisis-export/mutation/ignored_result.cpp:1:
bin/analisis-export/mutation/cpp/include/pinjamlab/service/loan_service.hpp:49:32: note: declared here
   49 |     [[nodiscard]] Result<Loan> borrow(const std::string& tag, const std::string& memberId, int days) {
      |                                ^~~~~~
cc1plus: all warnings being treated as errors

exit=1; durasi_detik=0.588
`````

Perintah: `PYTHONPATH=py .venv/bin/python -m pytest py/tests/test_dependency_gate.py -v -s -k "domain_io_rejected or each_forbidden_direction"`

`````text
STDOUT:
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.2.0, pluggy-1.7.0 -- ~/loanbench/.venv/bin/python
rootdir: ~/loanbench
collecting ... collected 19 items / 2 deselected / 17 selected

py/tests/test_dependency_gate.py::test_each_forbidden_direction[cpp-domain-io] REJECTED cpp domain -> io: cpp/include/pinjamlab/domain/gate_probe.hpp:1: forbidden domain -> io: pinjamlab/io/gate_probe.hpp
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[cpp-domain-service] REJECTED cpp domain -> service: cpp/include/pinjamlab/domain/gate_probe.hpp:1: forbidden domain -> service: pinjamlab/service/gate_probe.hpp
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[cpp-domain-app] REJECTED cpp domain -> app: cpp/include/pinjamlab/domain/gate_probe.hpp:1: forbidden domain -> app: pinjamlab/app/gate_probe.hpp
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[cpp-io-service] REJECTED cpp io -> service: cpp/include/pinjamlab/io/gate_probe.hpp:1: forbidden io -> service: pinjamlab/service/gate_probe.hpp
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[cpp-io-app] REJECTED cpp io -> app: cpp/include/pinjamlab/io/gate_probe.hpp:1: forbidden io -> app: pinjamlab/app/gate_probe.hpp
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[cpp-service-app] REJECTED cpp service -> app: cpp/include/pinjamlab/service/gate_probe.hpp:1: forbidden service -> app: pinjamlab/app/gate_probe.hpp
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[py-domain-io] REJECTED py domain -> io: py/pinjamlab/domain/gate_probe.py:1: forbidden domain -> io: pinjamlab.io.gate_probe
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[py-domain-service] REJECTED py domain -> service: py/pinjamlab/domain/gate_probe.py:1: forbidden domain -> service: pinjamlab.service.gate_probe
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[py-domain-app] REJECTED py domain -> app: py/pinjamlab/domain/gate_probe.py:1: forbidden domain -> app: pinjamlab.app.gate_probe
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[py-io-service] REJECTED py io -> service: py/pinjamlab/io/gate_probe.py:1: forbidden io -> service: pinjamlab.service.gate_probe
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[py-io-app] REJECTED py io -> app: py/pinjamlab/io/gate_probe.py:1: forbidden io -> app: pinjamlab.app.gate_probe
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_each_forbidden_direction[py-service-app] REJECTED py service -> app: py/pinjamlab/service/gate_probe.py:1: forbidden service -> app: pinjamlab.app.gate_probe
FAIL: 1 dependency/purity violation(s)
PASSED
py/tests/test_dependency_gate.py::test_domain_io_rejected[py-def hidden():\n    import csv as c\n] PASSED
py/tests/test_dependency_gate.py::test_domain_io_rejected[py-from builtins import open as op\nop('file')\n] PASSED
py/tests/test_dependency_gate.py::test_domain_io_rejected[py-print('forbidden')\n] PASSED
py/tests/test_dependency_gate.py::test_domain_io_rejected[cpp-#include <fstream>\n] PASSED
py/tests/test_dependency_gate.py::test_domain_io_rejected[cpp-void probe() { std::cout << 1; }\n] PASSED

======================= 17 passed, 2 deselected in 1.76s =======================

STDERR:

exit=0; durasi_detik=2.066
`````

Perintah: `cat bin/analisis-export/mutation/py/pinjamlab/domain/csv_probe.py`

`````text
import csv
`````

Perintah: `cat bin/analisis-export/mutation/cpp/include/pinjamlab/domain/csv_probe.hpp`

`````text
#include "pinjamlab/io/csv_reader.hpp"
`````

Perintah: `cat bin/analisis-export/mutation/csv_probe.cpp`

`````text
#include "pinjamlab/domain/csv_probe.hpp"
int main() { return 0; }
`````

Perintah: `cat bin/analisis-export/mutation/ignored_result.cpp`

`````text
#include "pinjamlab/service/loan_service.hpp"
int main() { pinjamlab::LoanService svc; svc.borrow("LP-001", "M-101", 7); }
`````

## §11 Jebakan yang dihindari (bukti, bukan klaim)

Audit faktual/T5: tidak semua catch(...) adalah defect. Service C++ kompensasi lalu throw; report constructor remove lalu throw; destructor report close catch kosong disengaja menjaga noexcept, tetapi tidak melaporkan error. Test robustness mempunyai catch kosong terkontrol untuk menguji cleanup (bukan handler produksi). TxnGuard C++ mencetak kegagalan rollback tanpa melempar dari destructor; Python guard mencetak kegagalan rollback lalu bare raise mempertahankan exception semula. Ini log cleanup-error + rethrow original, berbeda dari log-and-rethrow pesan error yang sama berulang di tiap layer. Runner C++ menangkap const reference (tidak slicing catch by value); Python mismatch/reservasi mendahului LoanError. Bare except produksi yang menelan error ada pada baseline rekonstruksi pra-fix A, bukan runner HEAD. Tidak ada klaim grep saja membuktikan seluruh keamanan: C++ parser dan Python AST gate juga punya batas pada alias/dynamic import, macro dan include kondisional. Tidak ada transformasi chain `raise ... from ...` yang dikarang; exception asli pada guard diteruskan dengan raise. Komentar sumber yang menyebut grep, ONE place, atau zero try/catch dapat kedaluwarsa: service kini punya kompensasi catch, runner tidak menetapkan exit proses sendiri, CLI yang mengembalikan exit.

Perintah: `grep -RnE 'catch[[:space:]]*\(|except([[:space:]:]|$)|return True|raise .* from |throw;|std::cerr|file=sys.stderr' cpp/include cpp/app py/pinjamlab --include='*.hpp' --include='*.cpp' --include='*.py'`

`````text
STDOUT:
cpp/include/pinjamlab/io/report_writer.hpp:39:        } catch (...) {
cpp/include/pinjamlab/io/report_writer.hpp:42:            throw;
cpp/include/pinjamlab/io/report_writer.hpp:47:    ~ScopedReportFile() noexcept {
cpp/include/pinjamlab/io/report_writer.hpp:48:        try { if (output_.is_open()) output_.close(); } catch (...) {}
cpp/include/pinjamlab/io/report_writer.hpp:54:    [[nodiscard]] std::ostream& stream() noexcept { return output_; }
cpp/include/pinjamlab/io/report_writer.hpp:55:    [[nodiscard]] const std::filesystem::path& temporaryPath() const noexcept { return temporary_; }
cpp/include/pinjamlab/app/runner.hpp:25:    [[nodiscard]] int exitCode() const noexcept { return rejected == 0 ? 0 : 1; }
cpp/include/pinjamlab/app/runner.hpp:57:        } catch (const AssetTagCaseMismatch& e) {
cpp/include/pinjamlab/app/runner.hpp:62:        } catch (const LoanError& e) {  // the family we understand
cpp/include/pinjamlab/domain/result.hpp:19:        Storage() noexcept {}
cpp/include/pinjamlab/domain/result.hpp:20:        ~Storage() noexcept {}
cpp/include/pinjamlab/domain/result.hpp:70:    [[nodiscard]] bool ok() const noexcept { return ok_; }
cpp/include/pinjamlab/domain/result.hpp:71:    [[nodiscard]] const std::string& error() const noexcept { return error_; }
cpp/include/pinjamlab/domain/equipment.hpp:27:    [[nodiscard]] const std::string& reservedFor() const noexcept { return reservedFor_; }
cpp/include/pinjamlab/domain/equipment.hpp:29:    [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
cpp/include/pinjamlab/domain/equipment.hpp:30:    [[nodiscard]] const std::string& model() const noexcept { return model_; }
cpp/include/pinjamlab/domain/equipment.hpp:31:    [[nodiscard]] EquipmentState state() const noexcept { return state_; }
cpp/include/pinjamlab/domain/equipment.hpp:32:    [[nodiscard]] bool isAvailable() const noexcept { return state_ == EquipmentState::Available; }
cpp/include/pinjamlab/domain/loan.hpp:22:    [[nodiscard]] const std::string& id() const noexcept { return id_; }
cpp/include/pinjamlab/domain/loan.hpp:23:    [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
cpp/include/pinjamlab/domain/loan.hpp:24:    [[nodiscard]] const std::string& memberId() const noexcept { return memberId_; }
cpp/include/pinjamlab/domain/loan.hpp:25:    [[nodiscard]] int days() const noexcept { return days_; }
cpp/include/pinjamlab/domain/member.hpp:27:    [[nodiscard]] const std::string& id() const noexcept { return id_; }
cpp/include/pinjamlab/domain/member.hpp:28:    [[nodiscard]] const std::string& name() const noexcept { return name_; }
cpp/include/pinjamlab/domain/member.hpp:29:    [[nodiscard]] int maxLoans() const noexcept { return static_cast<int>(role_); }
cpp/include/pinjamlab/domain/member.hpp:30:    [[nodiscard]] int activeLoans() const noexcept { return activeLoans_; }
cpp/include/pinjamlab/domain/member.hpp:31:    [[nodiscard]] bool canBorrow() const noexcept { return activeLoans_ < maxLoans(); }
cpp/include/pinjamlab/domain/loan_error.hpp:19:    [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
cpp/include/pinjamlab/domain/loan_error.hpp:28:    [[nodiscard]] const std::string& given() const noexcept { return tag(); }
cpp/include/pinjamlab/domain/loan_error.hpp:29:    [[nodiscard]] const std::string& suggestion() const noexcept { return suggestion_; }
cpp/include/pinjamlab/domain/loan_error.hpp:37:    [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
cpp/include/pinjamlab/domain/loan_error.hpp:38:    [[nodiscard]] const std::string& reservedFor() const noexcept { return reservedFor_; }
cpp/include/pinjamlab/domain/loan_error.hpp:45:    [[nodiscard]] const std::string& memberId() const noexcept { return memberId_; }
cpp/include/pinjamlab/domain/loan_error.hpp:53:    [[nodiscard]] int days() const noexcept { return days_; }
cpp/include/pinjamlab/domain/loan_error.hpp:54:    [[nodiscard]] int maxDays() const noexcept { return maxDays_; }
cpp/include/pinjamlab/domain/loan_error.hpp:61:    [[nodiscard]] const std::string& tag() const noexcept { return tag_; }
cpp/include/pinjamlab/domain/loan_error.hpp:69:    [[nodiscard]] int active() const noexcept { return active_; }
cpp/include/pinjamlab/domain/loan_error.hpp:70:    [[nodiscard]] int limit() const noexcept { return limit_; }
cpp/include/pinjamlab/service/database.hpp:29:    [[nodiscard]] const std::vector<std::string>& committed() const noexcept { return committed_; }
cpp/include/pinjamlab/service/database.hpp:30:    [[nodiscard]] std::size_t pendingCount() const noexcept { return pending_.size(); }
cpp/include/pinjamlab/service/txn_guard.hpp:34:    ~TxnGuard() noexcept {  // noexcept: destructors must NOT throw
cpp/include/pinjamlab/service/txn_guard.hpp:38:        } catch (...) {
cpp/include/pinjamlab/service/txn_guard.hpp:41:            std::cerr << "rollback failed during unwind\n";
cpp/include/pinjamlab/service/loan_service.hpp:83:        } catch (...) {
cpp/include/pinjamlab/service/loan_service.hpp:85:            throw;                 // never called, so the guard still rolls
cpp/include/pinjamlab/service/loan_service.hpp:109:    [[nodiscard]] const Database& ledger() const noexcept { return db_; }
cpp/app/main.cpp:20:        std::cerr << line << "\n";
py/pinjamlab/app/runner.py:54:        except AssetTagCaseMismatch as e:
py/pinjamlab/app/runner.py:59:        except ReservationConflict as e:
py/pinjamlab/app/runner.py:64:        except LoanError as e:  # the family we understand
py/pinjamlab/app/main.py:23:        print(line, file=sys.stderr)
py/pinjamlab/service/loan_service.py:92:            except Exception:
py/pinjamlab/service/txn_guard.py:4:`raise` in the except clause is essential -- without it this would silently
py/pinjamlab/service/txn_guard.py:22:    except Exception:
py/pinjamlab/service/txn_guard.py:25:        except Exception:
py/pinjamlab/service/txn_guard.py:29:            print("rollback failed during unwind", file=sys.stderr)

STDERR:

exit=0; durasi_detik=0.007
`````

Perintah: `grep -RnE 'catch[[:space:]]*\([^&)]*\)|except[[:space:]]*:|catch.*\{[[:space:]]*\}|return True|__exit__' cpp py --include='*.hpp' --include='*.cpp' --include='*.py'`

`````text
STDOUT:
cpp/tests/mini_catch.hpp:43:        } catch (...) {
cpp/tests/mini_catch.hpp:80:        } catch (...) {} \
cpp/tests/test_robustness.cpp:170:    } catch (const std::runtime_error&) {}
cpp/include/pinjamlab/io/report_writer.hpp:39:        } catch (...) {
cpp/include/pinjamlab/io/report_writer.hpp:48:        try { if (output_.is_open()) output_.close(); } catch (...) {}
cpp/include/pinjamlab/service/txn_guard.hpp:34:    ~TxnGuard() noexcept {  // noexcept: destructors must NOT throw
cpp/include/pinjamlab/service/txn_guard.hpp:38:        } catch (...) {
cpp/include/pinjamlab/service/loan_service.hpp:83:        } catch (...) {
py/tests/test_errors.py:79:    # never a bare `except:`.
py/pinjamlab/service/txn_guard.py:27:            # exception escaping __exit__ during unwinding would replace

STDERR:

exit=0; durasi_detik=0.007
`````

## §12 Perbandingan bahasa & biaya

LOC adalah baris fisik termasuk komentar dan blank, bukan logical LOC. Header C++ dan translation unit dipisah untuk menghindari hitungan ganda tiap include; module Python termasuk __init__ kosong. Delta adalah terhadap 5b26936, bukan starter asli. Durasi build/test/sanitizer tercatat di blok perintah §3/§7; tidak ada benchmark lintas sistem. Jika mypy/pyflakes tidak tersedia, kualitas statis itu BELUM DIVERIFIKASI, bukan dianggap lolos; tidak memasang dependency baru.

Perintah: `git ls-files 'cpp/*.cpp' 'cpp/**/*.hpp' 'cpp/**/*.cpp' 'py/**/*.py' 'scripts/*.py' 'tests/*' | xargs wc -l; git diff --numstat 5b26936 HEAD -- cpp py scripts tests run_tests.sh sample-data; git diff --shortstat 5b26936 HEAD -- cpp py scripts tests run_tests.sh sample-data`

`````text
STDOUT:
    26 cpp/app/main.cpp
    75 cpp/include/pinjamlab/app/runner.hpp
    48 cpp/include/pinjamlab/app/seed.hpp
    44 cpp/include/pinjamlab/domain/equipment.hpp
    30 cpp/include/pinjamlab/domain/loan.hpp
    73 cpp/include/pinjamlab/domain/loan_error.hpp
    51 cpp/include/pinjamlab/domain/member.hpp
    84 cpp/include/pinjamlab/domain/result.hpp
    53 cpp/include/pinjamlab/io/csv_reader.hpp
    83 cpp/include/pinjamlab/io/report_writer.hpp
    41 cpp/include/pinjamlab/io/validator.hpp
    35 cpp/include/pinjamlab/service/database.hpp
   120 cpp/include/pinjamlab/service/loan_service.hpp
    48 cpp/include/pinjamlab/service/txn_guard.hpp
    87 cpp/tests/mini_catch.hpp
    58 cpp/tests/test_app.cpp
   113 cpp/tests/test_errors.cpp
    63 cpp/tests/test_raii.cpp
   222 cpp/tests/test_result.cpp
   274 cpp/tests/test_robustness.cpp
     0 py/pinjamlab/__init__.py
     0 py/pinjamlab/app/__init__.py
    30 py/pinjamlab/app/main.py
    70 py/pinjamlab/app/runner.py
    29 py/pinjamlab/app/seed.py
     0 py/pinjamlab/domain/__init__.py
    34 py/pinjamlab/domain/equipment.py
    12 py/pinjamlab/domain/loan.py
    66 py/pinjamlab/domain/loan_error.py
    45 py/pinjamlab/domain/member.py
    28 py/pinjamlab/domain/result.py
     0 py/pinjamlab/io/__init__.py
    25 py/pinjamlab/io/atomic_writer.py
    37 py/pinjamlab/io/csv_reader.py
    12 py/pinjamlab/io/report_writer.py
    43 py/pinjamlab/io/validator.py
     0 py/pinjamlab/service/__init__.py
    31 py/pinjamlab/service/database.py
   113 py/pinjamlab/service/loan_service.py
    32 py/pinjamlab/service/txn_guard.py
    69 py/tests/test_app.py
   149 py/tests/test_cleanup.py
    73 py/tests/test_dependency_gate.py
   163 py/tests/test_errors.py
   163 py/tests/test_result.py
    84 py/tests/test_robustness.py
    38 scripts/audit_result_calls.py
   134 scripts/check_dependencies.py
    56 scripts/count_callsites.py
    73 scripts/gen_graphs.py
    37 tests/limits_demo.cpp
    39 tests/limits_demo.py
  3313 total
7	1	cpp/include/pinjamlab/app/runner.hpp
6	3	cpp/include/pinjamlab/app/seed.hpp
52	8	cpp/include/pinjamlab/domain/result.hpp
5	3	cpp/include/pinjamlab/service/loan_service.hpp
13	0	cpp/tests/test_app.cpp
10	11	cpp/tests/test_errors.cpp
1	1	cpp/tests/test_raii.cpp
139	0	cpp/tests/test_result.cpp
10	4	cpp/tests/test_robustness.cpp
6	1	py/pinjamlab/app/runner.py
6	3	py/pinjamlab/app/seed.py
5	3	py/pinjamlab/service/loan_service.py
10	0	py/tests/test_app.py
1	1	py/tests/test_cleanup.py
14	10	py/tests/test_errors.py
62	0	py/tests/test_result.py
9	3	py/tests/test_robustness.py
11	1	run_tests.sh
6	0	sample-data/my-bad-requests.csv
5	0	sample-data/my-expected-output.txt
38	0	scripts/audit_result_calls.py
29	0	scripts/run_result_asan.sh
37	0	tests/limits_demo.cpp
39	0	tests/limits_demo.py
 24 files changed, 521 insertions(+), 53 deletions(-)

STDERR:

exit=0; durasi_detik=0.026
`````

Perintah: `.venv/bin/python -c 'import importlib.util; print("mypy installed:",importlib.util.find_spec("mypy") is not None); print("pyflakes installed:",importlib.util.find_spec("pyflakes") is not None)'`

`````text
STDOUT:
mypy installed: False
pyflakes installed: False

STDERR:

exit=0; durasi_detik=0.019
`````

Perintah: `.venv/bin/python -m mypy --version; .venv/bin/python -m pyflakes --version`

`````text
STDOUT:

STDERR:
~/loanbench/.venv/bin/python: No module named mypy
~/loanbench/.venv/bin/python: No module named pyflakes

exit=1; durasi_detik=0.037
`````

Timing aktual sesi sekarang perf_counter subprocess:

| Log | Exit/durasi |
|---|---|

| command-001.txt | exit=0; durasi_detik=0.233 |

| command-005.txt | exit=0; durasi_detik=5.444 |

| command-007.txt | exit=0; durasi_detik=1.616 |

| command-014.txt | exit=1; durasi_detik=4.018 |

| command-015.txt | exit=0; durasi_detik=4.061 |

| command-016.txt | exit=1; durasi_detik=9.503 |

| command-018.txt | exit=1; durasi_detik=9.642 |

| command-021.txt | exit=0; durasi_detik=2.308 |

| command-024.txt | exit=126; durasi_detik=0.002 |

| command-025.txt | exit=0; durasi_detik=0.004 |

| command-026.txt | exit=0; durasi_detik=0.003 |

| command-027.txt | exit=0; durasi_detik=0.004 |

| command-028.txt | exit=0; durasi_detik=0.024 |

| command-029.txt | exit=0; durasi_detik=0.370 |

| command-030.txt | exit=0; durasi_detik=0.384 |

| command-031.txt | exit=0; durasi_detik=0.348 |

| command-032.txt | exit=0; durasi_detik=1.004 |

| command-035.txt | exit=0; durasi_detik=0.466 |

| command-036.txt | exit=1; durasi_detik=0.588 |

| command-037.txt | exit=0; durasi_detik=2.066 |

| command-040.txt | exit=0; durasi_detik=0.026 |

## §13 Anomali, risiko, hal yang belum terverifikasi

Pemetaan T1–T7 mengikuti definisi pengguna; hash merujuk perubahan nyata, bukan klaim rubrik selesai.

| Label | Jebakan dan bukti aktual | Hash / batas |
|---|---|---|
| T1 | CRLF: golden LF, pembandingan menghapus CR (§3/§5) | ab23da4; merah CRLF asli TIDAK DIREPRODUKSI |
| T2 | Gate bocor arah dependency: parser include/AST dan mutasi 12 arah terlarang (§5/§10) | 5f8fc29; gate menolak domain→CSV, compiler dapat menerima; bukan parser sempurna |
| T3 | Paritas parsing: underscore, spasi, Unicode, overflow, blank row, duplikasi, whitespace dan CRLF | 5f8fc29/ce8bec3; test_result strict_days/blank_fields, test_app physical_lines, C++ robustness validator/CRLF/duplicate; output §7 |
| T4 | Return ditelan: returnItem/return_item kini menolak salah pemilik/tidak dipinjam dan menjaga state | 5f8fc29/ce8bec3; test_errors invalid_returns dan robustness wrong-owner (§4/§7) |
| T5 | cerr/stderr service dibenarkan saat rollback gagal selama unwind, bukan pelaporan bisnis tiap layer | 5f8fc29; TxnGuard/txn_guard (§4), audit §11; C++ destructor noexcept, Python meneruskan original |
| T6 | ASan native: probe WSL dan leak monolit sebelum/sesudah unique_ptr | cc85467 setup; 67780d9 repair B; §0/§4: leak exit 23 sebelum, penolakan exit 1 tanpa sanitizer sesudah |
| T7 | Tes forgetting-with tautologis tidak cukup membuktikan resource leak; HEAD memakai handle nyata dan tes laziness terpisah | 5f8fc29; test_forgetting_with_retains_an_open_handle_until_manually_closed memeriksa open/closed; test_contextmanager_generator_is_lazy hanya membuktikan begin belum dipanggil (§7) |

Risiko tersisa: PROGRESS/README kedaluwarsa; Python WSL versi aktual tidak membuktikan 3.12; host tool Windows versus WSL harus dibedakan; starter m3-start asli TIDAK ADA; baseline sengaja direkonstruksi; tidak ada trace tangan, peer reproduction atau viva; analisis pribadi DRAF; ekuivalensi memakai adapter bukan implementasi lama independen; mixed Result/throw tidak menghapus semua exception; strong exception safety seluruh service belum dibuktikan; atomic replace bukan durability; BaseException transaksi Python belum dibersihkan oleh except Exception. Tidak mengklaim tugas praktikum final selesai. Tidak mengklaim baseline red T1 direproduksi atau waktu commit sebagai bukti penulis manusia.

Kutipan PROGRESS tetap arsip; label T3/T4/T7 di dalamnya bukan pemetaan koreksi tabel ini.

Tracked diff/index diverifikasi ulang di bawah.

Perintah: `git status --porcelain=v1 --untracked-files=all; git diff --exit-code; git diff --cached --exit-code; git rev-parse HEAD; git check-ignore bin/analisis-export`

`````text
?? docs/ANALISIS_INPUT.md
ce8bec3c830cfb1c8880453ff084a3aa62c6ac84
bin/analisis-export

STDERR:

exit=0
`````

## §14 Catatan mahasiswa (JANGAN DIISI Claude Code)

```text
Nama: 
Pendapat saya sendiri untuk A3 (kenapa node #1 error, bukan Result — 3–5 kalimat kata-kata saya):
Posisi lawan yang menurut saya paling kuat:
Dua keterbatasan Result<T> yang paling saya rasakan saat mengerjakan:
Bagian yang menurut saya paling sulit dan kenapa:
Hal yang saya ubah dari default prompt (jika ada):
Dosen/asisten sudah memberi m3-start asli? (ya/tidak, tanggal):
Hasil rekan menjalankan checklist reproduksi (ringkas):
```
