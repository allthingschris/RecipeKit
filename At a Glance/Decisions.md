# Decisions

<!-- Append-only. Reverse decisions with new entries that cite the earlier number. -->

## D001 — Separate the open toolkit from private collections

**Date:** 2026-11-15

**Context**
The standard, importer workflow, imagery system, and export tools are reusable; the owner’s recipe collection may include personal and family content.

**Decision**
Maintain RecipeKit as a shareable toolkit and recipe-library as a separate private consumer. Use ProjectKit in both repositories.

**Rationale**
Publishing tooling should not require exposing personal recipes, and the public project can serve other collections.

**Consequences**
No personal scans, recipe data, or finished private visuals in RecipeKit. The library references RecipeKit rather than forking its rules.

## D002 — Use Schema.org Recipe with structured private extensions

**Date:** 2026-11-15

**Context**
The collection must be readable by common recipe consumers while supporting reliable scaling, review, and exports.

**Decision**
Store one authoritative recipe.json per recipe; keep Schema.org fields at the root and structured ingredients, yields, and library metadata in _library. Derive recipeIngredient and other display values from structured fields.

**Rationale**
Schema.org works broadly across the web, but native ingredient strings do not fully express quantities and preparation.

**Consequences**
Public JSON-LD exports omit _library. Validators guard against duplicate facts drifting out of sync.

## D003 — Normalize display language without inventing facts

**Date:** 2026-11-15

**Context**
Source recipes vary in duration, unit abbreviations, capitalization, steps, and yields.

**Decision**
Display spelled-out durations and measurements; use context-sensitive ingredient capitalization; prefer action-first instruction steps; express yield as the product (e.g., 4 burritos). Omit unknown times rather than calling them out.

**Rationale**
Consistency improves readability, while preserving actual source meaning and allowing partial recipes.

**Consequences**
Internal duration fields use ISO 8601; units use controlled internal codes; no default Stovetop tag or missing-time label.

## D004 — Keep a small controlled taxonomy and cohesive imagery

**Date:** 2026-11-15

**Context**
A large library requires predictable classification; generated dish photos should resemble one editorial cookbook.

**Decision**
Start with twelve proposed primary categories, retaining separate Breakfast, Breads, and Desserts and combined Soups & Stews. Use a 4:3 photographic master with consistent lighting, color, and restrained styling; allow curated surfaces and dishes.

**Rationale**
A small vocabulary and restrained photographic presets make diverse recipes feel coherent without being repetitive.

**Consequences**
Taxonomy details remain reviewable until v1.0. Do not add generic method tags merely because a step happens on the stovetop.

## D005 — Make recipe reviews temporary

**Date:** 2026-11-15

**Context**
A review.md file beside every finalized recipe would create review clutter and duplicate project-wide decisions.

**Decision**
Conduct editorial review in chat or temporary review material. On approval, keep the pristine recipe and approved media, discard temporary review notes, and record only reusable decisions with rationale in ProjectKit Decisions.md.

**Rationale**
ProjectKit already owns durable project decisions; individual approval checklists do not need long-term residency.

**Consequences**
No review.md in finished recipe folders. Preserve durable source attribution in recipe data; use Next.md for active pending reviews.

## D006 — Require separate approval for source-image deletion

**Date:** 2026-11-15

**Context**
Most imported photographs are disposable after verified transcription, but handwritten family artifacts may be irreplaceable.

**Decision**
Stage source images outside Git. Verify transcription, final exports, and approval before removing any disposable capture; retain family/historical originals when desired.

**Rationale**
Git history retains deleted images and ordinary content approval is not the same as permission to discard sources.

**Consequences**
The workflow must ask for source-retention authorization and verify files before deleting; deletion must not happen by default.

## D007 — Support JSON, Markdown and HTML first

**Date:** 2026-11-15

**Context**
The user wants portable structured data and attractive browser/print-friendly representations, without immediate app-specific integration.

**Decision**
Make recipe.json authoritative and generate Markdown and HTML from it. Defer Mela-specific import/export.

**Rationale**
Fewer formats reduce maintenance and avoid drift. App adapters can be developed later.

**Consequences**
Tooling must include validation and reproducible rendering, including Schema.org Recipe JSON-LD in HTML without private metadata.

## D008 — Adopt the editorial HTML template and Google Sans Flex

**Date:** 2026-11-15

**Context**
The first rendered recipe's editorial redesign was reviewed and approved. The earlier generator used a denser generic layout, and the approved preview displayed an unnecessary footer image disclaimer.

**Decision**
Use the polished responsive recipe design as RecipeKit's shared HTML template, including ingredient checkboxes, prominent image, numbered steps, flavor-variation cards and print support. Prefer Google Sans Flex for typography with system-font fallbacks. Remove the bottom “Illustrative food imagery” notice while preserving accurate image-origin metadata.

**Rationale**
A single reusable template gives every collection a coherent, attractive interface without maintaining HTML independently for each recipe. The font and restrained editorial style reflect the chosen aesthetic.

**Consequences**
The renderer must load `Project Files/templates/recipe.html`, generate HTML from approved `recipe.json` data, preserve offline fallback behavior and render optional fields only when present. `Project Files/standards/HTML Style.md` owns the detailed presentation contract.

## D009 — Adopt approved Iconly icons for recipe UI

**Date:** 2026-11-15

**Context**
The recipe design used hand-written outline icons for yield and printing. Matching Iconly Pro spoon-and-fork and printer SVGs were supplied by the owner, who confirmed permission to use them.

**Decision**
Adopt the supplied Iconly Pro SVGs for yield and print controls, retaining their 24×24 viewBox, warm `#987762` fill and the duotone fork treatment. Store source SVGs as separate icon assets and embed them through the common renderer. Keep asset-specific licensing separate from the toolkit's code license.

**Rationale**
A matched icon family improves visual coherence, while single-source SVG assets simplify future replacements.

**Consequences**
Shared HTML templates and generated recipe pages must use the same assets and avoid inherited strokes that alter filled artwork. Verify any external redistribution scope before granting third-party icon rights.

## D010 — Exclude non-recipe editorial prose

**Date:** 2026-11-15

**Context**
Printed cookbook photographs can show multiple recipes and include personal anecdotes or quotations alongside the actual ingredients and instructions.

**Decision**
Import only the user-designated recipe area and exclude personal stories, quotations, testimonials and other narrative fluff from reader-facing recipes. Preserve real cooking details and optionally contributor/source attribution in provenance metadata instead.

**Rationale**
The library's house style is a focused, clean recipe that is immediately useful for cooking, without printed-cookbook editorial noise.

**Consequences**
The Recipe Standard and import skill describe this filter. Review source content to avoid accidentally discarding operational instructions or variations while removing narrative prose.

## D011 — Include timing and imagery in first recipe reviews

**Date:** 2026-11-15

**Context**
The initial drafts for Chicken Tortilla Casserole and Italian Turkey and Noodles contained source-faithful ingredients and instructions but did not display the source's explicit Bake duration, and generated hero photographs were handled after content review.

**Decision**
Make first review drafts complete by default: transcribe all available source timing headings, show a source's Bake label distinctly from generic Cook, generate a 4:3 image consistent with the approved photo style, and present the draft recipe and pending image together. Keep source discrepancies (such as a Bake: 30 minutes heading versus a 30–35-minute baking step) intact until review rather than silently reconciling them. Neither generated imagery nor source captures are finalized or deleted before explicit approval.

**Rationale**
A complete preview makes approval more efficient and avoids multiple avoidable review rounds.

**Consequences**
`_library.timeLabels.cookTime` may override the displayed duration label to Bake while Schema.org `cookTime` remains machine-readable. Update importer instructions, schema, and HTML renderer; leave finished-library commits gated on approval.

## D012 — Vary casserole serving vessels in food imagery

**Date:** 2026-11-15

**Context**
Consecutive casserole recipe images tended to show food in similar traditional rectangular casserole dishes, even though a consistent editorial style need not dictate the same cookware in every photograph.

**Decision**
Avoid defaulting to traditional casserole dishes for every casserole hero image. Vary the presentation with suitable round or oval bakeware, skillets, shallow serving bowls, plates or plated portions when faithful to the cooked dish.

**Rationale**
Varied food presentation avoids repetitive imagery while preserving the recognizable RecipeKit photographic identity.

**Consequences**
The image-style guidelines and visual review checklist distinguish a consistent photographic treatment from an unnecessarily fixed serving vessel.

## D013 — Adopt Bright Editorial photography and varied compositions

**Date:** 2026-11-15

**Context**
Food-photo experiments with Four-Pasta Beef Bake and chocolate chip cookies compared styled whole-dish imagery, individual plated portions, and overhead compositions. The owner liked all three and wanted a cohesive but nonrepetitive collection influenced by Real Simple's approachable editorial photography.

**Decision**
Adopt Bright Editorial as RecipeKit's shared photographic style: brighter natural light, realistic food texture, balanced neutral whites, restrained saturation, and deliberate composition. Allow three peer composition families—`styled-hero`, `plated-serving`, and `overhead-editorial`—chosen for the food with light variation across the library, not a fixed rotation. Preserve source accuracy and standalone 4:3 food imagery, never recipe-card composites or invented garnish.

**Rationale**
Consistent photographic treatment ties the collection together while compositional variation prevents identical casserole dish, towel, and camera-angle repetition across recipes and categories, including desserts.

**Consequences**
Update the image standard, general recipe standard, and initial import workflow. Existing approved photos are not replaced wholesale; future generated heroes use the new approach. User-approved image choices remain in the private collection.

## D014 — Make preparation needs visible and separate advice from actions

**Date:** 2026-11-16

**Decision**
Use source-supported cookware checklists with the same alignment and checkbox styling as ingredients. Preserve specified capacities, dimensions, quantities and special supplies. Break instructions at meaningful cooking phases rather than one step per printed paragraph or sentence. Render standalone handling advice as note callouts and vary instruction subtitles by length.

**Rationale**
Readers need to gather important equipment before discovering it late in a recipe. Cooking phases support following the process; safety advice and microwave test notes are useful context without being cooking actions.

**Consequences**
`_library.equipment` and `_library.notes` feed generated views. Do not invent equipment sizes, force a step count, or alter source details when dividing steps.

## D015 — Keep varied imagery crisp and provenance private

**Date:** 2026-11-16

**Decision**
Extend D013 with deliberate variation in left/center/right placement, overhead/oblique views, close/wider crops and tabletop surfaces. Prefer sharply resolved smooth tableware and realistic food texture. Keep AI origin in private metadata without visible image labels or captions.

**Rationale**
Shared lighting and realism provide consistency without repeating the same vessel, utensil position or concrete background. Visible image labels clutter the approved reader experience.

**Consequences**
Review neighboring images for repetition, retain prior alternatives, and generate fresh views only when needed. Source-faithful ingredients and textures remain the default.
