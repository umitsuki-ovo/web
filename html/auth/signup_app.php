<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $email = $_POST['email'];
    $password = $_POST['password'];
    
    $data = array(
        'username' => $username,
        'email' => $email,
        'password' => $password
    );
    
    $options = array(
        'http' => array(
            'header'  => "Content-type: application/json\r\n",
            'method'  => 'POST',
            'content' => json_encode($data),
        ),
    );
    $context  = stream_context_create($options);
    $result = file_get_contents('http://****/signup_request', false, $context);
    
    if ($result === FALSE) { 
        echo 'Error connecting to server.';
    }
}
?>
