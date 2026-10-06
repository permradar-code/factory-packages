#!/bin/bash
# Восстановить рабочую среду монтажа в новом контейнере (новый чат).
# Запуск: bash montage/setup_container.sh   (из корня клона factory-packages на ветке tools/montage)
set -e
REPO=$(git rev-parse --show-toplevel); cd "$REPO"
B="pkg/western_widows_piano_v1 film/western_widows_piano_v1 pkg/western_stagecoach_bride_v1 tools/montage"
for b in $B; do git remote set-branches --add origin "$b" 2>/dev/null || true; done
git fetch origin $(for b in $B; do echo "+refs/heads/$b:refs/remotes/origin/$b"; done)

# Исходники фильма 1 -> /home/claude/wwp_pkg, готовый фильм -> /home/claude/wwp_film
[ -d /home/claude/wwp_pkg ]  || git worktree add --detach /home/claude/wwp_pkg  origin/pkg/western_widows_piano_v1
[ -d /home/claude/wwp_film ] || git worktree add --detach /home/claude/wwp_film origin/film/western_widows_piano_v1
# Пакет фильма 2 (то, что пушит Claude Code) -> /home/claude/wsb_pkg
[ -d /home/claude/wsb_pkg ]  || git worktree add --detach /home/claude/wsb_pkg  origin/pkg/western_stagecoach_bride_v1

# Склеить фильм 1 (SHA256 должен начинаться с 4230b8b9)
if [ ! -f /home/claude/film.mp4 ]; then cat /home/claude/wwp_film/The_Widows_Piano_1080p.mp4.part0* > /home/claude/film.mp4; fi
sha256sum /home/claude/film.mp4 | cut -c1-8

# Скрипты монтажа фильма 1 ждут /home/claude/montage, шрифт /home/claude/fonts/Rye-Regular.ttf
mkdir -p /home/claude/montage /home/claude/fonts /home/claude/sh/fonts
cp -rn "$REPO"/montage/western_widows_piano/* /home/claude/montage/
cp -n "$REPO"/montage/fonts/* /home/claude/fonts/
# Скрипты шортсов ждут /home/claude/sh и /home/claude/sh/fonts (Rye + Inter ExtraBold)
cp -n "$REPO"/montage/western_widows_piano/shorts/*.py /home/claude/sh/
cp -n "$REPO"/montage/fonts/* /home/claude/sh/fonts/
mkdir -p ~/.fonts && cp -n "$REPO"/montage/fonts/* ~/.fonts/ && fc-cache -f >/dev/null 2>&1 || true
which ffmpeg >/dev/null || echo "!!! ffmpeg не установлен: apt-get install -y ffmpeg"
echo "OK: wwp_pkg, wwp_film, wsb_pkg, film.mp4, montage, sh готовы"
