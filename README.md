# ✈️ Agentic Travel Assistant

Welcome to the **Agentic Travel Assistant**! This comprehensive tool helps users plan perfect trips by providing personalized recommendations for flights, hotels, and activities based on individual preferences, budget, and travel duration. Developed using OpenAI's new Agents SDK, the assistant incorporates advanced features like guardrails to ensure realistic budget planning, structured agent handoffs, and an intuitive conversational interface.

---

## 🌟 Key Features

- **🛫 Flight Recommendations:** Personalized options based on price, timing, and flight preferences (direct or connecting).
- **🏨 Hotel Recommendations:** Suggestions tailored to your desired location, price range, and amenities.
- **☀️ Weather Forecasts:** Real-time forecasts for better destination planning.
- **💰 Budget Analysis with Guardrails:** Realistic budget assessments leveraging OpenAI's Agents SDK for enhanced accuracy.
- **💬 Interactive Chat Interface:** Engaging conversational UI powered by Streamlit.
- **⚙️ Customizable Preferences:** User-defined preferences for airlines, hotel amenities, and budget constraints.
- **🤖 Agent Handoffs:** Smooth transitions between agents for specialized recommendations using OpenAI's Agents SDK.

---

## 🛠️ Tech Stack & Tools

- **Language:** Python
- **Framework:** Streamlit
- **APIs:**
  - OpenWeatherMap API (Weather Data)
  - OpenAI API (AI-driven Recommendations & Agents SDK)
- **Libraries:**
  - `pydantic` – Structured data models
  - `requests` – API interactions
  - `dotenv` – Secure environment variable management
  - `asyncio` – Asynchronous operations
  - `logfire` – Advanced logging
- **Utilities:**
  - `uuid` – User session management
  - `json` – Data serialization
  - `datetime` – Date/time handling

---

## 📂 Project Structure

```
.
├── ai-agent/
├── context.py
├── home.py
├── output_with_guardrails_and_context.py
├── structured_output.py
├── structured_outputs_with_handoffs.py
├── tools.py
├── weather_test.py
├── requirements.txt
└── .logfire/
```

| File | Description |
|------|-------------|
| **`home.py`** | Main Streamlit application (chat interface). |
| **`tools.py`** | Core functions for flights, hotels, and weather searches. |
| **`context.py`** | Manages user preferences and context. |
| **`output_with_guardrails_and_context.py`** | Implements budget guardrails using OpenAI's Agents SDK. |
| **`structured_output.py`** | Defines structured outputs for travel plans. |
| **`structured_outputs_with_handoffs.py`** | Manages agent handoffs for specialized recommendations. |
| **`weather_test.py`** | API tests for weather data retrieval. |

---

## 🚀 Installation Guide

### **Prerequisites**

- Python 3.8+
- API keys:
  - [OpenWeatherMap API](https://openweathermap.org/api)
  - [OpenAI API](https://platform.openai.com/signup/)
  - [Logfire](https://logfire.io/)

### **Environment Setup**

Create a `.env` file in the project root:

```env
OPENWEATHER_API_KEY=your_openweather_api_key_here  
OPENAI_API_KEY=your_openai_api_key_here  
LOGFIRE_API_KEY=your_logfire_api_key_here
```

### **Installation Steps**

Clone the repository and set up the environment:

```bash
git clone https://github.com/your-username/travel-planner-assistant.git
cd travel-planner-assistant

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🖥️ Running the App

Launch the Streamlit app:

```bash
streamlit run home.py
```

Access the interface via browser:

```
http://localhost:8501
```

---

## 🧑‍💻 How to Use

1. **Set Your Preferences:**  
   Define your preferred airlines, amenities, and budget level using the sidebar.

2. **Interact via Chat:**  
   Ask questions like:
   - *"Find a flight from New York to Chicago tomorrow."*
   - *"Recommend hotels in Paris under $300 with a pool."*
   - *"Suggest activities in Tokyo for a week within a $3000 budget."*

3. **Receive Personalized Recommendations:**  
   The assistant provides structured suggestions for flights, hotels, and activities, supported by budget guardrails.

---

## 🔍 Detailed Feature Overview

### 🛫 Flight Recommendations
- Leverages `search_flights` from `tools.py`.
- Customized results based on user-defined criteria.

### 🏨 Hotel Recommendations
- Utilizes `search_hotels` in `tools.py`.
- Filters and recommends accommodations aligned with preferences.

### ☀️ Weather Forecasts
- Uses `get_weather_forecast` from `tools.py`.
- Integrates real-time weather data from OpenWeatherMap.

### 💰 Budget Analysis with Guardrails
- Advanced guardrails implemented via OpenAI's Agents SDK.
- Ensures trip feasibility within defined budget constraints.

### 🤖 Agent Handoffs
- Seamless agent handoffs for handling specific tasks (flights, hotels).
- Powered by OpenAI's Agents SDK for a cohesive user experience.

---

## 🌟 Customization & Extensions

- **Modify Preferences:**  
  Adjust `UserContext` in `context.py` for expanded customization.
- **Add New Integrations:**  
  Expand functionalities by adding new tools/APIs in `tools.py`.
- **Refine Guardrails:**  
  Enhance budget logic in `output_with_guardrails_and_context.py`.

---

## 🤝 Contributing

Your contributions are welcome! Follow these steps to contribute:

1. Fork and clone the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes clearly:
   ```bash
   git commit -m "Your feature description"
   ```
4. Push your changes:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request for review.

---

## 📄 License

This project is licensed under the **MIT License**. Refer to the LICENSE file for more details.

---

## 🙌 Acknowledgments

- Built with ❤️ using **OpenAI's new Agents SDK** and **Streamlit**.
- Weather data by **OpenWeatherMap API**.
- Enhanced logging powered by **Logfire**.

---

## 📧 Contact

For questions, feedback, or support:

**Hetav "GodSpeed" Patel**  
📨 Email: [your-email@example.com](mailto:your-email@example.com)  
🐙 GitHub: [Hetav01](https://github.com/Hetav01)  
🔗 [Project Repository](https://github.com/Hetav01/Agentic-Travel-Assistant)
