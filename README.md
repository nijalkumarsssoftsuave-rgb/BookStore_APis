# 📚 BookStore API – Project Abstract

A backend system built using FastAPI and MongoDB for managing an online bookstore.

Implements JWT-based authentication to secure all protected endpoints.

Supports role-based access control with multiple user roles:

Admin – Full system management.

Author – Create and manage books.

Publisher – Publish approved books.

Reader/User – Browse books and submit reviews.

Provides complete book lifecycle management, including:

Book creation, updates, deletion, and publishing.

Category assignment and automatic category creation.

Enables user authentication and authorization:

User registration and login.

Secure token generation and validation.

Supports review and rating system:

Users can submit reviews and ratings.

Automatically calculates average rating and total reviews for each book.

Uses data enrichment to return related entities in API responses:

Author details, category information, publisher data, and review statistics.

Designed with asynchronous I/O for high performance and scalability.

Built using Pydantic models for request validation and response serialization.

Follows a modular service-based architecture for clean, maintainable code.

Demonstrates modern backend best practices:

Dependency Injection

Secure API design

Clean separation of routes, services, and models
