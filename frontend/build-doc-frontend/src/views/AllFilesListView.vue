<template>
	<div class="files-list-container">
		<h1>Все файлы</h1>
		<!-- Фильтры -->
		<div class="filters">
			<input
				v-model="searchQuery"
				@input="debouncedSearch"
				placeholder="Поиск по названию..."
				class="search-input"
			/>
			<select
				v-model="selectedStage"
				@change="loadFiles"
				class="filter-select"
			>
				<option value="">Все этапы</option>
				<option
					v-for="stage in stageOptions"
					:key="stage.value"
					:value="stage.value"
				>
					{{ stage.label }}
				</option>
			</select>
			<input
				type="date"
				v-model="dateFrom"
				@change="loadFiles"
				class="filter-date"
			/>
			<input
				type="date"
				v-model="dateTo"
				@change="loadFiles"
				class="filter-date"
			/>
			<select v-model="sortBy" @change="loadFiles" class="filter-select">
				<option value="-uploaded_at">Дата (новые сначала)</option>
				<option value="uploaded_at">Дата (старые сначала)</option>
				<option value="title">Название (А-Я)</option>
				<option value="-title">Название (Я-А)</option>
			</select>
			<button @click="resetFilters" class="reset-btn">Сбросить</button>
		</div>
		<!-- Результаты -->
		<div v-if="loading" class="loading">Загрузка...</div>
		<div v-else-if="files.length === 0" class="empty">
			Нет файлов по заданным фильтрам.
		</div>
		<ul v-else class="files-list">
			<li v-for="file in files" :key="file.id" class="file-item">
				<router-link :to="`/file/${file.id}`" class="file-title-link">
					{{ file.title }}
				</router-link>
				<span class="stage">{{ stageLabel(file.stage) }}</span>
				<span class="date">{{ formatDate(file.uploaded_at) }}</span>
				<span class="owner">Пользователь: {{ fileOwner(file) }}</span>
				<button
					@click="toggleFavorite(file.id)"
					:class="
						file.is_favorite
							? 'favorite-btn active'
							: 'favorite-btn'
					"
				>
					{{ file.is_favorite ? '★' : '☆' }}
				</button>
				<button
					@click="downloadFile(file.id, file.title)"
					class="download-btn"
				>
					Скачать
				</button>
			</li>
		</ul>
		<div v-if="files.length > 0" class="results-info">
			Найдено: {{ files.length }} файлов
		</div>
		<button
			@click="downloadAllFiles"
			class="download-all-btn"
			v-if="files.length > 0"
		>
			Скачать все файлы (ZIP)
		</button>
		<button
			@click="exportToExcel"
			class="export-btn"
			v-if="files.length > 0"
		>
			Экспорт в Excel
		</button>
	</div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';

const files = ref([]);
const loading = ref(false);
const searchQuery = ref('');
const selectedStage = ref('');
const sortBy = ref('-uploaded_at');
const dateFrom = ref('');
const dateTo = ref('');

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

let debounceTimer = null;

const debouncedSearch = () => {
	clearTimeout(debounceTimer);
	debounceTimer = setTimeout(() => {
		loadFiles();
	}, 300);
};

const loadFiles = async () => {
	loading.value = true;
	try {
		const token = localStorage.getItem('access');
		const params = new URLSearchParams();

		if (searchQuery.value) params.append('search', searchQuery.value);
		if (selectedStage.value) params.append('stage', selectedStage.value);
		if (sortBy.value) params.append('sort', sortBy.value);
		if (dateFrom.value) params.append('date_from', dateFrom.value);
		if (dateTo.value) params.append('date_to', dateTo.value);

		const response = await axios.get(
			`http://localhost:8000/api/files/all/?${params}`,
			{
				headers: {
					Authorization: `Bearer ${token}`,
				},
			},
		);
		files.value = response.data;
	} catch (e) {
		files.value = [];
	} finally {
		loading.value = false;
	}
};

const downloadAllFiles = async () => {
	try {
		const token = localStorage.getItem('access');
		const response = await axios.get(
			'http://localhost:8000/api/files/download_all/',
			{
				headers: { Authorization: `Bearer ${token}` },
				responseType: 'blob',
			},
		);
		const url = window.URL.createObjectURL(new Blob([response.data]));
		const link = document.createElement('a');
		link.href = url;
		link.setAttribute('download', 'all_files.zip');
		document.body.appendChild(link);
		link.click();
		link.remove();
		window.URL.revokeObjectURL(url);
	} catch (e) {
		alert('Ошибка при скачивании всех файлов');
	}
};

const toggleFavorite = async id => {
	try {
		const token = localStorage.getItem('access');
		await axios.post(
			`http://localhost:8000/api/files/favorite/${id}/`,
			{},
			{
				headers: { Authorization: `Bearer ${token}` },
			},
		);
		loadFiles(); // перезагрузить список файлов
	} catch (e) {
		alert('Ошибка при изменении избранного');
	}
};

const exportToExcel = async () => {
	try {
		const token = localStorage.getItem('access');
		const params = new URLSearchParams();
		if (searchQuery.value) params.append('search', searchQuery.value);
		if (selectedStage.value) params.append('stage', selectedStage.value);
		if (sortBy.value) params.append('sort', sortBy.value);
		if (dateFrom.value) params.append('date_from', dateFrom.value);
		if (dateTo.value) params.append('date_to', dateTo.value);
		// ... другие фильтры, если есть

		const response = await axios.get(
			`http://localhost:8000/api/files/export_excel/?${params}`,
			{
				headers: { Authorization: `Bearer ${token}` },
				responseType: 'blob',
			},
		);
		const url = window.URL.createObjectURL(new Blob([response.data]));
		const link = document.createElement('a');
		link.href = url;
		link.setAttribute('download', 'all_files.xlsx');
		document.body.appendChild(link);
		link.click();
		link.remove();
		window.URL.revokeObjectURL(url);
	} catch (e) {
		alert('Ошибка при экспорте в Excel');
	}
};

const resetFilters = () => {
	searchQuery.value = '';
	selectedStage.value = '';
	sortBy.value = '-uploaded_at';
	dateFrom.value = '';
	dateTo.value = '';
	loadFiles();
};

function stageLabel(stage) {
	const found = stageOptions.find(opt => opt.value === stage);
	return found ? found.label : stage;
}

function fileUrl(path) {
	return `http://localhost:8000${path}`;
}

function formatDate(dateStr) {
	const date = new Date(dateStr);
	return date.toLocaleString('ru-RU');
}

// Для отображения владельца файла (если добавить в сериализатор)
function fileOwner(file) {
	// Если в API добавить поле owner_email или owner_username
	return file.owner_email || file.owner || 'неизвестно';
}

const downloadFile = async (id, title) => {
	try {
		const token = localStorage.getItem('access');
		const response = await axios.get(
			`http://localhost:8000/api/files/download/${id}/`,
			{
				headers: { Authorization: `Bearer ${token}` },
				responseType: 'blob',
			},
		);
		const contentDisposition = response.headers['content-disposition'];
		let filename = title;
		if (contentDisposition) {
			const match = contentDisposition.match(/filename="?([^"]+)"?/);
			if (match) filename = match[1];
		}
		const url = window.URL.createObjectURL(new Blob([response.data]));
		const link = document.createElement('a');
		link.href = url;
		link.setAttribute('download', filename);
		document.body.appendChild(link);
		link.click();
		link.remove();
		window.URL.revokeObjectURL(url);
	} catch (e) {
		alert('Ошибка при скачивании файла');
	}
};

onMounted(loadFiles);
watch([searchQuery, selectedStage, sortBy], loadFiles);
</script>

<style scoped>
/* Стили такие же, как в FilesListView.vue */
.files-list-container {
	max-width: 800px;
	margin: 40px auto;
	padding: 20px;
}
.filters {
	display: flex;
	flex-wrap: wrap;
	gap: 10px;
	margin-bottom: 30px;
	padding: 15px;
	background: #f8f9fa;
	border-radius: 8px;
}
.search-input,
.filter-select {
	padding: 8px 12px;
	border: 1px solid #ddd;
	border-radius: 4px;
	font-size: 14px;
}
.reset-btn {
	padding: 8px 16px;
	background: #dc3545;
	color: white;
	border: none;
	border-radius: 4px;
	cursor: pointer;
}
.reset-btn:hover {
	background: #c82333;
}
.loading,
.empty {
	text-align: center;
	padding: 40px;
	font-size: 18px;
	color: #666;
}
.files-list {
	list-style: none;
	padding: 0;
}
.file-item {
	display: flex;
	align-items: center;
	gap: 12px;
	padding: 15px;
	border: 1px solid #eee;
	border-radius: 6px;
	margin-bottom: 10px;
	background: white;
}
.file-title {
	flex: 1;
	font-weight: 500;
	color: #007bff;
	text-decoration: none;
}
.file-title:hover {
	text-decoration: underline;
}
.stage {
	background: #e3f2fd;
	color: #1976d2;
	padding: 4px 8px;
	border-radius: 12px;
	font-size: 0.85em;
	white-space: nowrap;
}
.date {
	color: #666;
	font-size: 0.9em;
}
.owner {
	color: #888;
	font-size: 0.9em;
}
.results-info {
	text-align: center;
	margin-top: 20px;
	padding: 10px;
	background: #d4edda;
	border-radius: 4px;
	color: #155724;
}
.download-btn {
	background: #28a745;
	color: white;
	border: none;
	border-radius: 4px;
	padding: 4px 10px;
	cursor: pointer;
	margin-right: 5px;
}
.download-btn:hover {
	background: #1e7e34;
}
.download-all-btn {
	background: #17a2b8;
	color: white;
	border: none;
	border-radius: 4px;
	padding: 8px 16px;
	margin-bottom: 15px;
	margin-right: 10px;
	cursor: pointer;
}
.download-all-btn:hover {
	background: #117a8b;
}
.favorite-btn {
	background: none;
	border: none;
	font-size: 22px;
	color: #aaa;
	cursor: pointer;
	margin-right: 5px;
}
.favorite-btn.active {
	color: #ffc107;
}
.export-btn {
	background: #007bff;
	color: white;
	border: none;
	border-radius: 4px;
	padding: 8px 16px;
	margin-bottom: 15px;
	margin-right: 10px;
	cursor: pointer;
}
.export-btn:hover {
	background: #0056b3;
}
</style>
