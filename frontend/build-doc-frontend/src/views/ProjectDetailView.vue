<template>
	<div class="project-detail-container" v-if="project">
		<h1>{{ project.name }}</h1>

		<div class="project-info">
			<span class="project-date"
				>Создан: {{ formatDate(project.created_at) }}</span
			>
			<span class="project-files-count"
				>{{ project.project_files.length }}
				{{ getFileWord(project.project_files.length) }}</span
			>
		</div>

		<!-- Добавление файла в проект -->
		<div class="add-file-section">
			<input
				v-model="fileSearch"
				placeholder="Поиск файла..."
				class="file-search-input"
			/>
			<select v-model="selectedFileId" class="file-select">
				<option value="">Добавить файл в проект...</option>
				<option
					v-for="file in filteredAvailableFiles"
					:key="file.id"
					:value="file.id"
				>
					{{ file.title }}
				</option>
			</select>
			<button
				v-if="selectedFileId"
				@click="addFileToProject"
				class="add-btn"
			>
				Добавить
			</button>
		</div>

		<div class="files-header">
			<h2>Файлы в проекте</h2>
			<div class="filter-and-actions">
				<select v-model="selectedStage" class="filter-select">
					<option value="">Все этапы</option>
					<option
						v-for="stage in stageOptions"
						:key="stage.value"
						:value="stage.value"
					>
						{{ stage.label }}
					</option>
				</select>
				<div class="action-buttons">
					<button @click="downloadAllFiles" class="download-all-btn">
						Скачать все файлы (ZIP)
					</button>
					<button @click="exportToExcel" class="export-btn">
						Выгрузить в Excel
					</button>
				</div>
			</div>
		</div>

		<div v-if="filteredProjectFiles.length === 0" class="empty">
			Нет файлов в проекте.
		</div>
		<div v-else class="files-grid">
			<div
				v-for="pf in filteredProjectFiles"
				:key="pf.id"
				class="file-item"
			>
				<router-link
					:to="`/file/${pf.file.id}`"
					class="file-title-link"
				>
					{{ pf.file.title }}
				</router-link>
				<div class="file-details">
					<span class="stage-label">{{
						stageLabel(pf.file.stage)
					}}</span>
					<span class="file-date">{{
						formatDate(pf.file.uploaded_at)
					}}</span>
				</div>
				<div class="file-actions">
					<button @click="removeFile(pf.file.id)" class="remove-btn">
						Убрать из проекта
					</button>
				</div>
			</div>
		</div>
	</div>
	<div v-else class="loading">Загрузка...</div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const project = ref(null);
const availableFiles = ref([]);
const selectedFileId = ref('');
const fileSearch = ref('');
const selectedStage = ref('');

const stageOptions = [
	{ value: 'preproject', label: 'Предпроектная подготовка' },
	{ value: 'design', label: 'Проектирование' },
	{ value: 'expertise', label: 'Экспертиза и согласование' },
	{ value: 'preconstruction', label: 'Подготовка к строительству' },
	{ value: 'construction', label: 'Строительно-монтажные работы' },
	{ value: 'commissioning', label: 'Пусконаладочные работы' },
	{ value: 'handover', label: 'Сдача объекта' },
	{ value: 'operation', label: 'Эксплуатация' },
];

const filteredProjectFiles = computed(() => {
	if (!project.value) return [];
	if (!selectedStage.value) return project.value.project_files;
	return project.value.project_files.filter(
		pf => pf.file.stage === selectedStage.value,
	);
});

const filteredAvailableFiles = computed(() => {
	if (!fileSearch.value.trim()) return availableFiles.value;
	return availableFiles.value.filter(f =>
		f.title.toLowerCase().includes(fileSearch.value.trim().toLowerCase()),
	);
});

const loadProject = async () => {
	try {
		const token = localStorage.getItem('access');
		const response = await axios.get(
			`http://localhost:8000/api/files/projects/${route.params.id}/`,
			{
				headers: { Authorization: `Bearer ${token}` },
			},
		);
		project.value = response.data;
		await loadAvailableFiles();
	} catch (e) {
		project.value = null;
	}
};

const loadAvailableFiles = async () => {
	try {
		const token = localStorage.getItem('access');
		const response = await axios.get(
			'http://localhost:8000/api/files/list/',
			{
				headers: { Authorization: `Bearer ${token}` },
			},
		);
		// Исключаем уже добавленные файлы
		const projectFileIds = project.value.project_files.map(
			pf => pf.file.id,
		);
		availableFiles.value = response.data.filter(
			f => !projectFileIds.includes(f.id),
		);
	} catch (e) {
		availableFiles.value = [];
	}
};

const addFileToProject = async () => {
	if (!selectedFileId.value) return;
	try {
		const token = localStorage.getItem('access');
		await axios.post(
			`http://localhost:8000/api/files/projects/${route.params.id}/add_file/`,
			{ file_id: selectedFileId.value },
			{ headers: { Authorization: `Bearer ${token}` } },
		);
		selectedFileId.value = '';
		await loadProject();
	} catch (e) {
		alert(
			e.response?.data?.error || 'Ошибка при добавлении файла в проект',
		);
	}
};

const removeFile = async fileId => {
	if (!confirm('Убрать файл из проекта?')) return;
	try {
		const token = localStorage.getItem('access');
		await axios.delete(
			`http://localhost:8000/api/files/projects/${route.params.id}/remove_file/${fileId}/`,
			{ headers: { Authorization: `Bearer ${token}` } },
		);
		await loadProject();
	} catch (e) {
		alert('Ошибка при удалении файла из проекта');
	}
};

const downloadAllFiles = async () => {
	try {
		const token = localStorage.getItem('access');
		const response = await axios.get(
			`http://localhost:8000/api/files/projects/${route.params.id}/download_all/`,
			{
				headers: { Authorization: `Bearer ${token}` },
				responseType: 'blob',
			},
		);
		const url = window.URL.createObjectURL(new Blob([response.data]));
		const link = document.createElement('a');
		link.href = url;
		link.setAttribute('download', `project_${route.params.id}_files.zip`);
		document.body.appendChild(link);
		link.click();
		link.remove();
		window.URL.revokeObjectURL(url);
	} catch (e) {
		alert('Ошибка при скачивании всех файлов проекта');
	}
};

const exportToExcel = async () => {
	try {
		const token = localStorage.getItem('access');
		const response = await axios.get(
			`http://localhost:8000/api/files/projects/${route.params.id}/export_excel/`,
			{
				headers: { Authorization: `Bearer ${token}` },
				responseType: 'blob',
			},
		);
		const url = window.URL.createObjectURL(new Blob([response.data]));
		const link = document.createElement('a');
		link.href = url;
		link.setAttribute('download', `project_${route.params.id}_files.xlsx`);
		document.body.appendChild(link);
		link.click();
		link.remove();
		window.URL.revokeObjectURL(url);
	} catch (e) {
		alert('Ошибка при экспорте файлов проекта в Excel');
	}
};

function formatDate(dateStr) {
	const date = new Date(dateStr);
	return date.toLocaleString('ru-RU');
}

function stageLabel(stage) {
	const found = stageOptions.find(opt => opt.value === stage);
	return found ? found.label : stage;
}

function getFileWord(count) {
	if (count === 0) return 'файлов';
	if (count === 1) return 'файл';
	if (count >= 2 && count <= 4) return 'файла';
	return 'файлов';
}

onMounted(loadProject);
</script>

<style scoped>
.project-detail-container,
.project-detail-container * {
	box-sizing: border-box;
}

.project-detail-container {
	max-width: 1400px;
	margin: 0 auto;
	padding: 36px 32px 48px;
	font-family: Roboto, 'Segoe UI', Arial, sans-serif;
	color: #1d1b20;
}

/* Заголовок */
h1 {
	margin: 0 0 16px;
	font-size: 32px;
	font-weight: 700;
	letter-spacing: -0.02em;
	text-align: center;
}

h2 {
	margin: 0;
	font-size: 24px;
	font-weight: 600;
	color: #1d1b20;
}

/* Информация о проекте */
.project-info {
	display: flex;
	justify-content: center;
	gap: 24px;
	margin-bottom: 32px;
	padding: 16px 24px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 20px;
	box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
	flex-wrap: wrap;
}

.project-date,
.project-files-count {
	font-size: 14px;
	color: #5f6368;
	display: inline-flex;
	align-items: center;
	gap: 8px;
}

/* Добавление файла */
.add-file-section {
	display: flex;
	flex-wrap: wrap;
	gap: 14px;
	margin-bottom: 32px;
	padding: 24px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 24px;
	box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05),
		0 12px 32px rgba(15, 23, 42, 0.08);
	justify-content: center;
}

.file-search-input,
.file-select {
	height: 48px;
	padding: 0 14px;
	border: 1px solid #c4c7c5;
	border-radius: 14px;
	background: #ffffff;
	font-size: 14px;
	outline: none;
	transition: 0.2s;
	min-width: 220px;
}

.file-search-input {
	flex: 1;
	max-width: 300px;
}

.file-select {
	min-width: 260px;
}

.file-search-input:focus,
.file-select:focus {
	border-color: #6750a4;
	box-shadow: 0 0 0 4px rgba(103, 80, 164, 0.14);
}

.add-btn {
	height: 48px;
	padding: 0 24px;
	border-radius: 999px;
	border: none;
	background: #6750a4;
	color: white;
	font-weight: 600;
	cursor: pointer;
	box-shadow: 0 2px 6px rgba(103, 80, 164, 0.28);
	transition: 0.2s;
}

.add-btn:hover {
	background: #5b4696;
	box-shadow: 0 6px 16px rgba(103, 80, 164, 0.3);
}

/* Заголовок файлов */
.files-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 24px;
	flex-wrap: wrap;
	gap: 16px;
}

.filter-and-actions {
	display: flex;
	gap: 16px;
	align-items: center;
	flex-wrap: wrap;
}

.filter-select {
	height: 44px;
	padding: 0 14px;
	border: 1px solid #c4c7c5;
	border-radius: 14px;
	background: #ffffff;
	font-size: 14px;
	outline: none;
	transition: 0.2s;
	min-width: 200px;
}

.filter-select:focus {
	border-color: #6750a4;
	box-shadow: 0 0 0 4px rgba(103, 80, 164, 0.14);
}

.action-buttons {
	display: flex;
	gap: 12px;
}

.download-all-btn,
.export-btn {
	height: 44px;
	padding: 0 20px;
	border-radius: 999px;
	border: none;
	font-weight: 600;
	cursor: pointer;
	transition: 0.2s;
}

.download-all-btn {
	background: #6750a4;
	color: white;
	box-shadow: 0 2px 6px rgba(103, 80, 164, 0.28);
}

.download-all-btn:hover {
	background: #5b4696;
	box-shadow: 0 6px 16px rgba(103, 80, 164, 0.3);
}

.export-btn {
	background: #22c55e;
	color: white;
	box-shadow: 0 2px 6px rgba(34, 197, 94, 0.28);
}

.export-btn:hover {
	background: #16a34a;
	box-shadow: 0 6px 16px rgba(34, 197, 94, 0.3);
}

/* Сетка файлов */
.files-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
	gap: 24px;
	justify-items: center;
	align-items: start;
}

/* Карточка файла */
.file-item {
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

.file-item:hover {
	transform: translateY(-4px);
	box-shadow: 0 12px 24px rgba(103, 80, 164, 0.12);
}

/* Ссылка на файл */
.file-title-link {
	font-size: 18px;
	font-weight: 600;
	color: #1d1b20;
	text-decoration: none;
	display: block;
	word-break: break-word;
}

.file-title-link:hover {
	color: #6750a4;
}

/* Детали файла */
.file-details {
	display: flex;
	flex-wrap: wrap;
	gap: 12px;
	align-items: center;
}

.stage-label {
	padding: 6px 12px;
	border-radius: 999px;
	background: #f3edff;
	color: #4f378b;
	font-size: 12px;
	font-weight: 500;
	border: 1px solid rgba(103, 80, 164, 0.12);
	white-space: nowrap;
}

.file-date {
	font-size: 13px;
	color: #5f6368;
}

/* Действия с файлом */
.file-actions {
	display: flex;
	gap: 12px;
	justify-content: flex-end;
	margin-top: 8px;
}

.remove-btn {
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

.remove-btn:hover {
	background: #f8d7d4;
	transform: translateY(-1px);
}

/* Пустое состояние */
.empty {
	padding: 60px 40px;
	text-align: center;
	color: #5f6368;
	font-size: 15px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 24px;
}

.loading {
	padding: 40px;
	text-align: center;
	color: #5f6368;
	font-size: 15px;
}

/* Адаптив */
@media (max-width: 900px) {
	.project-detail-container {
		padding: 20px 16px;
	}

	.files-grid {
		grid-template-columns: 1fr;
		justify-items: center;
	}

	.file-item {
		max-width: 100%;
	}

	.add-file-section {
		flex-direction: column;
		align-items: stretch;
	}

	.file-search-input,
	.file-select,
	.add-btn {
		max-width: 100%;
	}

	.filter-and-actions {
		flex-direction: column;
		align-items: stretch;
	}

	.filter-select {
		width: 100%;
	}

	.action-buttons {
		flex-direction: column;
	}

	.download-all-btn,
	.export-btn {
		width: 100%;
	}

	.files-header {
		flex-direction: column;
		align-items: stretch;
	}

	h2 {
		text-align: center;
	}

	.file-details {
		flex-direction: column;
		align-items: flex-start;
	}
}
</style>
