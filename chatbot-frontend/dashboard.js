// JavaScript for dashboard.html
// Login is now optional. You can access the dashboard directly.

// Load user data
const user = JSON.parse(localStorage.getItem('user') || '{}');
document.getElementById('userName').textContent = user.name || 'Demo Farmer';
document.getElementById('userInitial').textContent = (user.name || 'D').charAt(0).toUpperCase();
document.getElementById('userFarmType').textContent = user.farmType || 'Mixed Farming';
document.getElementById('welcomeName').textContent = user.name || 'Demo Farmer';

// Profile form
document.getElementById('profileName').value = user.name || '';
document.getElementById('profileEmail').value = user.email || '';
document.getElementById('profileFarmType').value = user.farmType || 'mixed';

// Sidebar toggle for mobile
function toggleSidebar() {
	const sidebar = document.getElementById('sidebar');
	sidebar.classList.toggle('-translate-x-full');
}

// Navigation
function showSection(sectionName) {
	// Hide all sections
	document.querySelectorAll('.section').forEach(section => {
		section.classList.add('hidden');
	});
	// Show selected section
	document.getElementById(sectionName + '-section').classList.remove('hidden');
	// Update navigation
	document.querySelectorAll('.nav-item').forEach(item => {
		item.classList.remove('bg-dark-card', 'text-dark-text');
		item.classList.add('text-dark-text-secondary');
	});
	// Highlight active nav item
	const activeNav = document.querySelector(`[onclick="showSection('${sectionName}')"]`);
	if (activeNav) {
		activeNav.classList.add('bg-dark-card', 'text-dark-text');
		activeNav.classList.remove('text-dark-text-secondary');
	}
	// Update page title
	const titles = {
		'dashboard': 'Dashboard',
		'crops': 'Crop Analysis',
		'weather': 'Weather',
		'market': 'Market Prices',
		'chatbot': 'AI Assistant',
		'profile': 'Profile Settings'
	};
	document.getElementById('pageTitle').textContent = titles[sectionName] || 'Dashboard';
	// Close sidebar on mobile
	if (window.innerWidth < 1024) {
		document.getElementById('sidebar').classList.add('-translate-x-full');
	}
}

// Logout function
function logout() {
	localStorage.removeItem('isLoggedIn');
	localStorage.removeItem('user');
	// No redirect to login, just reload the dashboard
	window.location.reload();
}

// Save profile
function saveProfile() {
	const updatedUser = {
		...user,
		name: document.getElementById('profileName').value,
		email: document.getElementById('profileEmail').value,
		farmType: document.getElementById('profileFarmType').value
	};
	localStorage.setItem('user', JSON.stringify(updatedUser));
	showNotification('Profile updated successfully!');
	// Update UI
	document.getElementById('userName').textContent = updatedUser.name;
	document.getElementById('userInitial').textContent = updatedUser.name.charAt(0).toUpperCase();
	document.getElementById('userFarmType').textContent = updatedUser.farmType;
	document.getElementById('welcomeName').textContent = updatedUser.name;
}

// Show notification
function showNotification(message) {
	const notification = document.getElementById('notification');
	document.getElementById('notificationText').textContent = message;
	notification.classList.remove('hidden');
	notification.classList.add('notification-slide');
	setTimeout(() => {
		notification.classList.add('hidden');
		notification.classList.remove('notification-slide');
	}, 3000);
}

// Show notifications
function showNotifications() {
	showNotification('You have 3 new insights from AI analysis');
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', function(e) {
	const sidebar = document.getElementById('sidebar');
	const sidebarToggle = e.target.closest('[onclick="toggleSidebar()"]');
	if (window.innerWidth < 1024 && !sidebar.contains(e.target) && !sidebarToggle) {
		sidebar.classList.add('-translate-x-full');
	}
});

// Chatbot backend configuration.
// Prefer calling a backend (safer) or a Gradio share URL. Your Gradio share link:
const BACKEND_BASE = "https://ae5a35a24c0afc8ea2.gradio.live/"; // <-- update if needed

// Try multiple common endpoint patterns (Gradio apps expose different paths depending on how they are hosted).
async function getBotResponse(userMessage) {
	const endpoints = [
		// Common Gradio endpoints
		`${BACKEND_BASE}api/predict`,
		`${BACKEND_BASE}run/predict`,
		`${BACKEND_BASE}predict`,
		// As a last resort, try posting directly to the base URL (some share links proxy predict calls)
		BACKEND_BASE
	];

	// Payload formats to try. Gradio typically expects { data: [ ... ] }.
	const payloads = [
		(msg) => JSON.stringify({ data: [msg] }),
		(msg) => JSON.stringify({ inputs: msg }),
		(msg) => JSON.stringify({ input: msg })
	];

	for (const url of endpoints) {
		for (const buildBody of payloads) {
			try {
				const res = await fetch(url, {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: buildBody(userMessage)
				});

				// Skip if not found; try next candidate
				if (res.status === 404) continue;

				// Try to parse JSON response
				let json;
				try { json = await res.json(); } catch (e) { continue; }

				// Common Gradio response shape: { data: [...] }
				if (json && Array.isArray(json.data) && json.data.length > 0) {
					// The model output may be nested; pick the first string-like value we find
					const first = json.data[0];
					if (typeof first === 'string') return first;
					if (Array.isArray(first) && typeof first[0] === 'string') return first[0];
					if (first && typeof first?.label === 'string') return first.label;
				}

				// Another common shape: [{ generated_text: '...' }] or { generated_text: '...' }
				if (Array.isArray(json) && json[0]?.generated_text) return json[0].generated_text;
				if (json.generated_text) return json.generated_text;

				// Some Gradio apps return { output: [...] }
				if (json && Array.isArray(json.output) && json.output.length > 0) {
					if (typeof json.output[0] === 'string') return json.output[0];
					if (Array.isArray(json.output[0]) && typeof json.output[0][0] === 'string') return json.output[0][0];
				}

				// If response had a plain text body, return that
				const text = await res.text();
				if (text && text.length > 0) return text;

			} catch (e) {
				// Continue to next payload/endpoint candidate
				continue;
			}
		}
	}

	// If nothing worked, give a helpful message.
	return "Error contacting AI model or unexpected response format. If you host on Gradio, confirm the app's API path (e.g. /api/predict) and that the share URL supports direct browser requests (CORS).";
}

function addMessage(text, isBot = false) {
	const messagesContainer = document.getElementById('chat-messages');
	const messageDiv = document.createElement('div');
	messageDiv.className = `flex ${isBot ? 'justify-start' : 'justify-end'}`;
	const messageContent = document.createElement('div');
	messageContent.className = `max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
		isBot ? 'bg-dark-card text-dark-text' : 'bg-accent-green text-white'
	}`;
	const messageText = document.createElement('p');
	messageText.className = 'text-sm';
	messageText.textContent = text;
	messageContent.appendChild(messageText);
	messageDiv.appendChild(messageContent);
	messagesContainer.appendChild(messageDiv);
	messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

async function sendMessage() {
	const input = document.getElementById('chat-input');
	const message = input.value.trim();
	if (!message) return;
	addMessage(message, false);
	input.value = '';
	// Show typing indicator
	const messagesContainer = document.getElementById('chat-messages');
	const typingDiv = document.createElement('div');
	typingDiv.className = 'flex justify-start';
	typingDiv.innerHTML = `
		<div class="bg-dark-card text-dark-text px-4 py-2 rounded-lg">
			<div class="flex space-x-1">
				<div class="w-2 h-2 bg-dark-text-secondary rounded-full typing-dots"></div>
				<div class="w-2 h-2 bg-dark-text-secondary rounded-full typing-dots" style="animation-delay: 0.1s"></div>
				<div class="w-2 h-2 bg-dark-text-secondary rounded-full typing-dots" style="animation-delay: 0.2s"></div>
			</div>
		</div>
	`;
	messagesContainer.appendChild(typingDiv);
	messagesContainer.scrollTop = messagesContainer.scrollHeight;
	// Fetch bot response from Hugging Face
	const botResponse = await getBotResponse(message);
	typingDiv.remove();
	addMessage(botResponse, true);
}

function handleKeyPress(event) {
	if (event.key === 'Enter') {
		sendMessage();
	}
}

// Disease detection functionality
function openDiseaseDetection() {
	window.open('https://plant-disease-frontend-ibpp.onrender.com', '_blank');
}

// Weather refresh functionality
function refreshWeather() {
	const tempElement = document.getElementById('current-temp');
	const conditionElement = document.getElementById('current-condition');
	const humidityElement = document.getElementById('current-humidity');
	const windElement = document.getElementById('current-wind');
	const iconElement = document.getElementById('weather-icon');
	// Simulate weather data refresh
	const temperatures = [26, 28, 30, 32, 25, 27, 29];
	const conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain'];
	const humidities = [60, 65, 70, 75, 55];
	const windSpeeds = [10, 12, 15, 18, 8];
	const icons = ['☀️', '⛅', '☁️', '🌦️'];
	tempElement.textContent = temperatures[Math.floor(Math.random() * temperatures.length)] + '°C';
	conditionElement.textContent = conditions[Math.floor(Math.random() * conditions.length)];
	humidityElement.textContent = humidities[Math.floor(Math.random() * humidities.length)] + '%';
	windElement.textContent = windSpeeds[Math.floor(Math.random() * windSpeeds.length)] + ' km/h';
	iconElement.textContent = icons[Math.floor(Math.random() * icons.length)];
	showNotification('Weather data updated successfully!');
}
