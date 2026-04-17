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
			<p>
				<strong>Версия:</strong> <mark>{{ file.version }}</mark>
			</p>
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
				<span
					v-if="file.is_favorite"
					style="
						color: orange;
						font-size: 1.2rem;
						margin-left: 0.5rem;
					"
					>★</span
				>
				<span v-else style="font-size: 1.2rem; margin-left: 0.5rem"
					>☆</span
				>
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
.file-detail-container,
.file-detail-container * {
	box-sizing: border-box;
}

.file-detail-container {
	max-width: 1000px;
	margin: 0 auto;
	padding: 36px 32px 48px;
	font-family: Roboto, 'Segoe UI', Arial, sans-serif;
	color: #1d1b20;
}

/* HEADER */

h1 {
	display: flex;
	align-items: center;
	flex-wrap: wrap;
	gap: 12px;
	margin: 0 0 24px;
	font-size: 32px;
	font-weight: 700;
	letter-spacing: -0.02em;
}

/* EDIT INPUT */

.edit-title-input {
	height: 44px;
	padding: 0 14px;
	border: 1px solid #c4c7c5;
	border-radius: 12px;
	font-size: 16px;
	outline: none;
	transition: 0.2s;
}

.edit-title-input:focus {
	border-color: #6750a4;
	box-shadow: 0 0 0 4px rgba(103, 80, 164, 0.14);
}

/* BUTTONS */

.edit-btn,
.save-btn,
.cancel-btn,
.download-btn,
.back-btn {
	height: 40px;
	padding: 0 16px;
	border-radius: 999px;
	border: none;
	font-size: 14px;
	font-weight: 600;
	cursor: pointer;
	transition: 0.2s;
	margin-left: 0.5rem;
}

.edit-btn {
	background: #ece6f0;
	color: #4f378b;
}

.edit-btn:hover {
	background: #e0d7f5;
}

.save-btn {
	background: #6750a4;
	color: #fff;
	box-shadow: 0 2px 6px rgba(103, 80, 164, 0.28);
}

.save-btn:hover {
	background: #5b4696;
	box-shadow: 0 6px 16px rgba(103, 80, 164, 0.3);
}

.cancel-btn {
	background: #fce8e6;
	color: #b3261e;
}

.cancel-btn:hover {
	background: #f8d7d4;
}

/* FILE CARD */

.file-info {
	padding: 24px;
	margin-bottom: 28px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 24px;
	box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05),
		0 12px 32px rgba(15, 23, 42, 0.08);
}

.file-info p {
	margin: 10px 0;
	font-size: 15px;
	color: #44474f;
}

.file-info strong {
	color: #1d1b20;
}

/* COMMENTS */

.comments-section {
	padding: 24px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 24px;
	box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05),
		0 12px 32px rgba(15, 23, 42, 0.08);
}

.comments-section h2 {
	margin: 0 0 16px;
	font-size: 22px;
	font-weight: 600;
}

/* FORM */

.comment-form {
	display: flex;
	flex-direction: column;
	gap: 12px;
	margin-bottom: 20px;
}

.comment-form textarea {
	min-height: 100px;
	padding: 12px 14px;
	border-radius: 14px;
	border: 1px solid #c4c7c5;
	font-size: 14px;
	resize: vertical;
	outline: none;
	transition: 0.2s;
}

.comment-form textarea:focus {
	border-color: #6750a4;
	box-shadow: 0 0 0 4px rgba(103, 80, 164, 0.14);
}

.comment-form button {
	align-self: flex-start;
	height: 40px;
	padding: 0 18px;
	border-radius: 999px;
	border: none;
	background: #6750a4;
	color: #fff;
	font-weight: 600;
	cursor: pointer;
	box-shadow: 0 2px 6px rgba(103, 80, 164, 0.28);
	transition: 0.2s;
}

.comment-form button:hover {
	background: #5b4696;
	box-shadow: 0 6px 16px rgba(103, 80, 164, 0.3);
}

/* LIST */

.comments-list {
	list-style: none;
	padding: 0;
	margin: 0;
	display: flex;
	flex-direction: column;
	gap: 14px;
}

.comment-item {
	padding: 16px;
	border-radius: 16px;
	background: #f7f5fb;
	border: 1px solid #e4def4;
}

.comment-header {
	display: flex;
	justify-content: space-between;
	margin-bottom: 6px;
	font-size: 13px;
	color: #5f6368;
}

.comment-author {
	font-weight: 600;
	color: #1d1b20;
}

.comment-text {
	font-size: 14px;
	color: #44474f;
	line-height: 1.5;
}

/* EMPTY */

.no-comments {
	text-align: center;
	color: #5f6368;
	font-size: 14px;
	margin-top: 12px;
}

/* BACK */

.back-btn {
	margin-top: 24px;
	background: #ece6f0;
	color: #4f378b;
}

.back-btn:hover {
	background: #e0d7f5;
}

/* LOADING */

.loading {
	padding: 40px;
	text-align: center;
	color: #5f6368;
}

/* ADAPTIVE */

@media (max-width: 700px) {
	h1 {
		font-size: 26px;
	}

	.file-detail-container {
		padding: 24px 20px;
	}
}
</style>
