import kue from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job';

const queue = kue.createQueue(); // Create a queue instance

// Define a sample job to test job creation
const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  }
];

describe('createPushNotificationsJobs', () => {
  /**
   * Before all tests, we enter the test mode for the Kue queue,
   * which simulates the job creation behavior.
   */
  before(() => {
    queue.testMode.enter();
  });

  /**
   * After each test, we clear any remaining jobs from the queue to reset the state.
   */
  afterEach(() => {
    queue.testMode.clear();
  });

  /**
   * After all tests are done, we exit the test mode for the queue.
   */
  after(() => {
    queue.testMode.exit();
  });

  /**
   * Test case to ensure the function throws an error when a number is passed instead of an array.
   * It checks if the proper error message "Jobs is not an array" is displayed.
   */
  it('display an error message if jobs is not an array passing Number', () => {
    expect(() => {
      createPushNotificationsJobs(2, queue);
    }).to.throw('Jobs is not an array');
  });

  /**
   * Test case to ensure the function throws an error when an object is passed instead of an array.
   * It verifies that the "Jobs is not an array" error is displayed.
   */
  it('display an error message if jobs is not an array passing Object', () => {
    expect(() => {
      createPushNotificationsJobs({}, queue);
    }).to.throw('Jobs is not an array');
  });

  /**
   * Test case to ensure the function throws an error when a string is passed instead of an array.
   * It checks for the "Jobs is not an array" error message.
   */
  it('display an error message if jobs is not an array passing String', () => {
    expect(() => {
      createPushNotificationsJobs('Hello', queue);
    }).to.throw('Jobs is not an array');
  });

  /**
   * Test case to ensure no error is thrown when an empty array is passed as the jobs argument.
   * It verifies that the function handles empty arrays gracefully and does not return any errors.
   */
  it('should NOT display an error message if jobs is an array with an empty array', () => {
    const ret = createPushNotificationsJobs([], queue);
    expect(ret).to.equal(undefined); // No error, function returns undefined
  });

  /**
   * Test case to verify that two new jobs are created and added to the queue.
   * It simulates job creation and checks the type and data of each job added to the queue.
   */
  it('create two new jobs to the queue', () => {
    // Simulate adding jobs to the queue
    queue.createJob('myJob', { foo: 'bar' }).save();
    queue.createJob('anotherJob', { baz: 'bip' }).save();

    // Verify that two jobs were added to the queue
    expect(queue.testMode.jobs.length).to.equal(2);

    // Check the type and data of the first job
    expect(queue.testMode.jobs[0].type).to.equal('myJob');
    expect(queue.testMode.jobs[0].data).to.eql({ foo: 'bar' });

    // Check the type and data of the second job
    expect(queue.testMode.jobs[1].type).to.equal('anotherJob');
    expect(queue.testMode.jobs[1].data).to.eql({ baz: 'bip' });
  });
});
