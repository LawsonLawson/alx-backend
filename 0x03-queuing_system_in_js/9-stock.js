import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

// Create a Redis client
const client = redis.createClient();
const app = express();

// Promisify Redis client methods for cleaner async/await usage
const clientGet = promisify(client.get).bind(client);
const clientSet = promisify(client.set).bind(client);

// List of products with their details (id, name, price, stock)
const listProducts = [
  { Id: 1, name: 'Suitcase 250', price: 50, stock: 0 },
  { Id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { Id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { Id: 4, name: 'Suitcase 1050', price: 550, stock: 15 }
];

/**
 * Function to get a product item by its ID.
 * @param {Number} id - The ID of the product.
 * @returns {Object} - The product object if found, else undefined.
 */
const getItemById = (id) => {
  for (const list of listProducts) {
    if (list.Id === id) return list;
  }
  return undefined;
};

/**
 * Reserve a certain amount of stock for a specific product.
 * Stores the reserved stock count in Redis.
 * @param {Number} itemId - The ID of the product to reserve stock for.
 * @param {Number} stock - The amount of stock to reserve.
 */
const reserveStockById = async (itemId, stock) => {
  await clientSet(itemId, stock);
};

/**
 * Retrieve the currently reserved stock of a product by its ID from Redis.
 * @param {Number} itemId - The ID of the product to check reserved stock for.
 * @returns {Number} - The reserved stock amount.
 */
const getCurrentReservedStockById = async (itemId) => {
  const currentReservedStock = await clientGet(itemId);
  return currentReservedStock;
};

/**
 * Endpoint to get the list of all products.
 * Responds with the full list of products in JSON format.
 */
app.get('/list_products', (req, res) => res.send(JSON.stringify(listProducts)));

/**
 * Endpoint to get the details of a specific product by its ID.
 * Includes the current reserved stock for the product from Redis.
 */
app.get('/list_products/:itemId', async (req, res) => {
  const id = Number(req.params.itemId);
  const item = getItemById(id);
  const currentReservedStock = await getCurrentReservedStockById(id);

  if (item) {
    // If the product is found, attach the reserved stock and respond with the product details
    item.reservedStock = (currentReservedStock) || 0;
    res.json(item);
    return;
  }

  // If product is not found, return a 404 status with an error message
  res.status(404).json({ status: 'Product not found' });
});

/**
 * Endpoint to reserve stock for a specific product by its ID.
 * Responds with confirmation if the reservation was successful or if there isn't enough stock.
 */
app.get('/reserve_product/:itemId', async (req, res) => {
  const id = Number(req.params.itemId);
  const item = getItemById(id);

  if (!item) {
    // If the product is not found, return a 403 status with an error message
    res.status(403).json({ status: 'Product not found' });
    return;
  }

  // Get the current reserved stock for the product
  const currentReservedStock = await getCurrentReservedStockById(id);
  item.reservedStock = (currentReservedStock) || 0;

  // Check if there is enough stock available to reserve
  if ((item.stock - item.reservedStock) < 1) {
    res.status(403).json({ status: 'Not enough stock available', id });
    return;
  }

  // Reserve stock by increasing the current reserved stock
  reserveStockById(id, Number(currentReservedStock) + 1);

  // Respond with a confirmation message
  res.json({ status: 'Reservation confirmed', id });
});

// Start the Express server on port 1245
app.listen(1245);
