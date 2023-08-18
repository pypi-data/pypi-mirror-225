# Release documentation

## How it works

GitLab CI automation will automatically upload wheels to PyPI on tagged versions.
So we need to do a Git tag.
At the same time, the wheel versions come out of `Cargo.toml` (via the [Maturin packaging tool](https://maturin.rs/)).

So we use [bump2version](https://github.com/c4urself/bump2version/) to update `Cargo.toml`, and then separately add a matching Git tag in GitLab.

## How to do it

1. `pip install bump2version`
2. Make sure you're on `main` git branch, or in PR that will get merged soon.
3. `bump2version --no-tag --no-commit --current-version 0.x.y minor` (or `patch`, depending)
4. Rebuild.
5. Check-in all files; make sure `Cargo.lock` was updated and checked-in too.
6. `git push`
7. Merge PR if relevant.
8. In GitLab UI, tag the release.
