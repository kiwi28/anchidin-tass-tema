<?php
$name = $_POST['name']??'';
$email = $_POST['email']??'';
$errName='';
$errEmail='';
 
$date = $_POST['date']??'date("Y-m-d")';
$errDate='';
 
if($_SERVER['REQUEST_METHOD']=='POST'){
    if(trim($name)===''){
        $errName='NUMELE ESTE OBLIGATORIU';
    }
    if(trim($email)===''||strpos($email,'@')===false){
        $errEmail='EMAILUL ESTE INVALID';
    }
//     if ($date===''){
//         $errDate='DATA ESTE OBLIGATORIE';
//     }elseif($date < date('Y-m-d')){
//         $errDate='DATA NU POATE FI IN TRECUT';
// }
}
 
 
 
?>
<!-- INCEPUT COD HTML -->
<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    <title>Formular simplu</title>
</head>
 
 
<body>
<h1>ACESTA ESTE UN FORMULAR SIMPLU</h1>
<form method="post">
    <label>Nume:</label><br>
    <input type="text"  data-testid="name" name="name" value="<?php echo $name; ?>"><br>
    <?php if($errName): ?>
        <div data-testid="err-name"><?php echo $errName; ?></div>
    <?php endif; ?>
    <br>
    <label>Email:</label><br>
    <input type="text" name="email" value="<?php echo $email; ?>"data-testid="email"><br>
    <?php if($errEmail): ?>
        <div data-testid="err-email"><?php echo $errEmail; ?></div>
    <?php endif; ?>
    <br>
 
    <!--CAMP DATA -->
 
    <label>Data:</label><br>
    <input type="date" name="date" value="<?php echo $date; ?>" data-testid="date"><br>
<br>
<?php if($errDate): ?>
    <div data-testid="err-date"><?php echo $errDate; ?></div>
<?php endif; ?>
<br>
<button type="submit" data-testid="submit">Trimite</button>
</form>
<?php
if($_SERVER['REQUEST_METHOD']==='POST' && !$errName && !$errEmail){
    echo '<h2>Datele au fost primite!</h2>';
    echo '<p>Nume: '.$name.'</p>';
    echo '<p>Email: '.$email.'</p>';
   // echo '<p>Data: '.$date.'</p>';
}
?>
</body>
</html>