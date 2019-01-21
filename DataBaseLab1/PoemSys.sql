-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- 主机： 127.0.0.1
-- 生成日期： 2018-10-03 02:17:12
-- 服务器版本： 8.0.12
-- PHP 版本： 7.1.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `PoemSys`
--

-- --------------------------------------------------------

--
-- 表的结构 `Author`
--

CREATE TABLE `Author` (
  `id` int(32) NOT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `gender` char(1) NOT NULL,
  `era` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='authors';

--
-- 转存表中的数据 `Author`
--

INSERT INTO `Author` (`id`, `name`, `gender`, `era`) VALUES
(1, '李白', '男', '唐'),
(2, '杜甫', '男', '唐'),
(3, '白居易', '男', '唐'),
(4, '辛弃疾', '男', '南宋'),
(5, '苏轼', '男', '宋'),
(6, '李清照', '女', '宋');

-- --------------------------------------------------------

--
-- 表的结构 `Poem`
--

CREATE TABLE `Poem` (
  `id` int(32) NOT NULL,
  `title` text NOT NULL,
  `content` text NOT NULL,
  `author_id` int(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 转存表中的数据 `Poem`
--

INSERT INTO `Poem` (`id`, `title`, `content`, `author_id`) VALUES
(1, '静夜思', '床前明月光，疑是地上霜。\r\n举头望明月，低头思故乡。', 1),
(2, '望庐山瀑布', '日照香炉生紫烟，遥看瀑布挂前川。\r\n飞流直下三千尺，疑是银河落九天。', 1),
(3, '春望', '国破山河在，城春草木深。\r\n感时花溅泪，恨别鸟惊心。\r\n烽火连三月，家书抵万金。\r\n白头搔更短，浑欲不胜簪。', 2),
(4, '望岳', '岱宗夫如何？齐鲁青未了。\r\n造化钟神秀，阴阳割昏晓。\r\n荡胸生曾云，决眦入归鸟。\r\n会当凌绝顶，一览众山小。', 2),
(5, '长恨歌', '汉皇重色思倾国，御宇多年求不得。\r\n杨家有女初长成，养在深闺人未识。\r\n天生丽质难自弃，一朝选在君王侧。\r\n回眸一笑百媚生，六宫粉黛无颜色。\r\n春寒赐浴华清池，温泉水滑洗凝脂。\r\n侍儿扶起娇无力，始是新承恩泽时。\r\n云鬓花颜金步摇，芙蓉帐暖度春宵。\r\n春宵苦短日高起，从此君王不早朝。\r\n承欢侍宴无闲暇，春从春游夜专夜。\r\n后宫佳丽三千人，三千宠爱在一身。\r\n金屋妆成娇侍夜，玉楼宴罢醉和春。\r\n姊妹弟兄皆列土，可怜光彩生门户。\r\n遂令天下父母心，不重生男重生女。\r\n骊宫高处入青云，仙乐风飘处处闻。\r\n缓歌慢舞凝丝竹，尽日君王看不足。\r\n渔阳鼙鼓动地来，惊破霓裳羽衣曲。\r\n九重城阙烟尘生，千乘万骑西南行。\r\n翠华摇摇行复止，西出都门百余里。\r\n六军不发无奈何，宛转蛾眉马前死。\r\n花钿委地无人收，翠翘金雀玉搔头。\r\n君王掩面救不得，回看血泪相和流。\r\n黄埃散漫风萧索，云栈萦纡登剑阁。\r\n峨嵋山下少人行，旌旗无光日色薄。\r\n蜀江水碧蜀山青，圣主朝朝暮暮情。\r\n行宫见月伤心色，夜雨闻铃肠断声。\r\n天旋地转回龙驭，到此踌躇不能去。\r\n马嵬坡下泥土中，不见玉颜空死处。\r\n君臣相顾尽沾衣，东望都门信马归。\r\n归来池苑皆依旧，太液芙蓉未央柳。\r\n芙蓉如面柳如眉，对此如何不泪垂。\r\n春风桃李花开日，秋雨梧桐叶落时。\r\n西宫南内多秋草，落叶满阶红不扫。\r\n梨园弟子白发新，椒房阿监青娥老。\r\n夕殿萤飞思悄然，孤灯挑尽未成眠。\r\n迟迟钟鼓初长夜，耿耿星河欲曙天。\r\n鸳鸯瓦冷霜华重，翡翠衾寒谁与共。\r\n悠悠生死别经年，魂魄不曾来入梦。\r\n临邛道士鸿都客，能以精诚致魂魄。\r\n为感君王辗转思，遂教方士殷勤觅。\r\n排空驭气奔如电，升天入地求之遍。\r\n上穷碧落下黄泉，两处茫茫皆不见。\r\n忽闻海上有仙山，山在虚无缥渺间。\r\n楼阁玲珑五云起，其中绰约多仙子。\r\n中有一人字太真，雪肤花貌参差是。\r\n金阙西厢叩玉扃，转教小玉报双成。\r\n闻道汉家天子使，九华帐里梦魂惊。\r\n揽衣推枕起徘徊，珠箔银屏迤逦开。\r\n云鬓半偏新睡觉，花冠不整下堂来。\r\n风吹仙袂飘飖举，犹似霓裳羽衣舞。\r\n玉容寂寞泪阑干，梨花一枝春带雨。\r\n含情凝睇谢君王，一别音容两渺茫。\r\n昭阳殿里恩爱绝，蓬莱宫中日月长。\r\n回头下望人寰处，不见长安见尘雾。\r\n惟将旧物表深情，钿合金钗寄将去。\r\n钗留一股合一扇，钗擘黄金合分钿。\r\n但教心似金钿坚，天上人间会相见。\r\n临别殷勤重寄词，词中有誓两心知。\r\n七月七日长生殿，夜半无人私语时。\r\n在天愿作比翼鸟，在地愿为连理枝。\r\n天长地久有时尽，此恨绵绵无绝期。', 3),
(6, '卖炭翁', '卖炭翁，伐薪烧炭南山中。\r\n满面尘灰烟火色，两鬓苍苍十指黑。\r\n卖炭得钱何所营？身上衣裳口中食。\r\n可怜身上衣正单，心忧炭贱愿天寒。\r\n夜来城外一尺雪，晓驾炭车辗冰辙。\r\n牛困人饥日已高，市南门外泥中歇。\r\n翩翩两骑来是谁？黄衣使者白衫儿。\r\n手把文书口称敕，回车叱牛牵向北。\r\n一车炭，千余斤，宫使驱将惜不得。\r\n半匹红绡一丈绫，系向牛头充炭直。', 3),
(7, '水龙吟·登建康赏心亭', '楚天千里清秋，水随天去秋无际。遥岑远目，献愁供恨，玉簪螺髻。落日楼头，断鸿声里，江南游子。把吴钩看了，栏杆拍遍，无人会，登临意。\r\n休说鲈鱼堪脍，尽西风，季鹰归未？求田问舍，怕应羞见，刘郎才气。可惜流年，忧愁风雨，树犹如此！倩何人唤取，红巾翠袖，揾英雄泪？', 4),
(8, '永遇乐·京口北固亭怀古', '千古江山，英雄无觅孙仲谋处。舞榭歌台，风流总被雨打风吹去。斜阳草树，寻常巷陌，人道寄奴曾住。想当年，金戈铁马，气吞万里如虎。\r\n元嘉草草，封狼居胥，赢得仓皇北顾。四十三年，望中犹记，烽火扬州路。可堪回首，佛狸祠下，一片神鸦社鼓。凭谁问：廉颇老矣，尚能饭否？', 4),
(9, '水调歌头·明月几时有', '丙辰中秋，欢饮达旦，大醉作此篇，兼怀子由。\r\n　　明月几时有？把酒问青天。不知天上宫阙，今夕是何年？我欲乘风归去，又恐琼楼玉宇，高处不胜寒。起舞弄清影，何似在人间？ 转朱阁，低绮户，照无眠。不应有恨，何事长向别时圆？人有悲欢离合，月有阴晴圆缺，此事古难全。但愿人长久，千里共婵娟。', 5),
(10, '题西林壁', '横看成岭侧成峰，远近高低各不同。\r\n不识庐山真面目，只缘身在此山中。', 5),
(11, '声声慢·寻寻觅觅', '寻寻觅觅，冷冷清清，凄凄惨惨戚戚。\r\n乍暖还寒时候，最难将息。\r\n三杯两盏淡酒，怎敌他、晚来风急？\r\n雁过也，正伤心，却是旧时相识。\r\n\r\n满地黄花堆积。憔悴损，如今有谁堪摘？\r\n守着窗儿，独自怎生得黑？\r\n梧桐更兼细雨，到黄昏、点点滴滴。\r\n这次第，怎一个愁字了得！', 6),
(12, '如梦令·常记溪亭日暮', '常记溪亭日暮，沉醉不知归路，\r\n兴尽晚回舟，误入藕花深处。\r\n争渡，争渡，惊起一滩鸥鹭。', 6);

--
-- 转储表的索引
--

--
-- 表的索引 `Author`
--
ALTER TABLE `Author`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `Poem`
--
ALTER TABLE `Poem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `itsAuthor` (`author_id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `Author`
--
ALTER TABLE `Author`
  MODIFY `id` int(32) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- 使用表AUTO_INCREMENT `Poem`
--
ALTER TABLE `Poem`
  MODIFY `id` int(32) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- 限制导出的表
--

--
-- 限制表 `Poem`
--
ALTER TABLE `Poem`
  ADD CONSTRAINT `itsAuthor` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
