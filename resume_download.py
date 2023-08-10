## playwright script to open ping job and download the resume

# U : XXXXX P : XXXXXX
import time 
import os 
import asyncio
from playwright.async_api import async_playwright

async def resume_downloder(resume_name):
    print("resume name",resume_name)
    resume_url = f'https://www.xyx.com/dashboard/employer/download_resume/{resume_name}'
    async with async_playwright() as playwright:
        webkit = playwright.webkit # or "firefox" or "chromium".
        browser = await webkit.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(0)
        await page.goto("https://www.xyx.com/login")
        # other actions...
        print("login started")
        await page.locator("xpath=/html/body/div[1]/div/div[1]/div/div/div/div[2]/form/div[1]/div/input").fill("admin1@gmail.com")
        await page.locator("xpath=/html/body/div[1]/div/div[1]/div/div/div/div[2]/form/div[2]/div/input").fill("123456")
        await page.locator("xpath=//html/body/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div/button").click()
        print("login done")
        

        page.set_default_timeout(0)

        async with page.expect_download() as download_info:
            try:
                await page.goto(f"{resume_url}", timeout= 0)
            except Exception as e :
                print(e)

                download = await download_info.value



                await download.save_as(os.path.join("Resumes/", f'{resume_name}'))
        await page.wait_for_timeout(200)    

        await browser.close()

        return f"Resumes/{resume_name}"


#print(asyncio.run(resume_downloder("1673034212im4gh-supriya-salesforce-developer.docx")))


