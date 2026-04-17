<template>
	<div class="login-container">
		<h1>Вход в систему</h1>
		<form @submit.prevent="login">
			<input v-model="email" type="email" placeholder="Почта" required />
			<input
				v-model="password"
				type="password"
				placeholder="Пароль"
				required
			/>
			<button type="submit">Войти</button>
			<p v-if="error" class="error">{{ error }}</p>
		</form>
		<router-link to="/register"
			>Нет аккаунта? Зарегистрироваться</router-link
		>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();

const login = async () => {
	error.value = '';
	try {
		const response = await axios.post('http://localhost:8000/api/token/', {
			username: email.value, // SimpleJWT ожидает поле username
			password: password.value,
		});
		// Сохраняем токен в localStorage
		localStorage.setItem('access', response.data.access);
		localStorage.setItem('refresh', response.data.refresh);
		// Редирект на главную страницу
		router.push({ name: 'Home' });
	} catch (err) {
		error.value = 'Неверная почта или пароль';
	}
};
</script>

<style scoped>
.login-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	margin-top: 100px;
}
form {
	display: flex;
	flex-direction: column;
	width: 300px;
}
input,
button {
	margin-bottom: 10px;
	padding: 8px;
	font-size: 16px;
}
.error {
	color: red;
}
</style>
