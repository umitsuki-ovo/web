<!DOCTYPE html>
<html>
<head>
    <title>Sign Up</title>
    <script>
        function validateForm() {
            var email = document.getElementById("email").value;
            var emailConfirm = document.getElementById("email_confirm").value;
            var password = document.getElementById("password").value;
            var passwordConfirm = document.getElementById("password_confirm").value;

            if (email !== emailConfirm) {
                alert("Emails do not match.");
                return false;
            }
            if (password !== passwordConfirm) {
                alert("Passwords do not match.");
                return false;
            }
            return true;
        }
    </script>
</head>
<body>
    <h2>Sign Up</h2>
    <form action="{{url_for('signup.signup')}}" method="post" onsubmit="return validateForm()">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username" required><br><br>
        <label for="email">Email:</label><br>
        <input type="email" id="email" name="email" required><br><br>
        <label for="email_confirm">Confirm Email:</label><br>
        <input type="email" id="email_confirm" name="email_confirm" required><br><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password" required><br><br>
        <label for="password_confirm">Confirm Password:</label><br>
        <input type="password" id="password_confirm" name="password_confirm" required><br><br>
        <input type="submit" value="Sign Up">
    </form>
</body>
</html>
