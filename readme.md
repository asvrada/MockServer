# Mock Server

A light way mock server that acts as a backend API for providing dummy response.

> Still in very early developing stage. Nearly all features are under development. 
> 
> Any contribution is welcomed!

## Install

## Usage

```python
from MockServer import MockServer

server = MockServer()

# First, add routes
server.get("/", body={
    'content': "Hello World"
})

server.when("PUT", "/user", body={
    "content": "User Created"
})

# All API are listed under API section

# Second, run the server
# And you are good to go
server.run(port=8080)

```

### Run

### API

```
server.get/post/put/delete (
    1st arg: path

--- or ---

server.when (
    1st arg: method: one of get/post/put/delete, case insensitive
    2nd arg: path

--- and ---
    
    status_code=
    type= one of json/html, defaults to json
    body=
    header=
)
```

