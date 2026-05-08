
---

# PhishGuard: AI-Powered Phishing Detection System

**PhishGuard** is a comprehensive cybersecurity tool designed to detect and mitigate phishing threats using machine learning and advanced data analysis. This project aims to provide a robust defense mechanism against deceptive digital communications by analyzing URLs and communication patterns in real-time.

## 🚀 Features

* **AI/ML Detection:** Utilizes supervised learning models to classify URLs as legitimate or phishing.
* **Heuristic Analysis:** Checks for common phishing indicators such as suspicious domain age, SSL certificate anomalies, and spoofed characters.
* **Real-time Alerts:** Provides immediate feedback on potential threats.
* **User-Friendly Dashboard:** A clean interface to monitor and analyze detected threats.

## 🛠️ Tech Stack

* **Frontend:** React.js, Tailwind CSS
* **Backend:** Node.js, Python (FastAPI/Flask)
* **Machine Learning:** Scikit-learn, Pandas, NumPy
* **Database:** MongoDB

## 📂 Project Structure

```text
├── client/          # Frontend React application
├── server/          # Backend API and ML integration
├── models/          # Trained ML models and datasets
├── scripts/         # Automation and data processing scripts
└── README.md

```

## 🔧 Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/Rishichauhan67/PhishGuard.git

```


2. **Install Dependencies:**
```bash
# For backend
cd server && npm install
# For frontend
cd client && npm install

```


3. **Run the Application:**
```bash
npm start

```



## 🛡️ Security Focus

This project was developed with a focus on digital forensics and proactive cybersecurity, incorporating RAM analysis techniques and sentiment visualization to better understand phishing trends.

---

### How to update your Project:

1. Go to your **[PhishGuard Settings](https://github.com/Rishichauhan67/PhishGuard/settings)**.
> *An advanced AI-driven phishing detection system designed for real-time URL analysis and cybersecurity forensics.*

## 📚 Academic Foundation & References

This project is built upon established research in machine learning and digital forensics. The following papers provide the theoretical basis for our detection logic and forensic analysis:

* **[Phishing Website Detection Using Machine Learning Algorithms](https://ieeexplore.ieee.org/document/9074312)** *Explores the performance of various supervised learning models in classifying malicious URLs, supporting our core detection engine.*

* **[A Novel Approach for Phishing Website Detection using URL Features](https://www.researchgate.net/publication/340455502_A_Novel_Approach_for_Phishing_Website_Detection_using_URL_Features)** *Provides a detailed analysis of heuristic features such as domain age and SSL anomalies used in our analysis phase.*

* **[Deep Learning for Phishing Detection: A Comprehensive Review](https://www.mdpi.com/2076-3417/10/18/6509)** *Offers insights into the evolution of AI-driven security and advanced neural network applications for real-time threat mitigation.*

* **[Digital Forensics in Cybersecurity: A Review of RAM Analysis](https://www.sciencedirect.com/science/article/abs/pii/S016740481930211X)** *Underpins the forensic focus of PhishGuard, specifically regarding volatile memory analysis and proactive threat hunting.*




