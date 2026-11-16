# Context

## Goals

- Enable repeatable, source-faithful ingestion of photographed, handwritten, printed and web recipes into consistent, portable data.
- Provide shareable, platform-neutral house standards, validation, rendering, review skills, and cohesive AI food imagery.
- Allow multiple collections to use the same toolkit without publishing any collection’s private content.

## Constraints

- Base representation: Schema.org Recipe JSON with `_library` extensions; one authoritative recipe file, generated views.
- No invented ingredients, quantities, durations, temperatures, author data, or nutrition.
- Photos/scans require independent retention decisions; family originals are typically preserved. Temporary reviews are not permanent recipe artifacts.
- Python standard library for first-stage validation and export; OCR is guided by skills rather than a self-running service.

## Terminology

| Term | Meaning |
| --- | --- |
| RecipeKit | Reusable toolkit and standard, never the personal recipe collection |
| Recipe Library | A separate consumer repository, often private |
| `_library` | Private structured extension inside the authoritative recipe JSON |
| Review | Temporary questions and approvals before committing finished content |
| ProjectKit | General-purpose Git/AI project continuity scaffold |

## Structure

The public toolkit owns all standards, taxonomy, skills, schemas and processing tools. A consuming recipe library owns actual recipes and final images, typically under `Project Files/recipes/<primary-category>/<recipe-slug>/`. `ProjectKit` keeps project-level continuity in `At a Glance/`.

## Editorial contract

- Group connected actions into cooking phases, splitting for equipment changes, timed stages and finishing. Preserve source wording and order; do not force a step count.
- List consequential source-supported cookware and special supplies before instructions, preserving stated sizes and quantities without inventing them. Use ingredient-style checkbox rows.
- Put standalone handling advice in note callouts rather than numbered steps.
- Keep AI origin in private metadata without visible image captions. Vary Bright Editorial placement, camera angle, crop, surfaces and vessels while maintaining natural light and sharply resolved materials.
- Keep content, image and source-retention approvals separate. Existing explicit authorization remains valid; verify exact captures and exports before any authorized deletion.
