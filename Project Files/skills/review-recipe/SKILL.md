---
name: review-recipe
description: Resolve recipe questions and get explicit content, image and source-retention approvals before finalizing an imported recipe.
---

# Review Recipe

Review **one recipe** at a time unless the collection owner explicitly requests a batch. The recipe preview should stay pristine: do not put editorial notes in ingredient or instruction fields.

1. Compare the provisional JSON against all current source material and any prior feedback from the owner.
2. Show only **unresolved or important** questions; organize by title/yield, ingredient fidelity, step fidelity, variations, generated image, and source-image retention. Avoid reasking answered questions.
3. Record feedback in the temporary review conversation/document. Update the provisional recipe; rerun validation. Keep a list of current unresolved uncertainties, not a growing permanent `review.md`.
4. For hero images, follow `Image Style.md`. Require approval of realism, ingredient plausibility, 4:3 crop, and editorial consistency. Clearly identify generated art as generated, not a genuine food photo.
5. Ask for **separate approval** to discard source captures; do not conflate validated content with deletion permission. Family originals should be presumed worth preserving unless told otherwise.
6. Get explicit final approval, then transfer to `finalize-recipe`. Note generalizable editorial-rule decisions for ProjectKit `Decisions.md`; one-off recipe choices are reflected in the recipe itself, not recorded as project-level precedents.

No permanent per-recipe review artifact should survive finalization. Keep source-provenance information inside recipe.json even if captures are deleted.
