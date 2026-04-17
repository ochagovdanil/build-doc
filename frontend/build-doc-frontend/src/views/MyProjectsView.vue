<template>
	<div class="projects-container">
		<h1>Мои проекты</h1>

		<!-- Create Project Form -->
		<form @submit.prevent="createProject" class="create-project-form">
			<input
				v-model="newProjectName"
				placeholder="Название проекта"
				required
			/>
			<button type="submit">Создать проект</button>
		</form>

		<!-- Projects Grid -->
		<div v-if="projects.length === 0" class="empty">
			У вас пока нет проектов.
		</div>
		<div v-else>
			<div class="projects-header">
				<div class="results-info">
					Всего проектов: {{ projects.length }}
				</div>
			</div>

			<div class="projects-grid">
				<div
					v-for="project in projects"
					:key="project.id"
					class="project-item"
				>
					<div class="project-content">
						<router-link
							:to="`/project/${project.id}`"
							class="project-link"
						>
							{{ project.name }}
						</router-link>
						<div class="project-details">
							<span class="files-count">
								{{ project.files_count }}
								{{ getFileWord(project.files_count) }}
							</span>
							<span class="project-date">
								Создан: {{ formatDate(project.created_at) }}
							</span>
						</div>
					</div>
					<div class="project-actions">
						<button
							@click="deleteProject(project.id)"
							class="delete-btn"
						>
							Удалить
						</button>
					</div>
				</div>
			</div>
		</div>
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
		await loadProjects();
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

function getFileWord(count) {
	if (count === 0) return 'файлов';
	if (count === 1) return 'файл';
	if (count >= 2 && count <= 4) return 'файла';
	return 'файлов';
}

onMounted(loadProjects);
</script>

<style scoped>
.projects-container,
.projects-container * {
	box-sizing: border-box;
}

.projects-container {
	max-width: 1400px;
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
	text-align: center;
}

/* CREATE FORM */
.create-project-form {
	display: flex;
	gap: 12px;
	margin-bottom: 32px;
	padding: 24px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 24px;
	box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05),
		0 12px 32px rgba(15, 23, 42, 0.08);
	justify-content: center;
}

.create-project-form input {
	flex: 1;
	max-width: 400px;
	height: 48px;
	padding: 0 14px;
	border-radius: 14px;
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
	height: 48px;
	padding: 0 24px;
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
	padding: 60px 40px;
	text-align: center;
	color: #5f6368;
	font-size: 15px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 24px;
}

/* HEADER */
.projects-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 24px;
	flex-wrap: wrap;
	gap: 16px;
}

.results-info {
	font-size: 14px;
	color: #5f6368;
}

/* PROJECTS GRID */
.projects-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
	gap: 24px;
	justify-items: center;
	align-items: start;
}

/* PROJECT CARD */
.project-item {
	width: 100%;
	max-width: 500px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 20px;
	padding: 20px;
	transition: 0.2s;
	box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
	display: flex;
	flex-direction: column;
	gap: 16px;
}

.project-item:hover {
	transform: translateY(-4px);
	box-shadow: 0 12px 24px rgba(103, 80, 164, 0.12);
}

/* PROJECT CONTENT */
.project-content {
	flex: 1;
	display: flex;
	flex-direction: column;
	gap: 12px;
}

.project-link {
	font-size: 18px;
	font-weight: 600;
	color: #1d1b20;
	text-decoration: none;
	display: block;
	word-break: break-word;
}

.project-link:hover {
	color: #6750a4;
}

.project-details {
	display: flex;
	flex-wrap: wrap;
	gap: 12px;
	align-items: center;
}

.files-count {
	padding: 6px 12px;
	border-radius: 999px;
	background: #f3edff;
	color: #4f378b;
	font-size: 13px;
	font-weight: 500;
	border: 1px solid rgba(103, 80, 164, 0.12);
	display: inline-flex;
	align-items: center;
	gap: 6px;
}

.project-date {
	font-size: 13px;
	color: #5f6368;
	display: inline-flex;
	align-items: center;
	gap: 6px;
}

/* PROJECT ACTIONS */
.project-actions {
	display: flex;
	gap: 12px;
	justify-content: flex-end;
	margin-top: 8px;
}

.delete-btn {
	height: 40px;
	padding: 0 20px;
	border-radius: 999px;
	border: none;
	background: #fce8e6;
	color: #b3261e;
	font-weight: 600;
	cursor: pointer;
	transition: 0.2s;
	flex: 1;
}

.delete-btn:hover {
	background: #f8d7d4;
	transform: translateY(-1px);
}

/* ADAPTIVE */
@media (max-width: 900px) {
	.projects-container {
		padding: 20px 16px;
	}

	.projects-grid {
		grid-template-columns: 1fr;
		justify-items: center;
	}

	.project-item {
		max-width: 100%;
	}

	.create-project-form {
		flex-direction: column;
		align-items: stretch;
	}

	.create-project-form input {
		max-width: 100%;
	}

	.create-project-form button {
		width: 100%;
	}

	.project-details {
		flex-direction: column;
		align-items: flex-start;
	}

	.project-actions {
		justify-content: stretch;
	}
}
</style>
