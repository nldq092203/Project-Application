# Sport api for orienteering 

## All apis

### Djoser for registration, login, logout and password reset.
*** Use Token-Based Authentication, each action that required authentication have include Token in Header

1. Registration: POST request - {{baseURL}}/api/auth/users/ 
-> body: username + password + first_name + last_name + email + ....
-> response.data: email + username

2. Login: POST request - {{baseURL}}/api/auth/token/login/
-> body: username + password
-> response.data: accessToken
Save accessToken in client-side : Local Storage, Session Storage or Cookies

3. Logout: POST request - {{baseURL}}/api/auth/token/logout/
-> no body, Token included in Header 
-> response.status 200 -> delete the current token 
-> need to delete the token saved in client-side 

4. Reset Password : POST request - {{baseURL}}/api/auth/users/reset_password/
-> body: email
-> send an email with a password reset link to the specified email address 
(URL sent: PASSWORD_RESET_CONFIRM_URL - in settings.py)
-> response status 200

5. Reset Password Confirm: POST - {{baseURL}}/api/auth/users/reset_password_confirm/
-> body: new_password
-> response status 200

6. Set New Password: POST - {{baseURL}}/api/auth/users/set_password/
-> body: 
current_password + new_password + logout_after_password_change(optional)
Token included in Header
logout_after_password_change: Logout in all devices
-> response.status 200 -> change password
In settings.py
PASSWORD_CHANGED_EMAIL_CONFIRMATION
CREATE_SESSION_ON_LOGIN


### App Logics




