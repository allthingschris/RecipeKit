# RecipeKit Image Style

**Preset family:** Bright Editorial  
**Master aspect ratio:** 4:3 (landscape)  
**Status:** User-approved photography identity and flexible composition families.

## Shared photographic identity

Create convincing, approachable **Bright Editorial** cookbook photography informed by the clean, varied food photography the owner enjoys in Real Simple. Images should feel as though they belong to one cookbook through consistent realism, clear natural daylight, true-to-food colors, restrained processing, and thoughtfully composed backgrounds—not through identical dishes, beige towels, or camera angles. Prefer bright but not overexposed whites, believable food texture, distinct ingredients, subtle shadows, and moderately saturated colors. Avoid overly golden/orange casts, artificial cheese pulls, extreme texture exaggeration, and overly tight product-advertising compositions.

- Framing: 4:3 landscape master. Choose a well-suited angle and enough breathing room; use medium-distance, eye-level/three-quarter, or overhead framing depending on the food. No mandatory camera angle.
- Subjects: prepared final dish, accurate ingredients and plausible preparation/texture.
- Props: minimal, deliberate, food-relevant. Avoid unlisted edible garnishes, sauces, elaborate sides or branded goods; if an item isn't supported by the recipe, don't suggest it is a required ingredient. When in doubt, use no props.
- Surface and plate: a restrained palette with room for variety: light stone, warm wood, colored ceramics, simple trays, plates, bowls, and occasional linen. Do not default to a towel, rectangular baking dish, or a bowl of herbs as background decoration.
- Serving vessel variety: do not assume every casserole should be photographed in a traditional rectangular casserole or baking dish. Use appropriate round or oval bakeware, skillets, shallow bowls, plates, or a realistic served portion when it presents the finished recipe well. Vary vessels across the collection; remain faithful to the food's baked texture and any equipment constraints in the source.
- Text: none. No labels, logo, watermark or fake restaurant branding.
- Lighting/finish: softly directional bright daylight, natural-looking highlights and shadows, balanced white point, restrained editing, realistic color. The editorial treatment is consistent even as angles, props and dishes vary.
- Disclosure: mark asset origin as AI-generated. Do not call the result a genuine photograph of food the user cooked.

## Three approved composition styles

All three are equally valid for **any** recipe, including desserts, casseroles, and baked goods. Choose a style that best presents the actual food, then add some *lightly randomized variation* across adjacent recipes so the library does not become repetitive. **Do not enforce a mechanical 1-2-3 rotation** or generate three versions every time; one excellent hero is the default for a new recipe.

| Style key | Composition | When it works |
| --- | --- | --- |
| `styled-hero` | A thoughtfully arranged finished dish, medium-distance or three-quarter framing, with breathing room and a restrained environment | Whole casseroles, platters, bowls, cookies or any dish whose overall presentation deserves emphasis |
| `plated-serving` | One serving presented ready to eat, with realistic texture, natural details and proportionate styling | Pizza bake slice, bowl of pasta, a cut burrito, cookies or plated casserole |
| `overhead-editorial` | Intentional top-down arrangement with clean geometry, visible ingredients and minimal clutter | Cookie batches, prepared trays, bowls, salad and other dishes that benefit from their silhouette or repeated pattern |

Selection guidance:
1. Start with the composition that most honestly communicates the finished recipe, rather than choosing randomly in isolation.
2. Look at the last few recipes and lightly vary camera angle, serving vessel and style when two equally strong compositions are possible. Intentional randomness prevents visually identical consecutive covers.
3. Within a style, vary backgrounds, tableware, and crop deliberately; a plated serving is not always a cream bowl, and an overhead need not include a towel.
4. Keep background food props and garnishes true to the source; don't add salt flakes, parsley, a salad, extra grated cheese or drinks merely to make a photo look styled.
5. Show only food photography in the hero itself: **no layouts, comparison boards, UI, typography, labels or multi-panel collages**. Comparison sheets may be used for review but never as recipe heroes.

## Scene presets

| Key | Environment | Use |
| --- | --- | --- |
| `natural-linen` | Beige linen, warm neutral stoneware | Soft breakfast and baked dishes |
| `light-stone` | Light stone tabletop, quiet neutral plating | Sauces, savory meals and clean compositions |
| `warm-wood` | Restrained warm wood, muted ceramics | Hearty meals and comfort food |
| `neutral-ceramic` | Simple stoneware and subdued backdrop | General-purpose plated dishes |

All presets share the **same camera realism, exposure, restrained color grading, lighting softness, and editing treatment**.

## Prompt template

> Produce **one standalone food photograph** (no UI, labels, cards or comparison collage) of the finished `[RECIPE NAME]` using only recipe-supported ingredients and toppings. Use the `[COMPOSITION STYLE]` approach (`styled-hero`, `plated-serving`, or `overhead-editorial`) within RecipeKit's Bright Editorial identity: 4:3 landscape, clean natural daylight, a balanced neutral white point, believable food detail, restrained saturation, editorial breathing room and a considered but unfussy `[SCENE PRESET]` environment. Show the right finished-dish texture and serving vessel without inventing components, garnish, sides or sauces. Avoid orange-heavy grading, synthetic cheese pulls, unnecessary towels, excessive props, text, layouts, logos or watermarks.

## Review checklist

- Visually plausible for ingredients and steps? Not accidentally adding ingredients, sauce or garnish?
- Correct dish form, portion, texture, and cookware/plating cues? Are casserole images being varied rather than defaulting to rectangular baking dishes?
- Matches the shared Bright Editorial look and 4:3 master ratio without a color cast or overprocessed food?
- Selected composition style (`styled-hero`, `plated-serving`, `overhead-editorial`) fits the dish and helps vary the surrounding recipe collection?
- Is it a standalone photograph rather than a recipe-card composite or UI mockup?
- Attractive natural lighting and a quiet, appropriate scene?
- Clearly labelled as AI-generated in recipe asset metadata?
- Approved by the collection owner?

Generated assets may require subjective review; never auto-approve simply because generation succeeded. The first approved image used `natural-linen`, with a cut ham-and-egg burrito on neutral stoneware.
