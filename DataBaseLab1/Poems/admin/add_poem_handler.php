<?php
	require_once('../connect_tar.php');
	//增加校验提高鲁棒性
	$author = $_POST['author'];
	$title = $_POST['title'];
	$content = $_POST['content'];
	//检查作者是否合法，并记录下其id
	$sql = "select * from Author where name='$author'";
	$data = mysqli_query($cnxn, $sql);
	$res = mysqli_fetch_array($data);
	if(!$res){
		echo "<script>window.alert('作者不存在！');</script>";
		header("refresh:1;url=../index.html");
		return;
	}
	$a_id = $res['id'];
	
	//检查标题是否存在
	$sql = "select * from Poem where title='$title'";
	$data = mysqli_query($cnxn, $sql);
	$res = mysqli_fetch_array($data);
	if($res){
		echo "<script>window.alert('条目已经存在！');</script>";
		header("refresh:1;url=../index.html");
	}
	else{
		$sql = "insert into Poem(title, content, author_id) values ('$title', '$content', '$a_id')";
		if(mysqli_query($cnxn, $sql))
			echo "<script>window.alert('成功添加！');</script>";
		else 
			echo "<script>window.alert('添加失败！');</script>";
		header("refresh:1;url=../index.html");
	}
	mysqli_close($cnxn);
?>