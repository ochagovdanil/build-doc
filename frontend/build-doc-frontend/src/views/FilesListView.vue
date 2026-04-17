<template>
	<div class="files-list-container">
		<h1>Мои файлы</h1>

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
		<div v-else>
			<div class="actions-header">
				<div class="results-info">
					Найдено: {{ files.length }} файлов
				</div>
				<div class="action-buttons">
					<button @click="downloadAllFiles" class="download-all-btn">
						Скачать все файлы (ZIP)
					</button>
					<button @click="deleteAllFiles" class="delete-all-btn">
						Удалить все файлы
					</button>
					<button @click="exportMyToExcel" class="export-btn">
						Экспорт в Excel
					</button>
				</div>
			</div>

			<div class="files-grid">
				<div v-for="file in files" :key="file.id" class="file-item">
					<router-link
						:to="`/file/${file.id}`"
						class="file-title-link"
					>
						{{ file.title }}
					</router-link>
					<div class="file-details">
						<span class="stage">{{ stageLabel(file.stage) }}</span>
						<span class="date">{{
							formatDate(file.uploaded_at)
						}}</span>
					</div>
					<div class="file-actions">
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
						<button @click="deleteFile(file.id)" class="delete-btn">
							Удалить
						</button>
					</div>
				</div>
			</div>
		</div>
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

// Функция поиска с задержкой (debounce)
const debouncedSearch = () => {
	clearTimeout(debounceTimer);
	debounceTimer = setTimeout(() => {
		loadFiles();
	}, 300);
};

// Загрузка файлов с параметрами
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
			`http://localhost:8000/api/files/list/?${params}`,
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

const deleteFile = async id => {
	if (!confirm('Удалить этот файл?')) return;
	try {
		const token = localStorage.getItem('access');
		await axios.delete(`http://localhost:8000/api/files/delete/${id}/`, {
			headers: { Authorization: `Bearer ${token}` },
		});
		files.value = files.value.filter(f => f.id !== id);
	} catch (e) {
		alert('Ошибка при удалении файла');
	}
};

const deleteAllFiles = async () => {
	if (!confirm('Удалить все файлы?')) return;
	try {
		const token = localStorage.getItem('access');
		await axios.delete('http://localhost:8000/api/files/delete_all/', {
			headers: { Authorization: `Bearer ${token}` },
		});
		files.value = [];
	} catch (e) {
		alert('Ошибка при удалении всех файлов');
	}
};

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
		// Получаем расширение из заголовков или из URL
		const contentDisposition = response.headers['content-disposition'];
		let filename = title;
		if (contentDisposition) {
			const match = contentDisposition.match(/filename="?([^"]+)"?/);
			if (match) filename = match[1];
		}
		// Создаём ссылку для скачивания
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

const exportMyToExcel = async () => {
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
			`http://localhost:8000/api/files/export_my_excel/?${params}`,
			{
				headers: { Authorization: `Bearer ${token}` },
				responseType: 'blob',
			},
		);
		const url = window.URL.createObjectURL(new Blob([response.data]));
		const link = document.createElement('a');
		link.href = url;
		link.setAttribute('download', 'my_files.xlsx');
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

// Загрузка при монтировании и при изменении фильтров
onMounted(loadFiles);
watch([searchQuery, selectedStage, sortBy], loadFiles);
</script>

<style scoped>
.files-list-container,
.files-list-container * {
	box-sizing: border-box;
}

.files-list-container {
	max-width: 1400px;
	margin: 0 auto;
	padding: 36px 32px 48px;
	font-family: Roboto, 'Segoe UI', Arial, sans-serif;
	color: #1d1b20;
}

/* Заголовок */
h1 {
	margin: 0 0 24px;
	font-size: 32px;
	font-weight: 700;
	letter-spacing: -0.02em;
	text-align: center;
}

/* ФИЛЬТРЫ */
.filters {
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

.search-input,
.filter-select,
.filter-date {
	height: 48px;
	padding: 0 14px;
	border: 1px solid #c4c7c5;
	border-radius: 14px;
	background: #ffffff;
	font-size: 14px;
	outline: none;
	transition: 0.2s;
}

.search-input {
	flex: 1;
	min-width: 220px;
	max-width: 300px;
}

.filter-select,
.filter-date {
	min-width: 180px;
}

.search-input:focus,
.filter-select:focus,
.filter-date:focus {
	border-color: #6750a4;
	box-shadow: 0 0 0 4px rgba(103, 80, 164, 0.14);
}

/* КНОПКА СБРОСА */
.reset-btn {
	height: 48px;
	padding: 0 18px;
	border-radius: 999px;
	border: none;
	background: #ece6f0;
	color: #4f378b;
	font-weight: 600;
	cursor: pointer;
	transition: 0.2s;
}

.reset-btn:hover {
	background: #e0d7f5;
}

/* СОСТОЯНИЯ */
.loading,
.empty {
	padding: 40px;
	text-align: center;
	color: #5f6368;
	font-size: 15px;
}

/* HEADER с действиями */
.actions-header {
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

.action-buttons {
	display: flex;
	gap: 12px;
	flex-wrap: wrap;
}

/* СЕТКА ФАЙЛОВ */
.files-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
	gap: 24px;
	justify-items: center;
	align-items: start;
}

/* КАРТОЧКА ФАЙЛА */
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

/* ЗАГОЛОВОК ФАЙЛА */
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

/* ДЕТАЛИ ФАЙЛА */
.file-details {
	display: flex;
	flex-wrap: wrap;
	gap: 12px;
	align-items: center;
}

.stage {
	padding: 6px 12px;
	border-radius: 999px;
	background: #f3edff;
	color: #4f378b;
	font-size: 12px;
	font-weight: 500;
	border: 1px solid rgba(103, 80, 164, 0.12);
	white-space: nowrap;
}

.date {
	font-size: 13px;
	color: #5f6368;
}

/* КНОПКИ ДЕЙСТВИЙ */
.file-actions {
	display: flex;
	gap: 12px;
	justify-content: flex-end;
	margin-top: 8px;
}

.favorite-btn,
.download-btn,
.delete-btn {
	height: 40px;
	padding: 0 16px;
	border-radius: 999px;
	border: none;
	cursor: pointer;
	font-size: 14px;
	font-weight: 600;
	transition: 0.2s;
}

.favorite-btn {
	background: transparent;
	font-size: 24px;
	padding: 0;
	width: 40px;
}

.favorite-btn.active {
	color: #fbbc04;
}

.favorite-btn:hover {
	transform: scale(1.1);
}

.download-btn {
	background: #6750a4;
	color: white;
	box-shadow: 0 2px 6px rgba(103, 80, 164, 0.28);
	flex: 1;
}

.download-btn:hover {
	background: #5b4696;
	box-shadow: 0 6px 16px rgba(103, 80, 164, 0.3);
}

/* DELETE (опасное действие) */
.delete-btn {
	background: #fce8e6;
	color: #b3261e;
	flex: 1;
}

.delete-btn:hover {
	background: #f8d7d4;
}

/* НИЖНЯЯ ПАНЕЛЬ */
.download-all-btn,
.export-btn,
.delete-all-btn {
	height: 44px;
	padding: 0 20px;
	border-radius: 999px;
	border: none;
	font-weight: 600;
	cursor: pointer;
	transition: 0.2s;
}

.download-all-btn,
.export-btn {
	background: #6750a4;
	color: white;
	box-shadow: 0 2px 6px rgba(103, 80, 164, 0.28);
}

.download-all-btn:hover,
.export-btn:hover {
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

.delete-all-btn {
	background: #b3261e;
	color: white;
	box-shadow: 0 2px 6px rgba(179, 38, 30, 0.3);
}

.delete-all-btn:hover {
	background: #8c1d18;
	box-shadow: 0 6px 16px rgba(179, 38, 30, 0.35);
}

/* АДАПТИВ */
@media (max-width: 900px) {
	.files-list-container {
		padding: 20px 16px;
	}

	.files-grid {
		grid-template-columns: 1fr;
		justify-items: center;
	}

	.file-item {
		max-width: 100%;
	}

	.filters {
		justify-content: stretch;
	}

	.search-input {
		max-width: none;
	}

	.actions-header {
		flex-direction: column;
		align-items: stretch;
	}

	.action-buttons {
		justify-content: center;
	}

	.file-details {
		flex-direction: column;
		align-items: flex-start;
	}

	.file-actions {
		flex-wrap: wrap;
	}

	.favorite-btn {
		width: auto;
		padding: 0 16px;
		font-size: 18px;
	}
}
</style>
