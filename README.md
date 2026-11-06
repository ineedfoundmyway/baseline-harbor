# Baseline Harbor

A defensive file-integrity baseline and comparison CLI with SHA-256 manifests, symlink exclusion and a reproducible change simulation.

Python 3.11+ · Standard library only · MIT · Maintained by [ineedfoundmyway](https://github.com/ineedfoundmyway)

## Run the proof

```sh
python -m unittest -v
python main.py demo
python scripts/prove.py
```

The checked-in [execution evidence](proof/report.json), [test transcript](proof/tests.txt), and [source hashes](proof/sha256.json) record a real local execution. Run the same commands to verify the result independently. CI regenerates evidence as an artifact on every push. Local results are not a claim that GitHub Actions has run.

## What you learn

Capture a manifest with `python main.py snapshot ./directory > ../baseline.json`, then compare it with `python main.py compare ../baseline.json ./directory`.

Store the baseline outside the scanned directory and protect it separately. The demo changes only a temporary fixture and removes it on exit. A change is evidence for triage, not proof of malicious activity. Legitimate updates also change hashes.

The scanner is intended for a quiescent directory under your control. It is not hardened against concurrent filesystem races, does not sign manifests, and does not capture permissions, ownership or extended attributes. Protecting and authenticating the baseline is essential in real monitoring.

## Design and limits

This is original educational code inspired by the reading below. Article text, screenshots and third-party tool code are not bundled. Examples use synthetic data and temporary directories. No Internet targets are contacted. Results describe the supplied fixtures and do not certify a production system.

## Reading

- https://www.hackingarticles.in/
- https://docs.python.org/3/library/hashlib.html

## License

MIT. Third-party tools and articles retain their own licenses.
