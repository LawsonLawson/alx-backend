/**
 * Import the Kue module to create and manage job queues.
 * This script processes push notification jobs while ensuring that blacklisted phone numbers are excluded.
 * It also updates job progress and handles job completion or failure accordingly.
 */
import { createQueue, Job } from 'kue';

// List of blacklisted phone numbers that should not receive notifications
const BLACKLISTED_NUMBERS = ['4153518780', '4153518781'];

// Create a queue instance for managing jobs
const queue = createQueue();

/**
 * Function to send a push notification to a user.
 * It simulates sending a notification by updating the job progress and handling blacklisted numbers.
 *
 * @param {String} phoneNumber - The phone number to send the notification to.
 * @param {String} message - The notification message to send.
 * @param {Job} job - The Kue job instance that contains job details and methods for tracking progress.
 * @param {Function} done - The callback function to mark the job as complete or failed.
 */
const sendNotification = (phoneNumber, message, job, done) => {
  const total = 2;
  let pending = 2;
  const sendInterval = setInterval(() => {
    // Update job progress when half of the steps are completed
    if (total - pending <= total / 2) {
      job.progress(total - pending, total);
    }

    // Check if the phone number is blacklisted, and if so, fail the job
    if (BLACKLISTED_NUMBERS.includes(phoneNumber)) {
      done(new Error(`Phone number ${phoneNumber} is blacklisted`));
      clearInterval(sendInterval);
      return;
    }

    // Simulate the action of sending the notification
    if (total === pending) {
      console.log(
        `Sending notification to ${phoneNumber},`,
        `with message: ${message}`
      );
    }

    // Decrement the pending steps; mark the job as done when completed
    --pending || done();

    // Stop the interval timer once all steps are complete
    pending || clearInterval(sendInterval);
  }, 1000);
};

/**
 * Process jobs from the 'push_notification_code_2' queue.
 * This handler processes two jobs concurrently and sends notifications to users.
 *
 * @param {Job} job - The job containing the phone number and message data.
 * @param {Function} done - The callback function to mark the job as complete or failed.
 */
queue.process('push_notification_code_2', 2, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});
