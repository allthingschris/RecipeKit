# Context

## Goals

- Enable repeatable, source-faithful ingestion of photographed, handwritten, printed and web recipes into consistent, portable data.
- Provide open, platform-neutral house standards, validation, rendering, review skills, and cohesive AI food imagery.
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
