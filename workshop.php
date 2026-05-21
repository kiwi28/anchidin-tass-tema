<?php
// Initializare variabile din POST sau valori goale implicite
$nume    = $_POST['nume']    ?? '';
$prenume = $_POST['prenume'] ?? '';
$telefon = $_POST['telefon'] ?? '';
$varsta  = $_POST['varsta']  ?? '';

// Variabile pentru mesaje de eroare (goale initial = fara eroare)
$errNume    = '';
$errPrenume = '';
$errTelefon = '';
$errVarsta  = '';

// Procesarea formularului la submit (doar la metoda POST)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    // Validare NUME - obligatoriu, minim 2 caractere
    if (trim($nume) === '') {
        $errNume = 'NUMELE ESTE OBLIGATORIU';
    } elseif (strlen(trim($nume)) < 2) {
        $errNume = 'NUMELE TREBUIE SA AIBA MINIM 2 CARACTERE';
    }

    // Validare PRENUME - obligatoriu
    if (trim($prenume) === '') {
        $errPrenume = 'PRENUMELE ESTE OBLIGATORIU';
    }

    // Validare TELEFON - obligatoriu si format de 10 cifre
    // Accepta doar cifre, fara spatii sau alte caractere
    if (trim($telefon) === '') {
        $errTelefon = 'TELEFONUL ESTE OBLIGATORIU';
    } elseif (!preg_match('/^[0-9]{10}$/', trim($telefon))) {
        $errTelefon = 'TELEFONUL TREBUIE SA CONTINA EXACT 10 CIFRE';
    }

    // Validare VARSTA - obligatorie, intre 18 si 99 ani
    if (trim($varsta) === '') {
        $errVarsta = 'VARSTA ESTE OBLIGATORIE';
    } elseif (!is_numeric($varsta) || intval($varsta) < 18) {
        $errVarsta = 'TREBUIE SA AI MINIM 18 ANI PENTRU INSCRIERE';
    } elseif (intval($varsta) > 99) {
        $errVarsta = 'VARSTA INTRODUSA NU ESTE VALIDA';
    }
}
?>

<!-- ======== INCEPUT COD HTML ======== -->
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Inscriere Workshop</title>
    <style>
        /* Stilizare minimala pentru claritate */
        body { font-family: Arial, sans-serif; max-width: 500px; margin: 40px auto; }
        label { font-weight: bold; }
        input { width: 100%; padding: 8px; margin: 5px 0; box-sizing: border-box; }
        button { padding: 10px 25px; font-size: 16px; cursor: pointer; }
        .eroare { color: red; font-size: 14px; margin-bottom: 10px; }
        .succes { background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; }
    </style>
</head>
<body>

<h1>INSCRIERE WORKSHOP - PROGRAMARE WEB</h1>
<p>Completati toate campurile pentru a va inregistra la workshop.</p>

<form method="post">
    <!-- CAMP NUME -->
    <label>Nume:</label><br>
    <input type="text" name="nume" data-testid="nume"
           value="<?php echo htmlspecialchars($nume); ?>"><br>
    <?php if ($errNume): ?>
        <div class="eroare" data-testid="err-nume"><?php echo $errNume; ?></div>
    <?php endif; ?>
    <br>

    <!-- CAMP PRENUME -->
    <label>Prenume:</label><br>
    <input type="text" name="prenume" data-testid="prenume"
           value="<?php echo htmlspecialchars($prenume); ?>"><br>
    <?php if ($errPrenume): ?>
        <div class="eroare" data-testid="err-prenume"><?php echo $errPrenume; ?></div>
    <?php endif; ?>
    <br>

    <!-- CAMP TELEFON -->
    <label>Telefon:</label><br>
    <input type="text" name="telefon" data-testid="telefon"
           value="<?php echo htmlspecialchars($telefon); ?>"
           placeholder="Ex: 0712345678"><br>
    <?php if ($errTelefon): ?>
        <div class="eroare" data-testid="err-telefon"><?php echo $errTelefon; ?></div>
    <?php endif; ?>
    <br>

    <!-- CAMP VARSTA -->
    <label>Varsta:</label><br>
    <input type="number" name="varsta" data-testid="varsta"
           value="<?php echo htmlspecialchars($varsta); ?>"
           min="1" max="99"><br>
    <?php if ($errVarsta): ?>
        <div class="eroare" data-testid="err-varsta"><?php echo $errVarsta; ?></div>
    <?php endif; ?>
    <br>

    <button type="submit" data-testid="submit">Trimite inscrierea</button>
</form>

<?php
// Afisare confirmare dupa submit valid (fara erori)
if ($_SERVER['REQUEST_METHOD'] === 'POST' && !$errNume && !$errPrenume && !$errTelefon && !$errVarsta) {
    echo '<div class="succes" data-testid="result">';
    echo '<h2>Inscriere reusita!</h2>';
    echo '<p><strong>Nume:</strong> ' . htmlspecialchars($nume) . '</p>';
    echo '<p><strong>Prenume:</strong> ' . htmlspecialchars($prenume) . '</p>';
    echo '<p><strong>Telefon:</strong> ' . htmlspecialchars($telefon) . '</p>';
    echo '<p><strong>Varsta:</strong> ' . htmlspecialchars($varsta) . ' ani</p>';
    echo '</div>';
}
?>

</body>
</html>
