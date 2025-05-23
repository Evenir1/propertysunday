# Application Architecture: PropertySunday.com

## 1. Overview

PropertySunday.com will be a real estate listing platform designed to replicate core functionalities of Zillow, with specific integrations and features tailored for the South African market. The architecture will be modular to accommodate future growth and feature additions. A monolithic architecture with clearly defined modules is suitable for the initial MVP, with the potential to evolve into microservices for specific, high-load components (like API integration or search) if needed.

## 2. Architectural Layers

The application will be structured into the following logical layers:

*   **Presentation Layer (Frontend):** Responsible for the user interface and user experience. This layer will interact with the Application Layer via APIs.
*   **Application Layer (Backend):** Contains the core business logic, API endpoints, user authentication, and service integrations.
*   **Data Access Layer:** Manages interactions with the database and external data sources (property listing APIs).
*   **Infrastructure Layer:** Includes database, hosting, deployment, and monitoring services.

## 3. Technology Stack (Initial Proposal)

*   **Frontend:** Next.js (as suggested in the provided PDF "Property Sunday Code Base and colour pallette .pdf") with React, Tailwind CSS.
    *   *Reasoning:* Next.js offers server-side rendering (SSR) and static site generation (SSG) beneficial for SEO and performance. React provides a robust component-based UI library. Tailwind CSS allows for rapid UI development.
*   **Backend:** Python with Flask (as per knowledge base guidance for applications requiring backend/database functionality).
    *   *Reasoning:* Flask is a lightweight and flexible framework suitable for building REST APIs. Python has strong libraries for web scraping and API integrations if direct API access to property sites is limited or requires complex data transformation.
*   **Database:** PostgreSQL or MySQL (MySQL is mentioned with Flask in the knowledge base).
    *   *Reasoning:* Relational databases are well-suited for structured data like property listings, user accounts, and transactions. They offer robust querying capabilities and data integrity.
*   **API Integration Module:** A dedicated Python module (potentially using libraries like `requests` and `BeautifulSoup` if scraping is needed, or SDKs if available) to fetch and normalize data from PrivateProperty.com and Property24.com.

## 4. Key Modules and Components

### 4.1. Frontend (Next.js)

*   **UI Components:** Reusable React components for listings, search filters, maps, user profiles, forms, etc.
*   **Pages:**
    *   Homepage with search bar and featured listings.
    *   Search Results Page with filters, map view, and list view.
    *   Property Details Page.
    *   User Account Pages (Dashboard, My Listings, Saved Searches, Profile Settings).
    *   Listing Submission Form (for manual input).
    *   Static Pages (About Us, Contact, Terms, etc.).
*   **State Management:** React Context API or a library like Zustand/Redux for managing global UI state.
*   **API Client:** To communicate with the backend Flask APIs.

### 4.2. Backend (Flask)

*   **API Endpoints (RESTful):**
    *   `/listings`: GET (search, filter, list), POST (create new manual listing), PUT (update listing), DELETE (remove listing).
    *   `/users`: POST (register), POST (login), GET (profile), PUT (update profile).
    *   `/auth`: Token generation, validation.
    *   `/payments`: Integration with a payment gateway (e.g., PayFast as mentioned in PDF) for charged listings.
    *   `/ads`: Endpoints for managing and displaying advertisements.
    *   `/external-listings`: Endpoints to trigger and manage data fetching from external property portals.
*   **User Authentication & Authorization:** JWT (JSON Web Tokens) for stateless authentication. Role-based access control (e.g., regular user, agent, admin).
*   **Business Logic:**
    *   Search and filtering logic.
    *   User account management.
    *   Listing management (including validation for manual inputs).
    *   Payment processing for charged listings.
    *   Advertisement management logic.
*   **Database Models (SQLAlchemy ORM):**
    *   `User`: Stores user information (id, name, email, password_hash, roles, etc.).
    *   `Listing`: Stores property details (id, title, description, price, location, bedrooms, bathrooms, images, user_id (owner), source (e.g., manual, property24), status (e.g., active, pending, sold), is_charged_listing).
    *   `SavedSearch`: Stores user-saved search criteria.
    *   `FavoriteListing`: Links users to their favorited listings.
    *   `Advertisement`: Stores ad content, targeting criteria, display duration.
    *   `PaymentTransaction`: Records payment details for charged listings/ads.

### 4.3. Data Access Layer & API Integration

*   **Database Interaction:** SQLAlchemy to interact with the chosen relational database (PostgreSQL/MySQL).
*   **External API Integration Module (Python):**
    *   **Connectors:** Specific functions/classes to connect to PrivateProperty.com and Property24.com. This will require investigation into their available APIs. If official APIs are not available or are restrictive, web scraping techniques might be necessary (though less reliable and potentially against terms of service – this needs to be confirmed).
    *   **Data Fetching:** Scheduled tasks (e.g., using Celery with Redis/RabbitMQ as a message broker, or a simpler cron job for an MVP) to periodically pull new listings.
    *   **Data Normalization:** Transforming data from different sources into a consistent format for the `Listing` model.
    *   **Duplicate Handling:** Logic to identify and manage duplicate listings from different sources or manual inputs.
*   **Manual Input:** A form in the frontend will send data to a backend API endpoint which will then create a new `Listing` record with `source` set to "manual".

## 5. Data Flow Examples

### 5.1. User Property Search

1.  User enters search criteria on the Next.js frontend.
2.  Frontend sends a GET request to `/listings` on the Flask backend with search parameters.
3.  Backend queries the database (Listings table) based on filters.
4.  Backend returns a JSON response with matching listings.
5.  Frontend displays the listings.

### 5.2. External Listing Ingestion

1.  A scheduled task (e.g., Celery beat) triggers the API Integration Module.
2.  The module fetches new/updated listings from PrivateProperty.com and Property24.com APIs (or via scraping).
3.  Data is normalized and checked for duplicates.
4.  New/updated listings are saved to the `Listing` table in the database with appropriate `source`.

### 5.3. User Account Creation & Listing Submission

1.  User registers/logs in via the Next.js frontend, interacting with `/users` and `/auth` backend endpoints.
2.  User navigates to the "Submit Listing" form.
3.  User fills in property details and submits.
4.  Frontend sends a POST request to `/listings` with listing data and user's auth token.
5.  Backend validates data, creates a new `Listing` record associated with the user, and sets `source` to "manual".
6.  If it's a charged listing, the user is redirected to a payment flow (integrated with PayFast).

## 6. Monetization Strategy Implementation

*   **Charged Listings:**
    *   `Listing` model will have a boolean field `is_charged_listing` and potentially `listing_tier`.
    *   Integration with a payment gateway (e.g., PayFast).
    *   Listings marked as charged will have higher visibility or special badges.
*   **Advertising:**
    *   `Advertisement` model to store ad details.
    *   Admin interface to manage ad campaigns.
    *   Logic in the backend to select and serve ads based on page context or user data (if applicable and compliant with privacy).
    *   Dedicated ad slots in the frontend UI.

## 7. Design & UX Considerations

*   **Zillow-inspired UX:** The general layout, search functionality, and map views will draw inspiration from Zillow.
*   **Differential Aspects:** Introduce unique UI elements or workflows to differentiate from Zillow, possibly focusing on the South African context or the specific color palette (Terracotta Red, Sand Beige, Olive Green) and typography (Playfair Display, Open Sans) provided.
*   **Mobile-first Responsive Design:** Ensure the platform is fully usable and looks good on all device sizes.

## 8. Deployment

*   **Frontend (Next.js):** Vercel, Netlify, or AWS Amplify.
*   **Backend (Flask):** Docker containers deployed on services like AWS ECS, Google Cloud Run, or Heroku. A virtual private server (VPS) could also be used for an MVP.
*   **Database:** Managed database service (e.g., AWS RDS, Google Cloud SQL) or self-hosted on a VPS.
*   **Scheduled Tasks (Celery):** Requires a worker service and a message broker (Redis/RabbitMQ).

## 9. Future Considerations

*   **Advanced Search Filters:** More granular filtering options.
*   **Agent Profiles & Directory:** Features for real estate agents.
*   **Mortgage Calculator:** As seen on Zillow.
*   **Property Value Estimates:** If data and algorithms become available.
*   **Real-time Notifications:** For new listings matching saved searches.
*   **Scaling:** If traffic grows, consider migrating parts of the backend to microservices and using a more scalable database solution.

This architecture provides a solid foundation for building PropertySunday.com, addressing the core requirements while allowing for future expansion.
