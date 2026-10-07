# MOIASTRO Film Factory production contract

Новые фильмы не должны добавлять film-specific Python в `moiastro-engine`.
Всё, что зависит от конкретного фильма, хранится в `shotlist.json -> production`.

Минимальный рекомендуемый контракт:

```json
{
  "production": {
    "schema_version": 1,
    "voice": {
      "provider": "elevenlabs",
      "voice_id": "<voice id>",
      "model": "eleven_multilingual_v2",
      "speed": 1.0,
      "timestamps": true,
      "output_format": "mp3_44100_128",
      "stability": 0.55,
      "similarity_boost": 0.8,
      "style": 0.15,
      "use_speaker_boost": true,
      "context_chars": 400
    },
    "first_frame_only_ids": [],
    "force_regenerate_image_ids": [],
    "music_anchor_map": {
      "M01": "<timeline id where cue begins>"
    },
    "review_gates": {
      "audio": {
        "enabled": true,
        "narration_sample_id": "<first narration id>",
        "music_sample_id": "<first generated music id>"
      },
      "visuals": {"enabled": true},
      "video_sample": {
        "enabled": true,
        "shot_ids": ["<first representative clips>"]
      },
      "videos": {"enabled": true}
    },
    "edit": {
      "dialogue_tail_seconds": 0.8,
      "narration_voice_offset_seconds": 0.4,
      "narration_tail_seconds": 0.4,
      "transition_seconds": 0.7,
      "end_screen_tail_seconds": 20.0,
      "contact_sheet": "one_frame_per_timeline_visual"
    },
    "audio_mix": {
      "speech_active_rms_db": -20.0,
      "ambient_clip_rms_db": -24.0,
      "music_base_rms_db": -18.0,
      "duck_under_speech_db": -15.0,
      "duck_under_clip_db": -6.0,
      "duck_attack_seconds": 0.15,
      "duck_release_seconds": 0.6,
      "integrated_lufs": -14.0,
      "true_peak_db": -1.5
    },
    "subtitle": {"language": "en", "name": "English"},
    "branding": {
      "title_font_source": "git:tools/montage:montage/fonts/Rye-Regular.ttf",
      "ui_font_source": "git:tools/montage:montage/fonts/Inter-ExtraBold.otf",
      "subscribe_overlay_source": "git:tools/montage:montage/overlays/subscribe_badge.py",
      "subscribe_times_s": []
    },
    "qc": {
      "long_duration_min_seconds": 0,
      "long_duration_max_seconds": 99999,
      "required_prefix_ids": [],
      "black_silence_max_seconds": 1.5
    },
    "export": {
      "package_branch": "pkg/<project_id>",
      "film_branch": "film/<project_id>"
    }
  }
}
```

## Правила

- `timeline` остаётся единственным источником порядка фильма.
- Все `ref_files` задаются в shotlist. Engine выбирает максимум шесть детерминированно: персонажи, затем локация, затем props/other.
- Уже существующие файлы из package автоматически reused и не входят в стоимость.
- Reuse — предпочтение, а не обязательная зависимость: если заявленного файла реально нет в package, Factory должна перейти на generation fallback до budget approval и пересчитать смету.
- Для любого reused asset должен существовать generation recipe: image/video prompts в shotlist, ref_prompt для canonical ref, а для reused music — `fallback_prompt`.
- Если source существует, но временно не скачался из-за Git/SSH/network ошибки, Factory не должна тратить деньги на замену: preflight остаётся незавершённым и повторяется.
- Если нет ни source, ни generation recipe, preflight блокируется как неполный контракт.
- `force_regenerate_image_ids` позволяет намеренно игнорировать плохой готовый still.
- `first_frame_only_ids` отключает end-frame для конкретных клипов.
- `music_anchor_map` задаётся редактором фильма; engine не угадывает музыкальную драматургию по старым descriptions.
- Budget approval выполняется один раз на fingerprint. Audio/visual/video approvals — quality gates, не новые финансовые approvals.
- До `Approve Visuals` видеогенерация запрещена.
- `video_sample` должен содержать репрезентативные первые сцены; для dialogue clips review ждёт transcript alignment.
- До `Approve All Videos` final montage запрещён.
- Generated asset можно Redo отдельно; downstream assets и downstream review approvals сбрасываются автоматически.
- Source/reused asset нельзя случайно перегенерировать через Redo.
- Final export разрешён только после `FINAL_READY`/QC PASS и запускается отдельно от production.
- Studio держится на `127.0.0.1:8788`; операторский доступ — через SSH tunnel.

Перед платным запуском всегда выполнить `film_package_prepare` и проверить, что все IDs/config валидны и цена полностью посчитана.
