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
	max-width: 700px;
	margin: 40px auto;
	padding: 20px;
}
.files-list {
	list-style: none;
	padding: 0;
}
.file-item {
	display: flex;
	align-items: center;
	gap: 10px;
	padding: 10px 0;
	border-bottom: 1px solid #eee;
}
.file-title-link {
	color: #007bff;
	text-decoration: none;
	font-weight: 500;
}
.file-title-link:hover {
	text-decoration: underline;
}
.remove-btn {
	background: #dc3545;
	color: white;
	border: none;
	border-radius: 4px;
	padding: 4px 10px;
	cursor: pointer;
}
.remove-btn:hover {
	background: #b71c1c;
}
.empty {
	color: #888;
	font-style: italic;
	margin-top: 20px;
}
.loading {
	text-align: center;
	padding: 40px;
	font-size: 18px;
	color: #666;
}
.add-file-section {
	display: flex;
	align-items: center;
	gap: 10px;
	margin-bottom: 20px;
}
.file-select {
	padding: 4px 8px;
	border-radius: 4px;
	border: 1px solid #ccc;
}
.add-btn {
	background: #28a745;
	color: white;
	border: none;
	border-radius: 4px;
	padding: 4px 10px;
	cursor: pointer;
}
.add-btn:hover {
	background: #1e7e34;
}
.file-search-input {
	padding: 4px 8px;
	border-radius: 4px;
	border: 1px solid #ccc;
	margin-right: 8px;
}
.filter-section {
	margin-bottom: 20px;
}
.filter-select {
	padding: 4px 8px;
	border-radius: 4px;
	border: 1px solid #ccc;
}
.stage-label {
	margin-left: 12px;
	background: #e3f2fd;
	color: #1976d2;
	padding: 4px 8px;
	border-radius: 12px;
	font-size: 0.95em;
	white-space: nowrap;
}
.project-actions {
	margin-bottom: 20px;
	display: flex;
	gap: 10px;
}
.download-all-btn,
.export-btn {
	background: #007bff;
	color: white;
	border: none;
	border-radius: 4px;
	padding: 8px 16px;
	cursor: pointer;
}
.download-all-btn:hover,
.export-btn:hover {
	background: #0056b3;
}
</style>
