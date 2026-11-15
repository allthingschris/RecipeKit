# RecipeKit

A portable toolkit for turning recipe photos, scans, and websites into consistent, structured recipes using Schema.org Recipe.

RecipeKit defines the **standards, style, reusable AI-assisted workflows, validation, and rendering tools**. Personal recipe content lives in separate repositories, such as a private Recipe Library.

The project uses [ProjectKit](https://github.com/allthingschris/ProjectKit) 2.0 for project continuity.

## Workflow

1. Import and faithfully transcribe a recipe; flag uncertain text rather than guessing.
2. Review the recipe, its image, and any proposed editorial changes in a temporary review workspace.
3. Finalize only after explicit approval; keep no per-recipe review document in the finished collection.
4. Validate and render structured JSON into Markdown, HTML, and public-safe JSON-LD.

## Source of truth

`recipe.json` is authoritative. All other recipe formats are generated from it, never maintained in parallel. RecipeKit does not contain a user's private recipes or source scans.

See `Project Files/standards/Recipe Standard.md` after scaffolding.
