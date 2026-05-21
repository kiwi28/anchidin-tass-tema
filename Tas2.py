#pip3 install playwright
import random
import string
#COD SURSA Python: https://pastebin.com/8keBaySs
#COD SURSA PHP: https://pastebin.com/77EZPCw6
from playwright.sync_api import sync_playwright
BASE_URL = "http://localhost/Tass.php"
def random_name(lenght=8):
    return ''.join(random.choices(string.ascii_letters ,k=lenght))
 
def random_email():
    user = random_name(6).lower()
    domain = random.choice(["gmail.com","yahoo.com","outlook.com","example.com"])
    return f"{user}@{domain}"
#####
def test_empty_submit(page):
    page.goto(BASE_URL)
    page.click('[data-testid="submit"]')
    assert page.inner_text('[data-testid="err-name"]') == "NUMELE ESTE OBLIGATORIU"
    assert page.inner_text('[data-testid="err-email"]') == "EMAILUL ESTE INVALID"
 
def test_invalid_email(page):
    page.goto(BASE_URL)
    page.fill('[data-testid="name"]',"Sorin")
    page.fill('[data-testid="email"]',"ORICE")
    page.click('[data-testid="submit"]')
    assert page.locator('[data-testid="err-email"]').inner_text() == " EMAILUL ESTE INVALID"
 
def test_succes(page):
    page.goto(BASE_URL)
    page.fill('[data-testid="name"]',"Sorin")
    page.fill('[data-testid="email"]',"sorin@gmail.com")
    page.click('[data-testid="submit"]')
    page.wait_for_selector('[data-testid="result"]')
    result = page.locator('[data-testid="result"]').inner_text()
    assert "DATELE PRIMITE: Sorin - sorin@gmail.com" in result
 
def test_random_fuzz(page,iter=5):
    print("TEST RANDOM FUZING") 
    for i in range(iter):
        name = random_name()
        email = random_email()
        print(f"Test {i+1}: {name}, {email}")
        page.goto(BASE_URL)
        page.fill('[data-testid="name"]',name)
        page.fill('[data-testid="email"]',email)
        page.click('[data-testid="submit"]')
        page.wait_for_timeout(100)
 
        page.wait_for_selector (
            '[data-testid="result"], [data-testid="err-name"], [data-testid="err-email"]'
        )
        has_success = page.locator('[data-testid="result"]').count() > 0
        has_error =(
            page.locator('[data-testid="err-name"]').count() > 0 or
            page.locator('[data-testid="err-email"]').count() > 0
        )
        assert has_success or has_error, "Nici eroare nici succes !"
        print("TEST PASSED")
 
def run():
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=False,slow_mo=500, channel="msedge")
      page = browser.new_page()
      #test_empty_submit(page)
      #test_invalid_email(page)
      #test_succes(page)
      test_random_fuzz(page,iter=5)
      browser.close()
 
run()