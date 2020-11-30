# vita-soft-test


Test project built in Django, with user authentication and authorization. Supports different user roles with different access rights to API endpoints.
For authorization, JWT is used which is available with the indication of the username and password at:
- token/

# Requirements
The project was built in Django using the following requirements:
- rest_framework,
- drf_yasg

A fixture file has been added to the application (custom_requests/dump.json), it contains test roles, users and models that extend them.
Also added a swagger, which is available at
- swagger/
