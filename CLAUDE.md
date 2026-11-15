# CLAUDE.md

## What this is

RecipeKit is the reusable recipe standard, review workflow, image style, validators, and renderers. It is intended to be publicly shareable; never add private recipe collections or family scans.

## Gotchas

- The Schema.org root is public-compatible, but `_library` is private extension data and **must never enter public JSON-LD**.
- `_library.ingredients` owns ingredient quantities and wording; `recipeIngredient` is derived. HTML and Markdown are generated, not edited by hand.
- Missing times and unknown metadata are omitted, never shown as a placeholder or invented.
- Source scans remain outside Git until approved for retention. Git deletion cannot reliably erase committed history.
- No permanent `review.md` beside finalized recipes. Temporary review material is discarded; durable project-wide decisions belong in `At a Glance/Decisions.md`.
- Use the platform-neutral `import-recipe`, `review-recipe`, and `finalize-recipe` skills when relevant.

## Continuity

Project state lives in `At a Glance/` and follows ProjectKit's one-fact-one-home rule: `Passport.md` (now), `Context.md` (durable), `Next.md` (next), `Decisions.md` (decided and why), `Log.md` (happened). Record new decisions when made, and run the ProjectKit `wrap-up` skill at session end. Use `apply-projectkit` or `update-projectkit` for scaffolding or migrations.

## Working agreement

Before structural changes to `Project Files/`, summarize the plan and confirm intent. Do not silently guess missing amounts, temperatures, times, nutrition, authors, or original titles.
