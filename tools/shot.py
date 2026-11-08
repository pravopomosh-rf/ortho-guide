import sys,asyncio
from playwright.async_api import async_playwright
async def main(url,out,h):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
        await pg.goto(url);await pg.wait_for_timeout(1500)
        await pg.screenshot(path=out,full_page=False,clip={'x':0,'y':0,'width':390,'height':int(h)})
        info=await pg.evaluate("""()=>[...document.querySelectorAll('video.vid')].filter(v=>v.offsetParent).map(v=>[v.src.split('/').pop(),v.clientWidth,v.clientHeight,v.preload])""")
        print(info)
        await b.close()
asyncio.run(main(sys.argv[1],sys.argv[2],sys.argv[3] if len(sys.argv)>3 else 844))
