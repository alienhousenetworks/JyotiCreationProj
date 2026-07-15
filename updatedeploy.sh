#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Configuration variables (Make sure they match setup_server.sh)
PROJECT_NAME="jyoti_saree_proj"
REPO_DIR="/root/JyotiCreationProj"

# Database Configuration (Make sure they match setup_server.sh)
DB_NAME="jyoti_saree_db"
DB_USER="jyoti_saree_user"
DB_PASSWORD="jyoti_saree_password"

echo "================================================================="
echo " Fetching latest updates from GitHub & Deploying...               "
echo "================================================================="

cd "${REPO_DIR}"

# 1. Pull changes
echo "--> Pulling latest code from GitHub..."
git pull origin main

# 2. Activate virtual environment
echo "--> Activating virtual environment..."
source venv/bin/activate

# 3. Install requirements
echo "--> Installing / updating pip requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Export database environment variables for migrations
export DB_NAME="${DB_NAME}"
export DB_USER="${DB_USER}"
export DB_PASSWORD="${DB_PASSWORD}"
export DB_HOST="localhost"
export DB_PORT="5432"

# 5. Run migrations (Updates database schema incrementally without data loss)
echo "--> Running database migrations..."
python manage.py migrate --noinput

# 6. Collect static files
echo "--> Collecting static files..."
python manage.py collectstatic --noinput

# 7. Restart Gunicorn and Nginx to apply updates
echo "--> Restarting services..."
systemctl restart ${PROJECT_NAME}
systemctl restart nginx

echo "================================================================="
echo " Update Completed Successfully!"
echo "================================================================="
