# Install Python dependencies
pip install -r requirements.txt

# Install missing system dependencies
apt-get update
apt-get install -y \
  libicu66 \
  libevent-2.1-7 \
  libjpeg8 \
  libenchant-2-2 \
  libsecret-1-0 \
  libffi7 \
  libgles2

# If libicu66 is not available, try libicu-dev
apt-get install -y libicu-dev

# Install Playwright browsers
playwright install