# Use the official Node.js image as a parent image
FROM node:16

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Expose port 3000 for React
EXPOSE 3000

# Run the app
CMD ["npm", "start"]
