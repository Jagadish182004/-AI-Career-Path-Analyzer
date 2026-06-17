# AI Career Path Analyzer

An interactive **Power BI dashboard** that analyzes career readiness, highlights skill gaps, and provides personalized upskilling recommendations.  
Built with **Python, Pandas, Scikit-learn, Power BI, and TensorFlow.js**.

---

## 🚀 Features
- **Career Readiness Score**: KPI card showing readiness out of 100.
- **Skill Gap Analysis**: Current vs Required skill levels visualized in bar charts.
- **Heatmap Matrix**: Career goals vs skill categories with conditional formatting.
- **Trend Line**: Readiness score progression over time.
- **Recommendations Table**: Personalized course suggestions with priority and impact.
- **Interactive Filters**: Slicers for Career Goal, Skill Category, and Date.

---

## 🛠 Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Scikit--learn](https://img.shields.io/badge/Scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![PowerBI](https://img.shields.io/badge/PowerBI-F2C811?logo=powerbi&logoColor=black)
![TensorFlow.js](https://img.shields.io/badge/TensorFlow.js-FF6F00?logo=tensorflow&logoColor=white)

---

## 📂 Project Structure
- `AI_Career_Path_Analyzer_Data.xlsx` → Sample dataset (star schema)
- `AI_Career_Path_Analyzer_Theme.json` → Custom Power BI theme
- `train_model.py` → ML model training script (requires `data_bundle.pkl`)
- `PowerBI_Build_Guide.md` → Step-by-step build instructions
- `README.md` → Project documentation

---

## ⚡ How to Run
1. Open **Power BI Desktop**.
2. Import `AI_Career_Path_Analyzer_Data.xlsx` (Get Data → Excel).
   - This Excel file is the **main entry point** for Power BI.
3. Apply relationships as per `PowerBI_Build_Guide.md`.
4. Add DAX measures from `_Measures` table.
5. Place visuals on canvas:
   - Bar Chart → Skill Gap
   - Matrix → Heatmap
   - Cards → KPIs
   - Line Chart → Readiness Trend
   - Table → Recommendations
6. Apply theme: `AI_Career_Path_Analyzer_Theme.json`.
7. (Optional) Run `train_model.py` with `data_bundle.pkl` if you want to retrain the ML model.

---

## 📈 Insights
- Average readiness score: **74.9/100** (close to the 75-point threshold).
- Skill gaps are most prominent in **SQL and Cloud Platforms**.
- Personalized recommendations highlight **Python** and **Statistics** as high-impact areas.

---

## 👤 Author
**Jagadish S**  
Aspiring Data Analyst | Web Developer  
📧 Email: jagadishmec18@gmail.com  
🔗 [LinkedIn](ca://s?q=Jagadish_LinkedIn_Profile) | [GitHub](ca://s?q=Jagadish_GitHub_Profile)

---

## ⭐ Contribute
Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 License
This project is licensed under the MIT License.
