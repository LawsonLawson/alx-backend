/**
 * Import the Kue module for managing job queues.
 * This script processes a queue that sends push notifications by handling jobs
 * in the 'push_notification_code' queue and invoking a notification function.
 */
import { createQueue } from 'kue';

// Create a queue instance for managing jobs
const queue = createQueue();

/**
 * Function to send a notification to a specified phone number with a message.
 * This simulates sending a notification by logging the phone number and message to the console.
 *
 * @param {string} phoneNumber - The phone number to send the notification to.
 * @param {string} message - The notification message to send.
 */
const sendNotification = (phoneNumber, message) => {
  console.log(
    `Sending notification to ${phoneNumber},`,
    'with message:',
    message
  );
};

/**
 * Queue processor that listens for jobs on the 'push_notification_code' queue.
 * When a job is received, it extracts the phone number and message and sends a notification.
 *
 * @param {Object} job - The job object containing the data (phoneNumber and message) for processing.
 * @param {Function} done - The callback to indicate that the job has been processed.
 */
queue.process('push_notification_code', (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message);
  done();
});
