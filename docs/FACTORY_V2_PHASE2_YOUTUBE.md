# MOIASTRO factory v2 — Phase 2: YouTube MCP (publish, edit, comments, analytics)

Кратко по-русски: через MCP Claude должен уметь залить фильм и шортсы целиком (расписание, субтитры, обложка,
плейлист, переводы), поправить уже залитое видео, читать и отвечать на комментарии по команде владельца,
и давать нормальную аналитику (удержание, источники, показы/CTR, сравнение роликов) плюс ежедневную сводку
в Telegram. Всё, что YouTube API не умеет (A/B-тест обложек, конечные заставки, подсказки, закреп коммента,
связанное видео у шортса), инструмент не делает, а возвращает владельцу чек-лист «сделать руками в Студии».

---

## 0. Ground rules

- Repo `permradar-code/moiastro-engine`. Branch `feature/youtube-mcp-phase2` from `feature/factory-v2-phase1-5` (deployed on the server);
  PR into `feature/factory-v2-phase1-5`.
- Existing modules to build on: `app/production/youtube_client.py`, `youtube_owned_analytics.py`,
  `youtube_profiles.py`, `youtube_public.py`, `youtube_reporting.py`, MCP tools `youtube_new_channel_*`,
  `youtube_public_*`.
- Never: deploy, restart, touch the VPS, read/print/commit tokens or `.env`, real API calls in tests (mock HTTP).
- Any new Python dependency goes into `requirements.txt` (Phase 1 forgot numpy; the Studio failed to start).
- **Channel profiles instead of hard-coded ones.** Today there are `new_channel` (= Tales of Cedar Bluff,
  scopes already include `youtube.upload` + `youtube.force-ssl`) and `sbr`. Make every new tool take
  `profile` (default `new_channel`) so more channels can be added later with the existing OAuth script.
  Do not change or request scopes for existing tokens.
- **Safety:** every write tool (publish, update, comment reply/post/moderate) supports `dry_run=true` (default
  for comment writes) that returns exactly what would be sent. Writes are logged to `ops/youtube_actions.jsonl`
  (no tokens). Rate-limit comment writes (e.g. ≤ 20 per call, ≤ 100 per day per channel).

## 1. Publish (full)

`youtube_publish_video(profile, project_id | file_path, kind="long"|"short", title, description, tags,
category_id=1, language="en", default_audio_language="en", privacy="private"|"unlisted"|"public",
publish_at=<RFC3339, optional>, made_for_kids=false, contains_synthetic_media=true|false,
subtitles_srt=<path>, thumbnail=<path>, playlist_id, localizations={"de": {title, description}, …}, dry_run)`
- Resumable upload with retries and progress written to a job (long files are 0.5–1 GB); MCP returns a job id;
  `youtube_upload_status(job_id)`.
- After upload: captions insert, thumbnails.set, playlistItems.insert, localizations — each step reported
  separately; one failing step never deletes the uploaded video.
- Returns `video_id`, Studio URL and a **manual checklist**: A/B test (Test & Compare), end screen, cards,
  pinned comment, Shorts "related video" — these are not in the API.
- Validation before upload: title ≤ 100 chars, description ≤ 5000, tags ≤ 500 chars total, thumbnail ≤ 2 MB
  JPG/PNG 1280×720, Shorts 9:16 and ≤ 3 min.

## 2. Edit an existing video

- `youtube_video_update(profile, video_id, title?, description?, tags?, privacy?, publish_at?, localizations?,
  confirm_title_change=false, dry_run)` — changing title or thumbnail requires `confirm_title_change=true`
  (owner rule: never touch them while an A/B test runs).
- `youtube_thumbnail_set`, `youtube_captions_upload`, `youtube_playlist_add`, `youtube_playlists_list`.
- `youtube_my_videos(profile, since?, kind?)` — id, title, publish time, privacy, duration, short/long.

## 3. Comments

- `youtube_comments_inbox(profile, since?, video_id?, unanswered_only=true, include_held=true)` — top-level
  threads across the channel (commentThreads, `allThreadsRelatedToChannelId`), with author, text, likes, time,
  video title, whether the channel already replied, and held-for-review ones.
- `youtube_comment_reply(profile, parent_id, text, dry_run=true)` — reply as the channel.
- `youtube_comment_post(profile, video_id, text, dry_run=true)` — top-level comment (e.g. the text to pin;
  pinning itself is manual).
- `youtube_comment_moderate(profile, comment_ids, action="publish"|"hold"|"reject", ban_author=false,
  dry_run=true)` — for spam (crypto/"WhatsApp me" etc.).
- Workflow we want: owner says "прочитай комменты и ответь" → Claude reads the inbox, drafts replies, shows them,
  and sends only after the owner's OK (dry_run first). No automatic replying without an explicit call.

## 4. Analytics (own channel)

- `youtube_video_retention(profile, video_id)` — audience retention curve (Analytics API
  `elapsedVideoTimeRatio` × `audienceWatchRatio`, `relativeRetentionPerformance`), plus the drop points
  (biggest falls, value at 0:30 / 1:00 / 50 %).
- `youtube_video_reach(profile, video_id, days)` — impressions, impressions CTR, unique viewers by day from the
  Reporting API reach reports (`youtube_reporting.py` already sets up jobs; note the 1–2-day lag).
- `youtube_video_sources(profile, video_id)` — traffic sources and, for suggested/browse, the top source videos
  (`insightTrafficSourceDetail`), so we see which videos feed ours.
- `youtube_video_compare(profile, video_ids, hours=[24, 48, 168])` — side-by-side first-day/first-week numbers
  (views, avg view duration/%, subs gained, likes, comments, CTR when available).
- `youtube_audience(profile, days)` — age/gender, country, device, subscribed vs not.
- `youtube_shorts_to_long(profile, days)` — Shorts views vs. long-video views coming from Shorts (traffic source
  "SHORTS"), per Short where possible.
- No realtime in the API — say so in the tool docstring instead of guessing.

## 5. External analytics (competitors)

- `youtube_competitors_set(profile, channel_ids)` / `youtube_competitors_report(profile, days=7)` — new videos of
  saved competitor channels with views, views/hour since publish, and outlier ratio vs. the channel's median;
  titles + thumbnail URLs for packaging research. Public Data API only; cache to save quota.

## 6. Daily digest

- Scheduled job (systemd timer or the existing scheduler) → Telegram via `app/notifications.py`, 09:00 MSK:
  yesterday per video (views, avg duration, subs), new comments needing an answer (count + 3 examples),
  spam held, quota used. Short, Russian. `youtube_digest_now(profile)` MCP tool for on-demand.

## 7. Quota

- Track API quota units per call (uploads are expensive) in `ops/youtube_quota.json`; refuse a publish when the
  day's remaining quota cannot cover it and say when it resets (midnight Pacific).

## 8. Acceptance

- [ ] All old tests pass; new tests with mocked HTTP for every tool, including dry_run outputs, the A/B
      title-change guard, partial failure after upload, comment rate limits, retention/reach parsing, quota guard.
- [ ] `docs/youtube_mcp.md` with each tool, an example call and the manual-checklist list.
- [ ] PR description with a short Russian summary and exact deploy steps (services to restart, deps to install).
