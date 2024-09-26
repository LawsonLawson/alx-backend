#!/usr/bin/npm dev
import express from 'express';
import { promisify } from 'util';
import { createQueue } from 'kue';
import { createClient } from 'redis';

const app = express();
const client = createClient({ name: 'reserve_seat' });
const queue = createQueue();
const INITIAL_SEATS_COUNT = 50;
let reservationEnabled = false;
const PORT = 1245;

/**
 * Modifies the number of available seats by setting the new value in Redis.
 * @param {number} number - The new number of available seats.
 * @returns {Promise<void>}
 */
const reserveSeat = async (number) => {
  return promisify(client.SET).bind(client)('available_seats', number);
};

/**
 * Retrieves the current number of available seats from Redis.
 * @returns {Promise<String>} The number of available seats as a string.
 */
const getCurrentAvailableSeats = async () => {
  return promisify(client.GET).bind(client)('available_seats');
};

/**
 * Route to get the number of available seats.
 * Sends the current available seat count in the response as JSON.
 */
app.get('/available_seats', (_, res) => {
  getCurrentAvailableSeats()
    .then((numberOfAvailableSeats) => {
      res.json({ numberOfAvailableSeats });
    });
});

/**
 * Route to reserve a seat.
 * Adds a job to the queue to reserve a seat and responds with the reservation status.
 */
app.get('/reserve_seat', (_req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }
  try {
    const job = queue.create('reserve_seat');

    // Event listener for when the job fails
    job.on('failed', (err) => {
      console.log(
        'Seat reservation job', job.id, 'failed:', err.message || err.toString()
      );
    });

    // Event listener for when the job completes successfully
    job.on('complete', () => {
      console.log('Seat reservation job', job.id, 'completed');
    });

    job.save(); // Save the job to the queue
    res.json({ status: 'Reservation in process' });
  } catch {
    res.json({ status: 'Reservation failed' });
  }
});

/**
 * Route to process the queue for reserving seats.
 * Handles seat reservation jobs from the queue.
 */
app.get('/process', (_req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', (_job, done) => {
    getCurrentAvailableSeats()
      .then((result) => Number.parseInt(result || 0))
      .then((availableSeats) => {
        // If only 1 or fewer seats are available, disable further reservations
        reservationEnabled = availableSeats <= 1 ? false : reservationEnabled;

        // If seats are available, reserve a seat by decrementing the count
        if (availableSeats >= 1) {
          reserveSeat(availableSeats - 1)
            .then(() => done());
        } else {
          done(new Error('Not enough seats available'));
        }
      });
  });
});

/**
 * Resets the number of available seats to the initial count when the server starts.
 * @param {number} initialSeatsCount - The initial number of seats to reset to.
 * @returns {Promise<void>}
 */
const resetAvailableSeats = async (initialSeatsCount) => {
  return promisify(client.SET)
    .bind(client)('available_seats', Number.parseInt(initialSeatsCount));
};

// Start the Express server and reset available seats when the server starts
app.listen(PORT, () => {
  resetAvailableSeats(process.env.INITIAL_SEATS_COUNT || INITIAL_SEATS_COUNT)
    .then(() => {
      reservationEnabled = true;
      console.log(`API available on localhost port ${PORT}`);
    });
});

export default app; // Export the Express app
