{% extends "template.html" %}


{% block title %}
Delete user
{% endblock  %}


{% block files %}

{% endblock  %}
    

{% block content %}
<h2>Delete User</h2>
    <form action="{{url_for('delete_user_request.delete_user_request')}}" method="post">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username" required><br><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password" required><br><br>
        <input type="submit" value="Delete User">
    </form>
{% endblock  %}
