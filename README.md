# JYOTICREATIONS - Django B2B Marketplace

A robust Django-based B2B (Business-to-Business) textile and saree marketplace. This project serves as a comprehensive platform for manufacturers and suppliers to showcase their products, manage catalog, and connect with wholesale buyers.

## 🚀 Features

- **Multi-Tenant / Brand Support**: Manage multiple brands/publishers with isolated content.
- **Advanced Catalog Management**:
  - **Categories & Sub-categories**: Hierarchical organization of products.
  - **Product Variants**: Support for multiple colors and sizes per product.
  - **Image Galleries**: Advanced image handling with placeholders and gallery support.
- **Homepage Customization**:
  - **WYSIWYG Editor**: Rich text editing for all homepage sections.
  - **Sortable Content**: Drag-and-drop reordering for Editorial, Why Choose, Metrics, and Countries sections.
  - **Dynamic Content Loading**: All homepage sections (Hero, Heritage, Editorial, etc.) are loaded dynamically from the database.
- **B2B Focus**:
  - **Enquiry Forms**: Dedicated forms for wholesale and B2B leads.
  - **Request-A-Quote**: Users can request quotes for specific products.
- **Advanced Filtering**: Filter products by category, collection (Best Sellers, New Arrivals, Handcrafted, etc.), material, and more.
- **SEO Optimized**: Ready for search engine optimization with proper metadata handling.

## 🛠️ Tech Stack

- **Core Framework**: Django 5.2
- **Frontend**: HTML5, CSS3 (Custom properties, Glassmorphism effects)
- **Icons**: Remix Icon
- **Fonts**: Outfit, Cormorant Garamond

## 📂 Project Structure

```
JyotiCreationProj/
├── core/                  # Core application (Models, Views, API)
├── theme_app/             # Theme-specific application (Templates, Static)
│   ├── static/            # CSS, JS, Images
│   └── templates/         # HTML Templates
└── jyoti_saree_proj/      # Project Settings & URL configuration
```

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd themesaree/JyotiCreationProj
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Seed the database (Optional - to populate initial categories, products, and homepage content)**
   ```bash
   python manage.py seed_data
   ```

6. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

Access the site at `http://localhost:8000`.
Access the admin panel at `http://localhost:8000/admin`.

## 📊 Admin Panel Overview

The Django admin panel (`/admin`) provides extensive management capabilities:

### Brands
- Manage parent brands and their relationships.

### Content Management
- **Homepage**: Configure Hero Section, Heritage, Editorial Sections, Why Choose Us, Process Steps, Metrics, Countries, Testimonials, and FAQs.
- **Pages**: Create and edit custom pages.
- **Settings**: Global application settings and social media links.

### Catalog Management
- **Categories & Sub-categories**: Add and organize product categories.
- **Products**: Manage detailed product listings including:
  - Product specifications (Weave, Work, Color, Material, etc.)
  - Pricing and inventory
  - Image management with placeholders and galleries
  - SEO metadata
  - Premium/Collection tags

### Leads & Forms
- **B2B Enquiries**: View and manage all incoming business enquiries.
- **Quote Requests**: Track and manage quote requests from customers.

## 📝 Database Schema (Core Models)

- **Brand**: Represents the manufacturing brand.
- **Product**: Core product model with attributes like `name`, `description`, `price`, `material`, `work_type`, etc.
- **ProductImage**: Handles multiple images per product.
- **HeroSection**, **EditorialSection**, **WhyChooseUsCard**, etc.: Models for managing homepage content blocks.
- **B2BEnquiry**: Model for capturing business leads.
- **GlobalSetting**: Application-wide settings.

## 📧 Email Configuration

The project includes basic email configuration in `settings.py`. For production, ensure you configure SMTP settings:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'your-email@example.com'
SERVER_EMAIL = 'your-email@example.com'
```

## 🤝 Contributing

1. Create a feature branch for your changes.
2. Follow the existing code style and naming conventions.
3. Ensure all new models have proper docstrings and type hints.
4. Run `python manage.py makemigrations` if you modify models.
5. Run `python manage.py test` to ensure no regressions.

## 🔐 Security

- Use `python manage.py check` regularly to identify security issues.
- Never expose secrets (DB passwords, API keys) in the codebase. Use environment variables.
- Keep your dependencies updated: `pip install --upgrade django`
