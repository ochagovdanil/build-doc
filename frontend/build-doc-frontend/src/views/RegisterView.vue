<template>
	<div class="register-container">
		<h1>Регистрация</h1>
		<form @submit.prevent="register">
			<input v-model="email" type="email" placeholder="Почта" required />
			<input
				v-model="password"
				type="password"
				placeholder="Пароль"
				required
			/>
			<button type="submit">Зарегистрироваться</button>
			<p v-if="error" class="error">{{ error }}</p>
			<p v-if="success" class="success">{{ success }}</p>
		</form>
		<router-link to="/">Уже есть аккаунт? Войти</router-link>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

const email = ref('');
const password = ref('');
const error = ref('');
const success = ref('');

const register = async () => {
	error.value = '';
	success.value = '';
	try {
		const response = await axios.post(
			'http://localhost:8000/api/users/register/',
			{
				email: email.value,
				password: password.value,
			},
		);
		success.value = response.data.message;
		email.value = '';
		password.value = '';
		// Редирект через 1 секунду на страницу логина
		setTimeout(() => {
			router.push({ name: 'Login' });
		}, 1000);
	} catch (err) {
		error.value = err.response?.data?.email?.[0] || 'Ошибка регистрации';
	}
};
</script>

<style scoped>
.register-container,
.register-container * {
	box-sizing: border-box;
}

.register-container {
	min-height: 100vh;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 32px 20px;
	background: radial-gradient(
			circle at top,
			rgba(103, 80, 164, 0.12),
			transparent 35%
		),
		linear-gradient(180deg, #f7f5fb 0%, #f3f4f8 100%);
	font-family: Roboto, 'Segoe UI', Arial, sans-serif;
}

h1 {
	width: min(100%, 380px);
	margin: 0 0 20px;
	color: #1d1b20;
	font-size: 32px;
	font-weight: 600;
	line-height: 1.2;
	letter-spacing: -0.02em;
	text-align: center;
}

form {
	width: min(100%, 380px);
	display: flex;
	flex-direction: column;
	gap: 14px;
	padding: 28px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 24px;
	box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05),
		0 12px 32px rgba(15, 23, 42, 0.08);
}

input {
	width: 100%;
	height: 52px;
	margin: 0;
	padding: 0 16px;
	border: 1px solid #c4c7c5;
	border-radius: 14px;
	background: #ffffff;
	color: #1d1b20;
	font-size: 15px;
	outline: none;
	transition: border-color 0.2s ease, box-shadow 0.2s ease,
		background-color 0.2s ease;
}

input::placeholder {
	color: #6f6f75;
}

input:hover {
	border-color: #9a8cc4;
	background: #fcfbff;
}

input:focus {
	border-color: #6750a4;
	box-shadow: 0 0 0 4px rgba(103, 80, 164, 0.14);
	background: #ffffff;
}

button {
	width: 100%;
	height: 48px;
	margin: 4px 0 0;
	border: none;
	border-radius: 999px;
	background: #6750a4;
	color: #ffffff;
	font-size: 15px;
	font-weight: 600;
	letter-spacing: 0.01em;
	cursor: pointer;
	box-shadow: 0 2px 6px rgba(103, 80, 164, 0.28);
	transition: background-color 0.2s ease, box-shadow 0.2s ease,
		transform 0.15s ease;
}

button:hover {
	background: #5b4696;
	box-shadow: 0 6px 16px rgba(103, 80, 164, 0.3);
}

button:active {
	transform: translateY(1px);
	box-shadow: 0 2px 6px rgba(103, 80, 164, 0.22);
}

button:focus-visible,
input:focus-visible,
.register-container a:focus-visible {
	outline: none;
	box-shadow: 0 0 0 4px rgba(103, 80, 164, 0.16);
}

.error {
	margin: 2px 0 0;
	padding: 12px 14px;
	border: 1px solid rgba(179, 38, 30, 0.18);
	border-radius: 12px;
	background: #fce8e6;
	color: #b3261e;
	font-size: 14px;
	line-height: 1.4;
}

.success {
	margin: 2px 0 0;
	padding: 12px 14px;
	border: 1px solid rgba(31, 128, 78, 0.18);
	border-radius: 12px;
	background: #e8f5e9;
	color: #1f804e;
	font-size: 14px;
	line-height: 1.4;
}

.register-container a {
	width: min(100%, 380px);
	margin-top: 14px;
	color: #6750a4;
	font-size: 14px;
	font-weight: 500;
	text-align: center;
	text-decoration: none;
	transition: color 0.2s ease;
}

.register-container a:hover {
	color: #4f378b;
	text-decoration: underline;
}
</style>
