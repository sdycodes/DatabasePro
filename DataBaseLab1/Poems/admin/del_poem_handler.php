<?php
	require_once('../connect_tar.php');
	$title = $_POST['title'];
	$sql = "delete from Poem where title='$title'";
	$data = mysqli_query($cnxn, $sql);
	if($data){
		echo "<script>window.alert('成功删除！');</script>";
	}
	else{
		echo "<script>window.alert('删除失败！');</script>";
	}
	header("refresh:1;url=../index.html");
	
?>
