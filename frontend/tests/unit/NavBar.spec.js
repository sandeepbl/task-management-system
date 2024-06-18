// Import necessary modules for testing
import { mount } from '@vue/test-utils';
import NavBar from './NavBar.vue'; // Adjust path as needed

describe('NavBar.vue', () => {
  // Test case 1: Mounting the component
  it('renders the component', () => {
    const wrapper = mount(NavBar);
    expect(wrapper.exists()).toBe(true);
  });

  // Test case 2: Check initial state and user login text
  it('displays correct user login text when user is logged in', async () => {
    // Set localStorage values to simulate logged-in state
    localStorage.setItem('username', 'testuser');
    localStorage.setItem('first_name', 'John');
    localStorage.setItem('last_name', 'Doe');
    localStorage.setItem('role', 'Admin');

    const wrapper = mount(NavBar);

    // Wait for component to update
    await wrapper.vm.$nextTick();

    // Assert that user login text is correctly updated
    expect(wrapper.find('.nav-link').text()).toContain('User Profile: John Doe (Admin)');
  });

  // Test case 3: Simulate logout action
  it('logs out the user on logout action', async () => {
    // Set localStorage values to simulate logged-in state
    localStorage.setItem('username', 'testuser');
    localStorage.setItem('first_name', 'John');
    localStorage.setItem('last_name', 'Doe');
    localStorage.setItem('role', 'Admin');

    const wrapper = mount(NavBar);

    // Simulate logout action
    await wrapper.find('a[href="#"]').trigger('click');

    // Assert that localStorage items are removed and user state is reset
    expect(localStorage.getItem('username')).toBeNull();
    expect(localStorage.getItem('first_name')).toBeNull();
    expect(localStorage.getItem('last_name')).toBeNull();
    expect(localStorage.getItem('role')).toBeNull();
    // Assuming router.push('/login') is correctly triggered
    expect(wrapper.vm.$route.path).toBe('/login');
    // Assuming currentUser state is reset
    expect(wrapper.vm.$store.state.currentUser.username).toBeNull();
  });
});
