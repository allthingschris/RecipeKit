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
