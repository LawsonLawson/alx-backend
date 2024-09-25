/**
 * Import the Redis client module
 * This script subscribes to a Redis channel and listens for incoming messages.
 * It automatically disconnects when a specific message is received.
 */
import { createClient } from 'redis';

// Create a Redis client instance
const client = createClient();

// Constant representing the exit message that triggers the server to shut down
const EXIT_MSG = 'KILL_SERVER';

/**
 * Event listener for handling Redis connection errors.
 * Logs an error message if the Redis client fails to connect to the server.
 *
 * @param {Error} err - The error object encountered during connection.
 */
client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

/**
 * Event listener for successful connection to the Redis server.
 * Logs a message to the console when the Redis client successfully connects.
 */
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

/**
 * Subscribes the client to the 'holberton school channel'.
 * The client will listen for messages published to this channel.
 */
client.subscribe('holberton school channel');

/**
 * Event listener that handles messages received from the subscribed channel.
 * Logs the message content and checks if it matches the exit message (EXIT_MSG).
 * If the message is the exit command, the client will unsubscribe and disconnect from the Redis server.
 *
 * @param {string} _err - Unused in this case, included for the event signature.
 * @param {string} msg - The message received from the Redis channel.
 */
client.on('message', (_err, msg) => {
  console.log(msg);
  if (msg === EXIT_MSG) {
    // If the exit message is received, unsubscribe and quit the Redis client
    client.unsubscribe();
    client.quit();
  }
});
