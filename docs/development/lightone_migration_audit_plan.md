# LIGHTONE V2 Django Migration Audit Plan

## Purpose

This document records the current `lightone_v2_django/lightone/migrations/` risk review and proposes a safe cleanup plan.

This PR intentionally does **not** delete, rewrite, or reorder migration files. It is a planning/audit PR only.

## Scope reviewed

Reviewed files:

- `lightone_v2_django/lightone/models.py`
- `lightone_v2_django/lightone/migrations/0001_initial.py`
- `lightone_v2_django/lightone/migrations/0002_membersession_member_membersession_trainer.py`
- `lightone_v2_django/lightone/migrations/0003_membersession_qc_score_and_more.py`
- `lightone_v2_django/lightone/migrations/0003_member_session_indicator.py`
- `lightone_v2_django/lightone/migrations/0004_membersession_function_training_score_and_more.py`

## Current model baseline

The current `lightone/models.py` defines the active `lightone` app models as:

- `MemberSession`
- `StrategyItem`

The current `MemberSession` model includes these notable fields:

- `member`
- `trainer`
- `member_name`
- `trainer_name`
- `goal`
- `discomfort_area`
- `qs_score`
- `jatc_score`
- `form_accuracy`
- `pain_response`
- `rpe`
- `qc_score`
- `qs_form_component`
- `qs_discomfort_component`
- `qs_rpe_component`
- `qs_qc_component`
- `safety_notice`
- `route`
- `qc_status`
- `memo`
- `created_at`

The current `models.py` does **not** define these legacy models:

- `Member`
- `Session`
- `Indicator`

## Findings

### 1. Duplicate `0003` migrations exist

There are two migrations numbered `0003`:

- `0003_membersession_qc_score_and_more.py`
- `0003_member_session_indicator.py`

Both depend on:

```text
("lightone", "0002_membersession_member_membersession_trainer")
```

This creates a migration branch conflict. Django can interpret this as multiple leaf nodes unless a merge migration or history cleanup is performed.

### 2. One `0003` migration introduces legacy models no longer present in `models.py`

`0003_member_session_indicator.py` creates:

- `Member`
- `Session`
- `Indicator`

These models are not present in the current active `models.py`. This indicates that a previous data model design was partially replaced but its migration history remains.

### 3. `0004` follows only one side of the duplicated `0003` branch

`0004_membersession_function_training_score_and_more.py` depends on:

```text
("lightone", "0003_member_session_indicator")
```

It does not depend on `0003_membersession_qc_score_and_more.py`. Therefore, one 0003 branch is not integrated into the later chain.

### 4. Potential duplicate field operations exist

`0003_membersession_qc_score_and_more.py` adds `MemberSession.qc_score` and `MemberSession.safety_notice`.

`0004_membersession_function_training_score_and_more.py` also adds `MemberSession.qc_score` and `MemberSession.safety_notice`.

This can cause duplicate-column or inconsistent migration-state issues depending on which migration branch has already been applied.

### 5. Current `models.py` and migration history are not aligned

Current `models.py` includes some fields introduced by `0003_membersession_qc_score_and_more.py`, such as:

- `qc_score`
- `qs_form_component`
- `qs_discomfort_component`
- `qs_rpe_component`
- `qs_qc_component`
- `safety_notice`

However, current `models.py` does not include several fields introduced by `0004_membersession_function_training_score_and_more.py`, such as:

- `function_training_score`
- `lifestyle_score`
- `posture_score`
- `review_note`
- `trainer_confirmed`

This means the active model definition and migration history should be reconciled before adding new schema work.

## Risk level

Overall migration risk: **High for schema changes, medium for local MVP recovery**.

Reason:

- The project appears to be in early MVP development.
- Migration history contains a branch conflict.
- Some migrations refer to legacy models not used by current code.
- The app may still be recoverable safely if database state is treated carefully.

## Safe cleanup principle

Do not delete or rewrite migrations until the target database policy is decided.

Before cleanup, decide one of the following:

1. **Disposable development DB policy**
   - Use this if there is no production data and no important SQLite data to preserve.
   - This is likely the simplest MVP path.

2. **Preserve existing DB policy**
   - Use this if any existing `db.sqlite3` or deployed DB data must be preserved.
   - Requires careful migration merge and possibly custom data migration.

## Recommended plan

### Phase 1 — Current PR

- Add this audit document only.
- Do not change migration files.
- Do not change `models.py`.
- Do not change database schema.

### Phase 2 — Local verification

Run locally in VS Code:

```bash
cd lightone_v2_django
python manage.py showmigrations lightone
python manage.py makemigrations --check --dry-run
python manage.py check
```

Record:

- Which migrations Django sees as unapplied/applied.
- Whether Django reports multiple leaf nodes.
- Whether `makemigrations --check --dry-run` reports model changes.

### Phase 3 — Choose cleanup route

#### Option A: MVP reset route

Use when DB is disposable.

Planned steps:

1. Back up current migration files into documentation or archive notes.
2. Remove local development DB only, not user data.
3. Rebuild migration history from current `models.py`.
4. Re-run:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py check
python manage.py runserver
```

Pros:

- Fastest route to a clean MVP.
- Best for early portfolio/project development.

Cons:

- Not suitable if real data must be preserved.

#### Option B: Preservation route

Use when DB data must be preserved.

Planned steps:

1. Create a merge migration to resolve duplicate `0003` leaf nodes.
2. Carefully reconcile duplicate `qc_score` and `safety_notice` operations.
3. Add or remove model fields only through explicit follow-up migrations.
4. Test on a copied database before touching the main DB.

Pros:

- Safer for real data.

Cons:

- More complex and slower.
- Requires exact knowledge of applied migration state.

## Recommendation for LIGHTONE V2

Recommended route: **Option A — MVP reset route**, but only after confirming that no real user data or important local DB state must be preserved.

Reason:

- LIGHTONE V2 appears to be an early MVP/portfolio-stage project.
- The active code has moved toward `MemberSession` and `StrategyItem`.
- Legacy `Member`, `Session`, and `Indicator` migrations remain from an older schema direction.
- A clean model-first migration chain will be easier to maintain and explain in GitHub, VS Code, and future demo settings.

## Follow-up PR proposal

Create a separate PR titled:

```text
Normalize LIGHTONE V2 migrations for current MVP models
```

That PR should only proceed after local verification and DB preservation decision.

Minimum acceptance criteria for the follow-up PR:

```bash
cd lightone_v2_django
python manage.py makemigrations --check --dry-run
python manage.py check
python manage.py migrate
python manage.py runserver
```

Expected result:

- No import errors.
- No duplicate migration leaf conflict.
- No unexpected model changes.
- Admin page loads after superuser creation.

## Safety notes

- Do not add medical diagnosis, disease prediction, treatment, or prescription language during migration cleanup.
- Do not commit `.env`, real member data, real counseling records, or private health-related data.
- Keep LIGHTONE positioned as a non-medical PT consultation support SaaS MVP.
