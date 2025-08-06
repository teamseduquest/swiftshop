# SwiftShop

SwiftShop is a simple e-commerce platform built with Django.

## Features
- Product catalog with images
- Admin dashboard
- Chart-based sales reports
- User authentication

## Installation

```bash
git clone https://github.com/teamseduquest/swiftshop.git
cd swiftshop
python -m venv .venv
source venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
