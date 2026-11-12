# Reconstructed Teaching Baseline

direkonstruksi oleh mahasiswa karena m3-start tidak diterima

Root pinjamlab.cpp and pinjamlab.py are standalone monolithic reconstructions,
not recovered instructor sources: parse, rules, print and main live together.
Baseline A deliberately swallows errors and exits zero. Baseline B allocates a
raw Loan before recordLoan throws quota, leaking on that error path.
Only defects A/B are addressed later; no production cpp/ or py/ files change.

Harness exception: the inherited runner accepts a GOLDEN environment override.
The received CRLF fixture fails the Linux byte comparison. Before every non-red
commit run the inherited suite using the main normalized fixture, without
editing either fixture:

    PY=/home/venerdi/loanbench/.venv/bin/python GOLDEN=/home/venerdi/loanbench/sample-data/expected-output.txt ./run_tests.sh

The inherited suite does not test the reconstructed monoliths. Separate tests
and actual execution evidence are under main docs/evidence/reconstructed.
