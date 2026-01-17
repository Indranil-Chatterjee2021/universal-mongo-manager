# 📝 Universal MongoDB Manager

A lightweight, secure, and real-time MongoDB administration tool built with Streamlit. This application allows multiple users to manage their own clusters independently by providing their connection strings, ensuring a session-isolated experience.

## 🚀 Key Features

* **Multi-User Isolation**: Every session is private. Users only access the data they have credentials for.
* **Dynamic Dashboard**: Instant insights into databases, collections, and document counts.
* **JSON Document Editor**: A dedicated interface to search, edit, and delete records with pagination support (25 records per page).
* **Secure Connection**: Automatic session timeout (10 minutes) and masked URI inputs for security.
* **Sticky UI**: Professional interface featuring a fixed footer and intuitive navigation.

## 🛠️ Tech Stack

* **Python 3.x**
* **Streamlit** (UI Framework)
* **PyMongo** (MongoDB Driver)
* **BSON** (Document Handling)

## 📋 Requirements & Dependencies

To run this application, you need **Python 3.8+** and the following libraries:

* **streamlit**: The core web framework.
* **pymongo**: The official Python driver for MongoDB.
* **dnspython**: Required to support `mongodb+srv://` connection strings.
* **bson**: For handling MongoDB-specific data types (installed automatically with pymongo).

### Current Version Specs:
| Package | Purpose |
| :--- | :--- |
| `streamlit` | UI and State Management |
| `pymongo` | Database connectivity |
| `dnspython` | DNS Seedlist support (SRV records) |

## 📦 Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Indranil-Chatterjee2021/universal-mongo-manager.git](https://github.com/Indranil-Chatterjee2021/universal-mongo-manager.git)
   cd universal-mongo-manager

## 🔒 Security & Privacy

This application is designed with a **Security-First** approach for multi-user environments:

* **Session Isolation**: Every user session is completely isolated. Connection strings (URIs) are stored in `st.session_state`, which exists only in the user's browser memory and is never shared across different sessions or users.
* **Inactivity Auto-Logout**: The application features a 10-minute (600 seconds) inactivity timer. If no interaction is detected, the session is wiped, and the URI is cleared from memory.
* **Secure Input masking**: All MongoDB URIs are entered via password-type fields. I have implemented custom CSS to disable "show password" toggles and browser inspection of the URI field.
* **No Data Persistence**: This tool does not use a local database or logs to store your connection strings. Once you close the tab or log out, all connection data is gone.
* **Zero-Telemetry**: No tracking or data collection is performed. Your data stays between your browser and your MongoDB cluster.

> **Note**: For production use, it is highly recommended to deploy this app using **HTTPS** to ensure that your URI is encrypted while in transit between your browser and the server.   