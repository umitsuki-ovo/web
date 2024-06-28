<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $role = $_POST['role'];
    
    $data = array(
        'username' => $username,
        'role' => $role
    );
    
    $options = array(
        'http' => array(
            'header'  => "Content-type: application/json\r\n",
            'method'  => 'POST',
            'content' => json_encode($data),
        ),
    );
    $context  = stream_context_create($options);
    $result = file_get_contents('http://****/change_role_request', false, $context);
    
    if ($result === FALSE) { 
        echo 'Error connecting to server.';
    } else {
        $response = json_decode($result, true);
        echo $response['message'];
    }
}
?>
