# API Endpoints Documentation

## Authentication
POST /login
- Required fields: username, password
- Default: admin / admin123

## Floor Management
GET /floors - Get all floors
GET /floors/<id> - Get specific floor
POST /floors - Create floor (level, name)
PUT /floors/<id> - Update floor (level, name)
DELETE /floors/<id> - Delete floor

## Room Management
GET /rooms - Get all rooms
GET /rooms/<id> - Get specific room
POST /rooms - Create room (capacity, number, floor)
PUT /rooms/<id> - Update room (capacity, number, floor)
DELETE /rooms/<id> - Delete room
Note: Room number must start with floor level

## Resident Management
GET /residents - Get all residents
GET /residents/<id> - Get specific resident
POST /residents - Create resident (firstname, lastname, age, room)
PUT /residents/<id> - Update resident (firstname, lastname, age, room)
DELETE /residents/<id> - Delete resident
