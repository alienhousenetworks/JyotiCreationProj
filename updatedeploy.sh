#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Configuration variables (Make sure they match setup_server.sh)
PROJECT_NAME="jyoti_saree_proj"
REPO_DIR="/opt/JyotiCreationProj/JyotiCreationProj"



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

# 4. Run migrations (Updates database schema incrementally without data loss)
echo "--> Running database migrations..."
python manage.py migrate --noinput

# 5. Collect static files
echo "--> Collecting static files..."
python manage.py collectstatic --noinput

# 6. Restart Gunicorn and Nginx to apply updates
echo "--> Restarting services..."
systemctl restart ${PROJECT_NAME}
systemctl restart nginx

echo "================================================================="
echo " Update Completed Successfully!"
echo "================================================================="
