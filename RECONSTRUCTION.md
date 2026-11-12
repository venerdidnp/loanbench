# Reconstructed Teaching Baseline

direkonstruksi oleh mahasiswa karena m3-start tidak diterima

Root pinjamlab.cpp and pinjamlab.py are standalone monolithic reconstructions,
not recovered instructor sources: parse, rules, print and main live together.
Baseline A deliberately swallows errors and exits zero. Baseline B allocates a
raw Loan before recordLoan throws quota, leaking on that error path.
Only defects A/B are addressed later; no production cpp/ or py/ files change.

Verification note: the original golden comparison actually passed in this WSL
checkout; the anticipated CRLF mismatch did not reproduce. GOLDEN is still set
explicitly to the main normalized fixture for every non-red pre-commit run.
Also set PYTHONSAFEPATH=1: the root monolith otherwise shadows the inherited
pinjamlab package during python -m pytest. No inherited Python source is changed.
The baseline commit preserves the two intentional defects; subsequent commits
contain red tests, the diagnostic fix, then the scoped-ownership fix.

Harness exception: the inherited runner accepts a GOLDEN environment override.
CRLF was an anticipated risk, not an observed failure here. Before every non-red
commit run the inherited suite using the main normalized fixture, without
editing either fixture:

    PYTHONSAFEPATH=1 PY=/home/venerdi/loanbench/.venv/bin/python GOLDEN=/home/venerdi/loanbench/sample-data/expected-output.txt ./run_tests.sh

The inherited suite does not test the reconstructed monoliths. Separate tests
and actual execution evidence are under main docs/evidence/reconstructed.
