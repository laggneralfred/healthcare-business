# Sprint Closure Checklist

Use this checklist whenever a sprint is being frozen from the current implemented baseline.

Closure rule:
- a sprint is not fully closed until tests are green, handoff is finalized, changes are committed, pushed to GitHub, and a sprint-freeze tag is created and pushed

## 1. Confirm The Target Baseline

- identify the sprint being frozen
- confirm the authoritative handoff document for that sprint
- confirm the sprint summary that will appear in the freeze commit and tag message
- update [SPRINT_INDEX.md](/home/alfre/healthcare-business/SPRINT_INDEX.md) so the baseline and target tag are recorded

Current naming convention:
- tag: `sprint-<number>-freeze`
- commit message: `Sprint <number> freeze: <baseline summary>`

Example:
- tag: `sprint-9-freeze`
- commit message: `Sprint 9 freeze: multi-line checkout baseline`

## 2. Verify Tests Are Green

- run the smallest relevant green test command for the sprint being closed
- if a summary log is needed for the clinic suite, use `make test-clinic-summary`
- record the final passing command and result in the handoff if that has not already been done

Current validated test-tooling posture:
- `Makefile` includes `test-scheduling`
- `test-clinic` and `test-clinic-summary` use the scheduling-inclusive clinic scope
- `logs/test-clinic.log` is the summary log artifact

Examples:

```bash
make test-clinic-summary
```

```bash
docker compose exec odoo odoo -d healthcare_dev -u hc_checkout,hc_pricing --test-enable --test-tags /hc_checkout,/hc_pricing --http-port=8070 --stop-after-init
```

## 3. Finalize The Handoff

- finish the sprint handoff document
- confirm the handoff reflects the implemented scope only
- confirm no product scope drift was added beyond the planned sprint slice
- confirm the handoff clearly states the new frozen baseline

Typical handoff file pattern:
- `SPRINT_<number>_HANDOFF.md`

## 4. Review The Diff Before Freezing

- review the staged and unstaged changes
- confirm the sprint closure contains only intended implementation, documentation, and minimal repo/process support
- do not freeze with unrelated experimental work mixed in

Typical Git review commands:

```bash
git status
git diff --stat
git diff
```

## 5. Commit The Freeze

- stage the intended files
- create one explicit freeze commit

Example:

```bash
git add .
git commit -m "Sprint 9 freeze: multi-line checkout baseline"
```

If a narrower add is safer, prefer explicit paths over `git add .`.

## 6. Push To GitHub

- push the freeze commit to the default remote branch or current branch as appropriate for the repo workflow

Examples:

```bash
git push origin HEAD
```

```bash
git push origin main
```

## 7. Create And Push The Freeze Tag

- create an annotated freeze tag that matches the sprint number
- push that tag to GitHub

Examples:

```bash
git tag -a sprint-9-freeze -m "Sprint 9 freeze: multi-line checkout baseline"
git push origin sprint-9-freeze
```

Optional helper:

```bash
make sprint-freeze SPRINT=9 MESSAGE="Sprint 9 freeze: multi-line checkout baseline"
```

The helper:
- creates the annotated `sprint-<number>-freeze` tag
- pushes `HEAD` to the selected remote
- pushes the freeze tag

Default remote:
- `origin`

Override example:

```bash
make sprint-freeze SPRINT=9 MESSAGE="Sprint 9 freeze: multi-line checkout baseline" REMOTE=upstream
```

## 8. Verify The Freeze

- confirm the commit exists on GitHub
- confirm the tag exists on GitHub
- confirm the tag matches the intended freeze commit
- confirm [SPRINT_INDEX.md](/home/alfre/healthcare-business/SPRINT_INDEX.md) points to the same handoff and tag

Useful commands:

```bash
git rev-parse HEAD
git rev-list -n 1 sprint-9-freeze
git tag -l "sprint-*-freeze"
```

## 9. Stop After Closure

Once the sprint is frozen:
- treat the handoff as the authoritative implemented baseline
- do not expand scope unless there is a specific bug, proven operational friction, or an explicit new sprint decision
