# Discovery Document

## AFC Restaurant Management System

Version: 1.0

---

# Executive Summary

AFC – Absolutely Fried Chicken is a growing Quick Service Restaurant chain with six operational branches and an ambitious plan to expand through franchising. The organization currently lacks an integrated Point of Sale (POS) and Restaurant Management System, relying on manual processes for billing, inventory, and reporting.

This project aims to develop a centralized, cloud-based Restaurant Management System that will streamline restaurant operations, improve efficiency, and provide a scalable platform for future franchise growth.

---

# Business Objectives

The primary business objectives are:

- Digitize restaurant operations.
- Centralize management across all branches.
- Improve billing efficiency.
- Reduce inventory wastage.
- Provide real-time business reporting.
- Standardize workflows.
- Prepare the business for franchise expansion.

---

# Existing Business Process

Current operations are largely manual.

Orders are taken by staff and processed without a dedicated POS.

Bills are generated manually.

Inventory is tracked separately by each branch using Excel or notebooks.

Management receives sales information manually.

This creates delays, inconsistencies, and limited business visibility.

---

# Business Pain Points

## Billing

- Slow billing during peak hours.
- Manual bill preparation.
- Difficult to track payment history.

## Inventory

- No real-time stock visibility.
- High wastage.
- Manual stock updates.
- No automated stock alerts.

## Reports

- Reports require manual preparation.
- No real-time dashboards.
- Difficult to compare branch performance.

## Branch Management

- No centralized control.
- Difficult to monitor operations remotely.
- Inconsistent reporting across branches.

---

# Proposed Solution

Develop a cloud-based Restaurant Management Platform consisting of:

## Core Modules

- Authentication
- Multi-Branch Management
- Restaurant Configuration
- Menu Management
- Category Management
- POS Billing
- Table Management
- Kitchen Order Ticket (KOT)
- Inventory Management
- Vendor Management
- Customer Management
- Reports Dashboard
- Role-Based Access Control

---

# Users

## Owner

Responsibilities

- View reports
- Monitor branches
- Configure system
- Manage franchise operations

---

## Branch Manager

Responsibilities

- Monitor branch
- Manage staff
- View reports
- Manage inventory

---

## Cashier

Responsibilities

- Billing
- Payments
- Customer management

---

## Kitchen Staff

Responsibilities

- Receive KOT
- Update order status

---

## Inventory Manager

Responsibilities

- Purchase management
- Stock management
- Vendor management

---

# Functional Scope (MVP)

Included

✔ Authentication

✔ Multi-Branch

✔ Menu

✔ Categories

✔ Tables

✔ POS

✔ KOT

✔ Inventory

✔ Customers

✔ Reports

✔ Dashboard

✔ Role Management

Excluded

- Customer Mobile App
- Online Ordering
- Loyalty Program
- Coupons
- Delivery Tracking
- Accounting Integration
- Franchise Billing
- AI Analytics

---

# Assumptions

- All branches use a standardized menu.
- Internet connectivity is available at each branch.
- Data will be stored centrally.
- Users will access the system through role-based permissions.
- Inventory is managed independently by each branch.

---

# Risks

- Different branches may have slight workflow differences.
- Staff training will be required.
- Future franchise requirements may introduce additional complexity.
- Inventory processes may evolve over time.

---

# Future Vision

The system should evolve into a SaaS platform capable of serving:

- AFC-owned branches
- Franchise branches
- Multiple restaurant brands
- Centralized franchise management

The architecture should therefore support multi-tenancy and horizontal scalability from the outset.

---

# Success Metrics

The project will be considered successful when:

- Billing time is reduced by at least 50%.
- Inventory is tracked accurately in real time.
- Management can monitor all branches through a centralized dashboard.
- Reports are generated automatically.
- New branches can be onboarded with minimal configuration.
- The platform is ready to support franchise expansion.

---

# Recommended Next Step

Proceed to the Product Requirements Document (PRD), where each business objective and functional area will be translated into detailed product requirements, user journeys, acceptance criteria, and MVP planning.
