# प्रांतीय युवा प्रकोष्ठ उत्तर प्रदेश - Replit Guide

## Overview

This is a Django-based web application for **प्रांतीय युवा प्रकोष्ठ उत्तर प्रदेश** (Provincial Youth Cell - Uttar Pradesh), a youth empowerment organization. The website provides news, events, contact forms, and registration capabilities with a modern, bilingual (Hindi/English) interface.

## System Architecture

### Backend Architecture
- **Framework**: Django 5.1+ with Python
- **Template Engine**: Django Templates with Jinja2-like syntax
- **Rich Text Editor**: CKEditor with file upload support
- **Form Handling**: Django Forms with Crispy Forms for enhanced styling
- **File Handling**: Pillow for image processing
- **PDF Generation**: ReportLab for ID card generation
- **QR Code**: qrcode library for registration verification

### Frontend Architecture
- **CSS Framework**: Bootstrap 5.3+ with custom theming
- **Icons**: Bootstrap Icons + Font Awesome 6.5+
- **Animations**: AOS (Animate On Scroll) library
- **Typography**: Google Fonts (Poppins) + custom Hindi font support
- **Color Scheme**: Saffron/Orange themed (#fd8535, #ffb300) following Indian cultural aesthetics

### Database Design
- **Primary Models**: News, Events, EventRegistration, ContactMessage, District, Category
- **Media Storage**: Local file system with organized upload paths
- **Relationships**: Foreign key relationships between content and geographic/categorical data

## Key Components

### Core Apps Structure
1. **core** - Base functionality, models (District, Category, SiteSettings), home/about pages
2. **news** - News management with images, comments, categories, and districts
3. **events** - Event management with registration system and ID card generation
4. **contact** - Contact form handling with admin notifications

### Authentication & Admin
- Django Admin interface with Hindi translations
- Custom admin configurations for each model
- No user authentication system (public-facing content only)

### Media & Static Files
- Organized static files in `/static/` with modular CSS architecture
- Media uploads handled via Django's file handling system
- Custom styling follows mobile-first responsive design

## Data Flow

### Content Management
1. Admins create news/events through Django admin
2. Content is categorized by District and Category
3. Rich text content supports embedded images and formatting
4. Published content appears on public pages with filtering/search

### Event Registration
1. Users register for events through public forms
2. Registration generates unique ID with QR code
3. PDF ID cards can be downloaded or emailed
4. Admin can manage registrations through Django admin

### Contact System
1. Public contact form captures user inquiries
2. Messages are stored in database with status tracking
3. Email notifications sent to both admin and user
4. Admin can reply and track message status

## External Dependencies

### Python Packages
- Django (5.1+) - Main framework
- django-ckeditor (6.7+) - Rich text editing
- Pillow (10.0+) - Image processing
- qrcode (7.4+) - QR code generation
- reportlab (4.0+) - PDF generation
- django-environ (0.11+) - Environment variable handling
- whitenoise (6.6+) - Static file serving
- django-crispy-forms (2.0+) - Enhanced form rendering

### Frontend Libraries
- Bootstrap 5.3.2 - UI framework
- Font Awesome 6.5.0 - Icons
- Bootstrap Icons 1.11.2 - Additional icons
- AOS 2.3.4 - Scroll animations
- Google Fonts (Poppins) - Typography

### Email Configuration
- SMTP email backend for notifications
- Configurable via environment variables
- Support for Gmail and other SMTP providers

## Deployment Strategy

### Environment Configuration
- Uses django-environ for settings management
- Separate configurations for development/production
- WhiteNoise for static file serving in production
- SQLite for development, PostgreSQL ready for production

### Static Files Strategy
- Modular CSS architecture with component-based styling
- Optimized for performance with minification ready
- CDN integration for external libraries
- Custom theme system with CSS variables

### Security Considerations
- CSRF protection on all forms
- Environment-based secret key management
- Input validation and sanitization
- Admin interface protection

## Changelog

- July 02, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.