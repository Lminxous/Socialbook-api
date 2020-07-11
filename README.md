# Socialbook-api
Blog website - REST API

# Getting and using an Auth token

To access the API endpoints, you will need an Auth token. Do the following to get one:

1) Go to (Google OAuth Playground)[https://developers.google.com/oauthplayground/].

2) In the first step, select Google OAuth2 API v2, select both user.email and user.profile. Login using BITS Mail when asked.

3) You will get a bunch of JSON data on the right side, copy the id_token from there.

4) Using this id_token, send a GET request to /auth/register endpoint.

```
 curl --location --request POST '127.0.0.1:8000/auth/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "id_token": <YOUR ID_TOKEN>
}' 
```

  
5) You will get a JSON response that is similar to this:
```
{
  "token": <token>,
  "username": <username>,
  "email": <email>
  } 
```   
  
6) Copy the value of the token field and save it somewhere.

7) Use this token in the Authorization header in all further requests.

```
var myHeaders = new Headers();
myHeaders.append("Authorization", "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6ImYyMDE5MDEyMCIsImV4cCI6MTU4NTI2Mjg4NCwiZW1haWwiOiJmMjAxOTAxMjBAcGlsYW5pLmJpdHMtcGlsYW5pLmFjLmluIn0.7WdcaO6mvlNEoFAz4ds7nvOWXLKJ5crDv3aPoj0F_YQ");

var requestOptions = {
 method: 'GET',
 headers: myHeaders,
 redirect: 'follow'
};

fetch("127.0.0.1:8000/api/get_listings", requestOptions)
 .then(response => response.text())
 .then(result => console.log(result))
 .catch(error => console.log('error', error)); 
 ```
