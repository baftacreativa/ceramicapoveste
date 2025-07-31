# Artisan Ceramics Website

## Overview

This is a Flask-based e-commerce website for showcasing and selling handmade ceramic products. The application features a clean, artisanal design with product catalogs, detailed product pages, contact forms, and multimedia content integration. The site emphasizes the handcrafted nature of ceramic art with AI-generated visual content to enhance the user experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite (default) or PostgreSQL (production)
- **Session Management**: Flask's built-in session handling with secret key
- **Middleware**: ProxyFix for handling reverse proxy headers

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Playfair Display, Open Sans)
- **JavaScript**: Vanilla JavaScript with Bootstrap components

### Database Schema
- **Product Model**: Core product information including name, description, price, category, multimedia URLs, and AI generation sources
- **Contact Model**: Contact form submissions with name, email, subject, and message

## Key Components

### Models (models.py)
- **Product**: Main product entity with support for images, videos, and audio content from AI sources
- **Contact**: Contact form submissions storage
- **Sample Data Initialization**: Automated sample product creation for development

### Routes (routes.py)
- **Home Page** (`/`): Featured and latest products display
- **Products Page** (`/products`): Product catalog with search and category filtering
- **Product Detail** (`/product/<id>`): Individual product pages with related products
- **About Page** (`/about`): Company story and artisan information
- **Contact Page** (`/contact`): Contact form handling

### Templates
- **Base Template**: Common layout with navigation, search, and footer
- **Product Pages**: Product grid and detail views with multimedia support
- **Static Pages**: About and contact pages with responsive design

### Static Assets
- **Custom CSS**: Earthy color palette reflecting ceramic art aesthetic
- **JavaScript**: Interactive features, smooth scrolling, and form enhancements

## Data Flow

1. **Product Display**: Products are fetched from database and rendered with AI-generated media
2. **Search & Filter**: Query parameters filter products by category and search terms
3. **Contact Forms**: Form submissions are validated and stored in the database
4. **Media Attribution**: All AI-generated content is properly attributed to its source

## External Dependencies

### AI Content Sources
- **Leonardo AI**: Primary source for product and artisan images
- **Synthesia**: Video content generation (referenced but not implemented)
- **AIVA**: Audio content generation (referenced but not implemented)

### CDN Resources
- **Bootstrap 5.3.0**: UI framework and components
- **Font Awesome 6.4.0**: Icon library
- **Google Fonts**: Typography (Playfair Display, Open Sans)

### Image Hosting
- **Pixabay**: Stock photography hosting for product images

## Deployment Strategy

### Environment Configuration
- **Development**: SQLite database with debug mode enabled
- **Production**: PostgreSQL database with environment-based configuration
- **Session Security**: Environment-based secret key management

### Database Management
- **Auto-initialization**: Database tables created automatically on startup
- **Sample Data**: Development database populated with sample ceramic products
- **Connection Pooling**: Configured for production reliability

### Server Configuration
- **WSGI Application**: Flask app with ProxyFix middleware
- **Host Configuration**: Configured for both local development and production deployment
- **Logging**: Debug-level logging enabled for development

The application is designed to be easily deployable on various platforms with minimal configuration changes, using environment variables for database URLs and security keys.