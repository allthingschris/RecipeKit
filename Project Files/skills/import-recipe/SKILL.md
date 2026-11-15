---
name: import-recipe
description: Convert recipe photographs, scans, printed cards or webpages into a source-faithful provisional RecipeKit recipe and temporary review questions.
---

# Import Recipe

Use `Project Files/standards/Recipe Standard.md`, taxonomy files, and Image Style for all imports. Keep the private content in the consuming recipe collection, never in the public RecipeKit repo.

1. **Capture:** accept all input pages, photograph order, and source links. Keep original pixels in a temporary local staging area outside committed Git history. Inspect images directly where possible; OCR is an aid, not a source of truth.
2. **Editorial filter:** identify which portions of a busy photo are inside the user's highlighted recipe boundary. Ignore adjacent recipes and food photos that are not the selected recipe. Omit anecdotal lead-ins, personal stories, testimonials, quotations and other non-instructional fluff from reader-facing recipe content; keep recipe-relevant facts and source attribution as metadata when known.
2. **Transcribe:** preserve legible ingredient quantities, units, steps, headings, branded ingredients, yield, cooking cues, and optional variants. Pay special attention to fractions, fine print, and multi-column layouts. Do not infer invisible title or missing times.
3. **Parse:** build provisional `recipe.json` with Schema.org Recipe at root and `_library.ingredients` as structured truth. Derive `recipeIngredient` from the ingredient rows. Use `needs_review`; do not mark validated yet.
4. **Normalize:** spell out units and durations in displayed text, use action-first steps where faithful, consistent ingredient capitalization, and the best-supported category. Do not auto-add a `Stovetop` tag. Leave missing fields absent.
5. **Compare:** reread the source and flag ambiguity (e.g., 3/4 vs 1/4 cup, tsp vs tbsp), missing titles, possible alternate yield interpretations, branded ingredients, and multi-step variations.
6. **Present:** deliver a beautiful provisional recipe **separately** from a short list of review questions. Include title/yield/ingredient/step checks, hero-image review if generated, and explicit source retention preferences. Do not persist review.md next to finished recipes.

Do not delete source images, add uncertain ingredients, claim OCR perfection, or record final approval during import. Use the `review-recipe` skill next.
