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
    $result = file_get_contents('http://****/login', false, $context);
    
    if ($result === FALSE) { 
        echo 'Error connecting to server.';
    } else {
        $response = json_decode($result, true);
        if (isset($response['message'])) {
            echo $response['message'];
            if (isset($response['redirect_url'])) {
                echo '<script>';
                echo 'setTimeout(function() { window.location.href = "' . $response['redirect_url'] . '"; }, 10000);';
                echo '</script>';
                header('Location: ' . $response['redirect_url']);
                exit();
            }
        }
    }
}
?>
