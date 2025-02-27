# Use an official Node.js runtime as a parent image
FROM node:18-alpine

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# RUN npm run build

# Copy the rest of the application code to the container
COPY . .

# Expose port 5173
EXPOSE 5173

# Define the command to run your app using npm start
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
