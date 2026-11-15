# RecipeKit

A portable, AI-assisted toolkit for transforming recipe photos, scans, and websites into beautifully consistent, structured recipes.

**Status:** Early alpha. The schema, human-assisted import/review skills, and standard-library validator/renderers are available.

RecipeKit owns the **how**: schema, normalization rules, review workflow, image style, validation, and renderers. Your actual recipes live in a different repository, such as a private `recipe-library`. The entire project is scaffolded with [ProjectKit](https://github.com/allthingschris/ProjectKit) 2.0.

## What it does

1. **Import** a recipe photograph, screenshot, or URL. Transcribe carefully; flag ambiguous quantities and instructions instead of guessing.
2. **Review** a provisional recipe and its image separately from the final recipe. Collect explicit content and source-retention approvals.
3. **Finalize** only approved recipes. Publish portable JSON, generated Markdown and HTML; remove transient review material.
4. **Validate** consistent categories, ingredients, yields, and public outputs.

The current import and review skills are **human/AI-assisted instructions**, not a self-running OCR service. The CLI provides real validation and rendering. Automated capture connectors can be added later.

## Quick start

Requires Python 3.10+; no third-party Python packages.

```bash
# See a worked synthetic example
python3 'Project Files/tools/recipekit.py' validate 'Project Files/examples/lemon-pasta/recipe.json'
python3 'Project Files/tools/recipekit.py' render 'Project Files/examples/lemon-pasta/recipe.json' --out /tmp/recipekit-demo --allow-draft

# Check every sample in this repo
python3 -m unittest discover -s 'Project Files/tests' -v
```

For an actual collection, run the tool against the private collection's `recipe.json`. The library pins the RecipeKit draft version it expects. The renderer writes the readable `recipe.md` and `recipe.html`, as well as a portable `recipe.jsonld` with private fields removed.

## Structure

- `At a Glance/` — ProjectKit continuity files (the project’s context, active work, decisions, and log)
- `Project Files/standards/` — authoritative written house standards and image guide
- `Project Files/taxonomy/` — categories, unit vocabulary, and available tag families
- `Project Files/schemas/` — structural JSON Schema (the CLI adds semantic checks)
- `Project Files/skills/` — reusable prompts/workflows for import, review, and finalize
- `Project Files/tools/recipekit.py` — deterministic validator and renderers
- `Project Files/examples/` — synthetic demonstration content, not anyone’s private recipes
- `CLAUDE.md` — working agreement

## Data design

One `recipe.json` is the source of truth. Schema.org `Recipe` properties remain at the root, with additional library structure under `_library`. Public JSON-LD removes `_library`; HTML and Markdown are regenerated, **never edited separately**. Metadata for AI-generated imagery clearly distinguishes it from an actual food photograph.

## Publishing

This repository is public. A redistribution license has not yet been selected, so this repository should not be described as open-source licensed until a license is approved. Do not add source scans or private library recipes here.

See `Project Files/standards/Recipe Standard.md` and `At a Glance/Next.md` for the remaining decisions.
