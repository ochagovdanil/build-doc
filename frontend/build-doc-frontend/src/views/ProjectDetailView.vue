<template>
	<div class="project-detail-container" v-if="project">
		<h1>{{ project.name }}</h1>
		<p>Создан: {{ formatDate(project.created_at) }}</p>

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

		<h2>Файлы в проекте</h2>
		<div v-if="project.project_files.length === 0" class="empty">
			Нет файлов в проекте.
		</div>
		<div class="filter-section">
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
		</div>
		<div class="project-actions">
			<button @click="downloadAllFiles" class="download-all-btn">
				Скачать все файлы (ZIP)
			</button>
			<button @click="exportToExcel" class="export-btn">
				Выгрузить в Excel
			</button>
		</div>
		<ul class="files-list">
			<li
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
				<span class="stage-label">{{ stageLabel(pf.file.stage) }}</span>
				<button @click="removeFile(pf.file.id)" class="remove-btn">
					Убрать из проекта
				</button>
			</li>
		</ul>
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

onMounted(loadProject);
</script>

<style scoped>
.project-detail-container {
	max-width: 1100px;
	margin: 0 auto;
	padding: 20px;
}

.project-detail-container h1 {
	margin-bottom: 5px;
}

.project-detail-container p {
	color: #666;
	margin-bottom: 20px;
}

/* Добавление файла */
.add-file-section {
	display: flex;
	flex-wrap: wrap;
	gap: 10px;
	margin-bottom: 20px;
}

.file-search-input {
	padding: 8px 12px;
	border: 1px solid #ddd;
	border-radius: 8px;
	min-width: 220px;
}

.file-select {
	padding: 8px 12px;
	border: 1px solid #ddd;
	border-radius: 8px;
	min-width: 220px;
}

.add-btn {
	background: #4f46e5;
	color: white;
	border: none;
	padding: 8px 14px;
	border-radius: 8px;
	cursor: pointer;
	transition: 0.2s;
}

.add-btn:hover {
	background: #4338ca;
}

/* Фильтр */
.filter-section {
	margin-bottom: 15px;
}

.filter-select {
	padding: 8px 12px;
	border-radius: 8px;
	border: 1px solid #ddd;
}

/* Кнопки действий */
.project-actions {
	display: flex;
	gap: 10px;
	margin-bottom: 15px;
}

.download-all-btn {
	background: #22c55e;
	color: white;
	border: none;
	padding: 8px 14px;
	border-radius: 8px;
	cursor: pointer;
}

.export-btn {
	background: #3b82f6;
	color: white;
	border: none;
	padding: 8px 14px;
	border-radius: 8px;
	cursor: pointer;
}

/* Список файлов */
.files-list {
	list-style: none;
	padding: 0;
	display: flex;
	flex-direction: column;
	gap: 10px;
}

.file-item {
	display: flex;
	align-items: center;
	gap: 15px;
	padding: 10px 15px;
	border: 1px solid #eee;
	border-radius: 10px;
	background: #fff;
	transition: 0.2s;
}

.file-item:hover {
	background: #f9fafb;
}

.file-title-link {
	flex: 1;
	text-decoration: none;
	color: #333;
	font-weight: 500;
}

.stage-label {
	background: #eef2ff;
	color: #4f46e5;
	padding: 4px 8px;
	border-radius: 6px;
	font-size: 12px;
	white-space: nowrap;
}

.remove-btn {
	background: #ef4444;
	color: white;
	border: none;
	padding: 6px 10px;
	border-radius: 6px;
	cursor: pointer;
	transition: 0.2s;
}

.remove-btn:hover {
	background: #dc2626;
}

/* Пусто / загрузка */
.empty {
	text-align: center;
	color: #888;
	margin-top: 20px;
}

.loading {
	text-align: center;
	padding: 40px;
}
</style>
