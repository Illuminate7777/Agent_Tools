# Start from a base image that has both Python and Node.js
# Here, we'll use a Python image and manually install Node.js 18
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install Node.js 18
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Install Playwright
# This step ensures Playwright's necessary browser binaries are installed
RUN npm i -D playwright

RUN npx playwright install 

RUN npx playwright install-deps 

# Copy the Python dependencies file to the working directory
COPY requirements.txt .

# Install any Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]