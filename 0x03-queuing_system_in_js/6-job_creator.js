/**
 * Import the Kue module for managing job queues
 * This script creates and manages a queue for sending push notifications.
 * It creates a job that sends a notification message and tracks its status (enqueue, complete, or failure).
 */
import { createQueue } from 'kue';

// Create a new queue named 'push_notification_code'
const queue = createQueue({ name: 'push_notification_code' });

/**
 * Define a job for the 'push_notification_code' queue.
 * This job represents a task to send a push notification with a phone number and a message.
 */
const job = queue.create('push_notification_code', {
  phoneNumber: '07045679939',
  message: 'Account registered'
});

/**
 * Event listener for when the job is enqueued.
 * Logs a message indicating that the notification job has been created and provides the job ID.
 */
job
  .on('enqueue', () => {
    console.log('Notification job created:', job.id);
  })

  /**
   * Event listener for when the job is completed.
   * Logs a message indicating that the notification job has been successfully processed.
   */
  .on('complete', () => {
    console.log('Notification job completed');
  })

  /**
   * Event listener for when the job fails an attempt.
   * Logs a message indicating that the notification job failed to process.
   */
  .on('failed attempt', () => {
    console.log('Notification job failed');
  });

// Save the job to the queue to start processing
job.save();
