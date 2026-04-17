<template>
	<div class="file-detail-container" v-if="file">
		<h1>
			<span v-if="!editMode">{{ file.title }}</span>
			<input v-else v-model="newTitle" class="edit-title-input" />
			<button v-if="!editMode" @click="editMode = true" class="edit-btn">
				Редактировать
			</button>
			<button v-if="editMode" @click="saveTitle" class="save-btn">
				Сохранить
			</button>
			<button v-if="editMode" @click="cancelEdit" class="cancel-btn">
				Отмена
			</button>
		</h1>
		<div class="file-info">
			<p><strong>Версия:</strong> {{ file.version }}</p>
			<p><strong>Этап:</strong> {{ stageLabel(file.stage) }}</p>
			<p>
				<strong>Дата загрузки:</strong>
				{{ formatDate(file.uploaded_at) }}
			</p>
			<p>
				<strong>Автор (создал):</strong>
				{{ file.owner_email || file.owner_username }}
			</p>
			<p v-if="file.last_edited_email">
				<strong>Кто последний менял:</strong>
				{{ file.last_edited_email || file.last_edited_username }}
				<span v-if="file.last_edited_at"
					>({{ formatDate(file.last_edited_at) }})</span
				>
			</p>
			<p>
				<strong>Файл:</strong>
				<button @click="downloadFile" class="download-btn">
					Скачать
				</button>
			</p>
			<p>
				<strong>Избранное:</strong>
				<span v-if="file.is_favorite">★</span>
				<span v-else>☆</span>
			</p>
		</div>
		<div class="comments-section">
			<h2>Комментарии</h2>
			<form @submit.prevent="addComment" class="comment-form">
				<textarea
					v-model="newComment"
					placeholder="Введите комментарий..."
					required
				></textarea>
				<button type="submit">Отправить</button>
			</form>
			<ul class="comments-list">
				<li
					v-for="comment in comments"
					:key="comment.id"
					class="comment-item"
				>
					<div class="comment-header">
						<span class="comment-author">{{
							comment.author_email
						}}</span>
						<span class="comment-date">{{
							formatDate(comment.created_at)
						}}</span>
					</div>
					<div class="comment-text">{{ comment.text }}</div>
				</li>
			</ul>
			<div v-if="comments.length === 0" class="no-comments">
				Комментариев пока нет.
			</div>
		</div>
		<button @click="goBack" class="back-btn">Назад</button>
	</div>
	<div v-else class="loading">Загрузка...</div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();

const file = ref(null);
const comments = ref([]);
const newComment = ref('');
const editMode = ref(false);
const newTitle = ref('');

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

function cancelEdit() {
	editMode.value = false;
	newTitle.value = file.value.title;
}

async function saveTitle() {
	if (!newTitle.value.trim() || newTitle.value === file.value.title) {
		editMode.value = false;
		return;
	}
	try {
		const token = localStorage.getItem('access');
		const response = await axios.patch(
			`http://localhost:8000/api/files/rename/${file.value.id}/`,
			{ title: newTitle.value },
			{ headers: { Authorization: `Bearer ${token}` } },
		);
		file.value = response.data;
		editMode.value = false;
	} catch (e) {
		alert('Ошибка при изменении названия файла');
	}
}

const downloadFile = async () => {
	try {
		const token = localStorage.getItem('access');
		const response = await axios.get(
			`http://localhost:8000/api/files/download/${file.value.id}/`,
			{
				headers: { Authorization: `Bearer ${token}` },
				responseType: 'blob',
			},
		);
		const contentDisposition = response.headers['content-disposition'];
		let filename = file.value.title;
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

const loadComments = async () => {
	try {
		const token = localStorage.getItem('access');
		const response = await axios.get(
			`http://localhost:8000/api/files/comments/${route.params.id}/`,
			{
				headers: { Authorization: `Bearer ${token}` },
			},
		);
		comments.value = response.data;
	} catch (e) {
		comments.value = [];
	}
};

const addComment = async () => {
	if (!newComment.value.trim()) return;
	try {
		const token = localStorage.getItem('access');
		await axios.post(
			`http://localhost:8000/api/files/comments/${route.params.id}/`,
			{ text: newComment.value },
			{ headers: { Authorization: `Bearer ${token}` } },
		);
		newComment.value = '';
		loadComments();
	} catch (e) {
		alert('Ошибка при добавлении комментария');
	}
};

function stageLabel(stage) {
	const found = stageOptions.find(opt => opt.value === stage);
	return found ? found.label : stage;
}

function formatDate(dateStr) {
	const date = new Date(dateStr);
	return date.toLocaleString('ru-RU');
}

function goBack() {
	router.back();
}

onMounted(async () => {
	try {
		const token = localStorage.getItem('access');
		const response = await axios.get(
			`http://localhost:8000/api/files/detail/${route.params.id}/`,
			{
				headers: { Authorization: `Bearer ${token}` },
			},
		);
		file.value = response.data;
	} catch (e) {
		file.value = null;
		alert('Ошибка при загрузке информации о файле');
	}

	loadComments();
	newTitle.value = file.value?.title || '';
});

watch(file, newVal => {
	newTitle.value = newVal?.title || '';
});
</script>

<style scoped>
.file-detail-container {
	max-width: 600px;
	margin: 40px auto;
	padding: 30px;
	background: #f8f9fa;
	border-radius: 10px;
}
.file-info p {
	margin: 10px 0;
	font-size: 1.1em;
}
.back-btn {
	margin-top: 20px;
	padding: 8px 16px;
	background: #007bff;
	color: white;
	border: none;
	border-radius: 4px;
	cursor: pointer;
}
.back-btn:hover {
	background: #0056b3;
}
.loading {
	text-align: center;
	padding: 40px;
	font-size: 18px;
	color: #666;
}
.download-btn {
	background: #28a745;
	color: white;
	border: none;
	border-radius: 4px;
	padding: 6px 14px;
	cursor: pointer;
	margin-left: 10px;
}
.download-btn:hover {
	background: #1e7e34;
}
.comments-section {
	margin-top: 40px;
	background: #fff;
	border-radius: 8px;
	padding: 20px;
}
.comment-form {
	display: flex;
	flex-direction: column;
	margin-bottom: 20px;
}
.comment-form textarea {
	resize: vertical;
	min-height: 60px;
	margin-bottom: 10px;
	padding: 8px;
	font-size: 15px;
	border-radius: 4px;
	border: 1px solid #ccc;
}
.comment-form button {
	align-self: flex-end;
	padding: 6px 16px;
	background: #007bff;
	color: white;
	border: none;
	border-radius: 4px;
	cursor: pointer;
}
.comment-form button:hover {
	background: #0056b3;
}
.comments-list {
	list-style: none;
	padding: 0;
}
.comment-item {
	border-bottom: 1px solid #eee;
	padding: 10px 0;
}
.comment-header {
	font-size: 0.95em;
	color: #888;
	margin-bottom: 4px;
	display: flex;
	gap: 15px;
}
.comment-author {
	font-weight: bold;
}
.comment-date {
	font-style: italic;
}
.comment-text {
	font-size: 1.05em;
}
.no-comments {
	color: #888;
	font-style: italic;
	margin-top: 10px;
}
.edit-title-input {
	font-size: 1.2em;
	padding: 4px 8px;
	margin-right: 8px;
}
.edit-btn,
.save-btn,
.cancel-btn {
	margin-left: 8px;
	padding: 4px 10px;
	border: none;
	border-radius: 4px;
	cursor: pointer;
}
.edit-btn {
	background: #ffc107;
	color: #333;
}
.save-btn {
	background: #28a745;
	color: white;
}
.cancel-btn {
	background: #dc3545;
	color: white;
}
.edit-btn:hover {
	background: #e0a800;
}
.save-btn:hover {
	background: #218838;
}
.cancel-btn:hover {
	background: #c82333;
}
</style>
