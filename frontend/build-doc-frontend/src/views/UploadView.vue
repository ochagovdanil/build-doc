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
.upload-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	margin-top: 100px;
}
form {
	display: flex;
	flex-direction: column;
	width: 350px;
}
input,
button {
	margin-bottom: 10px;
	padding: 8px;
	font-size: 16px;
}
.file-title-block {
	display: flex;
	align-items: center;
	gap: 10px;
	margin-bottom: 5px;
}
.error {
	color: red;
}
.success {
	color: green;
}
</style>
