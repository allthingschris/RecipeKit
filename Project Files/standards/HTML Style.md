# RecipeKit HTML Style

**Status:** Approved editorial recipe design  
**Preferred typeface:** Google Sans Flex  
**Implementation:** `Project Files/templates/recipe.html`, rendered by `Project Files/tools/recipekit.py`.

## Design system

- Editorial, minimal, Apple-inspired presentation on a warm-neutral background.
- Google Sans Flex is the preferred web font. Load it through Google Fonts CSS, with Apple system / Segoe UI / generic sans-serif fallbacks. Do not embed or copy font binaries into recipe exports.
- Responsive asymmetric hero: editorial title and yield on one side, approved 4:3 food image on the other. Stack image above copy on mobile.
- Ingredients show interactive checkboxes and check-off styling. Instructions show large numbered step markers and a subtle vertical connector.
- Flavor variations appear as restrained two-column cards, stacking on smaller screens.
- Use a simple masthead, accessible Print button, print stylesheet, semantic headings, image alt text, and Schema.org JSON-LD.
- Never show unknown durations, review questions, workflow status, generic cooking-method tags, or a bottom-of-page “Illustrative food imagery” notice.
- Where an illustration is generated, show an unobtrusive image caption and retain its `ai-generated` origin in structured private metadata; don't mistake it for a user's actual photo.
- Recipe content comes solely from `recipe.json`; update template/layout without hand-editing recipe exports.

## Technical contract

- The HTML template contains `{{UPPERCASE_PLACEHOLDERS}}`; the renderer escapes text and substitutes content.
- Generated `recipe.html` refers to `images/hero.webp` (or the file named in the recipe) rather than duplicating its bytes inline.
- The source `recipe.json` owns title, descriptions, category, yield, known times, ingredient order, steps, variations and approved hero path.
- The hosting site may specify `--site-name` for its masthead and page title; default is `Recipe Library`.
- Google Fonts requires a network connection; if unavailable, fall back to the system font stack and keep the page readable.
- Keep the print-only styles and accessibility behavior when adapting the template.

## Usage

```bash
python3 'Project Files/tools/recipekit.py' render /path/to/recipe.json
python3 'Project Files/tools/recipekit.py' verify /path/to/recipe.json
python3 'Project Files/tools/recipekit.py' render /path/to/recipe.json --site-name 'My Recipes'
```

The generated HTML, Markdown and JSON-LD should be checked into the consumer's recipe collection only after validation and review.

**Font reference:** https://fonts.google.com/specimen/Google+Sans+Flex

## Iconography

- Preferred icons: Iconly Pro artwork supplied and authorized for use by the collection owner. The specific printer and spoon-and-fork SVGs are kept as distinct, reusable assets in `Project Files/assets/icons/`.
- The renderer embeds each SVG inline into the generated HTML (no external icon library or network dependency).
- Icon geometry, the warm `#987762` fill, and the spoon-and-fork's 40% opacity secondary layer are preserved. Icons are decorative within labelled UI controls/metadata.
- Avoid inherited SVG stroke CSS on these filled icons; set dimensions and positioning on the SVG container without adding outlines.
- These Iconly assets have their own rights and permissions. Public users should not assume the icon assets have the same open-source license as RecipeKit's code. Confirm downstream redistribution terms before relicensing the artwork.
