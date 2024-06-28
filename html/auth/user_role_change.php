<!DOCTYPE html>
<html>
<head>
    <title>Change User Role</title>
</head>
<body>
    <h2>Change User Role</h2>
    <form action="{{url_for('change_role_request.change_role_request')}}" method="post">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username" required><br><br>
        <label for="role">Role:</label><br>
        <select id="role" name="role" required>
            <option value="user">User</option>
            <option value="admin">Admin</option>
        </select><br><br>
        <input type="submit" value="Change Role">
    </form>
</body>
</html>
