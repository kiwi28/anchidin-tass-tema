# pip install playwright
# python -m playwright install chromium
# Rulare: python test_workshop.py
# NOTA: Asigurati-va ca serverul PHP ruleaza inainte de a rula testele
#       cd /home/alexkiwi/projects/temp/anchidin-tass-tema && php -S localhost:8000

import random
import string
from playwright.sync_api import sync_playwright

# URL-ul unde ruleaza formularul PHP
BASE_URL = "http://localhost:8000/workshop.php"


def random_nume(lungime=8):
    """Genereaza un nume aleatoriu format din litere mari si mici."""
    return ''.join(random.choices(string.ascii_letters, k=lungime))


def random_prenume(lungime=7):
    """Genereaza un prenume aleatoriu format din litere mari si mici."""
    return ''.join(random.choices(string.ascii_letters, k=lungime))


def random_telefon():
    """Genereaza un numar de telefon romanesc valid (10 cifre, incepe cu 07)."""
    prefix = "07"
    restul = ''.join(random.choices(string.digits, k=8))
    return prefix + restul


def random_varsta(minim=18, maxim=65):
    """Genereaza o varsta aleatorie intre minim si maxim."""
    return str(random.randint(minim, maxim))


# ============== CAZURI DE TESTARE ==============

def test_empty_submit(page):
    """
    Test 1: Submit fara niciun camp completat.
    Verifica prezenta tuturor mesajelor de eroare obligatorii.
    """
    print("[TEST] Rulare test_empty_submit...")
    page.goto(BASE_URL)
    page.click('[data-testid="submit"]')

    # Verificam ca apar TOATE cele 4 erori
    assert page.inner_text('[data-testid="err-nume"]') == "NUMELE ESTE OBLIGATORIU"
    assert page.inner_text('[data-testid="err-prenume"]') == "PRENUMELE ESTE OBLIGATORIU"
    assert page.inner_text('[data-testid="err-telefon"]') == "TELEFONUL ESTE OBLIGATORIU"
    assert page.inner_text('[data-testid="err-varsta"]') == "VARSTA ESTE OBLIGATORIE"
    print("  [PASS] Toate cele 4 erori obligatorii sunt afisate corect.")


def test_invalid_phone(page):
    """
    Test 2: Nume si prenume valide, telefon invalid (prea scurt).
    """
    print("[TEST] Rulare test_invalid_phone...")
    page.goto(BASE_URL)
    page.fill('[data-testid="nume"]', "Popescu")
    page.fill('[data-testid="prenume"]', "Ion")
    page.fill('[data-testid="telefon"]', "123")       # Telefon prea scurt
    page.fill('[data-testid="varsta"]', "25")
    page.click('[data-testid="submit"]')

    # Trebuie sa apara eroarea de telefon (10 cifre)
    assert page.inner_text('[data-testid="err-telefon"]') == "TELEFONUL TREBUIE SA CONTINA EXACT 10 CIFRE"
    print("  [PASS] Eroarea de telefon este afisata corect.")


def test_phone_with_letters(page):
    """
    Test 3: Telefon care contine litere in loc de cifre.
    """
    print("[TEST] Rulare test_phone_with_letters...")
    page.goto(BASE_URL)
    page.fill('[data-testid="nume"]', "Ionescu")
    page.fill('[data-testid="prenume"]', "Maria")
    page.fill('[data-testid="telefon"]', "07ab345678")  # Contine litere
    page.fill('[data-testid="varsta"]', "30")
    page.click('[data-testid="submit"]')

    assert page.inner_text('[data-testid="err-telefon"]') == "TELEFONUL TREBUIE SA CONTINA EXACT 10 CIFRE"
    print("  [PASS] Eroarea de telefon (format invalid) este afisata corect.")


def test_underage(page):
    """
    Test 4: Varsta sub 18 ani - inscrierea este respinsa.
    """
    print("[TEST] Rulare test_underage...")
    page.goto(BASE_URL)
    page.fill('[data-testid="nume"]', "Vasilescu")
    page.fill('[data-testid="prenume"]', "Elena")
    page.fill('[data-testid="telefon"]', "0722111222")
    page.fill('[data-testid="varsta"]', "16")          # Minor, sub 18
    page.click('[data-testid="submit"]')

    assert page.inner_text('[data-testid="err-varsta"]') == "TREBUIE SA AI MINIM 18 ANI PENTRU INSCRIERE"
    print("  [PASS] Eroarea de varsta minima este afisata corect.")


def test_short_name(page):
    """
    Test 5: Nume prea scurt (o singura litera).
    """
    print("[TEST] Rulare test_short_name...")
    page.goto(BASE_URL)
    page.fill('[data-testid="nume"]', "A")              # Prea scurt
    page.fill('[data-testid="prenume"]', "Andrei")
    page.fill('[data-testid="telefon"]', "0744555666")
    page.fill('[data-testid="varsta"]', "22")
    page.click('[data-testid="submit"]')

    assert page.inner_text('[data-testid="err-nume"]') == "NUMELE TREBUIE SA AIBA MINIM 2 CARACTERE"
    print("  [PASS] Eroarea de lungime minima pentru nume este afisata corect.")


def test_success(page):
    """
    Test 6: Toate campurile sunt valide - inscriere reusita.
    """
    print("[TEST] Rulare test_success...")
    page.goto(BASE_URL)
    page.fill('[data-testid="nume"]', "Georgescu")
    page.fill('[data-testid="prenume"]', "Alexandru")
    page.fill('[data-testid="telefon"]', "0711222333")
    page.fill('[data-testid="varsta"]', "28")
    page.click('[data-testid="submit"]')

    # Asteptam sa apara elementul de succes
    page.wait_for_selector('[data-testid="result"]')
    result = page.locator('[data-testid="result"]').inner_text()
    assert "Inscriere reusita!" in result
    assert "Georgescu" in result
    assert "Alexandru" in result
    assert "0711222333" in result
    assert "28" in result
    print("  [PASS] Inscrierea a reusit si toate datele sunt afisate corect.")


def test_random_fuzz(page, iter=5):
    """
    Test 7: Fuzzing aleatoriu - genereaza date aleatorii si verifica
    ca formularul reactioneaza corect (fie eroare, fie succes).
    """
    print(f"[TEST] Rulare test_random_fuzz cu {iter} iteratii...")

    for i in range(iter):
        nume = random_nume(random.randint(1, 12))       # Uneori prea scurt
        prenume = random_prenume(random.randint(0, 10)) # Uneori gol
        telefon = random_telefon() if random.random() > 0.3 else "gresit"
        varsta = str(random.randint(10, 80))            # Uneori sub 18

        print(f"  Iteratia {i+1}: Nume={nume}, Prenume={prenume}, "
              f"Tel={telefon}, Varsta={varsta}")

        page.goto(BASE_URL)
        page.fill('[data-testid="nume"]', nume)
        page.fill('[data-testid="prenume"]', prenume)
        page.fill('[data-testid="telefon"]', telefon)
        page.fill('[data-testid="varsta"]', varsta)
        page.click('[data-testid="submit"]')
        page.wait_for_timeout(100)

        # Asteptam sa apara fie mesajul de succes, fie erorile
        page.wait_for_selector(
            '[data-testid="result"], '
            '[data-testid="err-nume"], '
            '[data-testid="err-prenume"], '
            '[data-testid="err-telefon"], '
            '[data-testid="err-varsta"]'
        )

        # Verificam ca exista o reactie (succes sau eroare)
        has_result = page.locator('[data-testid="result"]').count() > 0
        has_errors = (
            page.locator('[data-testid="err-nume"]').count() > 0 or
            page.locator('[data-testid="err-prenume"]').count() > 0 or
            page.locator('[data-testid="err-telefon"]').count() > 0 or
            page.locator('[data-testid="err-varsta"]').count() > 0
        )

        assert has_result or has_errors, \
            f"Iteratia {i+1}: NICI SUCCES, NICI EROARE! Formularul nu a reactionat."
        print(f"    [PASS] {'Succes' if has_result else 'Eroare'} detectat corect.")


# ============== FUNCTIA PRINCIPALA ==============

def run():
    """Punctul de intrare - lanseaza browserul si ruleaza toate testele."""
    with sync_playwright() as p:
        # Lansam browserul Edge in mod vizibil (headless=False)
        # slow_mo adauga o pauza de 500ms intre actiuni pentru debugging
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500,
            channel="msedge"
        )
        page = browser.new_page()

        # Rulam fiecare test in ordine
        # Comentati/decomentati testele pe care doriti sa le executati
        test_empty_submit(page)
        test_invalid_phone(page)
        test_phone_with_letters(page)
        test_underage(page)
        test_short_name(page)
        test_success(page)
        test_random_fuzz(page, iter=5)

        print("\n" + "=" * 50)
        print("TOATE TESTELE S-AU INcheiat CU SUCCES!")
        print("=" * 50)

        browser.close()


# Pornirea testelor
if __name__ == "__main__":
    run()
