<template>
	<div class="projects-container">
		<h1>Мои проекты</h1>
		<form @submit.prevent="createProject" class="create-project-form">
			<input
				v-model="newProjectName"
				placeholder="Название проекта"
				required
			/>
			<button type="submit">Создать проект</button>
		</form>
		<div v-if="projects.length === 0" class="empty">
			У вас пока нет проектов.
		</div>
		<ul class="projects-list">
			<li
				v-for="project in projects"
				:key="project.id"
				class="project-item"
			>
				<router-link
					:to="`/project/${project.id}`"
					class="project-link"
				>
					{{ project.name }}
				</router-link>
				<span class="project-info">
					({{ project.files_count }} файлов, создан:
					{{ formatDate(project.created_at) }})
				</span>
				<button @click="deleteProject(project.id)" class="delete-btn">
					Удалить
				</button>
			</li>
		</ul>
	</div>
</template>

<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';

const projects = ref([]);
const newProjectName = ref('');

const loadProjects = async () => {
	try {
		const token = localStorage.getItem('access');
		const response = await axios.get(
			'http://localhost:8000/api/files/projects/',
			{
				headers: { Authorization: `Bearer ${token}` },
			},
		);
		projects.value = response.data;
	} catch (e) {
		projects.value = [];
	}
};

const createProject = async () => {
	if (!newProjectName.value.trim()) return;
	try {
		const token = localStorage.getItem('access');
		await axios.post(
			'http://localhost:8000/api/files/projects/',
			{ name: newProjectName.value },
			{
				headers: { Authorization: `Bearer ${token}` },
			},
		);
		newProjectName.value = '';
		await loadProjects(); // <--- обязательно!
	} catch (e) {
		alert('Ошибка при создании проекта');
	}
};

const deleteProject = async id => {
	if (!confirm('Удалить проект?')) return;
	try {
		const token = localStorage.getItem('access');
		await axios.delete(`http://localhost:8000/api/files/projects/${id}/`, {
			headers: { Authorization: `Bearer ${token}` },
		});
		loadProjects();
	} catch (e) {
		alert('Ошибка при удалении проекта');
	}
};

function formatDate(dateStr) {
	const date = new Date(dateStr);
	return date.toLocaleString('ru-RU');
}

onMounted(loadProjects);
</script>

<style scoped>
.projects-container {
	max-width: 700px;
	margin: 40px auto;
	padding: 20px;
}
.create-project-form {
	display: flex;
	gap: 10px;
	margin-bottom: 25px;
}
.projects-list {
	list-style: none;
	padding: 0;
}
.project-item {
	display: flex;
	align-items: center;
	gap: 10px;
	padding: 12px;
	border-bottom: 1px solid #eee;
}
.project-link {
	font-weight: 500;
	color: #007bff;
	text-decoration: none;
}
.project-link:hover {
	text-decoration: underline;
}
.project-info {
	color: #888;
	font-size: 0.95em;
}
.rename-btn,
.delete-btn {
	margin-left: 10px;
	padding: 4px 10px;
	border: none;
	border-radius: 4px;
	cursor: pointer;
}
.rename-btn {
	background: #ffc107;
	color: #333;
}
.delete-btn {
	background: #dc3545;
	color: white;
}
.rename-btn:hover {
	background: #e0a800;
}
.delete-btn:hover {
	background: #b71c1c;
}
.empty {
	color: #888;
	font-style: italic;
	margin-top: 20px;
}
.modal {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background: rgba(0, 0, 0, 0.3);
	display: flex;
	align-items: center;
	justify-content: center;
}
.modal-content {
	background: #fff;
	padding: 30px;
	border-radius: 8px;
	min-width: 300px;
	display: flex;
	flex-direction: column;
	gap: 10px;
}
</style>
