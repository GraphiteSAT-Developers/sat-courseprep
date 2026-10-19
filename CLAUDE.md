# Notes for Claude

Start with `HANDOFF.md` for what the project is and where things live.

## Shipping a change (standing instruction from the owner)

When a change to the site is finished and checked, ship it without asking first:

1. Rebuild with `python website/build.py` and run the tests with `cd backend && python -m unittest discover tests`.
2. Commit on a `claude/...` branch made from the latest `main`, and push it.
3. Open a pull request into `main`, wait for CI (`secrets`, `tests`, `audit`) to pass, fixing anything that fails,
   then squash-merge it. Render rebuilds from `main` when auto-deploy is on (not confirmed from here).
4. Update the preview artifact, https://claude.ai/artifact/Etm9RYADujz8Pfv7GzmeBm, from `website/artifact/`.
   The pages add up to more than one publish can carry, so send them in two parts to the same URL. If another
   session published to it in the meantime, keep their changes rather than overwriting them.

Then tell the owner what shipped, the PR link, and that Render should be deploying it.

This covers changes the owner asked for. Still ask first before anything hard to undo or outside the site: deleting
data, changing `render.yaml` or the database, prices in `backend/app/services/plans.py`, or legal pages.
