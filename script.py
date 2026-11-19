import asyncio
import os
import random
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from playwright.async_api import async_playwright
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Railway Health Check ke liye chhota background web server
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    def log_message(self, format, *args):
        pass

def start_health_server():
    port = int(os.getenv("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (Version/17.4.1 Safari/605.1.15)",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/124.0.2478.51"
]

# ==========================================
# APNE MULTIPLE TARGET LINKS YAHAN DAALEIN
# ==========================================
TARGET_URLS = [
    "https://ouo.io/hYMPGs",
    "https://ouo.io/qPRPg1",
    "https://ouo.io/q5aykg",
    "https://ouo.io/iFfZoGd",
    "https://ouo.io/2wWoHfD",
    "https://ouo.io/Je2uk7",
    "https://ouo.io/DyLi0d",
    "https://ouo.io/UqkAbN",
    "https://ouo.io/4wmULK",
    "https://ouo.io/vhcWh4",
    "https://ouo.io/wiXHnHV",
    "https://ouo.io/y5uEZr",
    "https://ouo.io/xLmzKy",
    "https://ouo.io/SIU6gY",
    "https://ouo.io/DgAkqv",
    "https://ouo.io/n6sm8TH",
    "https://ouo.io/s35FBK"
]

def fetch_and_filter_free_proxies():
    print("[+] 15 mukhtalif reliable sources se fresh free proxies fetch ki ja rahi hain...", flush=True)
    sources = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=elite",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/ErcinArslan/Proxy-List/main/proxies/http.txt",
        "https://raw.githubusercontent.com/roosterkid/proxy-list/main/The_Proxies.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/Visualized/Proxy-List/main/http.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-list/master/proxies.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"
    ]
    
    all_proxies = set()
    for url in sources:
        try:
            response = requests.get(url, timeout=6)
            if response.status_code == 200:
                for line in response.text.splitlines():
                    proxy = line.strip()
                    if proxy and ":" in proxy:
                        all_proxies.add(proxy)
        except Exception:
            pass
            
    raw_list = list(all_proxies)
    print(f"[+] Total {len(raw_list)} raw proxies mili hain. Ab inhein test aur filter kiya ja raha hai...", flush=True)

    working_proxies = []
    
    def test_proxy(proxy):
        try:
            test_url = "https://httpbin.org/ip"
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
            res = requests.get(test_url, proxies=proxies, timeout=4)
            if res.status_code == 200:
                return proxy
        except:
            pass
        return None

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(test_proxy, p): p for p in raw_list[:400]}
        for future in as_completed(futures):
            res = future.result()
            if res:
                working_proxies.append(res)
                print(f"[✓] Working Proxy Mili: {res}", flush=True)
                if len(working_proxies) >= 60:
                    break

    print(f"[+] Filtering mukammal! Kul {len(working_proxies)} zinda aur fast proxies tayyar hain.", flush=True)
    return working_proxies

async def worker(worker_id, queue, browser, wait_time, proxy_list):
    while not queue.empty():
        try:
            task_data = await queue.get()
        except asyncio.QueueEmpty:
            break

        task_id = task_data["id"]
        retries = task_data["retries"]

        target_url = random.choice(TARGET_URLS)
        selected_ua = random.choice(USER_AGENTS)

        context_args = {
            "user_agent": selected_ua,
            "viewport": {"width": 1280, "height": 800},
            "locale": "en-US",
            "timezone_id": "America/New_York"
        }

        if proxy_list:
            chosen_proxy = random.choice(proxy_list)
            context_args["proxy"] = {"server": f"http://{chosen_proxy}"}

        success = False
        context = None
        try:
            context = await browser.new_context(**context_args)

            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                window.navigator.chrome = {
                    runtime: {},
                };
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
            """)

            page = await context.new_page()
            print(f"[Worker {worker_id}] Task {task_id} -> Link: {target_url} (Attempt: {4 - retries}/3)...", flush=True)

            response = await page.goto(target_url, timeout=30000, wait_until="domcontentloaded")

            if response and response.status == 200:
                print(f"[✓] [Worker {worker_id}] Task {task_id} successful! Page load ho gaya.", flush=True)

                await asyncio.sleep(random.uniform(1.5, 3.0))

                try:
                    human_btn = await page.wait_for_selector("text=I'M A HUMAN", timeout=5000)
                    if human_btn:
                        print(f"    [⌨️] 'I'M A HUMAN' button mil gaya, click kiya ja raha hai...", flush=True)
                        await human_btn.click()
                        await asyncio.sleep(random.uniform(2, 4))
                except Exception:
                    print(f"    [-] 'I'M A HUMAN' button nahi mila ya pehle se guzar gaya.", flush=True)

                try:
                    print(f"    [⌛] 'GET LINK' button ke liye wait kiya ja raha hai...", flush=True)
                    get_link_btn = await page.wait_for_selector("text=GET LINK", timeout=15000)
                    if get_link_btn:
                        print(f"    [⌨️] 'GET LINK' button mil gaya, click kiya ja raha hai...", flush=True)
                        await get_link_btn.click()
                        await asyncio.sleep(random.uniform(2, 4))
                except Exception:
                    print(f"    [-] 'GET LINK' button nahi mila.", flush=True)

                print(f"    [⌛] Page par {wait_time} seconds mazeed wait kiya ja raha hai...", flush=True)
                await asyncio.sleep(wait_time)
                success = True
            else:
                print(f"[x] [Worker {worker_id}] Task {task_id} failed / blocked!", flush=True)

        except Exception as e:
            print(f"[-] [Worker {worker_id}] Error in Task {task_id}: {e}", flush=True)
        finally:
            if context:
                try:
                    await context.close()
                except:
                    pass

        if not success:
            if retries > 1:
                print(f"[!] Task {task_id} dobara queue mein dala ja raha hai...", flush=True)
                await queue.put({"id": task_id, "retries": retries - 1})
            else:
                print(f"[-] Task {task_id} tamaam koshishein mukammal karne ke baad fail ho gaya.", flush=True)

        queue.task_done()

async def main():
    # Health server ko background thread mein start karein taake Railway container band na kare
    threading.Thread(target=start_health_server, daemon=True).start()

    print("==========================================", flush=True)
    print("  PLAYWRIGHT RAILWAY FREE PROXY BOT       ", flush=True)
    print("==========================================", flush=True)

    # Railway par RAM crash se bachne ke liye default 5 workers rakhe hain (Variables se change kar sakte hain)
    total_tasks = int(os.getenv("TOTAL_TASKS", "50"))
    concurrent_workers = int(os.getenv("CONCURRENT_WORKERS", "5"))
    wait_time = int(os.getenv("WAIT_TIME", "5"))

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--single-process",
                "--no-zygote"
            ]
        )

        batch_number = 1
        try:
            while True:
                print(f"\n==========================================", flush=True)
                print(f"      BATCH #{batch_number} START HO RAHA HAI", flush=True)
                print(f"==========================================", flush=True)

                proxy_list = fetch_and_filter_free_proxies()
                if not proxy_list:
                    print("[!] Koi bhi live proxy nahi mili, bina proxy ke chalaya ja raha hai.", flush=True)

                queue = asyncio.Queue()
                for i in range(total_tasks):
                    queue.put_nowait({"id": i + 1, "retries": 3})

                workers = [
                    asyncio.create_task(
                        worker(i + 1, queue, browser, wait_time, proxy_list)
                    )
                    for i in range(concurrent_workers)
                ]

                await queue.join()

                for w in workers:
                    w.cancel()

                print(f"\n[✓] Batch #{batch_number} mukammal ho gaya!", flush=True)
                batch_number += 1

                print(f"[⌛] Agla batch 15 seconds mein shuru hoga...", flush=True)
                await asyncio.sleep(15)

        except Exception as e:
            print(f"\n[!] Error: {e}", flush=True)
        finally:
            await browser.close()
            print("\n[✓] Browser safely close kar diya gaya hai.", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
