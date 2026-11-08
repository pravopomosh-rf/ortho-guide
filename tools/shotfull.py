import sys,asyncio
from playwright.async_api import async_playwright
async def main(url,out):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
        await pg.goto(url);await pg.wait_for_timeout(1500)
        h=await pg.evaluate("document.documentElement.scrollHeight"); print('height',h)
        await pg.screenshot(path=out,full_page=True)
        await b.close()
asyncio.run(main(sys.argv[1],sys.argv[2]))
