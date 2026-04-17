<template>
	<div class="home-container">
		<h1>Добро пожаловать{{ userEmail ? ', ' + userEmail : '' }}!</h1>
		<router-link to="/projects" class="nav-link">Мои проекты</router-link>
		<router-link to="/upload">Загрузить документ</router-link>
		<router-link to="/favorites">Мои избранные</router-link>
		<router-link to="/files">Мои файлы</router-link>
		<router-link to="/all-files">Все файлы</router-link>
		<button @click="logout">Выйти</button>
	</div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import axios from 'axios';

const router = useRouter();
const userEmail = ref('');

// Получаем email пользователя через запрос к бэку
onMounted(async () => {
	const token = localStorage.getItem('access');
	if (token) {
		try {
			const response = await axios.get(
				'http://localhost:8000/api/users/me/',
				{
					headers: {
						Authorization: `Bearer ${token}`,
					},
				},
			);
			userEmail.value = response.data.email;
		} catch (e) {
			// Если токен невалиден — выходим
			logout();
		}
	}
});

function logout() {
	localStorage.removeItem('access');
	localStorage.removeItem('refresh');

	router.push({ name: 'Login' });
}
</script>

<style scoped>
.home-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	margin-top: 100px;
}
button {
	margin-top: 20px;
	padding: 8px 16px;
	font-size: 16px;
}
</style>
