# Tales of Cedar Bluff: передача в новый чат

> **10 окт 2026, 11:00 МСК. Сначала прочитай `FACTORY_GUIDE.md` — это полная инструкция: как делать фильмы, шортсы и правки на фабрике.** Ниже — состояние дел.

## Состояние на 10 окт (утро)
- **Фильм 4 «The Widow's Rifle»** (конкурс стрелков): сценарий `briefs/western_widows_rifle/script.md`, раскадровка `build_shotlist.py` → `shotlist.json`. На фабрике проект `western_widows_rifle_v1` импортирован: **AWAITING_APPROVAL, $81.5 + запас = $93.8**, fingerprint `2b5cd0d53eaf573eef8d07e370e38d25b0db16f5929ca5c52b3bdd5564299c96`. Ждём «ок» владельца на бюджет → `montage_assets_approve`. Если сценарий меняется — заново `film_package_prepare` (package_branch `pkg/western_stagecoach_bride_v1`).
- **Фабрика, ветка `feature/youtube-mcp-phase2`, коммит `5df9cbf` — НЕ задеплоен** (на сервере `fc0b6db`). Новое: колокольчик плашки в монтаже v2; шортсы командами `film_short_scenes` / `film_frames` / `film_story_short`; правки фильма `film_timeline` / `film_edit_set`; починен `youtube_shorts_to_long`; понятные ошибки `film_package_prepare`. Деплой: `git pull` + перезапуск `moiastro-studio` и `moiastro-mcp` (раздел 6 инструкции), пока ничего не генерируется.
- **Шортсы фильма 3** у владельца в `film3_barn_storm\shorts\`: `short_mothers.mp4` (без плашки, выложить 10 окт ~22:00) и `short_harlan.mp4` (плашка + колокольчик, 11 окт ~22:00). Через 2 дня сравнить подписки на 1000 просмотров (хиты ≈ 2).
- Отчёты YouTube Reporting (показы/CTR и др., 13 шт.) заказаны 9 окт — данные с ~11–12 окт.
- Комментарии на 10 окт 08:40 отвечены все; название шортса-справедливости исправлено.
- Telegram не настроен; PR #3 → #2 → #1 не слиты (руками владелец).

---

## Архив: передача от 9 окт

# Tales of Cedar Bluff: передача в новый чат (9 окт 2026, 22:00 МСК)

> Документ для Claude в новом чате. Прочитай его целиком первым. Старая история и общие правила лежат в `HANDOFF_WESTERN.md`; версия этого файла от 8 окт есть в истории git.
> С пользователем говорить **по-русски, просто и коротко, без жаргона**. Он в Абхазии, часовой пояс МСК.
> **Картинки и файлы в чат не присылать** («сюда картинки вообще не кидай»). Готовые файлы класть ему на компьютер через мост (`device_commit_files`) в `C:\ai\projects\stagecoach_bride\...`, в чате писать коротко текстом.

---

## 0. План на 10 окт (по порядку)
1. **Утро:** цифры фильма 3 и фильма 2 (новые обложки). Пользователь присылает скриншоты Студии; задержанные данные смотреть самому новыми командами (раздел 5).
2. **Комментарии фильма 3** (было 6): прочитать `youtube_comments_inbox`, предложить ответы, отправлять только после его «ок» (`dry_run` сначала). Это заодно проверка новых команд.
3. **Слить три PR** в `permradar-code/moiastro-engine` руками (у Claude слияние без ревью блокирует среда): **#3 → #2 → #1**, у каждого «Ready for review» → «Merge pull request». Потом проверить, что `feature/google-ai-refresh-20261006` содержит всё.
4. **Telegram** для уведомлений фабрики и утренней сводки (раздел 4.3).
5. **Фильм 4:** показать пользователю 3 идеи сюжета (раздел 3), он выбирает, дальше сценарий и производство на новой фабрике.

## 1. Канал (на 9 окт вечер)
- **Tales of Cedar Bluff** (@TalesofCedarBluff, `UCRaldWksRYLzA_Xx_zUKqOg`), английский long-form, ИИ-вестерны. **678 подписчиков**, цель 1000 и монетизация. Аудитория 65+ (≈85%), 2/3 мужчины, больше половины смотрят с ТВ, половина из США.
- Вымышленный Cedar Bluff, Колорадо — **штат**, никогда не писать «Colorado Territory».
- **Фильм 1** «The Widow's Piano» `oxqtqbybpMM`: **77.5 тыс.**, +292 подписчика. Трафик: главная 83.5%, «Следующее» 13.5%, поиск 0.2%. Средний просмотр с показов 8:07. Его предлагают рядом с «Laugh While You Can…», «She Could Never Have Children…», «She Bought a Forgotten Farm for $1…», «She Gave a Broke Stranger a Job…» — **наша ниша: душевные истории про женщину и её второй шанс**. Превью-победитель: женщина с ружьём, «THAT'S FAR ENOUGH.».
- **Фильм 2** «The Stagecoach Bride» `gN-bWt8RKVU` (8 окт): ~300 просм., 2.3 тыс. показов, **CTR 4.2%**, ср. просмотр 4:32. Упаковка с арестом/наручниками провалилась. **9 окт вечером пользователь заменил упаковку** (новый A/B-тест):
  1. `1_wrong_bride` (Rose в свадебном платье с ружьём у дилижанса, «WRONG BRIDE.») + «She Came West to Be a Bride — Nobody Warned the Outlaws About Her | Full Western Movie»
  2. `2_laugh_now` (Rose с револьвером рядом с Калебом, «LAUGH NOW.») + «The Whole Town Laughed at the New Bride — Then the Deputy Stood Up for Her | Full Western Movie»
  3. `3_she_jumped` (прыжок с сундучком, «SHE JUMPED!») + «Outlaws Robbed the Stagecoach — They Never Expected the Bride to Jump | Full Western Movie»
  Запасная `4_marry_me`. Описание поправлено (без наручников, без «mail-order»), новый закреп. Обложки: `C:\ai\projects\stagecoach_bride\film2_thumbs_final\`, скрипт `montage/western_stagecoach_bride/thumbs_ai.py`. Переводы у канала автоматические.
- **Фильм 3** «The Barn in the Storm» `55FeA5seYsA` (опубл. 9 окт 15:54 МСК, 15:36): **лучший старт**. Через 5 ч: 227 просм., 841 показ, **CTR 8.0%**, ср. просмотр 5:25, с главной 62%, ускорялся (105 просм. за час). В 21:48: 342 просм., 13 лайков, 6 комментариев. A/B-тест 3 обложек из Flow:
  A `A_not_my_boy` («“NOT MY BOY.”») + «$500 for the Widow's Baby — They Didn't Know Whose Door She Knocked On | Full Western Movie»; B `B_he_was_a_ranger` + «Three Hired Guns Came for the Widow's Baby — The Rancher Was a Texas Ranger | Full Western Movie»; C `C_no_maam` + «"May We Sleep in Your Barn?" the Widow Begged — He Said, "No, Ma'am…" | Full Western Movie». **Не трогать название и обложки во время теста.**
  Сюжет: вдова Ellie Price с дочкой Molly и младенцем просится в амбар к вдовцу Wade Harlan (потерял жену Anna и сына Daniel), за младенцем охотятся люди богача Lucius Vance (наёмник Pike), Wade — бывший капитан техасских рейнджеров. Файлы: `C:\ai\projects\stagecoach_bride\film3_barn_storm\` (final\ части + join.bat, thumbs_final\, shorts\, upload_text.txt). Монтаж: `montage/western_barn_storm/` (build.py, plan.py, qc.py, thumbs_ai.py, short_fire.py). Фабричный проект `western_barn_storm_v1` (C65 FAILED, остальное READY).
- **Шортсы:** «прыжок» (фильм 2) 751 просм. +3 подп.; «I Wore It for You» (арест) `IvG_MqKlqJQ` ~150 просм., остаются 27%; «May We Sleep in Your Barn?» (фильм 3) `ih2I5TS2GAA` ~26 просм., остаются 37%; предложение `KPx3o5OonAM` умер. **Вывод:** листают с первой секунды — первый кадр должен быть действием/угрозой. Готов, но не выложен: `film3_barn_storm\shorts\short_barn_threat.mp4` (начинается с угрозы «$500 for the boy»), выложить через 1–2 дня как отдельный шортс. Шортсам нужны **родные вертикальные клипы** (в фильме 3 их было только 4).
- После выхода фильма 3: конечные заставки фильмов 1 и 2 и «Связанное видео» шортса — на фильм 3 (пользователь делает руками).

## 2. Чему научились (формула канала)
**Разбор хита «Millionaire Cowboy Heard Them Laugh at Widow's Old Dress—His Next Move Silenced Everyone»** (Legends in the Dust, `sBOlj4MFilY`, 818 тыс., 18:28; разбор vidIQ video_watch 9 окт):
- **Рассказчика нет вообще.** Только диалоги + музыкальные склейки 6–12 с (пейзаж, повозка, она шьёт у огня).
- **100% видео**, статичных картинок нет. Кадр 3–6 с, в диалоговой сцене 12–25 кадров (восьмёрка, крупные, через плечо).
- Первая минута: пролёт над заснеженным городком (0–8 с) → она у прилавка, не хватает двух центов (0:08–0:43) → взгляд на красную ткань → входят богатые дамы и смеются (0:50). **Хук — унижение и сочувствие, не экшен.**
- Расплата каждые 2–3 мин: 3:00 он скупает всю ткань обидчицы; 5:00 гасит её долг, банкир унижен; 7:00 работа, а не милостыня («I don't need charity»); 12:00 она сама стреляет в бандитов («The next one goes lower»); 15:00 раскрытие — он владелец железной дороги; 18:00 предложение.
- Нет титра, нет плашек «подпишись», одна надпись «FIVE MONTHS LATER», концовка 1–2 с.
- Звук: оркестр (струнные, пианино), под диалогом музыка тихо (~¼), в склейках громче; много шумов (снег, двери, камин, затвор).
- Соседи по ленте: «She Sheltered a Freezing Stranger, Thinking He Was…» (676 тыс. и 398 тыс., два канала), «"Can You Cook?" He Asked the Humiliated Bride» (483 тыс.), «A Widow Hired a Drifter to Guard Her Ranch, Unaware…» (172 тыс.), «Divorced and Kicked Out at 25, She Built a Home…» (157 тыс.).

**Правила упаковки (решения пользователя):**
- История про женщину и её второй шанс; у мужчины скрытая сила (богач, рейнджер, судья). Бытовые злодеи: банкир, сплетницы, долг, земля.
- **Никаких арестов, наручников, тюрьмы, «thief», «ordered/order»** в названиях, обложках и первых 30 с.
- Обложка: яркая, солнечная, она крупно **с оружием в руках** (сильная, не жертва), короткая жёлтая подпись 1–3 слова слева сверху (Anton, обводка). Картинки делает Claude Code во Flow, подпись ставит Claude (`thumbs_ai.py`).
- Название: «She…» или её реплика в кавычках + поворот, хвост **« | Full Western Movie»**, всего ≤ 100 символов (считать скриптом).

## 3. Фильм 4: что делаем
### 3.1 Рецепт
- 15–18 мин, **без рассказчика**, почти всё — видео с диалогами; склейки — музыка + пейзаж/проезд 6–12 с (можно 10–20% статичных картинок в склейках, если бюджет жмёт).
- 0:00 — сразу сцена унижения с репликами (без голоса за кадром, без титра; максимум один бейдж «подпишись» около 0:30).
- Расплата каждые 2–3 мин, раскрытие его силы в середине/конце, она хотя бы раз сама берёт ружьё (кадр для обложки и шортса), финал — предложение.
- Сразу заложить **8 вертикальных хуков** 9:16 (шаблон фабрики `docs/templates/hooks_8.json`): угроза, унижение, расплата, раскрытие, ружьё, предложение — для шортсов, первый кадр с действием.
- Cedar Bluff и жители (Клара, Мерсер, Агата Пелл — холодная сплетница, маршал Hart) можно давать камео, но главные герои новые.

### 3.2 Три идеи для выбора (показать пользователю коротко)
1. **«Two Cents Short»** — вдова у банковской стойки в Cedar Bluff: банкир при всех отказывает в отсрочке и смеётся над её латаным платьем; пыльный незнакомец в очереди молча слушает. Он — владелец крупнейшего скотоводческого счёта банка. Выкупает её закладную, она отказывается от милостыни — он нанимает её (лучшая повариха/объездчица долины). Ночью люди банкира ломают её изгородь — она встречает их с ружьём. Раскрытие: банк держится на его деньгах. Предложение.
2. **«She Sheltered the Stranger Everyone Turned Away»** — метель; сельская учительница-вдова пускает в дом обмороженного бродягу, которого не пустили в салун и церковь. Город сплетничает, её увольняют. Он оказывается новым окружным судьёй / федеральным маршалом, ехавшим инкогнито. Расплата сплетникам и попечителю школы, она защищает дом с ружьём от людей попечителя, финал — предложение.
3. **«Kicked Out at Twenty-Five»** — мужа нет (бросил/умер), родня мужа выгоняет её с ребёнком; она одна чинит заброшенный участок, город смеётся. Сосед-вдовец (молчаливый, бывший капитан кавалерии/наследник ранчо) помогает руками, а не деньгами. Земельный спекулянт хочет её воду — она стреляет первой. Раскрытие его силы, предложение.

### 3.3 Деньги и ресурсы
- Всё-видео ≈ 200–250 клипов. Flow у пользователя **≈480 кредитов, ~12 за клип ≈ 40 клипов** → во Flow (через Claude Code, «ингредиенты») — первая минута, унижение, кульминация, предложение, дети, обложки. Остальное (~160 клипов) через фабрику API ≈ **$90–110** (фильм 3: ~100 клипов ≈ $71 со всем).
- Удешевление: из одного 8-с клипа брать 2 кадра; склейки из пейзажей переиспользовать в серии; 15 мин вместо 18.
- **Музыка:** 3–4 новых трека ElevenLabs (тема унижения — пианино+струнные; расплата — нарастающие струнные; ночная угроза; любовный финал — скрипки), остальное из библиотеки серии (`S2:Mxx` фильм 2, M01–M04 фильм 3). Голос рассказчика не нужен.
- **Бюджет $90–110 пользователь ещё не одобрял** (раньше говорил «не готов к $120», фильм 3 одобрил ~$71+резерв). Перед запуском — смета через `film_package_prepare` и его «ок». Сам Claude одобряет только до $3.

### 3.4 Как производить
- Shotlist с `production.edit.engine = "v2"` (новый монтаж фабрики), `policy_retry_max` по умолчанию, 8 хуков. Ворота ревью не одобрять без «ок» пользователя.
- Фабрика теперь сама: обход отказов Google (варианты → «ингредиенты» Veo 3.1 Fast → Veo 3.1), статус NEEDS_MANUAL + «Пакет для Flow», кнопка «Остановить», финальный монтаж только по кнопке «Собрать фильм» / `film_edit_render`. Это **первая живая проверка** новой фабрики — сравнить её монтаж с ручным (`montage/western_barn_storm/build.py`) и записать косяки для Claude Code.

## 4. Фабрика (сервер root@94.183.189.187, `/opt/moiastro-engine`)
### 4.1 Состояние
- На сервере ветка **`feature/youtube-mcp-phase2` @ `4a3a3d5`** (внутри фазы 1, 1.5 и 2). Все сервисы `active`: `moiastro-provider-worker`, `moiastro-studio`, `moiastro-mcp`, `moiastro-oauth`. Доставлены `numpy`, `tzdata`.
- PR в `permradar-code/moiastro-engine`: **#1** фаза 1 (монтаж v2, загрузка/пропуск клипов, ZIP, переформулировки), **#2** фаза 1.5 (ингредиенты, NEEDS_MANUAL, отмена/приоритет/сторож, правки монтажа фильма 3, 8 хуков), **#3** YouTube MCP. Все draft, не слиты (см. план, п. 3). Задания: `docs/FACTORY_V2_PHASE1.md`, `docs/FACTORY_V2_PHASE1_5.md`, `docs/FACTORY_V2_PHASE2_YOUTUBE.md` в этом репо.
- Деплой делает пользователь под root: `cd /opt/moiastro-engine`, git **от `sudo -u moiastro`** (у root нет ключа GitHub), `pip` только конкретных пакетов (`sudo -u moiastro /opt/moiastro-engine/.venv/bin/pip install <пакет>`), не `-r requirements.txt`; перезапуск `systemctl restart moiastro-provider-worker` (если менялся provider_worker) → `moiastro-studio` → `moiastro-mcp`; проверка `curl -s http://127.0.0.1:8788/health` → PASS. Перезапуск только с его разрешения и когда ничего не генерируется.
- Следующий этап (не начат, по желанию): авто-шортсы из вертикальных хуков, авто-обложки, сценарий → shotlist с проверкой бюджета и запретных тем.

### 4.2 Новые MCP-команды (видны в новом чате)
- Фильмы: `film_asset_skip/_unskip`, `film_edit_render`, `film_download_links`, `film_job_cancel`.
- YouTube (профиль по умолчанию `new_channel` = Cedar Bluff): `youtube_publish_video` (+`youtube_upload_status`), `youtube_video_update` (название/обложка только с `confirm_title_change=true`), `youtube_thumbnail_set`, `youtube_captions_upload`, `youtube_playlist_add/_playlists_list`, `youtube_my_videos`, `youtube_comments_inbox`, `youtube_comment_reply/_post/_moderate` (по умолчанию `dry_run=true`, лимит 20 за вызов / 100 в день), `youtube_video_retention`, `youtube_video_reach` (показы/CTR из Reporting API, задержка 1–2 дня; первый вызов с `ensure_job=true`, проверить через 2 дня), `youtube_video_sources`, `youtube_video_compare`, `youtube_audience`, `youtube_shorts_to_long`, `youtube_competitors_set/_report`, `youtube_digest_now`, `youtube_quota_status`, `youtube_profiles_list`.
- API не умеет: A/B-тест обложек, конечные заставки, подсказки, закреп комментария, «Связанное видео» у шортса, статистика в реальном времени (за 60 мин). Это руками в Студии. Живые счётчики просмотров/лайков/комментариев есть (`youtube_public_video_report`).

### 4.3 Telegram (не настроен)
Токена нет ни в одном `/etc/moiastro-secrets/*.env`. MCP берёт секреты из `/etc/moiastro-secrets/montage.env`. Шаги для пользователя: @BotFather → `/newbot` → токен (**в чат не присылать**), написать боту `/start`; на сервере `nano /etc/moiastro-secrets/montage.env` → `MOIASTRO_TELEGRAM_TOKEN=...`; chat id: `set -a; . /etc/moiastro-secrets/montage.env; set +a; curl -s "https://api.telegram.org/bot$MOIASTRO_TELEGRAM_TOKEN/getUpdates" | grep -o '"chat":{"id":[-0-9]*'` → `MOIASTRO_TELEGRAM_CHAT_ID=...`. Проверить, какой `EnvironmentFile` у `moiastro-studio` (`systemctl cat moiastro-studio | grep EnvironmentFile`). Сводка: в `ops/moiastro-youtube-digest.service` поменять `EnvironmentFile` на `montage.env`, `cp ops/moiastro-youtube-digest.{service,timer} /etc/systemd/system/ && systemctl daemon-reload && systemctl enable --now moiastro-youtube-digest.timer`; перезапуск studio и mcp.

## 5. Как работать в новом чате
1. `git clone https://github.com/permradar-code/factory-packages && cd factory-packages && git checkout tools/montage` (если push не проходит — `add_repo` owner `permradar-code`, repo `factory-packages`, access `push`; для moiastro-engine — то же).
2. Мост к компьютеру пользователя работает, только если чат связан с компьютером через приложение Claude для ПК («Link to this computer») и подключена папка `C:\ai\projects`. Если инструментов `mcp__remote-devices__*` нет — попросить пользователя связать чат (или прикрепить файлы). Команды: `device_list_dir` / `device_stage_files` / `device_commit_files` (≤ ~20 МБ на файл через stagedPath; большое резать на части по 19 МБ + `join.bat`).
3. Фоновые процессы в контейнере умирают в конце хода — долгий рендер ждать в том же ходе.
4. vidIQ работает (outliers, similar_thumbnails, video_watch — разбор чужого ролика целиком, 25 кредитов). NexLev лимит до 11 окт 20:03 UTC.

## 6. Правила, которые не меняются
- Ключи (ElevenLabs/OpenAI/Google/Telegram) никогда не печатать, не писать в файлы и git, не просить в чат. Аккаунты за пользователя не создавать. Блокировки и фильтр знаменитостей не обходить.
- Файлы > 100 МБ в git не класть. Не перезаливать видео, ничего не накручивать, не спамить комментариями.
- Генерацию до $3 Claude одобряет сам, дальше спрашивать. Гейты фабрики без «ок» пользователя не одобрять. Незакоммиченное в `/opt/moiastro-engine` не затирать.
- Не менять название/обложку лонга во время A/B-теста без решения пользователя (фильм 2 он решил переупаковать сам).
