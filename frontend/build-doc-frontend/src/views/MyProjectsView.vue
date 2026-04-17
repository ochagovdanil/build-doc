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
.projects-container,
.projects-container * {
	box-sizing: border-box;
}

.projects-container {
	max-width: 1000px;
	margin: 0 auto;
	padding: 36px 32px 48px;
	font-family: Roboto, 'Segoe UI', Arial, sans-serif;
	color: #1d1b20;
}

/* TITLE */

h1 {
	margin: 0 0 24px;
	font-size: 32px;
	font-weight: 700;
	letter-spacing: -0.02em;
}

/* CREATE FORM */

.create-project-form {
	display: flex;
	gap: 12px;
	margin-bottom: 24px;
	padding: 20px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 20px;
	box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
}

.create-project-form input {
	flex: 1;
	height: 44px;
	padding: 0 14px;
	border-radius: 12px;
	border: 1px solid #c4c7c5;
	font-size: 14px;
	outline: none;
	transition: 0.2s;
}

.create-project-form input:focus {
	border-color: #6750a4;
	box-shadow: 0 0 0 4px rgba(103, 80, 164, 0.14);
}

.create-project-form button {
	height: 44px;
	padding: 0 20px;
	border-radius: 999px;
	border: none;
	background: #6750a4;
	color: #ffffff;
	font-weight: 600;
	cursor: pointer;
	box-shadow: 0 2px 6px rgba(103, 80, 164, 0.28);
	transition: 0.2s;
}

.create-project-form button:hover {
	background: #5b4696;
	box-shadow: 0 6px 16px rgba(103, 80, 164, 0.3);
}

/* EMPTY */

.empty {
	padding: 32px;
	text-align: center;
	color: #5f6368;
	font-size: 15px;
}

/* LIST */

.projects-list {
	list-style: none;
	padding: 0;
	margin: 0;
	display: flex;
	flex-direction: column;
	gap: 16px;
}

/* CARD */

.project-item {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 14px;
	padding: 20px 22px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 20px;
	box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
	transition: 0.2s;
}

.project-item:hover {
	transform: translateY(-2px);
	box-shadow: 0 12px 24px rgba(103, 80, 164, 0.12);
}

/* TEXT */

.project-link {
	font-size: 16px;
	font-weight: 600;
	color: #1d1b20;
	text-decoration: none;
}

.project-link:hover {
	color: #6750a4;
}

.project-info {
	font-size: 13px;
	color: #5f6368;
}

/* DELETE */

.delete-btn {
	height: 40px;
	padding: 0 16px;
	border-radius: 999px;
	border: none;
	background: #fce8e6;
	color: #b3261e;
	font-weight: 600;
	cursor: pointer;
	transition: 0.2s;
}

.delete-btn:hover {
	background: #f8d7d4;
}

/* ADAPTIVE */

@media (max-width: 700px) {
	.projects-container {
		padding: 24px 20px;
	}

	.project-item {
		flex-direction: column;
		align-items: flex-start;
	}
}
</style>
