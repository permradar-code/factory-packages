# ТЗ: montage_assets v3 — «сырьё для внешнего монтажа»

Репозиторий: /opt/moiastro-engine (живой сервер). База: текущее состояние рабочей копии = ветка `backup-2026-10-02` (fe3bd6b).
Цель: режим `montage_assets` выдаёт пакет сырья (картинки, клипы, голос, тайминги слов, музыка) и сам отправляет его в GitHub-репозиторий `permradar-code/factory-packages`. Монтаж и субтитры делаются вне фабрики.

## Жёсткие ограничения
- НЕ трогать астрологический конвейер: `app/production/{generator,job_loader,visual_pipeline,audio_pipeline,music_pipeline,renderer,subtitle_pipeline,timeline_builder,qc}.py`, `video_job_*`, `/api/jobs`.
- НЕ перезапускать MCP/OAuth control plane. Новые MCP-инструменты НЕ добавлять (всё работает через существующие `montage_assets_*` + флаг во входном JSON).
- Все новые поля — опциональные. Старые входные JSON (Paris и т.п.) должны валидироваться и давать тот же `input_fingerprint`, если новые поля не указаны.
- Существующий экспорт в Montage Bridge / CapCut оставить как есть.
- Секреты/токены в код и в пакеты не класть.

## 1. Последний кадр для Veo (first + last frame)
Контракт (`montage_assets_contract.py`), поле шота (только для `type: video`):
- `end_image_prompt_full` (str, опц.) — промпт конечного кадра. Генерируется тем же Google image с теми же референсами шота, ПЛЮС первым референсом передаётся уже готовая картинка первого кадра шота (`visuals/images/<id>.png`) — чтобы комната/свет/персонажи совпадали.
- Новый ассет `image_end:<id>` → `visuals/images/<id>_end.png`, генерируется после `image:<id>`.
Провайдер (`vertex_reference_media.py`, `provider_worker.py` `/generate/vertex/veo`): опц. параметр `last_frame` (путь из `visuals/images`), в instance Vertex → `"lastFrame": {"bytesBase64Encoded", "mimeType"}`. Только вместе с `source_image`; с `reference_images` — ошибка.
Runner: если у шота есть `end_image_prompt_full` и `image_end` READY — передать `last_frame`. Если `image_end` FAILED — видео НЕ генерировать без него, а пометить FAILED с dependency (чтобы не жечь деньги на неправильный клип).
Стоимость: +1 google image на такой шот.

## 2. Музыка по промпту
Контракт, верхний уровень, опц.:
```json
"music": {"prompt": "...", "model": "lyria-3-pro-preview" | "lyria-3-clip-preview", "duration_s": 20, "instrumental": true}
```
- duration_s: для clip — только 30; для pro — 1..184; по умолчанию = ожидаемая длительность ролика, округлённая вверх, минимум 10.
- Ассет `music:main` → `audio/music/main.mp3` через существующий `/generate/vertex/music`. Промпт передаётся как есть (провайдер сам добавляет только "instrumental only…" и длительность — это ок).
- Неудача музыки не блокирует остальные ассеты, но если `music` указан — он входит в обязательные для MONTAGE_READY.
- В оценку стоимости добавить строку `google_lyria` (константа-оценка в PRICING с пометкой estimate).

## 3. Сырые промпты для референсов
Сейчас референс оборачивается шаблоном «Create a canonical visual reference…». Добавить опц. поле референса `prompt_raw: true` — тогда в провайдер уходит ровно `description` + (если views > 1) только `View: <view>.` в конце. Без `prompt_raw` — как сейчас.
Также опц. поле референса `files: ["references/X/portrait.png", ...]` НЕ делаем сейчас (на будущее).

## 4. Выгрузка пакета в GitHub
Входной JSON, опц.:
```json
"delivery": {"github": {"repo": "permradar-code/factory-packages"}}
```
- Новый модуль `app/production/montage_assets_github.py`, функция `export_to_github(projects_root, project_id) -> dict`.
- Вызывается автоматически в конце `run_montage_assets`, ПОСЛЕ `finalize_project`, если указан `delivery.github` и статус MONTAGE_READY или PREPARED_WITH_GAPS (с gaps — тоже выгружать, с полем `missing` в манифесте, чтобы я видел что не так).
- Также CLI: `python -m app.production.montage_assets_github <project_id>` (ручной повтор).
- Механика: во временном каталоге (mktemp, вне /opt/moiastro-engine) создать orphan-ветку `pkg/<project_id>`, положить файлы в корень ветки, один коммит, `git push --force origin pkg/<project_id>` через SSH (`git@github.com:<repo>.git`, ключ уже есть у пользователя permradar-code). main репозитория не трогать.
- Состав пакета:
  - `manifest.json` — результат `build_manifest(allow_gaps=True)` + поля `music` (путь или null), `end_frames` по шотам, `exported_at`, `factory_commit`.
  - `input.json` (нормализованный вход), `audio/narration.wav`, `audio/narration.mp3` если есть, `audio/music/main.mp3` если есть, `timings/words.json`, `timings/shots.json`, `visuals/images/*.png`, `visuals/video/*.mp4`, `references/**.png`.
- Лимиты: файл > 95 МБ — не класть, записать в `manifest.missing` с причиной `too_large`. Весь пакет > 500 МБ — ошибка экспорта.
- Результат экспорта записать в `montage/state.json`: `github_export: {status: PUSHED|FAILED, branch, commit, error, at}` и отдать в `montage_assets_status` (если status читает state.json — проверить, что поле видно).
- Ошибка экспорта не меняет статус производства (MONTAGE_READY остаётся), только `github_export.status=FAILED`.

## 5. Проверки
- 9:16 уже поддержан (resolution 1080x1920 для картинок, aspectRatio для Veo) — покрыть тестом на вертикальный проект.
- Язык не ограничен — покрыть тестом `language: "en"`.
- Тесты (pytest, моки провайдеров и git): last_frame передаётся в Vertex payload; запрет last_frame без source_image; music ассет и стоимость; prompt_raw; export собирает правильное дерево и не трогает рабочую копию; старый Paris-вход даёт прежний fingerprint.
- Прогнать ВЕСЬ тест-сьют до и после. Регрессий в астрологических тестах быть не должно.

## 6. Git
После того как всё зелёное: закоммитить ВСЁ текущее состояние (включая то, что было только в бэкапе) в новую ветку `feature/montage-assets-v3` от main, запушить. В main не мержить без отдельного «ок». Аудио-файлы web/studio/*.mp3|*.wav в коммит не включать (добавить в .gitignore).

## 7. Деплой
Перезапуск только studio и provider-worker (не MCP). После рестарта — `montage_assets_list` должен отвечать, `factory_status` — сервисы active.
