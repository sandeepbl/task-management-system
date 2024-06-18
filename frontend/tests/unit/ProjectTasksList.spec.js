// Import necessary modules for testing
import { mount } from '@vue/test-utils';
import ProjectTasksList from './ProjectTasksList.spec.js'; // Adjust path as needed
import axios from 'axios';

// Mocking Axios for testing purposes
jest.mock('axios', () => ({
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
}));

describe('ProjectTasksList.vue', () => {
  // Test case 1: Mounting the component
  it('renders the component', () => {
    const wrapper = mount(ProjectTasksList);
    expect(wrapper.exists()).toBe(true);
  });

  // Test case 2: Check initial data and API call in mounted hook
  it('fetches tasks on component mount', async () => {
    axios.get.mockResolvedValue({ data: { project_tasks: [{ id: 1, title: 'Task 1', description: 'Description 1', project_title: 'Project A', assigned_user: 'User 1' }] } });

    const wrapper = mount(ProjectTasksList);

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.selected_tasks).toHaveLength(1);
    expect(wrapper.vm.userAuthenticated).toBe(true);
  });

  // Test case 3: Create task method
  it('creates a new task', async () => {
    axios.post.mockResolvedValue({ data: { message: 'Task created successfully' } });

    const wrapper = mount(ProjectTasksList);

    await wrapper.vm.createTask({
      title: 'New Task',
      description: 'New Task Description',
      project_id: '123',
      assigned_user_id: '456',
    });

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.alertBox.visible).toBe(true);
    expect(wrapper.vm.alertBox.type).toBe('alert alert-success alert-dismissible fade show');
    expect(wrapper.vm.alertBox.subject).toBe('Task Created');
    expect(wrapper.vm.alertBox.message).toBe('Task created successfully');
  });

  // Test case 4: Modify task method
  it('modifies an existing task', async () => {
    const task = { id: 1, title: 'Task 1', description: 'Updated Description', project_id: '123', assigned_user_id: '456' };
    axios.put.mockResolvedValue({ data: { message: 'Task updated successfully' } });

    const wrapper = mount(ProjectTasksList);

    await wrapper.vm.modifyTask(task);

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.alertBox.visible).toBe(true);
    expect(wrapper.vm.alertBox.type).toBe('alert alert-success alert-dismissible fade show');
    expect(wrapper.vm.alertBox.subject).toBe('Task Updated');
    expect(wrapper.vm.alertBox.message).toBe('Task updated successfully');
  });

  // Test case 5: Delete task method
  it('deletes an existing task', async () => {
    const task = { id: 1, title: 'Task 1' };
    axios.delete.mockResolvedValue({ data: { message: 'Task deleted successfully' } });

    const wrapper = mount(ProjectTasksList);

    // Mocking window.confirm
    window.confirm = jest.fn(() => true);

    await wrapper.vm.deleteTask(task);

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.alertBox.visible).toBe(true);
    expect(wrapper.vm.alertBox.type).toBe('alert alert-success alert-dismissible fade show');
    expect(wrapper.vm.alertBox.subject).toBe('Task Deleted');
    expect(wrapper.vm.alertBox.message).toBe('Task deleted successfully');
  });

  // Test case 6: Error handling in create task method
  it('handles error during task creation', async () => {
    axios.post.mockRejectedValue({ response: { data: { error: 'token_expired' } } });

    const wrapper = mount(ProjectTasksList);

    await wrapper.vm.createTask({
      title: 'New Task',
      description: 'New Task Description',
      project_id: '123',
      assigned_user_id: '456',
    });

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.userAuthenticated).toBe(false);
    // Add more assertions for error handling if needed
  });
});
