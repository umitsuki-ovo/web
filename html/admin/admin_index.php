<?php
session_start();

// dummy
$_SESSION['username'] = 'admin_user';
$_SESSION['role'] = 'admin';

// If not admin, redirect to login.php
if ($_SESSION['role'] != 'admin') {
    header('Location: ../auth/login.php');
    exit();
}
?>

<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Main Page</title>
    <link rel="stylesheet" href="../root.css">
    <link rel="stylesheet" href="styles.css">
    <script>
        function toggleUserMenu() {
            const userMenu = document.getElementById('user-menu');
            userMenu.style.display = userMenu.style.display === 'block' ? 'none' : 'block';
        }
        window.onclick = function(event) {
            if (!event.target.matches('.login')) {
                const userMenu = document.getElementById('user-menu');
                if (userMenu.style.display === 'block') {
                    userMenu.style.display = 'none';
                }
            }
        }
    </script>
</head>
<body>

<header>
    <a href="#" class="icon">アイコン</a>
    <div class="menu-container">
        <a href="#" class="menu">メニュー1</a>
        <a href="#" class="menu">メニュー2</a>
        <a href="../auth/user_role_change.php" class="menu">ユーザー権限変更</a>
    </div>
    <div class="login" onclick="toggleUserMenu()">
        <?php echo htmlspecialchars($_SESSION['username']); ?>
        <div id="user-menu" class="user-menu">
            <a href="../auth/logout.php">ログアウト</a>
        </div>
    </div>
</header>

<main>
    <h1>Welcome to the Admin Main Page</h1>
    <p>This is the main page for users with admin privileges.</p>
</main>

</body>
</html>
