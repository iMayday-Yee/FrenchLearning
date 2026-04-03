# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PhD research platform studying how AI interaction autonomy levels (low/adjustable/high) and avatar types (human/robot) affect French language learning. Designed for 200 participants across a 10-day study with 6 experimental groups (3 autonomy levels x 2 avatar types, 30 slots each).

The platform is written primarily in Chinese (UI, comments, prompts). All LLM interactions are in Chinese with French vocabulary content.

## Development Commands

### Backend
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 app.py                    # Runs on :5000 with debug mode
```

### Frontend
```bash
cd frontend
npm install
npm run dev                       # Runs on :3000, proxies /api to :5000
npm run build                     # Production build to dist/
```

### Both at once
```bash
./start.sh                        # Starts backend (:5000) + frontend (:3000)
```

### Production
Gunicorn with gevent workers behind Nginx. See `deploy.sh` and `nginx.conf` (paths need updating from `/path/to/`).

### System dependency
FFmpeg is required for audio processing (pydub).

## Architecture

### Backend (Flask)

**Entry point:** `app.py` -> `create_app()` initializes DB tables, system config, group slots, and scheduler.

**Extensions** (`extensions.py`): Shared Flask extension instances — SQLAlchemy `db`, JWTManager `jwt`, Limiter `limiter` (200/day, 50/hour default).

**Route blueprints** (all registered under `/api`):
- `auth` — registration, login, email verification
- `chat` — main learning flow: intent classification via LLM, word card delivery, audio upload
- `study` — study status, daily progress, phase tracking
- `assessment` — Day 5 vocabulary test (multiple choice + pronunciation)
- `admin` — dashboard, user management, word editing, CSV export
- `wechat` — WeChat public account binding and message handling

**Services:**
- `llm_service` — builds message context, calls MiniMax API, parses JSON response with intent classification (6 intents: `request_material`, `accept_learning`, `reject_learning`, `french_related_chat`, `unrelated_chat`, `other`)
- `group_service` — balanced assignment of users to experimental groups
- `scheduler_service` — APScheduler cron jobs for daily invitations/reminders
- `email_service` — SMTP verification codes via 163.com
- `audio_service` — WebM audio validation (duration/volume)
- `wechat_service` — WeChat template messages

**LLM integration:** System prompt in `prompts/system_prompt.py` instructs the model to return `{"intent": "...", "reply": "..."}` JSON. `parse_llm_response` handles non-JSON fallbacks and normalizes invalid intent labels.

**Data:** `backend/data/words.json` contains the 10-day vocabulary curriculum.

### Frontend (Vue 3 + Vite)

**State management** (Pinia stores in `src/stores/`):
- `user` — auth state and JWT token
- `study` — study phase, day, progress
- `toast` — notification system

**Key views:**
- `Chat.vue` — main learning interface with text chat + audio recording
- `Assessment.vue` — Day 5 vocabulary test
- `Waiting.vue` / `Completed.vue` — phase gates

**Routing** (`src/router/index.js`): Auth guard via `meta.auth`, admin guard via `meta.admin`. The `/chat` route has additional logic redirecting based on study phase (`not_started` -> `/waiting`, `completed` -> `/completed`, `needAssessment` -> `/assessment`).

**API layer** in `src/api/index.js` — Axios instance with JWT interceptor.

### Database (SQLite)

8 models in `models.py`. Key relationships:
- `User` -> `DailyStatus` (one per study day per user)
- `User` -> `ChatMessage` (indexed on user_id + study_day)
- `User` -> `AudioRecord`, `AssessmentAnswer`, `AssessmentSummary`
- `GroupSlot` — tracks capacity per experimental group
- `EmailVerification` — time-limited codes
- `SystemConfig` — key-value runtime settings (study_start_date, max_daily_rounds)

DB file: `backend/instance/french_study.db`. Auto-created by `db.create_all()` on startup.

### Study Flow

Days 1-4: Guided learning (word cards + pronunciation practice, max 20 conversation rounds/day)
Day 5: Assessment (vocabulary multiple choice test)
Days 6-10: Self-guided learning
`STUDY_START_DATE` in config controls when the 10-day timeline begins.

## Configuration

All config is in `backend/config.py`. Key settings:
- `LLM_API_URL` / `LLM_API_KEY` / `LLM_MODEL` — MiniMax LLM endpoint
- `STUDY_START_DATE` — experiment start date
- `MAX_DAILY_ROUNDS` — conversation limit per day (default 20)
- `GROUP_SLOTS` — per-group capacity (default 30 each)
- `REENTER_THRESHOLD_MINUTES` — session re-entry window

## No Automated Tests

This project has no test suite. All testing is manual.
