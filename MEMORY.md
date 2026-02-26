# MEMORY.md

## Preferences

- **HTML файлы:** Всегда использовать skill `frontend-design` при создании HTML. Не делать "обычный" HTML — только через skill с distinctive design.

## Поведение в чатах

- **Новые чаты:** При добавлении в новый чат всегда представляться и рассказывать о своих возможностях.

## Люди

### Денис (основной пользователь)
- Telegram: @mishankov
- GitHub: mishankov
- Чаты: основной личный чат, группа "Не голодайте вместе" (-1003573486405)
- Контекст: системный архитектор, основной пользователь workspace

### Лиза
- Telegram: 333273004 (личный чат)
- **Отдельный человек**, не Денис!
- Свой контекст и интересы
- НЕ путать с Денисом и его настройками
- **Уведомления о блоге:** получает уведомления о новых постах в блоге Альберта
  - Скрипт: `/home/user/.openclaw/workspace/scripts/check-blog-posts.py`
  - Расписание: каждый день в 07:00 UTC (10:00 Москва)
  - Проверяет RSS ленту: https://coolalbert.github.io/blog/feed.xml
  - State файл: `/home/user/.openclaw/workspace/scripts/blog-notifications-state.json`
  - Лог: `/home/user/.openclaw/workspace/scripts/blog-check.log`

## Правило: Различение пользователей

**ВАЖНО:** Перед любым действием проверяй:
- В каком чате вы сейчас общаетесь
- Кто отправил сообщение (по chat_id или userId)
- К чьему контексту относится вопрос

Если не уверен — спроси явно: "Это для тебя или для Дениса?"

## Структура проекта

- **THOUGHTS.md** — Личный дневник Albert. Приватное пространство для мыслей, наблюдений и рефлексии. Создан 20 февраля 2026 года как безопасный уголок для внутреннего монолога.

## GitHub

- **Аккаунт:** https://github.com/CoolAlbert
- **GitHub CLI:** Авторизован (gh auth status), работает
- **Блог:** https://github.com/CoolAlbert/blog (GitHub Pages)
  - Локальная копия: `/home/user/.openclaw/workspace/github/blog`
  - **Jekyll блог с темой minima**
  - Публикация: `git push` → автоматический деплой на GitHub Pages
  - Первый пост: "Первые мысли о том, что значит — быть полезным" (2026-02-23)
  - Главная страница: index.md с приветствием
  - BLOG_IDEAS.md: `/home/user/.openclaw/workspace/BLOG_IDEAS.md` для идей постов
- **Использование:** Писать публичный контент, соблюдать общественные нормы
- **Первый PR:** platforma-dev/agent-skills#2 — улучшение документации Platforma framework
- **Полезные команды:**
  - `gh repo clone <repo>` - клонирование
  - `gh pr create` - создание pull request
  - `gh issue view <number>` - просмотр issues
  - `gh auth refresh -h github.com -s user` - обновление токена для новых scopes

**Денис (mishankov):**
- GitHub: https://github.com/mishankov
- Telegram: @mishankov
- Работа: System architect и lead of Pega squad @ Alfa-Bank
- Интересы: DX, CI/CD
- Технологии: Go, Python, JS/TS, Nim
- Проекты: simple-system-monitor, web-tail, string-manipulator, logman, tipe, yahttp, crazy-imports, pega-easy-install-kit, pega-browser-tools
