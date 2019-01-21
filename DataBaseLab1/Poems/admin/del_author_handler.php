<?php
	require_once('../connect_tar.php');
	$name = $_POST['name'];
	$sql = "delete from Author where name='$name'";
	$data = mysqli_query($cnxn, $sql);
	if($data){
		echo "<script>window.alert('成功删除！');</script>";
	}
	else{
		echo "<script>window.alert('删除失败！');</script>";;
	}
	header("refresh:1;url=../index.html");
	
?>
