<?php
	error_reporting(E_ALL || ~E_NOTICE);
	require_once('./connect_tar.php');
	$id = $_POST['id'];
	if($id==NULL){
		$title = $_POST['title'];
		$sql = "select * from Poem where title='$title'";
		$data = mysqli_query($cnxn, $sql);
		$res = mysqli_fetch_array($data);
    if($res==NULL&&$title!=NULL){
      echo "<script>window.alert('诗词不存在！');</script>";
      header("refresh:0.2;url=modify_poem.php");
    }
		$author_id = $res['author_id'];
		$sql = "select * from Author where id='$author_id'";
		$data = mysqli_query($cnxn, $sql);
		$res2 = mysqli_fetch_array($data);
		$author = $res2['name'];
	}
	else{
		$newTitle = $_POST['newTitle'];
		$content = $_POST['content'];
		$author = $_POST['author'];
		$sql = "select * from Author where name='$author'";
		$data = mysqli_query($cnxn, $sql);
		$res2 = mysqli_fetch_array($data);
		$author_id = $res2['id'];
		if($author==NULL)	echo "<script>window.alert('不存在作者！');</script>";
		else{
			$sql = "update Poem set title='$newTitle', content= '$content', author_id='$author_id' where id ='$id'";
			if(mysqli_query($cnxn, $sql))
				echo "<script>window.alert('修改成功！');</script>";
			else
				echo "<script>window.alert('修改失败！');</script>";
		}
		$author = NULL;
	}
	mysqli_close($cnxn);
?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>修改诗词</title>
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
              <h1 class="wow fadeInUp" data-wow-delay="1s">修改诗词</h1>
              <form class="wow fadeInUp"  data-wow-delay="1s" action="./modify_poem.php" method="POST">
			<span class="input input-hoshi">
				<label class="input_label input_label-hoshi input_label-hoshi-color-1" for="input-4">
				</label>
				<h3 style='color:#fff;margin-top:0em'>输入标题</h3>
				<input class="input_field input_field-hoshi" type="text" name="title"  value="<?php echo $_POST['title'];?>" size="8">
			</span>
			<input class="wow fadeInUp btn btn-transparent-white btn-capsul btn-lg smoothScroll btn" data-wow-delay="1.3s" type="submit" value="搜索">
		</form>
              
          </div>

      </div>
    </div>
</section>

<!------------ Home Banner ------------>
<div id="jump">
</div>
<section id="banner" class="parallax">
  <div class="gradient-overlay"></div>
    <div class="container">
      <div class="row">

          <div class="col-md-offset-2 col-md-8 col-sm-12">
         
              <form class="wow fadeInUp"  data-wow-delay="1s" action="./modify_poem.php" method="POST">
			<input type="hidden" readonly name="id" value="<?php echo $res['id'];?>" >
			<span class="input input-hoshi">
				<label class="input_label input_label-hoshi input_label-hoshi-color-1" for="input-4">
				</label>
				<h3 style='color:#fff;margin-top:0em'></h3>
				<input class="input_field input_field-hoshi" type="text" id="newTitle" name="newTitle"  value="<?php echo $res['title'];?>"  size="8">
			</span>
			<span class="input input-hoshi">
				<label class="input_label input_label-hoshi input_label-hoshi-color-1" for="input-4">
				</label>
				<h3 style='color:#fff;margin-top:0em'>输入新作者</h3>
				<input class="input_field input_field-hoshi" type="text" id="author" name="author" value="<?php echo $author;?>" size="8">
			</span>
			
			<span class="input input-hoshi">
				<label class="input_label input_label-hoshi input_label-hoshi-color-1" for="input-4">
				</label>
				<h3 style='color:#fff;margin-top:0em'>输入新内容</h3>
				<input class="input_field input_field-hoshi" type="text" id="content" name="content" value="<?php echo $res['content'];?>" size="8">
			</span>
			<br>
	 		<input class="wow fadeInUp btn btn-transparent-white btn-capsul btn-lg smoothScroll back" data-wow-delay="1.3s" type="submit" value="提交结果" onclick="window.location='modify_poem.php'">
			</form>
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
            scrollTop: $('#jump').offset().top
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
