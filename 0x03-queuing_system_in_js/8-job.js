import { Queue, Job } from 'kue';

/**
 * Creates and enqueues push notification jobs from an array of job information objects.
 * Each job represents a task to send a push notification to a user.
 * It handles job creation, progress updates, job completion, and error logging.
 *
 * @param {Job[]} jobs - An array of job objects containing phone number and message details.
 * @param {Queue} queue - The Kue queue instance where jobs will be enqueued and processed.
 *
 * @throws {Error} If the provided jobs argument is not an array.
 */
export const createPushNotificationsJobs = (jobs, queue) => {
  // Ensure that the jobs parameter is an array, otherwise throw an error
  if (!(jobs instanceof Array)) {
    throw new Error('Jobs is not an array');
  }

  // Loop through each job info object and create a job in the queue
  for (const jobInfo of jobs) {
    const job = queue.create('push_notification_code_3', jobInfo);

    /**
     * Event listener for when the job is enqueued.
     * Logs the creation of the notification job along with the job ID.
     */
    job
      .on('enqueue', () => {
        console.log('Notification job created:', job.id);
      })

      /**
       * Event listener for when the job is completed.
       * Logs the successful completion of the job.
       *
       * @param {number} job.id - The unique identifier of the job.
       */
      .on('complete', () => {
        console.log('Notification job', job.id, 'completed');
      })

      /**
       * Event listener for when the job fails.
       * Logs an error message if the job fails during processing.
       *
       * @param {Error} err - The error object describing the reason for failure.
       */
      .on('failed', (err) => {
        console.log('Notification job', job.id, 'failed:', err.message || err.toString());
      })

      /**
       * Event listener for tracking job progress.
       * Logs the progress percentage of the job as it moves through the steps of notification.
       *
       * @param {number} progress - The percentage of the job that has been completed.
       */
      .on('progress', (progress, _data) => {
        console.log('Notification job', job.id, `${progress}% complete`);
      });

    // Save the job to the queue for processing
    job.save();
  }
};

export default createPushNotificationsJobs;
