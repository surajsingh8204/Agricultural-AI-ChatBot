# Deep Shiva - Agricultural Assistant Platform

A professional and responsive web application designed to help farmers with AI-powered agricultural insights. Deep Shiva is an all-in-one smart chatbot designed specially for farmers to make farming easier, smarter, and more profitable. It helps farmers with everything — from crop disease detection to market prices and weather updates — all in one place.

## 🌟 Features

### 🔐 Authentication System
- **Login Page**: Secure authentication with email/password
- **Sign Up**: Account creation with farm type selection
- **Demo Account**: Try the platform without registration
- **Dashboard**: Personalized user interface with sidebar navigation

### 🌾 Crop Disease Detection
- Click the card to open the external disease detection tool
- Links to: https://plant-disease-frontend-ibpp.onrender.com

### 💰 Market Price Analysis
- Real-time crop price display (Rice, Wheat, Corn, Soybean)
- Price change indicators
- Placeholder for future AI price predictor

### 🌦️ Weather Updates
- Current weather display with temperature and humidity
- 3-day weather forecast
- Refresh button to update weather data
- Ready for OpenWeatherMap API integration

### 🧑‍🌾 AI Chatbot Assistant
- ChatGPT-style chat interface
- Keyword-based responses for farming topics:
  - Fertilizers
  - Irrigation
  - Pest control
  - Crop selection
  - Weather
  - Market prices
  - Soil management
  - Harvesting
  - Seeds
  - Disease prevention

### 📊 Dashboard Features
- **Personalized Dashboard**: Welcome message with user's name
- **Statistics Cards**: Active crops, temperature, prices, AI insights
- **Quick Actions**: Easy access to all features
- **Recent Activity**: Timeline of user actions
- **Profile Management**: Update user information and farm type
- **Responsive Sidebar**: Navigation for all features

## 🚀 How to Use

1. **Start Here**: Open `landing.html` - it will redirect to login
2. **Login Options**:
   - Create a new account with the sign-up form
   - Use the demo account for quick access
   - Login with existing credentials
3. **Dashboard**: After login, access your personalized dashboard
4. **Navigation**: Use the sidebar to access different features
5. **Profile**: Update your information in the profile section

## 📁 File Structure

```
deep-shiva-chatbot/
├── landing.html          # Entry point (redirects to login)
├── login.html            # Authentication page
├── dashboard.html        # Main dashboard interface
├── index.html           # Original features page (requires login)
└── README.md            # This file
```

## 🎨 Design Features

- **Dark Theme**: Modern dark interface similar to ChatGPT
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Hover Animations**: Cards scale up and show shadows on hover
- **Modern UI**: Clean, professional interface
- **Tailwind CSS**: Styled with Tailwind CSS via CDN

## 🔧 Technical Details

- **Pure HTML/CSS/JavaScript**: No build process required
- **Local Storage**: User authentication and data persistence
- **Responsive Grid**: CSS Grid and Flexbox for layout
- **Interactive Components**: JavaScript-based functionality
- **External Integration**: Ready for API connections

## 🔐 Authentication Flow

1. **Landing Page**: Entry point that redirects to login
2. **Login Page**: 
   - Email/password authentication
   - Demo account option
   - Sign-up modal
   - Password visibility toggle
3. **Dashboard**: 
   - Personalized interface
   - Sidebar navigation
   - User profile management
   - Statistics and quick actions
4. **Logout**: Clears session and returns to login

## 🌱 Future Enhancements

- Connect to real weather APIs (OpenWeatherMap)
- Integrate with market price APIs
- Add OpenAI API for advanced chatbot responses
- Implement server-side authentication
- Add data persistence with backend
- Real-time notifications
- Advanced analytics and reporting

## 📱 Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers

## 🎯 Target Users

- Farmers and agricultural professionals
- Agricultural students and researchers
- Anyone interested in farming and agriculture

---

**© 2025 Deep Shiva | Empowering Farmers with AI**
