"""Targeted, user-authorized mobile-emulation inspection, separate public profile."""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

base = Path(__file__).parent
private = base / 'private_mobile_screenshots'
private.mkdir(exist_ok=True)
with sync_playwright() as p:
    device = p.devices['Pixel 7']
    try:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, chromium_sandbox=True)
    except Exception as exc:
        receipt = {'stage':'launch','status':'failed','exception':str(exc),'security':'Chromium sandbox requested; no insecure fallback, proxy alteration or SSL-ignore setting.'}
        (base/'mobile_capability_receipt.json').write_text(json.dumps(receipt,indent=2))
        print(json.dumps(receipt),flush=True)
        raise SystemExit(1)
    context = browser.new_context(**device, ignore_https_errors=False)
    page = context.new_page()
    page.set_default_timeout(10000)
    page.set_default_navigation_timeout(20000)
    metadata={'mode':'mobile emulation, not physical device or native app','browser_version':browser.version,'device_preset':'Pixel 7','viewport':device['viewport'],'device_scale_factor':device['device_scale_factor'],'is_mobile':device['is_mobile'],'has_touch':device['has_touch'],'user_agent':device['user_agent'],'profile':'new in-memory context; no copied cookies/accounts','https_errors_ignored':False,'chromium_sandbox':True,'native_app_tools':{'adb':False,'emulator':False}}
    (base/'mobile_capability_receipt.json').write_text(json.dumps(metadata,indent=2))
    print(json.dumps({'ready':metadata}),flush=True)
    def snap():
        return {'url':page.url,'title':page.title(),'viewport':page.evaluate('({width:innerWidth,height:innerHeight,dpr:devicePixelRatio})'),'text':page.locator('body').inner_text()[:16000],'controls':page.locator('a,button,input,select,[role="button"]').evaluate_all('(els)=>els.filter(e=>e.getClientRects().length).map(e=>({tag:e.tagName,role:e.getAttribute("role"),type:e.getAttribute("type"),id:e.id,placeholder:e.getAttribute("placeholder"),aria:e.getAttribute("aria-label"),text:(e.innerText||e.value||"").slice(0,180),href:e.href,disabled:e.disabled})).slice(0,100)')}
    for raw in sys.stdin:
        try:
            cmd=json.loads(raw)
            action=cmd['action']
            if action=='close':
                print(json.dumps({'closed':True}),flush=True)
                break
            if action=='goto':
                response=page.goto(cmd['url'],wait_until='domcontentloaded')
                print(json.dumps({'navigation_status':response.status if response else None,**snap()},ensure_ascii=False),flush=True)
            elif action=='snapshot':print(json.dumps(snap(),ensure_ascii=False),flush=True)
            elif action=='click':
                loc=page.locator(cmd['selector']) if cmd.get('selector') else page.get_by_role(cmd.get('role','button'),name=cmd['name'],exact=cmd.get('exact',True))
                loc.nth(cmd.get('index',0)).click()
                print(json.dumps(snap(),ensure_ascii=False),flush=True)
            elif action=='fill':
                page.locator(cmd['selector']).fill(cmd['value'])
                print(json.dumps(snap(),ensure_ascii=False),flush=True)
            elif action=='screenshot':
                name=Path(cmd['name']).name
                page.screenshot(path=str(private/name),full_page=False)
                print(json.dumps({'private_screenshot':str(private/name)}),flush=True)
            else:raise ValueError('Unsupported action')
        except Exception as exc:
            print(json.dumps({'error':str(exc),'url':page.url if page else ''}),flush=True)
    context.close()
    browser.close()
