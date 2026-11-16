# RecipeKit

A portable, AI-assisted toolkit for transforming recipe photos, scans, and websites into beautifully consistent, structured recipes.

**Status:** Early alpha, published on GitHub. The v0.3-draft standard, human/AI-assisted import/review skills, schema, validator and renderers are available and have been exercised through a complete consumer collection review. Licensing and v1.0 taxonomy decisions remain open.

RecipeKit owns the **how**: schema, normalization rules, review workflow, image style, validation, and renderers. Your actual recipes live in a different repository, such as a private `recipe-library`. The entire project is scaffolded with [ProjectKit](https://github.com/allthingschris/ProjectKit) 2.0.

## What it does

1. **Import** a recipe photograph, screenshot, or URL. Transcribe carefully; flag ambiguous quantities and instructions instead of guessing.
2. **Review** a provisional recipe and its image separately from the final recipe. Collect explicit content and source-retention approvals.
3. **Finalize** only approved recipes. Generate Markdown, HTML and public-compatible JSON-LD from authoritative JSON; remove transient review material.
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

One `recipe.json` is the source of truth. Schema.org `Recipe` properties remain at the root, with additional library structure under `_library`. Public JSON-LD removes `_library`; HTML and Markdown are regenerated, **never edited separately**. Private asset metadata records AI origin; reader-facing exports omit AI labels and photo captions. Important cookware is presented as an ingredient-style checklist, and standalone advice is rendered as a note rather than a numbered step.

## Publishing

This repository is public. A redistribution license has not yet been selected, so this repository should not be described as open-source licensed until a license is approved. Do not add source scans or private library recipes here.

See `Project Files/standards/Recipe Standard.md` and `At a Glance/Next.md` for the remaining decisions.

## HTML design

The `Project Files/templates/recipe.html` template provides the approved responsive editorial layout, powered by Google Sans Flex with system-font fallbacks. See `Project Files/standards/HTML Style.md` and render with `python3 "Project Files/tools/recipekit.py" render <recipe.json>`.

## Current editorial capabilities

- Source-faithful time labels, quantities, yield spacing and meaningful cooking-phase steps.
- Source-supported cookware capacities, dimensions and special supplies, displayed before instructions.
- Separate note callouts for handling advice and other non-step guidance.
- Bright Editorial 4:3 imagery with deliberate variation in framing, placement, surfaces and vessels.
- Independent content, image and source-retention review, followed by validated exports and verified authorized cleanup.

## Project continuity

Start with [Passport](At%20a%20Glance/Passport.md) for the current handoff and [Next](At%20a%20Glance/Next.md) for remaining work. Durable rules live in [Context](At%20a%20Glance/Context.md), rationale in [Decisions](At%20a%20Glance/Decisions.md), and milestones in [Log](At%20a%20Glance/Log.md). Private consumer recipes and assets stay outside this public repository.
