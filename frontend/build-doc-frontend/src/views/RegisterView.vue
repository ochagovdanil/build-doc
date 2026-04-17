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
.register-container {
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
.success {
	color: green;
}
</style>
