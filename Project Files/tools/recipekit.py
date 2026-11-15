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
    lines += ['','## Instructions','']
    lines += [f'{i}. {step}' for i,step in enumerate(steps(recipe),1)]
    if m.get('variations'):
        lines += ['','## Flavor variations','']
        for var in m['variations']:lines += ['### '+var['name'],'',var['description'],'']
    return '\n'.join(lines).rstrip()+'\n'

STYLE="""
:root{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f8f7f3;color:#292a26}
*{box-sizing:border-box}body{margin:0}main{max-width:1000px;margin:auto;padding:36px 30px 80px}
header{padding:20px 0 24px}.eyebrow{font-size:.73rem;letter-spacing:.16em;text-transform:uppercase;color:#73766c;font-weight:700}
h1{font-size:clamp(2.4rem,5.4vw,4.2rem);line-height:1.05;letter-spacing:-.055em;margin:12px 0 18px}
.lead{max-width:690px;color:#646861;font-size:1.1rem;line-height:1.55}.meta{display:flex;gap:9px;flex-wrap:wrap;margin-top:20px}
.chip{background:#e9e9e3;color:#464942;border-radius:40px;padding:8px 14px;font-size:.87rem}
.hero{aspect-ratio:4/3;border-radius:20px;overflow:hidden;margin:0 0 46px;background:#edede8}.hero img{display:block;width:100%;height:100%;object-fit:cover}
.columns{display:grid;grid-template-columns:minmax(250px,.85fr) minmax(0,1.15fr);gap:60px}
h2{letter-spacing:-.035em;font-size:1.55rem;margin:0 0 24px}h3{font-size:1rem;margin:24px 0 8px}
li{padding-left:4px;line-height:1.62;margin-bottom:11px}ul{padding-left:22px}ol{padding-left:26px}ol li{padding-left:8px;margin-bottom:24px}
.variations{margin-top:48px;border-top:1px solid #dbddd5;padding-top:35px}.variations p{line-height:1.6;color:#5e6159;margin:3px 0 18px}
footer{color:#878a82;font-size:.78rem;border-top:1px solid #dbddd5;margin-top:60px;padding-top:17px}
@media(max-width:700px){main{padding:22px 20px 64px}.columns{display:block}.columns section+section{margin-top:44px}.hero{border-radius:14px}}
""".strip()
def html_page(recipe: dict, base_url: str|None=None) -> str:
    e=html.escape;m=recipe['_library']
    chips=[recipe.get('recipeCategory'),recipe.get('recipeYield')]
    chips += [label+': '+duration_text(recipe[key]) for key,label in [('prepTime','Prep'),('cookTime','Cook'),('totalTime','Total')] if key in recipe]
    chips_html=''.join(f'<span class="chip">{e(v)}</span>' for v in chips if v)
    image=(m.get('assets') or {}).get('hero') or {}
    pic=f'<figure class="hero"><img src="{e(image["path"],quote=True)}" alt="{e(image.get("alt",recipe["name"]),quote=True)}"></figure>' if image.get('path') else ''
    li='';old=None
    for item in m['ingredients']:
        grp=item.get('group')
        if grp and grp!=old:li+=f'<h3>{e(grp)}</h3>'
        li+=f'<li>{e(ingredient_text(item))}</li>';old=grp
    ol=''.join(f'<li>{e(step)}</li>' for step in steps(recipe))
    variants=''
    if m.get('variations'):
        variants='<section class="variations"><h2>Flavor variations</h2>'+''.join(
            f'<h3>{e(v["name"])}</h3><p>{e(v["description"])}</p>' for v in m['variations'])+'</section>'
    lead=f'<p class="lead">{e(recipe["description"])}</p>' if recipe.get('description') else ''
    structured=json.dumps(jsonld(recipe,base_url),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(recipe['name'])}</title><meta name="description" content="{e(recipe.get('description',recipe['name']),quote=True)}">
<style>{STYLE}</style><script type="application/ld+json">{structured}</script></head>
<body><main><header><div class="eyebrow">Recipe</div><h1>{e(recipe['name'])}</h1>{lead}<div class="meta">{chips_html}</div></header>
{pic}<div class="columns"><section><h2>Ingredients</h2><ul>{li}</ul></section><section><h2>Instructions</h2><ol>{ol}</ol></section></div>
{variants}<footer>RecipeKit · Generated food imagery is illustrative.</footer></main></body></html>'''


def output_files(recipe: dict, base_url: str|None=None) -> dict[str,str]:
    return {'recipe.md':markdown(recipe),'recipe.html':html_page(recipe,base_url),
            'recipe.jsonld':json.dumps(jsonld(recipe,base_url),indent=2,ensure_ascii=False)+'\n'}


def write_outputs(recipe: dict, source: Path, out: Path, base_url: str|None=None) -> None:
    out.mkdir(parents=True,exist_ok=True)
    for filename,content in output_files(recipe,base_url).items():
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
        if command in ('render','verify'):p.add_argument('--base-url')
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
        if args.command=='render':write_outputs(recipe,args.recipe,args.out or args.recipe.parent,args.base_url)
        else:
            stale=[name for name,txt in output_files(recipe,args.base_url).items() if not (args.recipe.parent/name).exists() or (args.recipe.parent/name).read_text()!=txt]
            if stale:print('Stale or absent generated files:',', '.join(stale));return 1
            print('PASS: generated files are current')
    except (ValueError,OSError) as e:print('ERROR',e,file=sys.stderr);return 2
    return 0

if __name__=='__main__':sys.exit(run())
