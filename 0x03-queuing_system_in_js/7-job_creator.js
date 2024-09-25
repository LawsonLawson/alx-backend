/**
 * Import the Kue module for managing job queues.
 * This script enqueues multiple push notification jobs, each with a phone number
 * and a message to verify an account. The jobs are processed through the queue
 * 'push_notification_code_2', and their status (enqueue, complete, failed, progress)
 * is tracked and logged.
 */
import { createQueue } from 'kue';

// Array of job objects containing phone numbers and verification messages
const jobs = [
  { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
  { phoneNumber: '4153518781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4153518743', message: 'This is the code 4321 to verify your account' },
  { phoneNumber: '4153538781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4153118782', message: 'This is the code 4321 to verify your account' },
  { phoneNumber: '4153718781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4159518782', message: 'This is the code 4321 to verify your account' },
  { phoneNumber: '4158718781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4153818782', message: 'This is the code 4321 to verify your account' },
  { phoneNumber: '4154318781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4151218782', message: 'This is the code 4321 to verify your account' }
];

// Create a queue named 'push_notification_code_2'
const queue = createQueue({ name: 'push_notification_code_2' });

/**
 * Loop through each job in the jobs array and create a queue job for each notification.
 * Each job represents a task to send a push notification to a specific phone number with a message.
 */
for (const jobInfo of jobs) {
  const job = queue.create('push_notification_code_2', jobInfo);

  /**
   * Event listener for when the job is enqueued.
   * Logs a message indicating that the notification job has been created, along with the job ID.
   */
  job
    .on('enqueue', () => {
      console.log('Notification job created:', job.id);
    })

    /**
     * Event listener for when the job is completed.
     * Logs a message indicating that the notification job has successfully finished processing.
     *
     * @param {number} job.id - The unique identifier of the job.
     */
    .on('complete', () => {
      console.log('Notification job', job.id, 'completed');
    })

    /**
     * Event listener for when the job fails.
     * Logs an error message if the notification job fails during processing.
     *
     * @param {Error} err - The error object that caused the job to fail.
     */
    .on('failed', (err) => {
      console.log('Notification job', job.id, 'failed:', err.message || err.toString());
    })

    /**
     * Event listener for tracking job progress.
     * Logs the progress percentage of the notification job as it is processed.
     *
     * @param {number} progress - The percentage of the job that has been completed.
     */
    .on('progress', (progress, _data) => {
      console.log('Notification job', job.id, `${progress}% complete`);
    });

  // Save the job to the queue for processing
  job.save();
}
