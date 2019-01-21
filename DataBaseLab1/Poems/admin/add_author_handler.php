<?php
	require_once('../connect_tar.php');
	$name = $_POST['name'];
	$gender = $_POST['gender'];
	$era = $_POST['era'];
	$sql = "select * from Author where name='$name'";
	$data = mysqli_query($cnxn, $sql);
	$res = mysqli_fetch_row($data);
	//var_dump($res);
	if(!$res){
		$sql = "insert into Author(name, era, gender) values ('$name', '$era', '$gender')";
		mysqli_query($cnxn, $sql);
		echo "<script>window.alert('成功添加！');</script>";
	}
	else{
		echo "<script>window.alert('已经存在！');</script>";
	}
	header("refresh:1;url=../index.html");
	mysqli_close($cnxn);
?>
