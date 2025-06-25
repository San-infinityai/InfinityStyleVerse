# InfinityStyleVerse — AI Infrastructure for the Global Fashion Industry

## 🌍 Project Vision

InfinityStyleVerse is not just a website or platform — it is the world’s **first self-evolving AI operating system** designed to support the entire global apparel ecosystem. Inspired by the scalability of AWS and the intelligence of modern AI, InfinityStyleVerse aims to become the universal digital backbone of fashion, supporting:

- Designers
- Factories & Manufacturers
- Retailers & Brands
- Shoppers (B2C)
- Influencers & Creators
- Governments & NGOs

## 🚀 Core Systems

The platform is built around 8 intelligent core systems:

1. **MetaDesign System** – Moodboard-to-collection, trend prediction, pattern generation.
2. **Manufacturing System** – Ethical sourcing, demand forecasting, vendor matching.
3. **Retail & Sales System** – AI pricing, AR storefronts, bundle optimization.
4. **Personalization Engine** – Mood/intent-aware shopping, AR try-ons, smart stylist.
5. **Creator/Brand System** – AI capsule collections, licensing, royalties.
6. **Sustainability System** – ESG dashboards, circular economy tracking.
7. **Global Infrastructure** – Cross-border logistics, language, sizing, and compliance.
8. **Executive Intelligence** – Forecasting, BI dashboards, compliance, governance.

---

#  API Documentation
This section provides a comprehensive overview of all available API endpoints used in the InfinityStyleVerse platform. Each route is documented with:

URL and HTTP method

Expected input format (JSON, form-data, etc.)

Sample request and response

Error messages and status codes

These endpoints power core functionalities like user registration, authentication, product management, recommendations, feedback collection, and admin operations. All protected routes require a valid JWT access_token in the request header.

Base URL: http://127.0.0.1:5000/

Authentication Routes
1. Register User
Endpoint: POST /auth/register

Request Body (JSON):
{
"name": "admin",
"email": "admin@example.com",
"password": "admin",
"role": "admin"
}

Success Response:
Status: 201 Created
{
"msg": "User registered successfully"
}

Error Responses:

If email already exists:
{
"msg": "Email already registered"
}

If required fields are missing:
{
"msg": "Missing required fields"
}

2. Login User
Endpoint: POST /auth/login

Request Body (JSON):
{
"email": "admin@example.com",
"password": "admin"
}

Success Response:
Status: 200 OK
{
"access_token": "<jwt_token_here>",
"user": {
"id": 6,
"email": "admin@example.com",
"name": "admin",
"role": "admin",
"last_login": "2025-06-25 17:48:27",
"status": "Active"
}
}

Error Response:

Wrong email or password:
{
"msg": "Bad email or password"
}

Product Routes
Note: For POST and PUT requests that require images, use form-data in Postman.

1. Add Product
Endpoint: POST /product

Headers:
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

Form-data Fields:

product_name (string, required)

brand (string, optional)

category (string, required)

description (string, required)

sale_price (number, optional)

discount (number, optional)

size (string, optional, comma separated)

color (string, optional, comma separated)

tag (string, optional, comma separated)

visibility (string, optional, default "Published")

schedule_date (string, optional, format YYYY-MM-DD)

product_images[] (file, required, minimum 4 images)

Success Response:
Status: 201 Created
{
"msg": "Product uploaded successfully",
"product": {
"id": 1,
"title": "Product Name",
...
}
}

Error Responses:

Missing required fields:
{
"error": "Missing required fields"
}

Less than 4 images:
{
"error": "At least 4 images are required"
}

Invalid image file:
{
"error": "Invalid image file"
}

2. Update Product
Endpoint: PUT /product/{product_id}

Headers:
Authorization: Bearer <access_token>
Content-Type: application/json

Request Body (JSON):
{
"title": "Updated Shirt",
"brand": "Adidas",
"category": "Clothing",
"description": "Limited edition cotton shirt",
"sale_price": 4500,
"discount": 5,
"sizes": ["S", "M"],
"colors": ["Blue", "White"],
"tags": ["limited", "trending"],
"image_url": "/static/uploads/shirt1.jpg",
"image_gallery": ["/static/uploads/shirt2.jpg", "/static/uploads/shirt3.jpg"],
"visibility": "Published",
"publish_date": "2025-07-01",
"esg_score": 4.2,
"likes": 0,
"views": 0
}

Success Response:
Status: 200 OK
{
"msg": "Product updated successfully",
"product": {
"id": 1,
"title": "Updated Shirt",
...
}
}

Error Response:

Product not found:
{
"error": "Product not found"
}

3. Delete Product
Endpoint: DELETE /product/{product_id}

Headers:
Authorization: Bearer <access_token>

Success Response:
Status: 200 OK
{
"msg": "Product with id 1 deleted successfully"
}

Error Response:

Product not found:
{
"error": "Product not found"
}

4. Get Products (Paginated)
Endpoint: GET /product

Query Parameters:

limit (integer, optional, default 10)

offset (integer, optional, default 0)

Success Response:
Status: 200 OK
{
"limit": 10,
"offset": 0,
"products": [
{
"id": 2,
"title": "jhj",
"brand": "ss",
"category": "clothing",
"description": "ss",
"sale_price": 122.0,
"discount": 12.0,
"sizes": ["M"],
"colors": ["rgb(2", " 97", " 50)"],
"tags": ["11"],
"image_url": "/static/uploads/download_8.jpg",
"image_gallery": [
"/static/uploads/download_7.jpg",
"/static/uploads/download_6.jpg",
"/static/uploads/download_5.jpg"
],
"visibility": "published",
"publish_date": "2025-06-25",
"esg_score": 0.0,
"likes": 0,
"views": 0
}
]
}

Error Response:

Invalid limit or offset:
{
"error": "Invalid limit or offset"
}

Recommendation Route
Get Recommended Products by Product ID
Endpoint: GET /api/recommend/{product_id}

Headers:
Authorization: Bearer <access_token>

Success Response:
Status: 200 OK
{
"similar": [
{
"product_id": "1",
"title": "empire midi dress",
"score": 0.5186,
"image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1hIW9STeP6RSOYt8bVC8kVwo8Nlq03-eBKQ&s"
},
...
]
}

Error Responses:

Product ID not found:
{
"error": "Product ID {product_id} not found"
}

Internal server error:
{
"error": "Internal server error"
}

Feedback Route
Submit Feedback
Endpoint: POST /feedback

Headers:
Authorization: Bearer <access_token>
Content-Type: application/json

Request Body (JSON):
{
"message": "That's a fantastic product",
"rating": 5
}

Success Response:
Status: 201 Created
{
"message": "Feedback submitted successfully"
}

Error Responses:

Missing message or user_id:
{
"error": "Message and user_id are required"
}

No input data provided:
{
"error": "No input data provided"
}

Internal server error:
{
"error": "Internal server error"
}

Admin Routes
1. Get All Users
Endpoint: GET /admin/users

Success Response:
Status: 200 OK
[
{
"id": 2,
"email": "creator@example.com",
"role": "Creator",
"status": "Active"
},
{
"id": 3,
"email": "customer@example.com",
"role": "Customer",
"status": "Inactive"
}
]

2. Update User
Endpoint: PUT /admin/users/{user_id}

Headers:
Content-Type: application/json

Request Body (JSON):
{
"email": "newemail@example.com",
"role": "admin"
}

Success Response:
Status: 200 OK
{
"msg": "User updated successfully"
}

Error Response:

User not found:
{
"msg": "User not found"
}

3. Delete User
Endpoint: DELETE /admin/users/{user_id}

Success Response:
Status: 200 OK
{
"msg": "User deleted successfully"
}

Error Response:

User not found:
{
"msg": "User not found"
}

Notes
All endpoints requiring authentication expect a valid JWT token passed via the Authorization header as:
Authorization: Bearer <token>

Date formats (e.g. publish_date) should be in YYYY-MM-DD.

For file uploads in /product POST route, use multipart/form-data.

Ensure to provide at least 4 images when adding a product.

Status fields (user status) are computed based on last login timestamp.

