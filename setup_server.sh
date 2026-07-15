#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Configuration variables (Adjust these if needed)
PROJECT_NAME="jyoti_saree_proj"
REPO_DIR="/root/JyotiCreationProj" # Assuming cloned into /root/
SERVER_IP="187.127.160.134"
SOCKET_FILE="/run/${PROJECT_NAME}.sock"

echo "================================================================="
echo " Starting Django Production Deployment Setup on Hostinger VPS    "
echo " Target IP: ${SERVER_IP}                                         "
echo "================================================================="

# 1. Update and install system dependencies
echo "--> Updating system packages and installing dependencies..."
apt-get update -y
apt-get install -y python3 python3-pip python3-venv nginx curl git ufw

# 2. Set up virtual environment and install requirements
echo "--> Setting up virtual environment..."
cd "${REPO_DIR}"
python3 -m venv venv
source venv/bin/activate

echo "--> Installing pip packages..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# 3. Django Setup (Migrations, Staticfiles)
echo "--> Running Django migrations..."
python manage.py migrate --noinput

echo "--> Collecting static files..."
python manage.py collectstatic --noinput

# 4. Create Systemd Service for Gunicorn
echo "--> Creating Gunicorn systemd service..."
cat <<EOF > /etc/systemd/system/${PROJECT_NAME}.service
[Unit]
Description=gunicorn daemon for ${PROJECT_NAME}
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=${REPO_DIR}
ExecStart=${REPO_DIR}/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:${SOCKET_FILE} \
          ${PROJECT_NAME}.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# 5. Start and Enable Gunicorn Service
echo "--> Starting and enabling Gunicorn service..."
systemctl daemon-reload
systemctl start ${PROJECT_NAME}
systemctl enable ${PROJECT_NAME}

# 6. Configure Nginx
echo "--> Creating Nginx site configuration..."
cat <<EOF > /etc/nginx/sites-available/${PROJECT_NAME}
server {
    listen 80;
    server_name ${SERVER_IP};

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

# 7. Configure Firewall (UFW)
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
