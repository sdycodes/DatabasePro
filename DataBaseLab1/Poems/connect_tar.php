<?php
	require_once('config.php');
	$cnxn = mysqli_connect(HOST, USERNAME, PASSWORD, DATABASET);
	$sql = "set names utf8";
	mysqli_query($cnxn, $sql);
?>
