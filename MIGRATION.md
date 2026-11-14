# Replacing the existing repository safely

This release is for a **private repository**. It preserves historical inputs and
source text. Do not change repository visibility without a separate privacy and
licensing review.

## Recommended: clean working-tree replacement

1. Commit or back up your current changes. Keep a separate copy of any uncommitted
   work. Do not put a backup ZIP inside the Git working tree.
2. Extract this release into a new folder and inspect `README.md`.
3. Copy the new release tree into your existing repository folder, keeping its
   `.git` directory. The release does not include a `.git` directory.
4. If old files remain after **Replace All**, run the dry-run command below.
5. Inspect the move list. Apply the migration only when it contains the expected
   old files. Unknown files and changed legacy files remain untouched.
6. Verify the release and inspect `git status` before committing.

On Windows use `python` or `py -3`; on macOS/Linux use `python3` if necessary.
Commands below assume the current directory is the repository root.

On Windows, use a short extraction/repository path such as `C:\auto-data`.
The longest distributed relative path is about 187 characters; a deeply nested
Downloads or OneDrive folder can exceed the traditional 260-character Windows
path limit even though individual filenames are valid. Long-path support is not
required when the repository root is short.

```console
python scripts/migrate_legacy.py
python scripts/migrate_legacy.py --apply
python scripts/verify_release.py
python scripts/source_archive.py verify
git status --short
```

The migration moves eligible legacy files to a timestamped **sibling backup
folder outside the repository**. It does not delete those files. Only paths
present in the original-repository manifest, absent from the new release, and
still matching their original SHA-256 qualify. New release paths, `.git`,
symlinks, unknown files and modified files are never moved.

**Replace All alone cannot delete obsolete files.** In particular, a pre-existing
large raw CSV remains until the migration moves it. A retained modified file
above 90,000,000 bytes will make release verification fail; move that file to a
separate backup or partition it before committing. The migration intentionally
does not make that decision for user edits.

## File-size rule

Every distributed file is at most **90,000,000 bytes**, below the user's
100,000,000-byte limit. Large originals are stored as 80,000,000-byte binary
parts. This is ordinary Git storage and does not require Git LFS. The release
ZIP itself can be larger because it is a delivery container and must not be
committed to the repository.

`scripts/source_archive.py restore "<logical_path>"` reconstructs a selected
original under `.restored/` and verifies its original SHA-256. `.restored/` is
ignored by Git. Do not force-add restored files to Git.

## Read the old repository

The original non-`.git` repository files are retained under
`archive/legacy_repo/`, with original paths and hashes recorded in
`manifests/source_inventory.jsonl`. Large files use parts instead of a single
oversized file. Historical reports retain their original findings and dates;
the active report and context identify which findings have been superseded.
