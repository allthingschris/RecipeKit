#!/usr/bin/env python3
"""RecipeKit: stdlib-only validation and export (JSON-LD, Markdown, HTML)."""
from __future__ import annotations
import argparse, html, json, re, shutil, sys, uuid
from fractions import Fraction
from pathlib import Path
from urllib.parse import urljoin, urlparse

BASE = Path(__file__).resolve().parents[1]
CATEGORIES = {c['name'] for c in json.loads((BASE/'taxonomy/categories.json').read_text())['categories']}
UNITS = json.loads((BASE/'taxonomy/units.json').read_text())['units']
DURATION = re.compile(r'^P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?)?$')


def fraction(value: str) -> Fraction:
    if not isinstance(value, str) or not value.strip(): raise ValueError('Expected quantity string')
    bits = value.strip().split()
    if len(bits) == 2 and bits[0].isdigit(): n = Fraction(bits[0]) + Fraction(bits[1])
    elif len(bits) == 1: n = Fraction(bits[0])
    else: raise ValueError(f'Unsupported quantity: {value!r}')
    if n <= 0: raise ValueError('Quantity must be positive')
    return n


def display_number(value: str) -> str:
    n = fraction(value)
    whole, rem = divmod(n.numerator, n.denominator)
    return str(whole) if rem == 0 else (f'{whole} ' if whole else '') + f'{rem}/{n.denominator}'


def ingredient_text(item: dict) -> str:
    name = (item.get('name') or '').strip()
    if not name: raise ValueError('Ingredient name required')
    preparation = (item.get('preparation') or '').strip()
    before = item.get('preparationPosition') == 'before'
    if before and preparation: name = preparation + ' ' + name
    q, qmax = item.get('quantity'), item.get('quantityMax')
    unit = item.get('unit')
    if qmax and not q: raise ValueError('quantityMax without quantity')
    if unit and not q: raise ValueError('Unit without quantity')
    qty = display_number(q) if q else ''
    if qmax:
        if fraction(qmax) < fraction(q): raise ValueError('quantityMax smaller than quantity')
        qty += '–' + display_number(qmax)
    u = ''
    if unit:
        if unit not in UNITS: raise ValueError(f'Unknown unit: {unit}')
        singular = fraction(q) <= 1 and (qmax is None or fraction(qmax) <= 1)
        u = UNITS[unit]['singular' if singular else 'plural']
    result = ' '.join(x for x in (qty, u, name) if x)
    if not qty and not u: result = result[0].upper() + result[1:]
    if preparation and not before: result += ', ' + preparation
    if item.get('note'): result += ', ' + item['note'].strip()
    if item.get('optional'): result += ' (optional)'
    return result


def yield_text(y: dict | None) -> str | None:
    if not y: return None
    q, unit = y.get('quantity'), (y.get('unit') or '').strip()
    if not q or not unit: raise ValueError('Yield needs quantity and unit')
    irregular = {'loaf':'loaves','fish':'fish','leaf':'leaves'}
    plural = irregular.get(unit, unit + ('es' if unit.endswith(('ch','sh','x','s')) else 's'))
    return display_number(q) + ' ' + (unit if fraction(q)==1 else plural)


def duration_text(iso: str) -> str:
    match = DURATION.fullmatch(iso) if isinstance(iso, str) else None
    if not match or not any(g is not None for g in match.groups()): raise ValueError(f'Invalid ISO duration: {iso!r}')
    values = [int(x or 0) for x in match.groups()]
    parts = [f'{v} {sing if v==1 else plural}' for v,sing,plural in zip(values, ('day','hour','minute'), ('days','hours','minutes')) if v]
    return ' '.join(parts) if parts else '0 minutes'


def steps(recipe: dict) -> list[str]:
    output=[]
    for item in recipe.get('recipeInstructions',[]):
        if not isinstance(item,dict): continue
        if item.get('@type')=='HowToStep': output.append(item.get('text',''))
        elif item.get('@type')=='HowToSection':
            output.extend(s.get('text','') for s in item.get('itemListElement',[]) if isinstance(s,dict) and s.get('@type')=='HowToStep')
    return output


def validate(recipe: dict, publish: bool=False) -> list[str]:
    if not isinstance(recipe,dict): return ['Recipe must be an object']
    errors=[]
    if recipe.get('@context')!='https://schema.org' or recipe.get('@type')!='Recipe': errors.append('Expected Schema.org Recipe root')
    if not isinstance(recipe.get('name'),str) or not recipe.get('name','').strip(): errors.append('Recipe name missing')
    meta=recipe.get('_library')
    if not isinstance(meta,dict): return errors+['_library object missing']
    if not meta.get('schemaVersion'):errors.append('_library.schemaVersion missing')
    try: uuid.UUID(meta.get('id',''))
    except (ValueError, TypeError, AttributeError):errors.append('_library.id must be a UUID')
    if meta.get('status') not in ('captured','needs_review','validated'):errors.append('Invalid recipe status')
    if publish and meta.get('status')!='validated':errors.append('Unapproved recipe; use --allow-draft for a demonstration')
    cat=meta.get('primaryCategory')
    if cat not in CATEGORIES:errors.append('Invalid primary category')
    if recipe.get('recipeCategory')!=cat:errors.append('recipeCategory disagrees with _library.primaryCategory')
    if not isinstance(meta.get('source'),dict) or not meta['source'].get('type'):errors.append('source.type is required')
    ing=meta.get('ingredients')
    if not isinstance(ing,list) or not ing:errors.append('Structured ingredients required')
    else:
        expected=[]
        for i,item in enumerate(ing,1):
            try: expected.append(ingredient_text(item))
            except (ValueError,TypeError,KeyError) as e:errors.append(f'Ingredient {i}: {e}')
        if expected!=recipe.get('recipeIngredient'):errors.append('recipeIngredient must match structured ingredient rows')
    if meta.get('yield'):
        try:
            if yield_text(meta['yield'])!=recipe.get('recipeYield'):errors.append('recipeYield and structured yield disagree')
        except (ValueError,TypeError) as e:errors.append(f'Yield: {e}')
    ss=steps(recipe)
    if not ss or any(not s.strip() for s in ss):errors.append('At least one nonempty HowToStep required')
    for field in ('prepTime','cookTime','totalTime'):
        if field in recipe:
            try:duration_text(recipe[field])
            except ValueError as e:errors.append(f'{field}: {e}')
    if meta.get('status')=='validated' and (meta.get('reviewIssues') or meta.get('titleStatus')=='provisional'):
        errors.append('Validated recipe has unresolved review data')
    for var in meta.get('variations',[]):
        if not isinstance(var,dict) or not var.get('name') or not var.get('description'):errors.append('Incomplete variation')
    return errors


PUBLIC_FIELDS = ('@context','@type','name','description','author','url','recipeCategory','recipeCuisine',
                 'keywords','recipeYield','prepTime','cookTime','totalTime','recipeIngredient',
                 'recipeInstructions','nutrition','datePublished','image')
def jsonld(recipe: dict, base_url: str|None=None) -> dict:
    out={k:recipe[k] for k in PUBLIC_FIELDS if k in recipe}
    if 'image' in out and (not isinstance(out['image'],str) or not out['image'].startswith(('https://','http://'))):out.pop('image')
    hero=(recipe['_library'].get('assets') or {}).get('hero') or {}
    if base_url and hero.get('path'):
        if urlparse(base_url).scheme not in ('http','https'):raise ValueError('Invalid public base URL')
        out['image']=urljoin(base_url.rstrip('/')+'/',hero['path'])
    return out


def markdown(recipe: dict) -> str:
    m=recipe['_library']
    lines=['# '+recipe['name'],'']
    if recipe.get('description'):lines += [recipe['description'],'']
    lines += [' · '.join(x for x in [recipe.get('recipeCategory'),recipe.get('recipeYield')] if x),'']
    times=[label+': '+duration_text(recipe[key]) for key,label in [('prepTime','Prep'),('cookTime','Cook'),('totalTime','Total')] if key in recipe]
    if times:lines += [' · '.join(times),'']
    hero=(m.get('assets') or {}).get('hero') or {}
    if hero.get('path'):lines += [f"![{hero.get('alt',recipe['name'])}]({hero['path']})",'']
    lines += ['## Ingredients','']
    oldgroup=None
    for item in m['ingredients']:
        g=item.get('group')
        if g and g!=oldgroup:lines += ['### '+g,'']
        lines.append('- '+ingredient_text(item));oldgroup=g
    if m.get('equipment'):
        lines += ['','## Cookware & equipment',''] + ['- [ ] '+item for item in m['equipment']]
    lines += ['','## Instructions','']
    lines += [f'{i}. {step}' for i,step in enumerate(steps(recipe),1)]
    if m.get('variations'):
        lines += ['','## Flavor variations','']
        for var in m['variations']:lines += ['### '+var['name'],'',var['description'],'']
    return '\n'.join(lines).rstrip()+'\n'

# HTML is rendered from a standalone RecipeKit template rather than inline HTML.
# Edit Project Files/templates/recipe.html to adjust the shared design.
TEMPLATE_PATH = BASE / "templates" / "recipe.html"
ICON_PRINTER = (BASE / "assets" / "icons" / "printer.svg").read_text(encoding="utf-8").strip()
ICON_UTENSILS = (BASE / "assets" / "icons" / "spoon-fork.svg").read_text(encoding="utf-8").strip()


def _count_words(n: int) -> str:
    numbers = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten")
    return numbers[n] if 0 <= n < len(numbers) else str(n)


def html_page(recipe: dict, base_url: str | None = None, site_name: str = "Recipe Library") -> str:
    e = html.escape
    meta = recipe["_library"]
    ing_html, previous_group = [], None
    for item in meta["ingredients"]:
        group = item.get("group")
        if group and group != previous_group:
            ing_html.append(f'<li class="ingredient-group">{e(group)}</li>')
        label = ingredient_text(item)
        ing_html.append(
            f'<li class="ingredient"><label><input type="checkbox" aria-label="Gather {e(label, quote=True)}">'
            f'<span>{e(label)}</span></label></li>'
        )
        previous_group = group
    step_html = [
        f'<li class="step"><span class="step-number" aria-hidden="true">{i}</span><p>{e(step)}</p></li>'
        for i, step in enumerate(steps(recipe), 1)
    ]
    count = len(step_html)
    if count <= 3:
        steps_subtitle = "Let’s get cooking."
    elif count <= 5:
        steps_subtitle = "Here’s how to make it."
    else:
        steps_subtitle = "Follow along, one step at a time."

    image = (meta.get("assets") or {}).get("hero") or {}
    hero_block = ""
    if image.get("path"):
        image_path = Path(image["path"])
        if image_path.is_absolute() or ".." in image_path.parts:
            raise ValueError("Unsafe hero image path")
        hero_block = (
            '<figure class="image-wrap">'
            f'<img class="hero" src="{e(image["path"], quote=True)}" '
            f'alt="{e(image.get("alt", recipe["name"]), quote=True)}">'
            '</figure>'
        )

    equipment = meta.get("equipment") or []
    equipment_block = ""
    if equipment:
        items = "".join(
            f'<li class="ingredient"><label><input type="checkbox" aria-label="Gather {e(item, quote=True)}"><span>{e(item)}</span></label></li>'
            for item in equipment
        )
        equipment_block = (
            '<section class="equipment" aria-labelledby="equipment-heading">'
            '<h2 class="section-title" id="equipment-heading">Cookware &amp; equipment</h2>'
            '<p class="section-sub">Gather these before you begin.</p>'
            f'<ul class="ingredients">{items}</ul></section>'
        )

    variation_items = meta.get("variations") or []
    variations_block = ""
    if variation_items:
        v_count = len(variation_items)
        heading = f'{_count_words(v_count).capitalize()} flavor {"variation" if v_count == 1 else "variations"}'
        cards = "\n".join(
            '<article class="variation">'
            f'<p class="eyebrow">Variation {i:02d}</p>'
            f'<h3>{e(v["name"])}</h3><p>{e(v["description"])}</p></article>'
            for i, v in enumerate(variation_items, 1)
        )
        variations_block = (
            '<section class="variations" aria-labelledby="variations-heading">'
            '<div class="variation-head">'
            '<h2 class="section-title" id="variations-heading">Make it your own</h2>'
            f'<p>{heading}</p></div>'
            f'<div class="variation-grid">{cards}</div></section>'
        )

    yield_block = ""
    if recipe.get("recipeYield"):
        yield_block = (
            '<div class="yield">'
            f'{ICON_UTENSILS}'
            f'<span>Makes: <strong>{e(recipe["recipeYield"])}</strong></span></div>'
        )
    time_fields = (("prepTime", "Prep"), ("cookTime", "Cook"), ("totalTime", "Total"))
    time_labels = meta.get("timeLabels") or {}
    times = [f'<span><strong>{e(time_labels.get(key, label))}:</strong> {e(duration_text(recipe[key]))}</span>' for key, label in time_fields if key in recipe]
    time_block = '<div class="time-meta">' + "".join(times) + '</div>' if times else ""
    structured = json.dumps(jsonld(recipe, base_url), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    mapping = {
        "TITLE": e(recipe["name"]),
        "PRINT_ICON": ICON_PRINTER,
        "SITE_NAME": e(site_name),
        "DESCRIPTION_ATTR": e(recipe.get("description") or recipe["name"], quote=True),
        "JSON_LD": structured,
        "INTRO_CLASS": "" if hero_block else "intro--no-image",
        "CATEGORY": e(recipe.get("recipeCategory", "")),
        "SUMMARY_BLOCK": f'<p class="summary">{e(recipe["description"])}</p>' if recipe.get("description") else "",
        "YIELD_BLOCK": yield_block,
        "TIME_BLOCK": time_block,
        "HERO_BLOCK": hero_block,
        "EQUIPMENT_BLOCK": equipment_block,
        "INGREDIENT_ITEMS": "\n".join(ing_html),
        "STEPS_SUBTITLE": e(steps_subtitle),
        "STEP_ITEMS": "\n".join(step_html),
        "VARIATIONS_BLOCK": variations_block,
    }
    page = TEMPLATE_PATH.read_text(encoding="utf-8")
    for key, value in mapping.items():
        page = page.replace("{{" + key + "}}", value)
    if re.search(r"\{\{[A-Z_]+\}\}", page):
        raise ValueError("Unresolved recipe template placeholder")
    return page.rstrip() + "\n"


def output_files(recipe: dict, base_url: str|None=None, site_name: str="Recipe Library") -> dict[str,str]:
    return {'recipe.md':markdown(recipe),'recipe.html':html_page(recipe,base_url,site_name),
            'recipe.jsonld':json.dumps(jsonld(recipe,base_url),indent=2,ensure_ascii=False)+'\n'}


def write_outputs(recipe: dict, source: Path, out: Path, base_url: str|None=None, site_name: str="Recipe Library") -> None:
    out.mkdir(parents=True,exist_ok=True)
    for filename,content in output_files(recipe,base_url,site_name).items():
        (out/filename).write_text(content,encoding='utf-8');print('Wrote',out/filename)
    hero=(recipe['_library'].get('assets') or {}).get('hero') or {}
    if hero.get('path'):
        rel=Path(hero['path'])
        if rel.is_absolute() or '..' in rel.parts:raise ValueError('Unsafe relative image path')
        src=source.parent/rel;dst=out/rel
        if src.is_file() and src.resolve()!=dst.resolve():
            dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);print('Copied',dst)


def run() -> int:
    ap=argparse.ArgumentParser(description='RecipeKit validator / recipe views')
    sp=ap.add_subparsers(dest='command',required=True)
    for command in ('validate','render','verify'):
        p=sp.add_parser(command);p.add_argument('recipe',type=Path)
        if command=='render':
            p.add_argument('--out',type=Path);p.add_argument('--allow-draft',action='store_true')
        if command in ('render','verify'):
            p.add_argument('--base-url')
            p.add_argument('--site-name', default='Recipe Library')
    sp.add_parser('validate-all').add_argument('root',type=Path)
    args=ap.parse_args()
    if args.command=='validate-all':
        paths=sorted(args.root.rglob('recipe.json'))
        if not paths:print('No recipe.json found',file=sys.stderr);return 1
        errors=0
        for p in paths:
            try: problems=validate(json.loads(p.read_text()))
            except (OSError,ValueError) as e: problems=[str(e)]
            print('PASS' if not problems else 'FAIL',p)
            for x in problems:print(' -',x)
            errors+=bool(problems)
        return int(errors>0)
    try:recipe=json.loads(args.recipe.read_text(encoding='utf-8'))
    except (OSError,ValueError) as e:print('ERROR',e,file=sys.stderr);return 2
    errors=validate(recipe,publish=args.command=='render' and not args.allow_draft)
    if errors:
        print('FAIL',args.recipe)
        for x in errors:print(' -',x)
        return 1
    if args.command=='validate':
        print('PASS',args.recipe)
        return 0
    try:
        if args.command=='render':write_outputs(recipe,args.recipe,args.out or args.recipe.parent,args.base_url,args.site_name)
        else:
            stale=[name for name,txt in output_files(recipe,args.base_url,args.site_name).items() if not (args.recipe.parent/name).exists() or (args.recipe.parent/name).read_text()!=txt]
            if stale:print('Stale or absent generated files:',', '.join(stale));return 1
            print('PASS: generated files are current')
    except (ValueError,OSError) as e:print('ERROR',e,file=sys.stderr);return 2
    return 0

if __name__=='__main__':sys.exit(run())
