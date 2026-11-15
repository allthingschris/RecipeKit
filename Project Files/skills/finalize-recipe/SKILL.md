---
name: finalize-recipe
description: Validate an approved provisional recipe, render its final outputs, clean up temporary review material, and document reusable rules in ProjectKit.
---

# Finalize Recipe

**Preflight:** Verify the owner explicitly approved (1) final recipe content and variations, (2) image if present, and (3) a separate source-retention decision. If any are missing, stop and return a concise targeted review question. Approval to delete is distinct from evidence deletion occurred.

1. Read `Recipe Standard.md` and relevant taxonomy. Ensure all critical OCR questions are closed. Update `_library.status` to `validated`; remove `reviewIssues`, `titleStatus`, `originalText` duplicates and other temporary review state before committing.
2. Check title, yield, ingredients, rendered ingredient strings, instructions, variants, source metadata, category and imagery. Use `recipekit.py validate` and fix only confirmed discrepancies.
3. Copy only approved source-of-truth JSON and finished assets into the consuming library's category/slug recipe folder. **Do not** add a permanent `review.md` or disposable source photos to Git.
4. Run `recipekit.py render` to generate `recipe.md`, `recipe.html`, and `recipe.jsonld`. Verify each representation matches the JSON. Mark AI imagery accurately in private metadata; HTML must omit `_library` from public JSON-LD.
5. If deletion of temporary captures was authorized, check the final JSON and exports exist and are readable, then delete only the specific approved disposable captures from staging. Never blindly remove family originals or committed Git history. Confirm actual deletion separately.
6. Discard temporary review notes after recording any **reusable** editorial or technical decisions in the toolkit's `At a Glance/Decisions.md` and updating standards if necessary. Do not duplicate one-off recipe approvals there.
7. If applicable, update the consuming library's `At a Glance/Log.md` with a concise milestone and `Passport.md`/`Next.md` with status and next work using ProjectKit's wrap-up discipline.

If the finalizer cannot access files or cannot verify a deletion, say so explicitly rather than claiming completion.
