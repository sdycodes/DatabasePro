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
	<title>全部诗词检索</title>
	<!-- stylesheets css -->
	<link rel="stylesheet" href="css/bootstrap.min.css">
  <link rel="stylesheet" href="css/custom.css">
  <link rel="stylesheet" type="text/css" href="css/loaders.css"/>
  <link rel="stylesheet" href="css/magnific-popup.css">
  <link rel="stylesheet" href="css/animate.min.css">
	<link rel="stylesheet" href="css/font-awesome.min.css">
  <link rel="stylesheet" href="css/nivo-lightbox.css">
  <link rel="stylesheet" href="css/nivo_themes/default/default.css">
  <link rel="stylesheet" href="css/hover-min.css">
  <link rel="stylesheet" href="css/contact-input-style.css">
</head>
<body>
<div class="loader loader-bg">
      <div class="loader-inner ball-pulse-rise">
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      </div>
    </div>
<!------------Static navbar ------------>
    <nav class="navbar navbar-default top-bar affix" data-spy="affix" data-offset-top="250" >
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="index.html">中华诗词库</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
        </div><!--/.nav-collapse -->
      </div>
    </nav>
	
<!------------ Home Banner ------------>
<section id="banner" class="parallax">
  <div class="gradient-overlay"></div>
    <div class="container">
      <div class="row">

          <div class="col-md-offset-2 col-md-8 col-sm-12">
              <h1 class="wow fadeInUp" data-wow-delay="1s">全部诗词</h1>
              <form class="wow fadeInUp" data-wow-delay="1s" 
              action="list_poem.php" method="get">
              
			<span class="input input-hoshi">
				<label class="input_label input_label-hoshi input_label-hoshi-color-1" for="input-4">
				</label>
				<h2 style='color:#fff'>搜索作者</h2>
				<input class="input_field input_field-hoshi" type="text" name="name" value="" size="8">
			</span>
			<br>
			<ul class="filter-wrapper clearfix">
		<li>
	 		<input href="#todo" class="wow fadeInUp btn btn-transparent-white btn-capsul btn-lg smoothScroll btn" data-wow-delay="1.3s" type="button" value="查看全部" onclick="window.location='list_poem.php'">
	 	</li>
	 	<li>
	 		<input href="#todo" class="wow fadeInUp btn btn-transparent-white btn-capsul btn-lg smoothScroll btn" data-wow-delay="1.3s" type="submit" value="搜索">
		</li>
			</form>
          </div>

      </div>
    </div>
</section>

<!------------ List section ------------>
<section id="todo" class="parallax">
  <div class="container">
    <div class="row">

      <div class="col-md-12">

       <div class="col-md-offset-2 col-md-8 col-sm-offset-1 col-sm-10 text-center">
         <div class="wow fadeInUp section-title" data-wow-delay="1s">
            <h2>找到的结果<small>古诗与诗人们的故事</small></h2>
        </div>
      </div>
        <br>
<br/>
	<table border="1" width="500" >
	 <tr>
	 <td>编号</td>
	 <td>作者</td>
	 <td>年代</td>
	 <td>性别</td>
	 </tr>
	<?php 
	if($res)
		while($row=mysqli_fetch_array($res)){?>
	<tr>
	 <td><?php echo $row['id'] ?></td>
	 <td><?php echo $row['name'] ?></td>
	 <td><?php echo $row['era'] ?></td>
	 <td><?php if($row['gender']){echo '男';}else{echo '女';} ?></td>
	 </tr>
	<?php }?>
	<tr>
	 <td colspan="6">
	</td>
	</tr>
	</table>

	<br>
	<div align="center">
	<?php
	echo "<h4 style='color:#A9537B'>当前第 {$page}/{$maxpage} 页 共 {$totalnum} 条</h4>";
	?>
		<ul class="filter-wrapper clearfix">
	<?php
	echo "<li><a class='btn btn-capsul btn-transparent-prime' href='list_poem.php?page=1{$url}'>首页</a></li>";
	echo "<li><a class='btn btn-capsul btn-transparent-prime' href='list_poem.php?page=".(($page-1) < 1 ? 1 : ($page-1))."{$url}'>上一页</a></li>";
	echo "<li><a class='btn btn-capsul btn-transparent-prime' href='list_poem.php?page=".(($page+1) > $maxpage ? $maxpage : ($page+1))."{$url}'>下一页</a></li>";
	echo "<li><a class='btn btn-capsul btn-transparent-prime' href='list_poem.php?page={$maxpage}{$url}'>尾页</a></li>";
	?>
	</ul>
	</div>
	<br>
          <!-- iso section -->
          <div class="iso-section wow fadeInUp text-center" data-wow-delay="0.5">

            		<ul class="filter-wrapper clearfix">
                        <li><a href="#banner" class="wow fadeInUp btn btn-transparent-white btn-capsul btn-lg smoothScroll back" data-wow-delay="1.3s" style="font-size: 20px;">返回</a></li>
                    </ul>
         </div>

          </div>

      </div>

    </div>
  </div>
</section>


<!------------ Footer section ------------>
<footer>
    
        <div class="container">
            <div class="row">
                <div class="col-sm-12 col-md-3">&copy;<script type="text/javascript">document.write(new Date().getFullYear());</script> 史鼎元 & 白心宇呈现</div>
                <div class="col-sm-12 col-md-2 col-md-offset-7">用 <i class="fa fa-heart"></i> 制作</div>
            </div>
        
        </div>
    
    </footer>
<script src="js/jquery.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery.magnific-popup.min.js"></script>
<script src="js/jquery.backstretch.min.js"></script>
<script src="js/isotope.js"></script>
<script src="js/imagesloaded.min.js"></script>
<script src="js/nivo-lightbox.min.js"></script>
<script src="js/jquery.parallax.js"></script>
<script src="js/smoothscroll.js"></script>
<script src="js/wow.min.js"></script>
<script src="js/core.js"></script>
    <script type="text/javascript">
    

    $(function() {
    var to = function() {
    	if (sessionStorage.getItem('down'))
    		$('body,html').animate({
            scrollTop: $('#todo').offset().top
        }, 200);
        if (sessionStorage.getItem('up'))
        	$('body,html').animate({
            scrollTop: $('#banner').offset().top
        }, 200);
        sessionStorage.removeItem('down');
        sessionStorage.removeItem('up');
    };
    if (sessionStorage.getItem('anchor')) {
        to();
    }
    $('.btn').on('click', function() {
        sessionStorage.setItem('anchor', true);
        sessionStorage.setItem('down', true);
        location.reload(true);
    });
    $('.back').on('click', function() {
        sessionStorage.setItem('anchor', true);
        sessionStorage.removeItem('down');
        sessionStorage.setItem('up', true);
        location.reload(true);
    });


});</script>
</body>
</html>