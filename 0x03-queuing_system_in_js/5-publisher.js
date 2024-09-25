/**
 * Import the Redis client module
 * This script uses Redis to publish messages to a specific channel.
 * The script connects to a Redis server and publishes several messages on a timer.
 */
import { createClient } from 'redis';

// Create a Redis client instance
const client = createClient();

/**
 * Event listener for handling Redis connection errors.
 * If the Redis client encounters an error while connecting to the server,
 * it logs an error message to the console.
 *
 * @param {Error} err - The error object encountered during connection.
 */
client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

/**
 * Publishes a message to the 'holberton school channel' on the Redis server after a specified time delay.
 *
 * @param {string} message - The message to be published.
 * @param {number} time - The delay (in milliseconds) before the message is published.
 */
const publishMessage = (message, time) => {
  setTimeout(() => {
    console.log(`About to send ${message}`);
    client.publish('holberton school channel', message);
  }, time);
};

/**
 * Event listener for successful connection to the Redis server.
 * Logs a message to the console when the Redis client successfully connects.
 */
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Schedule messages to be published with specific delays
publishMessage('Holberton Student #1 starts course', 100);
publishMessage('Holberton Student #2 starts course', 200);
publishMessage('KILL_SERVER', 300);
publishMessage('Holberton Student #3 starts course', 400);
