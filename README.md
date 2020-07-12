# Socialbook-api
A blog website made exclusively for BITS students.

# Getting and using an Auth token

To access the API endpoints, you will need an Auth token. Do the following to get one:

1) Go to (Google OAuth Playground)[https://developers.google.com/oauthplayground/].

2) In the first step, select Google OAuth2 API v2, select both user.email and user.profile. Login using BITS Mail when asked.

3) You will get a bunch of JSON data on the right side, copy the id_token from there.

4) Using this id_token, send a GET request to /user/register endpoint.

```
 curl --location --request POST '127.0.0.1:8000/user/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "id_token": <YOUR ID_TOKEN>
}' 
```
  
You will get a JSON response that is similar to this:
```
{
  "token": <token>,
  "username": <username>,
  "email": <email>
  } 
```   
5) Using this id_token, send a GET request to /user/login endpoint.

```
 curl --location --request POST '127.0.0.1:8000/user/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "id_token": <YOUR ID_TOKEN>
}' 
```
  
6) Copy the value of the token field & save it somewhere.[<LOGIN_TOKEN>]

7) Use this token in the Authorization header in all further requests.

``` Using Postman :```

```
In Headers:

Key = Authorization
Value = JWT <LOGIN_TOKEN>

```

``` Using Developer Browsing Tools :```

```
var myHeaders = new Headers();
myHeaders.append("Authorization", "JWT <LOGIN_TOKEN>");

var requestOptions = {
 method: 'GET',
 headers: myHeaders,
 redirect: 'follow'
};

fetch("127.0.0.1:8000/api/get_posts", requestOptions)
 .then(response => response.text())
 .then(result => console.log(result))
 .catch(error => console.log('error', error)); 
 ```
# Explanation of Models

Authenticated User(BITS mail)

1. An authenticated user can post & update blogs. It must be given the following attributes:
```
author
date_posted
title
content
```
2. An authenticated user can comment on blogs. It must be given the following attributes:
```
author
post
content
```
3. An authenticated user can report blogs written by other users & if a blog is reported by atleast 5 independent users, blog would be deleted. It must be given the following attributes:
```
author
date_posted
title
content
reported_by
```
4. User Model is just used for the Authentication(security reasons) , both Post & Comment models are related to Profile model.