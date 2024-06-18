import { mount } from '@vue/test-utils';
import TasksList from '@/components/TasksList.vue';
import axios from 'axios';

jest.mock('axios');

describe('TasksList.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(TasksList, {
      global: {
        mocks: {
          $router: {
            push: jest.fn(),
          },
          $store: {
            state: {
              tasks: [],
            },
          },
        },
      },
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('creates a new task successfully', async () => {
    axios.post.mockResolvedValue({ data: { message: 'Task created successfully' } });
    
    // Set input values and trigger form submission
    await wrapper.setData({
      newTask: {
        title: 'New Task Title',
        description: 'New Task Description',
        project_id: '123',
        assigned_user_id: '456',
      },
    });
    await wrapper.find('form').trigger('submit.prevent');
    
    // Ensure axios.post is called with correct data
    expect(axios.post).toHaveBeenCalledWith('/tasks/create/', {
      title: 'New Task Title',
      description: 'New Task Description',
      project_id: '123',
      assigned_user_id: '456',
    }, { headers: { 'Authorization': 'Bearer ' } }); // Adjust token as per your implementation
    
    // Simulate axios response
    await axios.post.mockResolvedValueOnce({ data: { message: 'Task created successfully' } });
    
    // Assert that alert box is shown and tasks are refreshed
    expect(wrapper.vm.alertBox.visible).toBe(true);
    expect(wrapper.vm.alertBox.type).toBe('alert alert-success alert-dismissible fade show');
    expect(wrapper.vm.alertBox.subject).toBe('Task Created');
    expect(wrapper.vm.alertBox.message).toBe('Task created successfully');
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/tasks');
  });

  it('handles task creation failure', async () => {
    axios.post.mockRejectedValue(new Error('Task creation failed'));
    
    // Set input values and trigger form submission
    await wrapper.setData({
      newTask: {
        title: 'New Task Title',
        description: 'New Task Description',
        project_id: '123',
        assigned_user_id: '456',
      },
    });
    await wrapper.find('form').trigger('submit.prevent');
    
    // Ensure axios.post is called with correct data
    expect(axios.post).toHaveBeenCalledWith('/tasks/create/', {
      title: 'New Task Title',
      description: 'New Task Description',
      project_id: '123',
      assigned_user_id: '456',
    }, { headers: { 'Authorization': 'Bearer ' } }); // Adjust token as per your implementation
    
    // Simulate axios error response
    await axios.post.mockRejectedValueOnce(new Error('Task creation failed'));
    
    // Assert that alert box is shown with appropriate error message
    expect(wrapper.vm.alertBox.visible).toBe(true);
    expect(wrapper.vm.alertBox.type).toBe('alert alert-warning alert-dismissible fade show');
    expect(wrapper.vm.alertBox.subject).toBe('User is not a Registered User');
    expect(wrapper.vm.alertBox.message).toBe('Not Authorized to Delete Tasks! Please contact the Team');
    
    // Ensure tasks are not pushed to $router on failure
    expect(wrapper.vm.$router.push).not.toHaveBeenCalled();
  });

  it('deletes a task successfully', async () => {
    const mockTask = { id: 1, title: 'Task to delete' };
    axios.delete.mockResolvedValue({ data: { message: 'Task deleted successfully' } });
    
    // Simulate a confirm dialog (mocking confirm)
    window.confirm = jest.fn(() => true);
    
    // Trigger deleteTask method with mockTask
    await wrapper.vm.deleteTask(mockTask);
    
    // Ensure axios.delete is called with correct endpoint
    expect(axios.delete).toHaveBeenCalledWith('/tasks/1/', { headers: { 'Authorization': 'Bearer ' } }); // Adjust token as per your implementation
    
    // Simulate axios response
    await axios.delete.mockResolvedValueOnce({ data: { message: 'Task deleted successfully' } });
    
    // Assert that alert box is shown and tasks are refreshed
    expect(wrapper.vm.alertBox.visible).toBe(true);
    expect(wrapper.vm.alertBox.type).toBe('alert alert-success alert-dismissible fade show');
    expect(wrapper.vm.alertBox.subject).toBe('Task Deleted');
    expect(wrapper.vm.alertBox.message).toBe('Task deleted successfully');
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/tasks');
  });

  it('handles task deletion failure', async () => {
    const mockTask = { id: 1, title: 'Task to delete' };
    axios.delete.mockRejectedValue(new Error('Task deletion failed'));
    
    // Simulate a confirm dialog (mocking confirm)
    window.confirm = jest.fn(() => true);
    
    // Trigger deleteTask method with mockTask
    await wrapper.vm.deleteTask(mockTask);
    
    // Ensure axios.delete is called with correct endpoint
    expect(axios.delete).toHaveBeenCalledWith('/tasks/1/', { headers: { 'Authorization': 'Bearer ' } }); // Adjust token as per your implementation
    
    // Simulate axios error response
    await axios.delete.mockRejectedValueOnce(new Error('Task deletion failed'));
    
    // Assert that alert box is shown with appropriate error message
    expect(wrapper.vm.alertBox.visible).toBe(true);
    expect(wrapper.vm.alertBox.type).toBe('alert alert-warning alert-dismissible fade show');
    expect(wrapper.vm.alertBox.subject).toBe('User is not a Manager');
    expect(wrapper.vm.alertBox.message).toBe('Not Authorized to Delete Tasks! Please contact the Task Manager');
    
    // Ensure tasks are not pushed to $router on failure
    expect(wrapper.vm.$router.push).not.toHaveBeenCalled();
  });

  // Additional tests can be added for modifyTask, getAllTasks, and error handling scenarios
});
