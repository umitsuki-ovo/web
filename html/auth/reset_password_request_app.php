<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $email = $_POST['email'];
    
    $data = array('email' => $email);
    
    $options = array(
        'http' => array(
            'header'  => "Content-type: application/json\r\n",
            'method'  => 'POST',
            'content' => json_encode($data),
        ),
    );
    $context  = stream_context_create($options);
    $result = file_get_contents('http://127.0.0.1:5000/reset_password_request', false, $context);
    
    if ($result === FALSE) { 
        echo 'Error connecting to server.';
    } else {
        $response = json_decode($result, true);
        echo $response['message'];
    }
}
?>
