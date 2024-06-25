<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];
    
    $data = array(
        'username' => $username,
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
    $result = file_get_contents('http://127.0.0.1:5000/login', false, $context);
    
    if ($result === FALSE) { 
        echo 'Error connecting to server.';
    } else {
        $response = json_decode($result, true);
        if (isset($response['message'])) {
            echo $response['message'];
            if (isset($response['redirect_url'])) {
                header('Location: ' . $response['redirect_url']);
                exit();
            }
        }
    }
}
?>
