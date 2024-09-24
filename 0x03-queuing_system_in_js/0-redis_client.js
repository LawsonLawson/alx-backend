// Import the createClient function from the redis package
import { createClient } from 'redis';

// Create a new Redis client instance
const client = createClient();

/**
 * Initializes the Redis client connection.
 * Sets up event listeners for connection status and errors.
 */
const redisConnect = () => {
  // Listen for errors in the Redis client
  client.on('error', err => {
    console.log('Redis client not connected to the server: ', err);
  });
  
  // Listen for successful connection to the Redis server
  client.on('connect', () => {
    console.log('Redis client connected to the server');
  });
}

// Call the redisConnect function to set up the listeners
redisConnect();
