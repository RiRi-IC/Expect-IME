# Release checklist

Use this checklist before publishing ExpectIME packages.

1. Confirm the version in `expect_ime/__init__.py`, `pyproject.toml`, and `CHANGELOG.md` matches.
2. Run `python -m pytest`.
3. Run `python -m build` to create source and wheel distributions.
4. Inspect `dist/` artifacts and publish them from a clean working tree.
5. Tag the release, for example `git tag v0.1.0 && git push origin v0.1.0`.
