// Import necessary modules for testing
import { mount } from '@vue/test-utils';
import HelloWorld from './HelloWorld.vue'; // Adjust path as needed

describe('HelloWorld.vue', () => {
  // Test case 1: Mounting the component
  it('renders the component', () => {
    const wrapper = mount(HelloWorld);
    expect(wrapper.exists()).toBe(true);
  });

  // Test case 2: Simulating user login
  it('logs in the user on form submission', async () => {
    const wrapper = mount(HelloWorld);

    // Simulate user input
    await wrapper.setData({ username: 'testuser', password: 'testpassword' });

    // Simulate form submission
    await wrapper.find('form').trigger('submit.prevent');

    // Since Axios calls are asynchronous, we need to wait for the promise chain to resolve
    await wrapper.vm.$nextTick();

    // Assert that user is authenticated and login response is shown
    expect(wrapper.vm.userAuthenticated).toBe(true);
    expect(wrapper.vm.showLogin).toBe(false);
    expect(wrapper.vm.showLoginResponse).toBe(true);
  });

  // Test case 3: Simulate unsuccessful login
  it('handles unsuccessful login', async () => {
    const wrapper = mount(HelloWorld);

    // Simulate invalid credentials
    await wrapper.setData({ username: 'invaliduser', password: 'invalidpassword' });

    // Simulate form submission
    await wrapper.find('form').trigger('submit.prevent');

    // Since Axios calls are asynchronous, we need to wait for the promise chain to resolve
    await wrapper.vm.$nextTick();

    // Assert that user is not authenticated and error message is shown
    expect(wrapper.vm.userAuthenticated).toBe(false);
    expect(wrapper.vm.showLogin).toBe(true);
    expect(wrapper.vm.showLoginResponse).toBe(true);
    expect(wrapper.vm.alertLevel).toBe('alert alert-danger');
  });
});
