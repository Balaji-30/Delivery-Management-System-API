# Shippin: Full-Stack Delivery Management Platform

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-4E85A9?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

A modern, scalable delivery management system connecting sellers with delivery partners, featuring automated notifications and real-time shipment tracking.

## 🚀 Live Demo & API

This project is fully deployed and live on the web:

- **Frontend (Vercel):** [**https://shippin.vercel.app**](https://shippin.vercel.app)
- **Backend API (Render):** [**https://shippin-backend-qzwz.onrender.com**](https://shippin-backend-qzwz.onrender.com)
- **API Documentation (Swagger):** [**https://shippin-backend-qzwz.onrender.com/docs**](https://shippin-backend-qzwz.onrender.com/docs)

> **Note on Performance (Cold Starts)**
> This project is hosted on Render's free tier. The backend service will "spin down" after 15 minutes of inactivity. As a result, the **first request may take up to 2 minutes** while the server restarts. Subsequent requests will be fast.

---

## 🎯 Problem Statement

In the modern "gig economy" and e-commerce landscape, logistics is no longer a simple A-to-B process. It's a complex, multi-sided marketplace between sellers, independent delivery partners, and end-customers. This creates significant data and communication silos:

- **Data Fragmentation:** Sellers use one system (e.g., spreadsheets) to manage orders, while delivery partners use another (e.g., text messages, gig-work apps), and customers are left with a static "your order has shipped" email. There is no single source of truth.
- **Inefficient Coordination:** Assigning a shipment is a high-friction, manual process that relies on phone calls or texts, leading to wasted partner capacity and delays for the seller.
- **Poor Stakeholder Experience:** The lack of a unified, event-driven notification system results in a poor experience for all parties. Customers overwhelm sellers with support requests, and partners are burdened with "check-in" calls, distracting them from driving.

## ✨ Solution

Shippin solves this by acting as a lightweight, centralized **Logistics-as-a-Service (LaaS)** platform. It provides a single, unified interface that coordinates all three parties in real-time.

- **Multi-Role Authentication:** Secure JWT-based portals for **Sellers** to create shipments and **Delivery Partners** to manage assigned orders.
- **Shipment Management:** Full CRUD (Create, Read, Update, Delete) functionality for shipments, which serve as the core resource.
- **Automated Notifications:** Asynchronous, event-driven alerts using **Resend** (for email verification, password resets) and **Twilio** (for SMS alerts) ensure all stakeholders are updated instantly and automatically.
- **Real-Time Tracking:** A public-facing tracking page (rendered server-side by FastAPI with Jinja2) provides customers with live status updates.
- **Delivery Verification:** (e.g., OTP-based confirmation).

---

## 🛠️ Architecture & Tech Stack

This project is built as a decoupled, cloud-native application.

### Frontend (`/frontend`)

- **Framework:** React (with React Router v7)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **API Client:** `swagger-typescript-api` (Auto-generated client)
- **Deployment:** Vercel

### Backend (`/backend`)

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (with SQLAlchemy and Alembic for migrations)
- **Async Tasks:** FastAPI `BackgroundTasks`
- **Email Service:** **Resend** (via HTTP API)
- **SMS Service:** **Twilio**
- **Authentication:** `passlib`[bcrypt] for hashing, JWT for sessions
- **Deployment:** Docker container hosted on Render