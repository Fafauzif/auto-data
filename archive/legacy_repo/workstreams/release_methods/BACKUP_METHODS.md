# Backup methods checked against operator documentation

Checked 11 November2026. No files were uploaded by this workstream. Endpoint reachability is not proof of a successful upload or durable retention. The root release process owns any final upload and must use the exact validated release archive, then retain its checksum and actual response.

## Recommended fallback after a Filebin failure

For an archive below95,000,000 bytes, TmpFiles is the clearest documented temporary fallback in this review. Its official API page documents `POST https://tmpfiles.org/api/v1/upload`, multipart field `file`, optional `expire` in seconds from60 to172800, and default3600. The official terms specify100MiB per upload, retention up to48hours and no registration. The API labels the limit100MB, so the conservative95MB threshold avoids relying on the decimal/binary discrepancy. Request172800seconds for a two-day copy; report actual expiry when the response supplies it, otherwise label the retention requested rather than confirmed.

Sources: https://tmpfiles.org/api ; https://tmpfiles.org/tos ; https://tmpfiles.org/ . The terms describe legitimate documents/backups/collaboration, require rights to content and prohibit third-party personal data without consent. A HEAD request to the API documentation returned200 during this run; no upload POST was tested. Do not infer backup success from that.

The documented command shape is `curl -F file=@ARCHIVE -F expire=172800 https://tmpfiles.org/api/v1/upload`. Use an actual local path, explicit timeout, one initial attempt and a recorded HTTP status/body. Parse the operator-returned URL rather than invent an address. Verify that the returned resource serves the uploaded bytes, ideally by downloading and matching SHA256. Retain failed attempts as failures; a successful upload response with a missing/expired resource is not verified backup. No account, API key or third-party upload wrapper is needed for this documented route.

## Other examined candidates

| Service | Verified operator claims | Runtime evidence and disposition |
|---|---|---|
| Catbox | Official homepage allows200MB. Official tools page allows anonymous uploads by omitting userhash, at https://catbox.moe/user/api.php with reqtype=fileupload and fileToUpload. FAQ states anonymous retention until two years of inactivity; account uploads are permanent. | HEAD to upload endpoint returned412. This does not prove all POSTs fail, but access is unresolved. Long anonymous retention and limited self-service deletion make it less suitable than a timed backup. Never call it permanently guaranteed storage. |
| Litterbox | Catbox homepage identifies it as a temporary-file sister service. | Operator homepage/docs retrieval returned403 and HEAD homepage405. Current size/API/retention limits could not be verified from accessible primary documentation here. Third-party1GB/72h claims were deliberately not adopted as verified facts. Do not promise availability or force a blocked route. |

Catbox sources: https://catbox.moe/ ; https://catbox.moe/tools.php ; https://catbox.moe/faq.php ; https://catbox.moe/legal.php . Litterbox: https://litterbox.catbox.moe/ . Catbox's documentation requires content rights and restricts commercial hosting. This research backup is a one-off user-authorized distribution, not a CDN or an operational commercial service. Any final archive must already pass the root's release review; external hosting does not confer rights to redistribute source material.

## Release controls that affect backup

- Upload the sanitized deliverable, not private_cache, cookies, raw reviewer identities, dependency environments, user credentials or unlicensed bulk review text.
- Preserve permitted licensed raw datasets under their actual licenses and provenance. Keep original source units distinct from derived features, labels and repeated captures.
- Include an archive manifest and checksum. State file size, actual status and expiry boundary. Temporary hosting supplements the main saved artifact and is not a durable preservation guarantee.
- If the archive exceeds the verified host limit, stop that candidate and retain the primary saved artifact. A split release would need meaningful parts and clear reassembly instructions, not silent truncation or fake fullness.

## Reachability log

| Request | Result | Meaning |
|---|---:|---|
| HEAD https://tmpfiles.org/api |200|Documentation reachable; upload untested.|
| HEAD https://catbox.moe/user/api.php |412|Upload endpoint HEAD not usable on this surface; POST untested.|
| HEAD https://litterbox.catbox.moe/ |405|HEAD rejected; does not establish POST/upload capability.|
| Search-service GET Litterbox homepage |403|Primary documentation not retrieved by that surface.|

No response cookies, IP-related headers, account data or session values are included in this public log.
