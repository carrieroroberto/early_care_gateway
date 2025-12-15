# Use the official Node.js version 20 image as the base image
FROM node:20

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json (if present)
# This allows dependency installation before copying the full source code
COPY package*.json ./

# Install all project dependencies
RUN npm install

# Copy the entire application source code into the container
COPY . .

# Expose port 3000 to allow external access to the application
EXPOSE 3000

# Command to start the application when the container runs
CMD ["npm", "start"]