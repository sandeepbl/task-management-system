import { mount, shallowMount } from '@vue/test-utils';
import ProjectsList from '@/components/ProjectsList.vue';
import axios from 'axios';

jest.mock('axios');

describe('ProjectsList.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(ProjectsList, {
      global: {
        mocks: {
          $router: {
            push: jest.fn(),
          },
          $store: {
            state: {
              projects: [],
            },
          },
        },
        stubs: ['router-link'],
      },
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('renders the component properly when user is authenticated', async () => {
    wrapper.setData({ userAuthenticated: true });
    await wrapper.vm.$nextTick();
    expect(wrapper.find('h1').text()).toBe('Projects');
  });

  it('creates a new project when createProject method is called', async () => {
    axios.post.mockResolvedValue({ data: { message: 'Project created successfully' } });
    wrapper.setData({
      userAuthenticated: true,
      newProject: { title: 'New Project', description: 'Project description', manager_user_id: '1' },
    });
    await wrapper.vm.createProject(wrapper.vm.newProject);
    expect(axios.post).toHaveBeenCalledWith('/projects/create/', {
      title: 'New Project',
      description: 'Project description',
      manager_user_id: '1',
    });
    expect(wrapper.vm.alertBox.visible).toBeTruthy();
    expect(wrapper.vm.alertBox.type).toBe('alert alert-success alert-dismissible fade show');
    expect(wrapper.vm.alertBox.subject).toBe('Project Created');
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/projects');
  });

  it('handles error when creating project fails due to token expiration', async () => {
    axios.post.mockRejectedValue({ response: { data: { error: 'token_expired' } } });
    wrapper.setData({ userAuthenticated: true });
    await wrapper.vm.createProject({});
    expect(axios.post).toHaveBeenCalled();
    expect(wrapper.vm.alertBox.visible).toBeTruthy();
    expect(wrapper.vm.alertBox.type).toBe('alert alert-warning alert-dismissible fade show');
    expect(wrapper.vm.alertBox.subject).toBe('User is not a Registered User');
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/projects');
  });

  it('modifies a project when modifyProject method is called', async () => {
    const project = { id: 1, title: 'Modified Project', description: 'Updated description', manager_user_id: '2' };
    axios.put.mockResolvedValue({ data: { message: 'Project updated successfully' } });
    wrapper.setData({ userAuthenticated: true });
    await wrapper.vm.modifyProject(project);
    expect(axios.put).toHaveBeenCalledWith('/projects/1/', {
      title: 'Modified Project',
      description: 'Updated description',
      manager_user_id: '2',
    });
    expect(wrapper.vm.alertBox.visible).toBeTruthy();
    expect(wrapper.vm.alertBox.type).toBe('alert alert-success alert-dismissible fade show');
    expect(wrapper.vm.alertBox.subject).toBe('Project Updated');
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/projects');
  });

  it('deletes a project when deleteProject method is called', async () => {
    const project = { id: 1, title: 'Project to Delete' };
    axios.delete.mockResolvedValue({ data: { message: 'Project deleted successfully' } });
    wrapper.setData({ userAuthenticated: true });
    window.confirm = jest.fn(() => true);
    await wrapper.vm.deleteProject(project);
    expect(axios.delete).toHaveBeenCalledWith('/projects/1/');
    expect(wrapper.vm.alertBox.visible).toBeTruthy();
    expect(wrapper.vm.alertBox.type).toBe('alert alert-success alert-dismissible fade show');
    expect(wrapper.vm.alertBox.subject).toBe('Project Deleted');
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/projects');
  });

  it('handles error when deleting project fails due to not being a manager', async () => {
    const project = { id: 1, title: 'Project to Delete' };
    axios.delete.mockRejectedValue({ response: { data: { error: 'not_manager_user' } } });
    wrapper.setData({ userAuthenticated: true });
    window.confirm = jest.fn(() => true);
    await wrapper.vm.deleteProject(project);
    expect(axios.delete).toHaveBeenCalled();
    expect(wrapper.vm.alertBox.visible).toBeTruthy();
    expect(wrapper.vm.alertBox.type).toBe('alert alert-warning alert-dismissible fade show');
    expect(wrapper.vm.alertBox.subject).toBe('User is not a Manager');
  });

  it('fetches all projects when getAllProjects method is called', async () => {
    const projects = [{ id: 1, title: 'Project 1', description: 'Description 1', manager: 'Manager 1' }];
    axios.get.mockResolvedValue({ data: { projects } });
    wrapper.setData({ userAuthenticated: true });
    await wrapper.vm.getAllProjects();
    expect(axios.get).toHaveBeenCalledWith('/projects/', { headers: { 'Authorization': 'Bearer ' } });
    expect(wrapper.vm.$store.state.projects).toEqual(projects);
    expect(wrapper.vm.userAuthenticated).toBeTruthy();
  });

  it('handles error when fetching projects fails', async () => {
    axios.get.mockRejectedValue(new Error('Failed to fetch projects'));
    wrapper.setData({ userAuthenticated: true });
    await wrapper.vm.getAllProjects();
    expect(axios.get).toHaveBeenCalled();
    expect(wrapper.vm.userAuthenticated).toBeTruthy();
  });

  it('mounts the component and performs initial API calls and checks', async () => {
    axios.get.mockResolvedValue({ data: { message: 'Backend is up and running' } });
    axios.get.mockResolvedValueOnce({ data: { message: 'User has access' } });
    wrapper.setData({ userAuthenticated: true });
    await wrapper.vm.$options.mounted.call(wrapper.vm);
    expect(axios.get).toHaveBeenCalledWith('/healthcheck/');
    expect(axios.get).toHaveBeenCalledWith('/access/', { headers: { 'Authorization': 'Bearer ' } });
    expect(wrapper.vm.userAuthenticated).toBeTruthy();
  });

  it('handles error when initial healthcheck fails', async () => {
    axios.get.mockRejectedValue(new Error('Healthcheck failed'));
    wrapper.setData({ userAuthenticated: true });
    await wrapper.vm.$options.mounted.call(wrapper.vm);
    expect(axios.get).toHaveBeenCalled();
    expect(wrapper.vm.userAuthenticated).toBeFalsy();
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/login');
  });
});
