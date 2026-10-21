# 🛒 UniTrade (Uzmusika E-Commerce Platform)

> A modern, multi-university student marketplace and campus e-commerce platform built with Django.

UniTrade connects students, campus vendors, and university communities across Zimbabwe, enabling peer-to-peer commerce, student business promotion, textbook exchange, electronics trading, dorm essentials, and campus service delivery.

---

## 🔒 Security & Credential Hygiene (MUST READ)

> [!CAUTION]
> **Zero-Credential Exposure Policy**
> 
> **Never commit or push passwords, database credentials, API keys, private certificates, or secret tokens to GitHub or any public/shared repository.**
> 
> If sensitive credentials have ever been committed to Git history:
> 1. **Removing the secret from the latest commit is NOT enough** — Git preserves complete historical revisions in its commit tree.
> 2. **Immediately rotate and revoke** all exposed keys, app passwords, database logins, and API tokens.
> 3. Clean up the Git repository cache and history (see instructions below).

### Untracking Sensitive Files Already Committed

To remove tracked cache files, local databases, and secrets from Git without deleting them from your local disk:

```bash
# Untrack SQLite database
git rm --cached db.sqlite3

# Untrack Python cache directories
git rm -r --cached "**/__pycache__"

# Untrack user-uploaded media files
git rm -r --cached media/

# Commit the removal
git commit -m "fix(security): untrack local database, pycache, and runtime media"
```

---

## 🎓 Supported Institutions

UniTrade supports campus-specific filtering and cross-institution trade across leading Zimbabwean universities:

- 🏛️ **University of Zimbabwe (UZ)** — Harare
- 🔬 **National University of Science and Technology (NUST)** — Bulawayo
- 🎓 **Midlands State University (MSU)** — Gweru
- ⚙️ **Chinhoyi University of Technology (CUT)** — Chinhoyi
- 🌍 **Africa University (AU)** — Mutare
- 💻 **Harare Institute of Technology (HIT)** — Belvedere, Harare

---

## 🌟 Key Features

### 🛍️ Marketplace & Product Catalog
- **Multi-Category Catalog:** Textbooks 📚, Electronics 💻, Fashion 👟, Room & Living 🛏️, Services 🛠️, and Food & Snacks 🍱.
- **Condition Grading:** Clear item conditions (*New*, *Like new*, *Used*).
- **Institution Filtering:** Filter deals by specific university campus or browse nationwide student listings.
- **Product Search & Category Navigation:** Fast browsing by department, category, and keyword.

### 👥 Dual-Role Account System
- **Buyers:** Dedicated buyer dashboard, profile management, order history tracking, and instant checkout.
- **Vendors / Sellers:** Dedicated seller dashboard, inventory management (Add/Edit/Delete listings), order fulfillment, and revenue analytics.
- **Dual Mode:** Users can operate simultaneously as buyers and sellers on the same student account.

### 💳 Local Campus Checkout & Payments
- Tailored for Zimbabwean campus payment ecosystems:
  - 📱 **EcoCash**
  - 💳 **InnBucks**
  - 📲 **OneMoney**
  - 🏦 **ZIPIT / Bank Transfer**
  - 💵 **Cash on Campus** (hand-to-hand exchange at campus landmarks)
  - 💳 **Stripe** (integrated readiness for international card payments)

### 📦 Order Management & Analytics
- Unique alphanumeric order reference generation (e.g., `UT-A1B2C3D4`).
- Real-time order status tracking: `Pending` ➔ `Confirmed` ➔ `Completed` ➔ `Cancelled`.
- Vendor revenue summary displaying completed orders, total revenue in US$, and active listings.

### 🚀 Production & Cloud Ready
- **Vercel Deployable:** Configured with `vercel.json` and WSGI serverless runtime.
- **Static Assets:** Optimized with [WhiteNoise](http://whitenoise.evans.io/) and Django staticfiles collection.
- **Automated Build Script:** `build.sh` manages package installation, migrations, and static file collection.

---

## 📂 Project Architecture

```
Uzmusika_project1/
├── ECOMMERCE/                    # Django Project Configuration Root
│   ├── __init__.py
│   ├── asgi.py                   # ASGI interface for async servers
│   ├── settings.py               # Main Django settings (env-ready)
│   ├── urls.py                   # Global URL routing
│   └── wsgi.py                   # WSGI entrypoint for web servers & Vercel
│
├── Emarket/                      # Main Marketplace Application
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py      # Sample campus listings seeding command
│   ├── migrations/               # Database migrations history
│   ├── static/Emarket/           # App static assets (CSS, icons, images)
│   │   ├── images/               # PWA icons, favicons, campus hero
│   │   └── styles.css            # Custom UI stylesheet
│   ├── Templates/Emarket/        # Modular HTML templates
│   │   ├── includes/             # Partials (navbar, footer, sidebar, product_card)
│   │   ├── home.html             # Landing page with campus hero & deals
│   │   ├── buyer_dashboard.html  # Buyer order history and account overview
│   │   ├── vendor_dashboard.html # Seller management hub
│   │   └── ...
│   ├── admin.py                  # Django Admin models registration
│   ├── apps.py                   # App configuration
│   ├── context_processors.py     # Cart count context processor
│   ├── forms.py                  # User registration and product forms
│   ├── models.py                 # Profile, Product, Service, Order, OrderItem
│   ├── urls.py                   # Application route declarations
│   └── views.py                  # View controllers & business logic
│
├── build.sh                      # Deployment build script (migrations, collectstatic)
├── vercel.json                   # Vercel deployment specification
├── requirements.txt              # Production and development dependencies
├── .env.example                  # Environment configuration template
├── .gitignore                    # Git ignore file for secrets and build artifacts
├── manage.py                     # Django CLI management utility
└── README.md                     # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python**: Version `3.10` or higher (`3.11` / `3.12` recommended)
- **Git**: Installed on your system
- **Virtual Environment**: `venv` or `virtualenv`

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/Jo-sephkat/Uzmusika_project1.git
cd Uzmusika_project1
```

---

### Step 2: Set Up Virtual Environment

On Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4: Configure Environment Variables

1. Copy the sample environment template:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` in your text editor and fill in your configuration:
   - Generate a strong `DJANGO_SECRET_KEY`
   - Set `DJANGO_DEBUG=True` for local development (`False` in production)
   - Configure your email credentials or Google App Password for mail delivery

---

### Step 5: Run Database Migrations

Apply database schemas for users, profiles, products, and orders:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Step 6: Seed Sample Campus Marketplace Data

Populate the local database with realistic vendor profiles and sample student listings across all 6 universities:

```bash
python manage.py seed_data
```

---

### Step 7: Create a Superuser (Admin Access)

Create an administrative account to access the Django Admin Portal (`/admin/`):

```bash
python manage.py createsuperuser
```

---

### Step 8: Start the Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to:
👉 **http://127.0.0.1:8000/**

---

## 📊 Sample Demo Accounts (Seeded Data)

When you run `python manage.py seed_data`, the following test seller accounts are created with default password `pass1234`:

| Username | University | Store Name | Focus Category |
| :--- | :--- | :--- | :--- |
| `tariro_books` | University of Zimbabwe | Tariro's Book Nook | Textbooks & Tutoring |
| `campus_tech` | Harare Institute of Technology | CampusTech ZW | Laptops, Gadgets & Calculators |
| `sole_society` | Midlands State University | Sole Society | Student Fashion & Sneakers |
| `res_essentials`| NUST — Bulawayo | Res Room Essentials | Dorm Essentials & Food |

*(Remember to change or delete demo passwords before publishing to a live environment!)*

---

## ☁️ Deployment

### Deploying to Vercel

The project includes pre-configured [vercel.json](file:///c:/Users/User/uz_market/Uzmusika_project1/vercel.json) and [build.sh](file:///c:/Users/User/uz_market/Uzmusika_project1/build.sh):

1. Install the Vercel CLI or connect your GitHub repository to Vercel.
2. In the Vercel project dashboard, set your Environment Variables:
   - `DJANGO_SECRET_KEY`
   - `DJANGO_DEBUG = False`
   - `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`
   - Database connection string (PostgreSQL / Neon / Supabase recommended for serverless production)
3. Deploy:
   ```bash
   vercel --prod
   ```

---

## 🛡️ Best Security Practices for Contributors

1. **Keep `.env` out of Git:** Check `git status` before committing to verify `.env` is never staged.
2. **Review Diffs:** Always run `git diff --staged` before creating a commit.
3. **Use Secret Scanners:** Consider using tools such as `git-secrets`, `trufflehog`, or GitHub Secret Scanning.
4. **App Passwords for SMTP:** Never use your primary Google account password; always use a dedicated Google App Password and revoke it when no longer needed.

---

## 📄 License

This project is licensed for student and community marketplace use. Check with the repository owners for commercial licensing terms.
