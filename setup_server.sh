#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Configuration variables (Adjust these if needed)
PROJECT_NAME="jyoti_saree_proj"
REPO_DIR="/opt/JyotiCreationProj/JyotiCreationProj" # Added the nested folder
SERVER_IP="187.127.160.134"
SOCKET_FILE="/run/${PROJECT_NAME}.sock"
# Database Configuration
DB_NAME="jyoti_saree_db"
DB_USER="jyoti_saree_user"
DB_PASSWORD="jyoti_saree_password" # Change this to a secure password in production

echo "================================================================="
echo " Starting Django Production Deployment Setup on Hostinger VPS    "
echo " Target IP: ${SERVER_IP}                                         "
echo " Database: PostgreSQL                                            "
echo "================================================================="

# 1. Update and install system dependencies
echo "--> Updating system packages and installing dependencies..."
apt-get update -y
apt-get install -y python3 python3-pip python3-venv nginx curl git ufw postgresql postgresql-contrib libpq-dev

# 2. Configure PostgreSQL
echo "--> Configuring PostgreSQL database and user..."
# Start PostgreSQL service if not running
systemctl start postgresql
systemctl enable postgresql

# Create Database and User (ignores error if they already exist)
sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME};" || true
sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';" || true
sudo -u postgres psql -c "ALTER ROLE ${DB_USER} SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE ${DB_USER} SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE ${DB_USER} SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};"
# Grant permissions to schema public (required for PostgreSQL 15+)
sudo -u postgres psql -d ${DB_NAME} -c "GRANT ALL ON SCHEMA public TO ${DB_USER};"

# 3. Create .env file
echo "--> Creating .env file..."
cat <<EOF > "${REPO_DIR}/.env"
DEBUG=True
SECRET_KEY=django-insecure-@j1-%i5=\$a+x@-t^4o!16phwyg)*sua_)aru3v7t#rqq%+in@)
ALLOWED_HOSTS=${SERVER_IP},localhost,127.0.0.1,jyoticreations.com,www.jyoticreations.com
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_HOST=localhost
DB_PORT=5432
EOF

# 4. Set up virtual environment and install requirements
echo "--> Setting up virtual environment..."
cd "${REPO_DIR}"
python3 -m venv venv
source venv/bin/activate

echo "--> Installing pip packages..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# 5. Django Setup (Migrations, Staticfiles)
echo "--> Running Django migrations..."
python manage.py migrate --noinput

echo "--> Collecting static files..."
python manage.py collectstatic --noinput

# 6. Create Systemd Service for Gunicorn
echo "--> Creating Gunicorn systemd service..."
cat <<EOF > /etc/systemd/system/${PROJECT_NAME}.service
[Unit]
Description=gunicorn daemon for ${PROJECT_NAME}
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=${REPO_DIR}
EnvironmentFile=${REPO_DIR}/.env
ExecStart=${REPO_DIR}/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:${SOCKET_FILE} \
          ${PROJECT_NAME}.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# 7. Start and Enable Gunicorn Service
echo "--> Starting and enabling Gunicorn service..."
systemctl daemon-reload
systemctl restart ${PROJECT_NAME}
systemctl enable ${PROJECT_NAME}

# 8. Configure Nginx
echo "--> Creating Nginx site configuration..."
cat <<EOF > /etc/nginx/sites-available/${PROJECT_NAME}
server {
    listen 80;
    server_name ${SERVER_IP} jyoticreations.com www.jyoticreations.com;

    client_max_body_size 50M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root ${REPO_DIR};
    }

    location /media/ {
        root ${REPO_DIR};
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:${SOCKET_FILE};
    }
}
EOF

# Enable Nginx configuration
echo "--> Enabling Nginx configuration..."
if [ -f /etc/nginx/sites-enabled/${PROJECT_NAME} ]; then
    rm /etc/nginx/sites-enabled/${PROJECT_NAME}
fi
ln -s /etc/nginx/sites-available/${PROJECT_NAME} /etc/nginx/sites-enabled/

# Remove default nginx config if exists to prevent conflicts
if [ -f /etc/nginx/sites-enabled/default ]; then
    rm /etc/nginx/sites-enabled/default
fi

# Test Nginx and restart
echo "--> Restarting Nginx..."
nginx -t
systemctl restart nginx

# 9. Configure Firewall (UFW)
echo "--> Configuring firewall (UFW)..."
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

echo "================================================================="
echo " Deployment Setup Completed Successfully!"
echo " Your Django app is now running on http://${SERVER_IP}"
echo " Check status with: systemctl status ${PROJECT_NAME}"
echo " Nginx logs: tail -f /var/log/nginx/error.log"
echo " Gunicorn logs: journalctl -u ${PROJECT_NAME} -f"
echo "================================================================="
