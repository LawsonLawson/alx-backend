import { createClient, print } from 'redis';

// Create a Redis client instance
const client = createClient();

// Event listener for error handling
client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

// Event listener for successful connection
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

/**
 * Stores a new value for a given school name in the Redis database.
 *
 * @param {string} schoolName - The name of the school to be used as the key.
 * @param {string} value - The value to be associated with the school name.
 */
const setNewSchool = (schoolName, value) => {
  client.SET(schoolName, value, print);
};

/**
 * Retrieves and displays the value associated with a school name from the Redis database.
 *
 * @param {string} schoolName - The name of the school whose value is to be retrieved.
 */
const displaySchoolValue = (schoolName) => {
  client.GET(schoolName, (_err, reply) => {
    console.log(reply);
  });
};

// Example usage of the functions:
displaySchoolValue('Holberton'); // Retrieves and displays the value for 'Holberton'
setNewSchool('HolbertonSanFrancisco', '100'); // Stores '100' under 'HolbertonSanFrancisco'
displaySchoolValue('HolbertonSanFrancisco'); // Retrieves and displays the value for 'HolbertonSanFrancisco'
