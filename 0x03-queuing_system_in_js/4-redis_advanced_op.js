/**
 * Importing the required modules from the Redis library:
 * - `createClient`: This is used to create a new Redis client that allows us to connect to a Redis server.
 * - `print`: A built-in utility from the Redis library that logs the result of Redis commands.
 */
import { createClient, print } from 'redis';

/**
 * Create a new Redis client instance that will be used to communicate with the Redis server.
 */
const client = createClient();

/**
 * Error handling for the Redis client.
 * If the client encounters an error (e.g., unable to connect to the server),
 * this function logs an error message to the console.
 *
 * @param {Error} err - The error object containing details about the error.
 */
client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

/**
 * Function to update a field-value pair within a Redis hash.
 *
 * A Redis hash is a data structure that stores field-value pairs, similar to a dictionary or object in JavaScript.
 *
 * @param {string} hashName - The name of the Redis hash (like a key) where the data will be stored.
 * @param {string} fieldName - The field or key inside the hash (e.g., a city name).
 * @param {number|string} fieldValue - The value associated with the `fieldName` inside the hash (e.g., a population count).
 */
const updateHash = (hashName, fieldName, fieldValue) => {
  client.HSET(hashName, fieldName, fieldValue, print);
};

/**
 * Function to retrieve and print all the field-value pairs from a Redis hash.
 *
 * The `HGETALL` command is used to fetch all the field-value pairs in a given hash.
 *
 * @param {string} hashName - The name of the Redis hash from which the field-value pairs will be fetched.
 */
const printHash = (hashName) => {
  client.HGETALL(hashName, (_err, reply) => console.log(reply));
};

/**
 * Main function that demonstrates how to update a Redis hash and print its contents.
 *
 * - It defines an object `hashObj` with city names as keys and values representing some data (e.g., population or capacity).
 * - Each key-value pair is added to the Redis hash `HolbertonSchools` using the `updateHash` function.
 * - After all the data is added, it retrieves and prints the entire hash using the `printHash` function.
 */
function main () {
  // Defining an object with cities and corresponding values.
  const hashObj = {
    Portland: 50,
    Seattle: 80,
    'New York': 20,
    Bogota: 20,
    Cali: 40,
    Paris: 2
  };

  // Iterating over each city-value pair and updating the Redis hash `HolbertonSchools`.
  for (const [field, value] of Object.entries(hashObj)) {
    updateHash('HolbertonSchools', field, value);
  }

  // After the updates, print the entire hash to the console.
  printHash('HolbertonSchools');
}

/**
 * Event listener for when the Redis client successfully connects to the server.
 * Upon connection, it logs a success message and runs the `main` function.
 */
client.on('connect', () => {
  console.log('Redis client connected to the server');
  main();
});
