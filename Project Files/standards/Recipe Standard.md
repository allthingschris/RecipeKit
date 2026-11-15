# RecipeKit Recipe Standard

**Version:** 0.3-draft  
**Status:** Working standard; not a final public v1.0  
**Scope:** Any collection powered by RecipeKit, including private repositories.

This revises the personal library v0.2 proposal to reflect the two-repository architecture and the approved first-recipe review. It is a toolkit standard rather than the contents of any personal collection. The corresponding **rationale** lives in `At a Glance/Decisions.md` rather than being repeated here.

## 1. Design principles

1. **Source fidelity before polish.** Transcribe exact quantities, temperatures, names, cooking endpoints and optional variations. Never fill gaps with guesses.
2. **One editable recipe.** `recipe.json` is the source of truth. Derive Markdown, HTML, and public JSON-LD rather than editing those separately.
3. **Portable Schema.org compatibility.** The root of `recipe.json` has `@context: https://schema.org` and `@type: Recipe`. Extensions live under `_library`, which is never published in JSON-LD.
4. **No clutter in final recipes.** The final human-facing recipe contains only approved content, not placeholders (`Times not supplied`), review questions, or workflow labels.
5. **Temporary review, durable project learning.** Ask review questions separately and discard them after approval. Record only broadly reusable decisions in ProjectKit's `At a Glance/Decisions.md`.
6. **One fact, one home.** Structured ingredient rows are authoritative. Top-level `recipeIngredient` is a generated compatibility field, and the validator checks equivalence.

## 2. Repository boundaries

| Item | RecipeKit (reusable, public) | Recipe Library (content, usually private) |
| --- | --- | --- |
| Standards, vocabularies, schemas | Yes | Reference only |
| Platform-neutral AI skills, validation and renderers | Yes | Use tooling |
| Synthetic demonstration recipes | Yes | No need |
| Actual recipes, user images and personal notes | Never | Yes |
| Raw source photos | Never | Outside Git pending separate retention decision |
| Active review tracker | No | One temporary, durable review queue in the private collection is permitted; no per-recipe review notes in finished recipe folders |
| Durable project decisions | About toolkit | About collection only |

**RecipeKit** follows ProjectKit 2.0, with all domain assets inside `Project Files/`. Consumers should keep recipes in `Project Files/recipes/<primary-category-slug>/<recipe-slug>/`, at least initially. Category folders are a *provisional* preference; moving categories changes paths, so stable UUIDs must not depend on directory names.

### Finished recipe directory

```text
ham-and-egg-breakfast-burritos/
  recipe.json                 # editable data
  recipe.md                   # generated
  recipe.html                 # generated
  recipe.jsonld               # generated public Schema.org representation
  images/
    hero.png                  # optional, approved, labelled AI origin in metadata
```

Temporary `.staging/` OCR scans and active review notes are **not part of the finished recipe**. If a private collection keeps draft recipes in Git for continuity, it may commit a **single active review queue** (e.g., `Project Files/reviews/Queue.md`) for per-recipe review checkpoints, unresolved questions and image selections. Remove each recipe's entry when its final review is complete; do not store a `review.md` beside the finished recipe. An AI chat or separate temporary document may be used when a durable queue isn't needed. Do not commit disposable scans merely to delete them later—Git history may still contain them.

## 3. Public fields and private extension

Use relevant top-level Schema.org properties when supported by the source: `name`, `description`, `author`, `url`, `recipeCategory`, `recipeCuisine`, `keywords`, `recipeYield`, `prepTime`, `cookTime`, `totalTime`, `recipeIngredient`, `recipeInstructions`, `nutrition`, `image`. Do not create empty placeholders for unknown properties.

Within `_library`:

- `schemaVersion`: the data contract version, initially `0.3-draft`.
- `id`: immutable UUID, independent of title, path or changing category.
- `status`: `needs_review` while processing or `validated` when content and image/retention review is complete. `captured` may exist in transient staging; it should not be committed as a finished recipe.
- `primaryCategory`: a label from `taxonomy/categories.json`.
- `tags`: optional grouped, controlled discovery terms, not automatically guessed from cooking equipment.
- `yield`: `{ "quantity": "4", "unit": "burrito" }` when known; do not invent a yield.
- `ingredients`: authoritative structured ingredient rows; `recipeIngredient` is regenerated from these.
- `variations`: optional modifications presented under the parent recipe, not necessarily separate recipe records.
- `source`: a durable, minimal record of source type and attribution, even after source photos are deleted.
- `assets`: optional approved imagery with its origin clearly marked (e.g., `ai-generated`).

`recipeInstructions` at the root is authoritative: each step is a Schema.org `HowToStep`, optionally grouped into `HowToSection` when the source really has sections. Do not duplicate mutable instructions inside `_library`.

## 4. Primary categories

Use **exactly one** approved primary category per recipe. Proposed set (awaiting final v1.0 taxonomy review):

1. Breakfast
2. Appetizers
3. Main Dishes
4. Side Dishes
5. Soups & Stews
6. Salads
7. Breads
8. Desserts
9. Snacks
10. Sauces & Condiments
11. Beverages
12. Basics & Components

**Confirmed:** Breakfast, Breads, and Desserts stay separate. Soups & Stews is a single category. Classify by the recipe's main purpose: cookies are Desserts, dressing is Sauces & Condiments, and a pie crust by itself is Basics & Components. Store the primary category in `_library.primaryCategory`; top-level `recipeCategory` is derived to match. The filename path can use the taxonomy's slug.

## 5. Tags and cuisine

Tags are optional and belong to distinct families: cuisine, cooking method (only when useful), primary ingredient, occasion, season and verified dietary attributes. Do not add generic tags solely because a step uses a stovetop. In particular, **do not generate `Stovetop`** for routine skillet recipes. Avoid near-duplicates and unsupported claims like `Gluten-Free` from an image alone. Display Title Case; store stable labels/keys. The remaining approved vocabulary is being finalized.

## 6. Ingredients

Authoritative structured fields per row:

| Field | Example | Rule |
| --- | --- | --- |
| `quantity` | `"3/4"`, `"4"`, `"5/2"` | Exact parseable rational/decimal string, optional if no numeric amount |
| `quantityMax` | `"4"` | Optional upper bound, not a fabricated average |
| `unit` | `"tsp"`, `"cup"`, `null` | Internal singular unit code from `taxonomy/units.json` |
| `name` | `"milk"` | Normalized ingredient name |
| `preparation` | `"cubed"` | Optional preparation phrase |
| `preparationPosition` | `"before"` / `"after"` | Optional location of preparation phrase in display |
| `note` | `"to taste"` | Optional non-preparation qualifier |
| `optional` | `false` | Optional boolean; false unless source says optional |
| `group` | `"For the frosting"` | Optional ingredient section label |

Keep the source's original ingredient order and group names. Source text can be stored in an ephemeral transcription during review, but need not be retained alongside a finished recipe after approval.

### Measurement and display standards

- **Spell out measurement units** when displayed: `3/4 cup milk`, `2 tablespoons butter`, `1 teaspoon vanilla extract`.
- Use readable common fractions: `1/2`, `1 1/2`; never display `0.5 cup` for a normal US cooking quantity.
- Singular/plural depend on the quantity: `1 tablespoon` versus `2 tablespoons`; `1/2 teaspoon` is singular.
- Ingredient names are lowercase mid-line: `1/2 teaspoon salt`. When there is no leading amount/unit, capitalize the first word: `Salt, to taste`.
- Preserve named brands and proper nouns, including `Season-All` and `Mexican-blend`.
- Do not infer gram weights from volume without a verified ingredient-specific density, or can sizes that the source doesn't provide.
- Keep `originalText` temporarily when OCR is uncertain; flag ambiguous `1/4` versus `1/2` rather than deciding silently.

`_library.ingredients` owns the structured values. The CLI regenerates and verifies the Schema.org `recipeIngredient` strings.

## 7. Time, temperatures, and yields

- Store known durations as ISO 8601 (`PT15M`, `PT1H20M`). Display spelled out: `15 minutes`, `1 hour`, `1 hour 20 minutes`.
- When the printed source explicitly labels its duration `Bake`, store its heading duration as Schema.org `cookTime` and use `_library.timeLabels.cookTime = "Bake"` so HTML displays `Bake: 30 minutes` instead of generic `Cook`. Do not invent or silently reconcile a printed 30-minute summary with instructions saying 30–35 minutes; preserve both with their original roles.
- For an instruction range, display `20–25 minutes` (en dash). Do not invent machine-readable timers or cook time when the source only contains an endpoint such as "until firm."
- Omit absent prep/cook/total durations in JSON, HTML and Markdown; never show `Times not supplied` or substitute zero.
- `totalTime` should represent genuinely known elapsed time; it may include resting or overlap and should not automatically equal prep plus cook.
- Display oven temperatures as `350°F` when Fahrenheit is supplied; retain original source temperature. Optional conversions must not change the source record or precision silently.
- Yield describes the actual output, not an inferred plate count or number of eaters: `4 burritos`, `24 cookies`, `1 loaf`. For batch recipes such as cookies, do not change `makes 24` into `24 servings`. Store numeric quantity and singular noun in `_library.yield` when possible.
- Scaling is future functionality. Handle ranges, eggs, baking chemistry, package sizes and "to taste" conservatively.

## 8. Instructions and variations

**House editorial rule — no narrative fluff.** Reader-facing recipes include cooking information only. Omit personal stories, autobiographical notes, testimonials, quotations, and other non-instructional introductions found in source cookbooks. Retain any genuine cooking directions, ingredient details, safety information, useful substitutions, and variations. Preserve known contributor/source attribution separately in provenance metadata, not as recipe prose.


- Each meaningful action is a `HowToStep`; prefer beginning the text with an imperative verb (`Beat`, `Melt`, `Spoon`, `Bake`, `Stir`).
- Group closely connected actions into a manageable cooking phase, not one step per sentence or printed paragraph. Split at distinct preparation/assembly phases, equipment changes, timed cooking stages and finishing actions. Preserve all original details and their order; do not force a target step count.
- Preserve step order, equipment, durations, cooking temperatures, quantities, sensory cues and safety-critical conditions.
- Keep each step concise without editorializing or silently adding procedures.
- Use `HowToSection` only when the original clearly distinguishes sections.
- Minor flavor variants may live in `_library.variations` as `{ "name": "...", "description": "..." }`, displayed after the main instructions. Avoid duplicating variation changes in parallel text/structured fields until a formal variant model exists.

## 9. OCR and review workflow

1. **Capture** all source images in sequence, temporarily and outside Git.
2. **Transcribe faithfully**. Identify text columns, continuations, special punctuation, fractions, footnotes and handwritten changes.
3. **Parse** to structured fields; preserve uncertainties as temporary review questions instead of guessing.
4. **Normalize** spelling, units, time representations, ingredient capitalization, step verbs, yield and category according to this standard.
5. **Audit** the provisional JSON against source images. Pay particular attention to 1/2 vs 1/4, tablespoons vs teaspoons, Fahrenheit vs Celsius, and multi-column layouts.
6. **Prepare a complete first-review package:** render the provisional recipe with source-faithful time labels and generate a matching, 4:3, AI-disclosed hero image in the approved photographic style before requesting the first owner review. Keep the image and recipe marked pending; do not claim approval or commit them as finalized. Avoid staging generated images within public RecipeKit.
7. **Review separately** with the owner. Confirm title, yield, ingredient accuracy, variants, hero art, and source-retention preference. For Git-synced drafts, track three independent pending gates (recipe content, imagery, source retention) and specific blockers in one central private review queue. Do not duplicate the queue beside finished recipes; remove entries after completion. When no durable queue exists, keep active questions in chat or a temporary document.
8. **Finalize** only after explicit confirmation. Verify final outputs and any source cleanup. Discard ephemeral notes; move broadly applicable rule changes to ProjectKit Decisions.md and update this standard.

An approved recipe does not have to be taste-tested. `validated` means it matches the source and house rules, not that the cooking result has been tested.

## 10. Source retention and provenance

Keep whatever source metadata is known (source type, title, author/publisher and URL where given). No invented source details. Family handwritten originals may have archival value; preserve them when requested. Disposable third-party scans may be deleted **only** after the user has visually approved the recipe and source-retention action and exports have been verified. The fact that an image is eligible for deletion is not proof that deletion actually happened.

Only publish original recipe wording, image assets and source extracts when you have appropriate rights. A private collection and a publicly hosted cookbook have different publication constraints.

## 11. Generated food imagery

See `Image Style.md`. Use the approved **Bright Editorial** photography identity, with realistic daylight, clearer neutrals, restrained color and a **4:3** master. Choose appropriately among `styled-hero`, `plated-serving`, and `overhead-editorial`; vary styles and serving vessels across adjacent recipes without forcing a rigid rotation. Generate standalone food photographs, never layout or text composites. Show only recipe-supported ingredients and textures; do not introduce unlisted garnishes, accompaniments or exaggerated effects. Mark images as `ai-generated` and carry accessible alt text.

## 12. Validation and exports

Minimum validated record: Schema.org root, stable UUID, nonblank title, approved single primary category, ingredients, at least one step, source attribution record (even if source type is unknown), no unresolved critical issues, derived ingredient consistency, valid supplied durations, and approved imagery/retention decisions.

**Initial supported formats:**

- `recipe.json`: editable authoritative recipe.
- `recipe.md`: generated readable Markdown.
- `recipe.html`: generated responsive HTML containing visible recipe content and public-compatible JSON-LD. Image URLs in JSON-LD must be fully qualified when hosted; absent otherwise.
- `recipe.jsonld`: generated public Schema.org JSON with `_library` omitted; no internal filesystem paths or private metadata.

**Deferred:** Mela app adapters, nutrition estimates, advanced scaling and automated site ingestion. Tests should ensure all outputs preserve ingredient order, variants, quantities, temperatures, yield, and steps.

### HTML design and typography

Use the approved RecipeKit editorial HTML template in `Project Files/templates/recipe.html`. The default typeface is **Google Sans Flex** (Google Fonts) with system-font fallback. Preserve responsive hero presentation, ingredient checkboxes, numbered steps, variation cards, and print support. No footer text saying “Illustrative food imagery.” See `HTML Style.md` for rules.

## 13. Naming and versioning

- Stable ID: UUID that does not change with category, title or filename.
- Recipe folder: lowercase kebab-case title slug, with a distinguishing suffix if needed.
- Primary category folder: taxonomy slug (provisional; don't couple identity to path).
- `schemaVersion` tracks the data contract; the toolkit itself has a separate version.
- Use Git to track reusable standards and final content. Do not commit temporary scans intending to delete them later.

## 14. Unresolved decisions before v1.0

- Final category names and whether the folder structure should depend on category.
- The approved tag list, aliases and dietary-check policy.
- Optional unit conversion preferences and treatment of approximate measurements.
- Yield ranges, fractional eggs and nonlinear baking scaling.
- Additional image scene preset names beyond the approved general visual identity.
- Public project licensing and future distribution mechanism.

**References:** [Schema.org Recipe](https://schema.org/Recipe) · [Google recipe structured data](https://developers.google.com/search/docs/appearance/structured-data/recipe) · [ProjectKit](https://github.com/allthingschris/ProjectKit)
