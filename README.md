# Reducto server

---
## Routes
|Request|Path|Request| Response| Comment|
|---|---|---|---|---|---|
|GET| `/`| `tbc`|`code: 200`|N/A|
|GET| `/login`| `tbc`|`code: 200`|N/A|
|POST| `/login`| `{ "username": [username], "password": [password] }`| `{ "bearer token": "Bearer [token]"}, code: 200`| N/A|
|GET| `/register`| `tbc` | `code: 200`|N/A|
|POST| `/register`| `{ "username": [username], "password": [password], "business_name": [business_name] }` | `{ "bearer token": "Bearer [token]"}, code: 200`| N/A|
