<template>
	<div class="home-page">
		<header class="topbar">
			<div class="brand-block">
				<div class="brand-eyebrow">Платформа для строительства</div>
				<div class="brand-title">Строй Док</div>
			</div>

			<div class="topbar-actions">
				<div class="user-chip">
					<span class="user-chip-label">Пользователь</span>
					<span class="user-chip-value">{{
						userEmail || 'Авторизованный пользователь'
					}}</span>
				</div>
				<button class="logout-button" @click="logout">Выйти</button>
			</div>
		</header>

		<main class="home-container">
			<section class="hero-section">
				<div class="hero-content">
					<p class="hero-kicker">Информационная система</p>
					<h1>
						Добро пожаловать{{ userEmail ? ', ' + userEmail : '' }}!
					</h1>
					<p class="hero-description">
						<strong>Строй Док</strong> — это система для
						информационного сопровождения технологий информационного
						моделирования на этапе строительства.
					</p>
					<p class="hero-description secondary">
						Сервис помогает загружать нормативные документы,
						классифицировать их, быстро находить нужные материалы
						через фильтрацию и формировать проекты с набором
						необходимой документации.
					</p>

					<div class="hero-badges">
						<span class="badge">Нормативные документы</span>
						<span class="badge">Классификация</span>
						<span class="badge">Фильтрация</span>
						<span class="badge">Проекты строительства</span>
					</div>
				</div>

				<aside class="info-card">
					<h2>Что можно сделать</h2>
					<ul>
						<li>Загрузить строительную документацию</li>
						<li>Работать с личными и общими файлами</li>
						<li>Формировать подборки и избранное</li>
						<li>Организовывать документы по проектам</li>
					</ul>
				</aside>
			</section>

			<section class="actions-section">
				<div class="section-header">
					<h2>Основные разделы</h2>
					<p>Быстрый доступ к ключевым инструментам системы</p>
				</div>

				<div class="actions-grid">
					<router-link to="/projects" class="action-card primary">
						<span class="action-title">Мои проекты</span>
						<span class="action-text">
							Создание и ведение проектов с набором документов
						</span>
					</router-link>

					<router-link to="/upload" class="action-card">
						<span class="action-title">Загрузить документ</span>
						<span class="action-text">
							Добавление новых файлов и нормативной документации
						</span>
					</router-link>

					<router-link to="/favorites" class="action-card">
						<span class="action-title">Мои избранные</span>
						<span class="action-text">
							Быстрый доступ к важным и часто используемым
							документам
						</span>
					</router-link>

					<router-link to="/files" class="action-card">
						<span class="action-title">Мои файлы</span>
						<span class="action-text">
							Просмотр и управление личной загруженной
							документацией
						</span>
					</router-link>

					<router-link to="/all-files" class="action-card">
						<span class="action-title">Все файлы</span>
						<span class="action-text">
							Общий каталог документов с возможностью поиска и
							отбора
						</span>
					</router-link>
				</div>
			</section>
		</main>
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
.home-page,
.home-page * {
	box-sizing: border-box;
}

.home-page {
	min-height: 100vh;
	background: radial-gradient(
			circle at top,
			rgba(103, 80, 164, 0.1),
			transparent 28%
		),
		linear-gradient(180deg, #f7f5fb 0%, #f3f4f8 100%);
	font-family: Roboto, 'Segoe UI', Arial, sans-serif;
	color: #1d1b20;
}

.topbar {
	position: sticky;
	top: 0;
	z-index: 20;
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 24px;
	padding: 16px 32px;
	background: rgba(255, 255, 255, 0.86);
	backdrop-filter: blur(14px);
	border-bottom: 1px solid rgba(103, 80, 164, 0.08);
	box-shadow: 0 2px 12px rgba(15, 23, 42, 0.04);
}

.brand-block {
	display: flex;
	flex-direction: column;
	gap: 4px;
}

.brand-eyebrow {
	color: #6750a4;
	font-size: 12px;
	font-weight: 600;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.brand-title {
	color: #1d1b20;
	font-size: 26px;
	font-weight: 700;
	letter-spacing: -0.02em;
}

.topbar-actions {
	display: flex;
	align-items: center;
	gap: 16px;
}

.user-chip {
	display: flex;
	flex-direction: column;
	padding: 10px 14px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.1);
	border-radius: 16px;
	box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

.user-chip-label {
	font-size: 11px;
	font-weight: 600;
	letter-spacing: 0.06em;
	text-transform: uppercase;
	color: #6f6f75;
}

.user-chip-value {
	font-size: 14px;
	font-weight: 500;
	color: #1d1b20;
}

.logout-button {
	height: 44px;
	padding: 0 20px;
	border: none;
	border-radius: 999px;
	background: #6750a4;
	color: #ffffff;
	font-size: 14px;
	font-weight: 600;
	cursor: pointer;
	box-shadow: 0 2px 6px rgba(103, 80, 164, 0.28);
	transition: background-color 0.2s ease, box-shadow 0.2s ease,
		transform 0.15s ease;
}

.logout-button:hover {
	background: #5b4696;
	box-shadow: 0 6px 16px rgba(103, 80, 164, 0.3);
}

.logout-button:active {
	transform: translateY(1px);
}

.home-container {
	max-width: 1280px;
	margin: 0 auto;
	padding: 36px 32px 48px;
}

.hero-section {
	display: grid;
	grid-template-columns: minmax(0, 1.7fr) minmax(320px, 0.9fr);
	gap: 24px;
	align-items: stretch;
	margin-bottom: 32px;
}

.hero-content {
	padding: 32px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 28px;
	box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05),
		0 12px 32px rgba(15, 23, 42, 0.08);
}

.hero-kicker {
	margin: 0 0 12px;
	color: #6750a4;
	font-size: 13px;
	font-weight: 700;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.hero-content h1 {
	margin: 0 0 16px;
	font-size: 40px;
	font-weight: 700;
	line-height: 1.15;
	letter-spacing: -0.03em;
	color: #1d1b20;
}

.hero-description {
	margin: 0 0 12px;
	max-width: 860px;
	color: #44474f;
	font-size: 16px;
	line-height: 1.7;
}

.hero-description.secondary {
	color: #5f6368;
}

.hero-badges {
	display: flex;
	flex-wrap: wrap;
	gap: 12px;
	margin-top: 24px;
}

.badge {
	display: inline-flex;
	align-items: center;
	padding: 10px 14px;
	border-radius: 999px;
	background: #f3edff;
	color: #4f378b;
	font-size: 14px;
	font-weight: 500;
	border: 1px solid rgba(103, 80, 164, 0.12);
}

.info-card {
	padding: 28px;
	background: linear-gradient(180deg, #ffffff 0%, #fcfbff 100%);
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 28px;
	box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05),
		0 12px 32px rgba(15, 23, 42, 0.08);
}

.info-card h2 {
	margin: 0 0 18px;
	font-size: 22px;
	font-weight: 600;
	color: #1d1b20;
}

.info-card ul {
	margin: 0;
	padding-left: 20px;
	color: #44474f;
	font-size: 15px;
	line-height: 1.7;
}

.info-card li + li {
	margin-top: 10px;
}

.actions-section {
	padding: 28px;
	background: #ffffff;
	border: 1px solid rgba(103, 80, 164, 0.08);
	border-radius: 28px;
	box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05),
		0 12px 32px rgba(15, 23, 42, 0.08);
}

.section-header {
	margin-bottom: 20px;
}

.section-header h2 {
	margin: 0 0 8px;
	font-size: 26px;
	font-weight: 650;
	color: #1d1b20;
}

.section-header p {
	margin: 0;
	color: #5f6368;
	font-size: 15px;
}

.actions-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 18px;
}

.action-card {
	display: flex;
	flex-direction: column;
	gap: 10px;
	min-height: 144px;
	padding: 22px;
	text-decoration: none;
	background: #fbfaff;
	border: 1px solid #e4def4;
	border-radius: 22px;
	color: #1d1b20;
	box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
	transition: transform 0.18s ease, box-shadow 0.2s ease,
		border-color 0.2s ease, background-color 0.2s ease;
}

.action-card:hover {
	transform: translateY(-2px);
	border-color: #c8bce8;
	background: #ffffff;
	box-shadow: 0 12px 24px rgba(103, 80, 164, 0.12);
}

.action-card.primary {
	background: linear-gradient(180deg, #f3edff 0%, #ede4ff 100%);
	border-color: rgba(103, 80, 164, 0.2);
}

.action-title {
	font-size: 18px;
	font-weight: 650;
	line-height: 1.3;
	color: #1d1b20;
}

.action-text {
	font-size: 14px;
	line-height: 1.6;
	color: #5f6368;
}

.action-card:focus-visible,
.logout-button:focus-visible {
	outline: none;
	box-shadow: 0 0 0 4px rgba(103, 80, 164, 0.16);
}

@media (max-width: 1100px) {
	.hero-section {
		grid-template-columns: 1fr;
	}

	.actions-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}
}

@media (max-width: 760px) {
	.topbar {
		flex-direction: column;
		align-items: flex-start;
		padding: 16px 20px;
	}

	.topbar-actions {
		width: 100%;
		flex-direction: column;
		align-items: stretch;
	}

	.user-chip {
		width: 100%;
	}

	.logout-button {
		width: 100%;
	}

	.home-container {
		padding: 24px 20px 36px;
	}

	.hero-content,
	.info-card,
	.actions-section {
		padding: 22px;
		border-radius: 24px;
	}

	.hero-content h1 {
		font-size: 32px;
	}

	.actions-grid {
		grid-template-columns: 1fr;
	}
}
</style>
