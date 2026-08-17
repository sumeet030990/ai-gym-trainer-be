# Plan Generation Endpoint & Progress Tracking

Companion notes to [ai-integration-plan.md](./ai-integration-plan.md) — covers
where the AI call should be triggered from, and how ongoing tracking/
regeneration should work.

## Endpoint placement

- Don't call the AI from `GET /users/me` (`routers/users.py`) — that's a plain
  auth/profile-fetch endpoint and should stay a pure read with no side effects.
- Plan generation is a heavier, external-API operation with its own latency/
  failure modes — give it a dedicated endpoint, e.g. `POST /plans/generate`.
- Trigger it explicitly: after the user finishes the goal questionnaire, or on
  a user-initiated "regenerate my plan" action — not implicitly on every
  profile fetch.

## Folder structure

Follows the existing `router → controller → service → repository` layering
used across the app, with `ai/` as the vendor-agnostic layer:

- `ai/`
  - `agent.py` — provider factory (already exists)
  - `providers/` — one file per vendor: `groq.py`, `ollama.py` (already exist),
    add others as needed
  - `prompts/` — prompt templates for plan generation, kept out of service code
  - `schemas.py` — Pydantic models for structured LLM output (the plan JSON
    shape)
- `app/services/plan_services.py` — builds prompt from user goals/answers,
  calls `ai.agent.get_llm_provider(...)`, parses response
- `app/controllers/plan_controller.py` — orchestrates service + repository
- `app/repositories/plan_repository.py` — DB reads/writes for plans
- `routers/plans.py` — new router, mounted like `routers/users.py`

Provider/model resolution should go through the existing per-user
`user_ai_settings` table (already modeled) rather than a hardcoded vendor, to
satisfy the multi-vendor requirement.

## Progress tracking & regeneration

- **Generate**: after goal questions are answered, call the AI and save the
  structured plan to a new `workout_plans` table (+ day/exercise breakdown,
  linked to the existing `exercises` / `workout_exercises` schemas).
- **Track adherence**: log actual completion against the plan (e.g. a
  `plan_progress` table: planned vs. completed per session/day).
- **On-track check**: a scheduled job (cron) or a check triggered on each
  workout log:
  - compute adherence % (completed vs. planned)
  - below threshold → flag the plan `needs_regeneration`
- **User absent**: same job also checks "last activity date"; no logs for N
  days → flag `needs_regeneration` regardless of the adherence calc.
- **Regenerate**: reuse the generate flow, but feed it the prior plan plus
  actual progress/absence as extra context so the new plan adapts instead of
  starting cold.
- **Versioning**: don't overwrite plans on regeneration — insert a new row
  with a `previous_plan_id` FK, so plan history stays available for display
  and debugging.

## Step-by-step implementation

Status markers below reflect what's already in the repo (`git status`) vs.
what's still to build.

1. **✅ Route** — `routers/ai.py`, mounted in `routers/__init__.py`.
   `POST /ai/generate-plan`, depends on `is_user_authenticated` + `get_session`,
   delegates straight to the controller.

2. **✅ Controller** — `app/controllers/ai_controller.py`.
   `generate_plan(auth_user, db_session)` — currently only loads the user via
   `user_services.get_auth_user_details`. Still needs to call the service layer
   below instead of stopping at "user found".

3. **⬜ Service** — `app/services/ai_services.py` (file exists, empty).
   This is where the real orchestration goes:
   - `build_context(user_id, db_session)` — pull `user_goal_answers`,
     `user_conditions`, `body_measurements`, and gym equipment access into one
     structured dict/Pydantic object.
   - `resolve_ai_setting(user_id, db_session)` — read the user's
     `user_ai_settings` row (provider + model + key), 404 if none configured.
   - `generate_plan(user_id, db_session)` — calls context + settings above,
     invokes the provider, persists the result, returns it.

4. **⬜ Provider config resolution** — extend `ai/agent.py`'s
   `get_llm_provider(llm_name, model_name)` to also accept `api_key`/`api_url`
   and thread them through to `ai/providers/groq.py` /
   `ai/providers/ollama.py` (today `groq.py` takes a `groq_api_key` param but
   `agent.py` never passes one in — that's the gap to close). The value comes
   from the `user_ai_settings` row resolved in step 3, not a hardcoded default.

5. **⬜ Repository** — new `app/repositories/plan_repository.py`, following
   the pattern in `app/repositories/goal_questions_repository.py` (plain
   async functions over `db_session.execute(select(...))`, no classes):
   - `create_plan(db_session, user_id, plan_data) -> WorkoutPlan`
   - `get_active_plan(db_session, user_id) -> WorkoutPlan | None`
   - `get_plan_history(db_session, user_id) -> list[WorkoutPlan]`

6. **⬜ DB schema** — new files under `db/schemas/`, same shape as
   `db/schemas/body_measurements.py` (UUID PK + timestamp mixins):
   - `workout_plans.py` — `user_id`, `status` (`active`/`stale`/`archived`),
     `previous_plan_id` (self FK, nullable), plan payload/reference to
     `workout_exercises`.
   - `plan_progress.py` — `plan_id`, `user_id`, `logged_at`, adherence data
     (planned vs. completed).
   - Register both in `db/schemas/__init__.py` like the existing schemas, then
     `alembic revision --autogenerate` + `alembic upgrade head`.

7. **⬜ Response schemas** — `app/schemas/ai_schemas.py` (new file, mirrors
   `app/schemas/goal_questions_schemas.py`) — Pydantic response models for
   `POST /ai/generate-plan` so the router doesn't return raw ORM objects.

8. **⬜ Wire it up** — update `ai_controller.generate_plan` to call
   `ai_services.generate_plan(user.id, db_session)` and return the schema from
   step 7, replacing today's "just fetch the user" stub.

9. **⬜ Tracking job** — a scheduled task (cron/celery-beat/APScheduler,
   whichever the project standardizes on) that scans `plan_progress` +
   `workout_plans.updated_at` for low adherence or inactivity, and flips
   `workout_plans.status = "stale"`.

10. **⬜ Regenerate endpoint** — `POST /ai/regenerate-plan`, same
    router/controller/service chain as steps 1-3, but `build_context` also
    pulls the previous plan + its progress so the new plan adapts instead of
    starting cold.

## Note on existing schema

`user_ai_settings.api_key` is currently a plaintext column. Since API keys are
credentials, encrypt at rest (app-level encryption before insert, decrypt only
inside the provider adapter) before this ships.
