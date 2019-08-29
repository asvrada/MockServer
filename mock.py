from MockServer import MockServer

server = MockServer()

# usage
server.get("/", body={
    'content': "Hello World"
})

server.post("/user", body={
    "content": "User Created"
})

server.get("/api", body={
    "entry": ["user", "admin"]
})

server.when("DELETE", "/delete")

server.run(port=8080)
