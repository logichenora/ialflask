# ialflask
Base Python-Flask Tutorial Project for IAL 2021 - Covid Analytics FrontEnd/Backend


[Unit]
#  specifies metadata and dependencies
Description=Ialflask Gunicorn instance to serve myproject
After=network.target
# tells the init system to only start this after the networking target has been reached
# We will give our regular user account ownership of the process since it owns all of the relevant files
[Service]
# Service specify the user and group under which our process will run.
User=ubuntu
# give group ownership to the www-data group so that Nginx can communicate easily with the Gunicorn processes.
Group=www-data
# We'll then map out the working directory and set the PATH environmental variable so that the init system knows where our the executables for the process are located (within our virtual environment).
WorkingDirectory=/var/www/ialflask
Environment="PATH=/var/www/ialflask/venv/bin"
# We'll then specify the commanded to start the service
ExecStart=/var/www/ialflask/venv/bin/gunicorn --workers 3 --bind unix:app.sock -m 007 wsgi:app
# This will tell systemd what to link this service to if we enable it to start at boot. We want this service to start when the regular multi-user system is up and running:
[Install]
WantedBy=multi-user.target


