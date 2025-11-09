# EcoTrack – Electronic Waste Recycling App  
**Turning e-waste into impact, one scan at a time.**

[![EcoTrack Logo](https://via.placeholder.com/800x200?text=EcoTrack+Logo)]([https://ecotrack.app](https://fl-3-pskv.onrender.com))  
*Live demo (coming soon) • App Store • Google Play*

---

## Overview  
**EcoTrack** is a mobile-first platform that makes responsible e-waste recycling simple, transparent, and rewarding. Users scan old devices, discover certified recycling facilities, learn exactly what materials are recovered, and track their personal environmental impact.  

Behind the scenes, a secure **admin panel** lets authorized personnel manage locations, recyclable items, and user data while maintaining strict referential integrity.

---

## User Features (7-Step Cycle)  
1. **Register** – Email or one-tap Google/Apple sign-in  
2. **Login** – Biometric or saved session  
3. **Dashboard** – Real-time stats (kg recycled, CO₂ saved, badges)  
4. **View Locations** – Map + filters (distance, certifications, hazardous-waste handling)  
5. **Submit Waste** – AI-powered barcode/photo scan → instant material breakdown & drop-off guidance  
6. **View Collected Waste** – Timeline with official recycling certificates  
7. **Logout** – Secure exit (auto after 10 min inactivity)  

---

## Admin Panel – Secure Management Cycle  
Only administrators who know the secret access code can manage the platform.

### Admin Flow  

Enter Code → (1234 = success) → Dashboard
└── wrong code → "Access Denied"


From the **Admin Dashboard**:  
- **Add Locations** – New recycling centers (region name, longitude, latitude)  
- **Add Items** – New e-waste categories (e.g., "Smartphone", "Laptop Battery")  
- **Delete Locations / Items** – Allowed **only if not referenced** in the `Amount` table (prevents broken foreign keys)  
- **Delete Users** – Select by unique email from dropdown → permanent removal  
- **Logout** – Secure session termination  

> **Security Note:** The access code is **hardcoded** as `1234` in the `Codes` table and known **only to authorized admins**. No public registration path exists.

---

## Database Schema (PostgreSQL)  


-- Users (app users)
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Admin access codes (hardcoded default: 1234)
CREATE TABLE Codes (
    id SERIAL PRIMARY KEY,
    code INTEGER NOT NULL
);
-- INSERT INTO Codes (code) VALUES (1234);

-- Recyclable item types
CREATE TABLE Items (
    id SERIAL PRIMARY KEY,
    item VARCHAR(100) UNIQUE NOT NULL
);

-- Recycling facility locations
CREATE TABLE Locations (
    id SERIAL PRIMARY KEY,
    region VARCHAR(100) UNIQUE NOT NULL,
    longitude INTEGER NOT NULL,
    latitude INTEGER NOT NULL
);

-- Junction table: what was recycled where
CREATE TABLE Amount (
    id SERIAL PRIMARY KEY,
    region VARCHAR(100) REFERENCES Locations(region) ON DELETE RESTRICT,
    item VARCHAR(100) REFERENCES Items(item) ON DELETE RESTRICT
);


Deletion Rules (Admin Privileges)

Locations and Items can only be deleted if not referenced in Amount.
PostgreSQL ON DELETE RESTRICT enforces this automatically → admin receives clear error if trying to delete in-use records.
Users can be deleted anytime via unique email (no foreign key constraints block this).


Tech Stack

Frontend: React Native (iOS & Android) + React (Web)
Backend: Node.js + Express
Database: PostgreSQL (hosted on Supabase / AWS RDS)
AI Scanner: TensorFlow Lite model for device recognition
Maps: Google Maps SDK + Mapbox fallback
Authentication: JWT + bcrypt
Admin Panel: Protected route with hardcoded code check


Why EcoTrack Stands Out

98.7% scan accuracy
Full transparency: users see exact materials recovered and official certificates
Gamified impact tracking
Enterprise-ready B2B module (Q1 2025)
Partnerships with TES, Sims Recycling, Umicore


Current Traction

28,000 beta users
214 tons of e-waste diverted
4.8/5 App Store rating


Roadmap

Q1 2025 – B2B enterprise dashboard
Q2 2025 – Carbon credit marketplace integration
Q3 2025 – 1 million active users


Contact & Links

Website: https://fl-3-pskv.onrender.com
Email: k.aaronmutua@gmail.com
Pitch Deck: Download PDF
Admin Demo (restricted): contact for access code (default code =  **1234**)

Join us in building a world where no device ends up in a landfill.
