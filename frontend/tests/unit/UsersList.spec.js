import { mount } from '@vue/test-utils';
import UsersList from '@/components/UsersList.vue';
import axios from 'axios';

jest.mock('axios');

describe('UsersList.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(UsersList, {
      global: {
        mocks: {
          $router: {
            push: jest.fn(),
          },
          $store: {
            state: {
              users: [],
            },
          },
        },
      },
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('modifies a user successfully', async () => {
    const mockUser = {
      id: 1,
      username: 'testuser',
      first_name: 'Test',
      last_name: 'User',
      role: 'user',
    };
    axios.put.mockResolvedValue({ data: { message: 'User updated successfully' } });

    // Trigger modifyUser method with mockUser
    await wrapper.vm.modifyUser(mockUser);

    // Ensure axios.put is called with correct endpoint and data
    expect(axios.put).toHaveBeenCalledWith('/users/1/', {
      username: 'testuser',
      first_name: 'Test',
      last_name: 'User',
      role: 'user',
    }, { headers: { 'Authorization': 'Bearer ' } }); // Adjust token as per your implementation

    // Simulate axios response
    await axios.put.mockResolvedValueOnce({ data: { message: 'User updated successfully' } });

    // Assert that alert box is shown and users are refreshed
    expect(wrapper.vm.alertBox.visible).toBe(true);
    expect(wrapper.vm.alertBox.type).toBe('alert alert-success alert-dismissible fade show');
    expect(wrapper.vm.alertBox.subject).toBe('User Updated');
    expect(wrapper.vm.alertBox.message).toBe('User updated successfully');
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/users');
  });

  it('handles user modification failure', async () => {
    const mockUser = {
      id: 1,
      username: 'testuser',
      first_name: 'Test',
      last_name: 'User',
      role: 'user',
    };
    axios.put.mockRejectedValue(new Error('User update failed'));

    // Trigger modifyUser method with mockUser
    await wrapper.vm.modifyUser(mockUser);

    // Ensure axios.put is called with correct endpoint and data
    expect(axios.put).toHaveBeenCalledWith('/users/1/', {
      username: 'testuser',
      first_name: 'Test',
      last_name: 'User',
      role: 'user',
    }, { headers: { 'Authorization': 'Bearer ' } }); // Adjust token as per your implementation

    // Simulate axios error response
    await axios.put.mockRejectedValueOnce(new Error('User update failed'));

    // Assert that alert box is shown with appropriate error message
    expect(wrapper.vm.alertBox.visible).toBe(true);
    expect(wrapper.vm.alertBox.type).toBe('alert alert-warning alert-dismissible fade show');
    expect(wrapper.vm.alertBox.subject).toBe('User Update failed...');
    // Adjust the error message based on your error handling in the component
    expect(wrapper.vm.alertBox.message).toBe('User Update failed...'); 

    // Ensure users are not pushed to $router on failure
    expect(wrapper.vm.$router.push).not.toHaveBeenCalled();
  });

  // Additional tests can be added for getAllUsers method, error handling scenarios, etc.
});
