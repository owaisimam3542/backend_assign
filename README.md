# Notification Management System

A full-stack notification management system built with **Django REST Framework** and **React/Vite**.

The system allows administrators to manage notification triggers and templates for **WhatsApp, Email, and Web Push** from a single dashboard.

---

## Live Application

### Frontend

https://backend-assign-rjsw.vercel.app/

### Backend API

https://backend-assign-2-nomi.onrender.com/

### Admin Panel

https://backend-assign-2-nomi.onrender.com/admin/

### GitHub Repository

https://github.com/owaisimam3542/backend_assign

---

## Features

- Admin authentication
- Notification trigger management
- Notification template management
- Enable/disable notification triggers
- Enable/disable individual notification templates
- WhatsApp notifications
- Email notifications
- Browser Web Push notifications
- Test notification functionality
- Dynamic template variables
- Notification delivery logs
- Automatic notifications based on application events
- PostgreSQL database
- REST APIs
- React admin dashboard
- Render backend deployment
- Vercel frontend deployment

---

# Notification Channels

The system supports three notification channels.

## Email

Email notifications are sent using the **Brevo Transactional Email API**.

## WhatsApp

WhatsApp notifications are sent using the **Meta WhatsApp Cloud API**.

## Web Push

Browser push notifications are handled using **OneSignal**.

---

# Notification Triggers

The system currently contains the following triggers.

## 1. User Login

Triggered when a user successfully logs into the application.

Supported channels:

- WhatsApp
- Email
- Web Push

## 2. Order Placed

Triggered when an authenticated user successfully creates an order.

Supported channels:

- WhatsApp
- Email
- Web Push

## 3. Inactive for 1 Day

Triggered for users who have not been active for one day.

Supported channels:

- WhatsApp
- Email
- Web Push

The inactive-user notification logic is implemented using a Django management command.

---

# Admin Dashboard

The admin dashboard provides a single interface for managing notification triggers and templates.

Administrators can:

- Create triggers
- Edit triggers
- Enable/disable triggers
- Create notification templates
- Edit notification templates
- Enable/disable templates
- Configure WhatsApp templates
- Configure Email templates
- Configure Web Push templates
- Test notification templates

Each trigger can have a separate template for each notification channel.

---

# Template Variables

Notification templates support dynamic user variables.

Example:

```text
Hello {{user_name}}, welcome to our application!
