# Digiroom KEY repo update —16 November 2026

Extract this ZIP **inside the existing auto-data repository root**, so its `context/` folder merges into the repo’s `context/` folder. Do not create an extra `auto-data/auto-data/` layer. Allow replacement of this snapshot’s context files, but preserve any newer local edits. No existing files need deletion.

Base checkout:`63b859b9040ba055465fec70669344d766091d52`. This is an overlay, not a complete repository; existing research, reference files and prototype/screenshot inventory are required. The root README, PROJECT_CONTEXT and CURRENT_STATUS gain a pointer to the completed proposal state. Other additions and updates are under `context/digiroom-key-proposal/`.

Start with `context/digiroom-key-proposal/START_HERE.md`. The final current draft is `drafts/Digiroom_KEY_Chapters_1_to_3.docx` with a matching PDF. All source inputs added in this chat are retained, including the full NutriSari reference, author annotations and supplied persona. `SESSION_HANDOFF_2026-11-16.md` records the completed work, approved decisions, evidence boundaries, QA and deferred work. `NEXT_CHAT_PROMPT.md` contains the continuation prompt.

For package integrity, run `sha256sum -c DIGIROOM_KEY_UPDATE_FILES.sha256` from the repo root after extraction. This checksum file covers the ZIP payload except itself. The proposal folder’s `FILES.sha256` separately covers that folder except itself.

No commit, push or public publication was performed. After extraction you can inspect `git status` and commit/push the files yourself. This update does not delete or migrate unrelated historical paths.
