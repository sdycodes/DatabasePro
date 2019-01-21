<?php
	require_once('./connect_tar.php');
	$wherelist=array();
	$urlist=array();
	if(!empty($_GET['id'])){
		$wherelist[]=" id like '%".$_GET['id']."%'";
		$urllist[]="id=".$_GET['id'];
	}
	if(!empty($_GET['name'])){
		$wherelist[]=" name like '%".$_GET['name']."%'";
		$urllist[]="name=".$_GET['name'];
	}
	if(!empty($_GET['era'])){
		$wherelist[]=" era like '%".$_GET['era']."%'";
		$urllist[]="era=".$_GET['era'];
	}
	$where="";
	$url="";
	if(count($wherelist)>0){
		$where=" where ".implode(' and ',$wherelist);
		$url='&'.implode('&',$urllist);
	}
	$sql = "select * from Author $where";
	$res = mysqli_query($cnxn, $sql);
	$totalnum=mysqli_num_rows($res);
	//每页显示条数
	$pagesize=5;
	//总共有几页
	$maxpage=ceil($totalnum/$pagesize);
	$page=isset($_GET['page'])?$_GET['page']:1;
	if($page <1){
		$page=1;
	}
	if($page>$maxpage){
		$page=$maxpage;
	}
	$limit=" limit ".($page-1)*$pagesize.",$pagesize";
	$sql1="select * from Author {$where} order by id desc {$limit}";
	//此处加了id降序
	$res = mysqli_query($cnxn, $sql1);
?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>用户资料显示</title>
</head>
<body>
	<form action="list_author.php" method="get">
	id：<input type="text" name="id" value="" size="8">
	用户名<input type="text" name="name" value="" size="8">
	年龄：<input type="text" name="era" value="" size="8">
	 <input type="button" value="查看全部" onclick="window.location='list_author.php'">
	 <input type="submit" value="搜索">
	</form>
	<br/>
	<table border="1" width="500" >
	 <tr>
	 <td>编号</td>
	 <td>用户名</td>
	 <td>年龄</td>
	 <td>性别</td>
	 </tr>
	<?php while($row=mysqli_fetch_array($res)){?>
	<tr>
	 <td><?php echo $row['id'] ?></td>
	 <td><?php echo $row['name'] ?></td>
	 <td><?php echo $row['era'] ?></td>
	 <td><?php if($row['gender']){echo '男';}else{echo '女';} ?></td>
	 </tr>
	<?php }?>
	<tr>
	 <td colspan="6">
	<?php
	echo " 当前{$page}/{$maxpage}页 共{$totalnum}条";
	echo "<a href='list_author.php?page=1{$url}'>首页</a> ";
	echo "<a href='list_author.php?page=".(($page-1) < 1 ? 1 : ($page-1))."{$url}'>上一页</a>";
	echo "<a href='list_author.php?page=".(($page+1) > $maxpage ? $maxpage : ($page+1))."{$url}'>下一页</a>";
	echo " <a href='list_author.php?page={$maxpage}{$url}'>尾页</a> ";
	?>
	</td>
	 </tr>
	</table>
	<button onclick="location.href='/index.html'" type="button">返回</button>
</body>
</html>
