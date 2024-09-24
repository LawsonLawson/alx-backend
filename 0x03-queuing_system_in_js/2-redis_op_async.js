/**
 * Importing required modules:
 * - `promisify` from the `util` module allows for converting callback-based functions to promises.
 * - `createClient` and `print` are imported from the `redis` module for creating a Redis client and printing Redis command outputs.
 */
import { promisify } from 'util';
import { createClient, print } from 'redis';

/**
 * Create a new Redis client instance.
 * This will allow us to interact with the Redis database.
 */
const client = createClient();

/**
 * Error handling for the Redis client.
 * If the client cannot connect to the server, it logs an error message.
 *
 * @param {Error} err - The error object containing the details of the connection failure.
 */
client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

/**
 * Function to set a new key-value pair in Redis.
 *
 * @param {string} schoolName - The key that will be stored in Redis (e.g., name of the school).
 * @param {string} value - The value to be associated with the `schoolName` key.
 */
const setNewSchool = (schoolName, value) => {
  client.SET(schoolName, value, print);
};

/**
 * Function to retrieve and display the value associated with a given key in Redis.
 *
 * This function uses `promisify` to convert Redis' callback-based `GET` function into a promise.
 *
 * @param {string} schoolName - The key whose value will be retrieved from Redis.
 */
const displaySchoolValue = async (schoolName) => {
  // `promisify(client.GET).bind(client)` converts the GET method into a promise and binds it to the client.
  console.log(await promisify(client.GET).bind(client)(schoolName));
};

/**
 * Main function that drives the flow of the program.
 *
 * - Retrieves and displays the value for the key "Holberton".
 * - Sets a new key-value pair ("HolbertonSanFrancisco", "100").
 * - Retrieves and displays the value for the newly set key.
 */
async function main () {
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
}

/**
 * Event listener for when the Redis client successfully connects to the server.
 * Upon connection, it logs a success message and runs the `main` function.
 */
client.on('connect', async () => {
  console.log('Redis client connected to the server');
  await main();
});
