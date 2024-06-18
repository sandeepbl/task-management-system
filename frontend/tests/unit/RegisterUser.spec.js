import { mount } from '@vue/test-utils';
import RegisterUser from '@/components/RegisterUser.vue';
import axios from 'axios';

jest.mock('axios');

describe('RegisterUser.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(RegisterUser, {
      global: {
        mocks: {
          $router: {
            push: jest.fn(),
          },
        },
      },
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('registers a new user when form is submitted', async () => {
    axios.post.mockResolvedValue({ data: { message: 'User registered successfully' } });
    
    // Set input values
    await wrapper.setData({
      username: 'testuser',
      password: 'testpassword',
      first_name: 'John',
      last_name: 'Doe',
    });
    
    // Trigger form submission
    await wrapper.find('form').trigger('submit.prevent');
    
    // Ensure axios.post is called with correct data
    expect(axios.post).toHaveBeenCalledWith('/users/register/', {
      username: 'testuser',
      password: 'testpassword',
      first_name: 'John',
      last_name: 'Doe',
      role: 'User',
    }, { headers: { 'Authorization': 'Bearer ' } }); // Adjust token as per your implementation
    
    // Simulate axios response
    await axios.post.mockResolvedValueOnce({ data: { message: 'User registered successfully' } });
    
    // Check that the form clears after submission
    expect(wrapper.vm.username).toBe('');
    expect(wrapper.vm.password).toBe('');
    expect(wrapper.vm.first_name).toBe('');
    expect(wrapper.vm.last_name).toBe('');
    
    // Verify router redirection
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/'); // Adjust the route as per your implementation
  });

  it('handles registration failure', async () => {
    axios.post.mockRejectedValue(new Error('Registration failed'));
    
    // Set input values
    await wrapper.setData({
      username: 'testuser',
      password: 'testpassword',
      first_name: 'John',
      last_name: 'Doe',
    });
    
    // Trigger form submission
    await wrapper.find('form').trigger('submit.prevent');
    
    // Ensure axios.post is called with correct data
    expect(axios.post).toHaveBeenCalledWith('/users/register/', {
      username: 'testuser',
      password: 'testpassword',
      first_name: 'John',
      last_name: 'Doe',
      role: 'User',
    }, { headers: { 'Authorization': 'Bearer ' } }); // Adjust token as per your implementation
    
    // Simulate axios error response
    await axios.post.mockRejectedValueOnce(new Error('Registration failed'));
    
    // Check that the form does not clear on failure
    expect(wrapper.vm.username).toBe('testuser');
    expect(wrapper.vm.password).toBe('testpassword');
    expect(wrapper.vm.first_name).toBe('John');
    expect(wrapper.vm.last_name).toBe('Doe');
    
    // Ensure no router navigation on failure
    expect(wrapper.vm.$router.push).not.toHaveBeenCalled();
  });
});
