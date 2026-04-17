<template>
	<div class="upload-container">
		<h1>Загрузка документов</h1>
		<form @submit.prevent="uploadDocuments" enctype="multipart/form-data">
			<input
				ref="fileInput"
				type="file"
				multiple
				@change="handleFileChange"
				required
			/>
			<div
				v-for="(file, idx) in files"
				:key="idx"
				class="file-title-block"
			>
				<span>{{ file.name }}</span>
				<input
					v-model="titles[idx]"
					type="text"
					:placeholder="`Название для ${file.name}`"
					required
				/>
				<select v-model="stages[idx]" required>
					<option disabled value="">Выберите этап</option>
					<option
						v-for="stage in stageOptions"
						:key="stage.value"
						:value="stage.value"
					>
						{{ stage.label }}
					</option>
				</select>
			</div>
			<button type="submit">Загрузить</button>
			<p v-if="error" class="error">{{ error }}</p>
			<p v-if="success" class="success">{{ success }}</p>
		</form>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const files = ref([]);
const titles = ref([]);
const stages = ref([]);

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

const error = ref('');
const success = ref('');

function handleFileChange(event) {
	files.value = Array.from(event.target.files);
	titles.value = files.value.map(f => f.name);
	stages.value = files.value.map(() => '');
}

async function uploadDocuments() {
	error.value = '';
	success.value = '';
	if (!files.value.length) {
		error.value = 'Выберите файлы';
		return;
	}
	const formData = new FormData();
	files.value.forEach(file => formData.append('files', file));
	titles.value.forEach(title => formData.append('titles', title));
	stages.value.forEach(stage => formData.append('stages', stage));

	try {
		const token = localStorage.getItem('access');
		await axios.post('http://localhost:8000/api/files/upload/', formData, {
			headers: {
				Authorization: `Bearer ${token}`,
				'Content-Type': 'multipart/form-data',
			},
		});
		success.value = 'Файлы успешно загружены!';
		files.value = [];
		titles.value = [];
		stages.value = [];
		document.querySelector('input[type="file"]').value = '';
	} catch (err) {
		error.value = 'Ошибка загрузки файлов';
	}
}
</script>

<style scoped>
.upload-container,
.upload-container * {
	box-sizing: border-box;
}

.upload-container {
	max-width: 900px;
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

/* FORM CARD */

form {
	display: flex;
	flex-direction: column;
	gap: 18px;
	padding: 28px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 28px;
	box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05),
		0 12px 32px rgba(15, 23, 42, 0.08);
}

/* FILE INPUT */

input[type='file'] {
	padding: 14px;
	border-radius: 16px;
	border: 1px dashed #c4c7c5;
	background: #f7f5fb;
	cursor: pointer;
	transition: 0.2s;
}

input[type='file']:hover {
	border-color: #6750a4;
	background: #f3edff;
}

/* FILE BLOCK */

.file-title-block {
	display: flex;
	flex-direction: column;
	gap: 10px;
	padding: 16px;
	border-radius: 18px;
	background: #faf8ff;
	border: 1px solid #e4def4;
}

/* FILE NAME */

.file-title-block span {
	font-size: 14px;
	font-weight: 600;
	color: #1d1b20;
}

/* INPUTS */

.file-title-block input,
.file-title-block select {
	height: 44px;
	padding: 0 14px;
	border-radius: 12px;
	border: 1px solid #c4c7c5;
	font-size: 14px;
	outline: none;
	transition: 0.2s;
	background: #ffffff;
}

.file-title-block input:focus,
.file-title-block select:focus {
	border-color: #6750a4;
	box-shadow: 0 0 0 4px rgba(103, 80, 164, 0.14);
}

/* BUTTON */

button[type='submit'] {
	margin-top: 8px;
	height: 48px;
	border-radius: 999px;
	border: none;
	background: #6750a4;
	color: #ffffff;
	font-size: 15px;
	font-weight: 600;
	cursor: pointer;
	box-shadow: 0 2px 6px rgba(103, 80, 164, 0.28);
	transition: 0.2s;
}

button[type='submit']:hover {
	background: #5b4696;
	box-shadow: 0 6px 16px rgba(103, 80, 164, 0.3);
}

button[type='submit']:active {
	transform: translateY(1px);
}

/* STATES */

.error {
	margin-top: 4px;
	padding: 12px 14px;
	border-radius: 12px;
	background: #fce8e6;
	border: 1px solid rgba(179, 38, 30, 0.2);
	color: #b3261e;
	font-size: 14px;
}

.success {
	margin-top: 4px;
	padding: 12px 14px;
	border-radius: 12px;
	background: #e6f4ea;
	border: 1px solid rgba(52, 168, 83, 0.25);
	color: #1e8e3e;
	font-size: 14px;
}

/* ADAPTIVE */

@media (max-width: 700px) {
	.upload-container {
		padding: 24px 20px;
	}

	form {
		padding: 20px;
		border-radius: 24px;
	}
}
</style>
