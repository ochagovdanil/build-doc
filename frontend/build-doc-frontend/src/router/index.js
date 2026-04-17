import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import UploadView from '../views/UploadView.vue';
import FilesListView from '../views/FilesListView.vue';
import AllFilesListView from '../views/AllFilesListView.vue';
import MyFavoritesView from '../views/MyFavoritesView.vue';
import FileDetailView from '../views/FileDetailView.vue';
import MyProjectsView from '../views/MyProjectsView.vue';
import ProjectDetailView from '../views/ProjectDetailView.vue';

const routes = [
	{
		path: '/',
		name: 'Login',
		component: LoginView,
	},
	{
		path: '/register',
		name: 'Register',
		component: RegisterView,
	},
	{
		path: '/home',
		name: 'Home',
		component: HomeView,
		meta: { requiresAuth: true },
	},
	{
		path: '/upload',
		name: 'Upload',
		component: UploadView,
		meta: { requiresAuth: true },
	},
	{
		path: '/files',
		name: 'FilesList',
		component: FilesListView,
		meta: { requiresAuth: true },
	},
	{
		path: '/all-files',
		name: 'AllFilesList',
		component: AllFilesListView,
		meta: { requiresAuth: true },
	},
	{
		path: '/favorites',
		name: 'MyFavorites',
		component: MyFavoritesView,
		meta: { requiresAuth: true },
	},
	{
		path: '/file/:id',
		name: 'FileDetail',
		component: FileDetailView,
		meta: { requiresAuth: true },
	},
	{
		path: '/projects',
		name: 'MyProjects',
		component: MyProjectsView,
		meta: { requiresAuth: true },
	},
	{
		path: '/project/:id',
		name: 'ProjectDetail',
		component: ProjectDetailView,
		meta: { requiresAuth: true },
	},
];

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes,
});

router.beforeEach((to, from, next) => {
	const isAuthenticated = !!localStorage.getItem('access');

	if (to.meta.requiresAuth && !isAuthenticated) next({ name: 'Login' });
	else next();
});

export default router;
