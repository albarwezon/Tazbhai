import asyncio
import os
import random
from playwright.async_api import async_playwright
import requests

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (Version/17.4.1 Safari/605.1.15)",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/124.0.2478.51"
]

REFERERS = [
    "https://www.google.com/",
    "https://www.google.pk/",
    "https://www.youtube.com/",
    "https://m.facebook.com/",
    "https://l.whatsapp.com/",
    "https://www.pinterest.com/",
    "https://twitter.com/",
    "https://www.instagram.com/",
    "https://www.reddit.com/"
]

# ==========================================
# APNE TARGET LINKS YAHAN DAALEIN
# ==========================================
TARGET_URLS = [
"https://ouo.io/4ZY8rI",
"https://ouo.io/dnyXUc",
"https://ouo.io/7Eqku9w",
"https://ouo.io/CeqFDN",
"https://ouo.io/UPO9gI",
"https://ouo.io/SWlJvg",
"https://ouo.io/SWlJvg",
"https://ouo.io/SWlJvg",
"https://ouo.io/UPO9gI",
"https://ouo.io/PrFNQFS"
]

def fetch_free_proxy():
    sources = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=elite",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
    ]
    for url in sources:
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                lines = [l.strip() for l in res.text.splitlines() if l.strip() and ":" in l]
                if lines:
                    return random.choice(lines[:50])
        except:
            continue
    return None

async def run_single_bot():
    print("==========================================")
    print("  RAILWAY DOCKER SAFE BOT RUNNING...      ")
    print("==========================================")

    wait_time = int(os.getenv("WAIT_TIME", "10"))

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars"
            ]
        )

        loop_count = 1
        try:
            while True:
                target_url = random.choice(TARGET_URLS)
                selected_ua = random.choice(USER_AGENTS)
                selected_referer = random.choice(REFERERS)
                proxy = fetch_free_proxy()

                context_args = {
                    "user_agent": selected_ua,
                    "viewport": {"width": 1280, "height": 800},
                    "locale": "en-US",
                    "timezone_id": "America/New_York"
                }

                if proxy:
                    context_args["proxy"] = {"server": f"http://{proxy}"}
                    print(f"[Loop #{loop_count}] Proxy: {proxy}")
                else:
                    print(f"[Loop #{loop_count}] Bina proxy ke chal raha hai.")

                print(f"[Loop #{loop_count}] Target: {target_url}")

                context = None
                try:
                    context = await browser.new_context(**context_args)
                    page = await context.new_page()
                    response = await page.goto(target_url, timeout=30000, wait_until="domcontentloaded", referer=selected_referer)

                    if response and response.status == 200:
                        print(f"[✓] Page load ho gaya!")
                        await asyncio.sleep(random.uniform(2.0, 4.0))
                        
                        try:
                            human_btn = await page.wait_for_selector("text=I'M A HUMAN", timeout=4000)
                            if human_btn:
                                await human_btn.click()
                                print("    [⌨️] 'I'M A HUMAN' click ho gaya.")
                                await asyncio.sleep(2)
                        except:
                            pass

                        try:
                            get_link_btn = await page.wait_for_selector("text=GET LINK", timeout=10000)
                            if get_link_btn:
                                await get_link_btn.click()
                                print("    [⌨️] 'GET LINK' click ho gaya.")
                                await asyncio.sleep(2)
                        except:
                            pass

                        await asyncio.sleep(wait_time)
                    else:
                        print(f"[x] Page load fail.")

                except Exception as e:
                    print(f"[-] Error: {e}")
                finally:
                    if context:
                        try:
                            await context.close()
                        except:
                            pass

                print(f"[✓] Loop #{loop_count} mukammal. Agla loop shuru ho raha hai...\n")
                loop_count += 1
                await asyncio.sleep(10)

        except Exception as e:
            print(f"[!] Main Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_single_bot())
