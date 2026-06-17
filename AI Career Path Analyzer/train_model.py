import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

rng = np.random.default_rng(42)

# ---------------------------------------------------------------
# Dimensions
# ---------------------------------------------------------------
CAREER_GOALS = ["Data Analyst", "Data Scientist", "ML Engineer", "BI Developer", "Data Engineer"]
SKILL_CATEGORIES = ["Python", "SQL", "Statistics", "Machine Learning",
                     "Data Visualization", "Cloud Platforms", "Communication"]
REGIONS = ["South Asia", "North America", "Europe", "Middle East", "Southeast Asia"]

# Required skill level (0-100) per career goal x skill category
goal_requirements = {
    "Data Analyst":   {"Python": 60, "SQL": 85, "Statistics": 65, "Machine Learning": 35,
                        "Data Visualization": 85, "Cloud Platforms": 40, "Communication": 75},
    "Data Scientist": {"Python": 85, "SQL": 70, "Statistics": 85, "Machine Learning": 85,
                        "Data Visualization": 65, "Cloud Platforms": 55, "Communication": 65},
    "ML Engineer":    {"Python": 90, "SQL": 60, "Statistics": 75, "Machine Learning": 90,
                        "Data Visualization": 40, "Cloud Platforms": 75, "Communication": 50},
    "BI Developer":   {"Python": 45, "SQL": 90, "Statistics": 50, "Machine Learning": 25,
                        "Data Visualization": 90, "Cloud Platforms": 50, "Communication": 70},
    "Data Engineer":  {"Python": 80, "SQL": 85, "Statistics": 45, "Machine Learning": 40,
                        "Data Visualization": 35, "Cloud Platforms": 90, "Communication": 55},
}

req_rows = []
for goal, reqs in goal_requirements.items():
    for cat, lvl in reqs.items():
        req_rows.append({"CareerGoal": goal, "SkillCategory": cat, "RequiredLevel": lvl})
df_requirements = pd.DataFrame(req_rows)

# ---------------------------------------------------------------
# Profiles
# ---------------------------------------------------------------
N = 160
first_names = ["Aarav","Vihaan","Aditya","Diya","Ananya","Ishaan","Kavya","Rohan","Meera","Arjun",
               "Sara","Liam","Olivia","Noah","Emma","Mateo","Sofia","Lucas","Mia","Ethan",
               "Priya","Karthik","Naveen","Divya","Sanjay","Pooja","Rahul","Neha","Vikram","Shreya"]
last_names = ["Sharma","Patel","Kumar","Nair","Iyer","Reddy","Singh","Gupta","Rao","Menon",
              "Smith","Johnson","Brown","Garcia","Müller","Dubois","Tanaka","Kim","Hassan","Ali"]

profiles = []
for i in range(1, N + 1):
    name = f"{rng.choice(first_names)} {rng.choice(last_names)}"
    goal = rng.choice(CAREER_GOALS)
    region = rng.choice(REGIONS)
    join_date = datetime(2024, 1, 1) + timedelta(days=int(rng.integers(0, 540)))
    years_exp = round(float(rng.uniform(0, 8)), 1)
    profiles.append({
        "ProfileID": f"P{i:04d}", "Name": name, "CareerGoal": goal,
        "Region": region, "JoinDate": join_date.date(), "YearsExperience": years_exp,
    })
df_profiles = pd.DataFrame(profiles)

# ---------------------------------------------------------------
# Current skill levels per profile x category (latest snapshot)
# Skill level correlates with years experience + noise, with some
# profiles deliberately strong/weak to create realistic skill gaps
# ---------------------------------------------------------------
skill_rows = []
profile_skill_matrix = {}
for _, prof in df_profiles.iterrows():
    base = 30 + prof["YearsExperience"] * 6
    cats = {}
    for cat in SKILL_CATEGORIES:
        req = goal_requirements[prof["CareerGoal"]][cat]
        affinity = rng.normal(0, 18)
        level = base * 0.5 + req * 0.35 + affinity + rng.normal(0, 8)
        level = float(np.clip(level, 5, 100))
        cats[cat] = level
        skill_rows.append({
            "ProfileID": prof["ProfileID"], "SkillCategory": cat,
            "CurrentLevel": round(level, 1),
        })
    profile_skill_matrix[prof["ProfileID"]] = cats
df_skills = pd.DataFrame(skill_rows)

# ---------------------------------------------------------------
# Readiness score per profile (weighted: how close current skills
# are to the requirements of their stated career goal)
# ---------------------------------------------------------------
def readiness_for(profile_id, goal, skill_levels):
    reqs = goal_requirements[goal]
    ratios = [min(skill_levels[cat] / reqs[cat], 1.15) for cat in SKILL_CATEGORIES]
    return float(np.clip(np.mean(ratios) * 100, 0, 100))

df_profiles["ReadinessScore"] = df_profiles.apply(
    lambda r: round(readiness_for(r["ProfileID"], r["CareerGoal"], profile_skill_matrix[r["ProfileID"]]), 1),
    axis=1
)
df_profiles["MissingSkillsCount"] = df_profiles["ProfileID"].apply(
    lambda pid: sum(1 for cat in SKILL_CATEGORIES
                    if profile_skill_matrix[pid][cat] < goal_requirements[
                        df_profiles.loc[df_profiles.ProfileID == pid, "CareerGoal"].iloc[0]][cat])
)

# ---------------------------------------------------------------
# Readiness history (12 monthly snapshots ending current month)
# ---------------------------------------------------------------
months = pd.date_range(end=pd.Timestamp(2026, 6, 1), periods=12, freq="MS")
history_rows = []
for _, prof in df_profiles.iterrows():
    final = prof["ReadinessScore"]
    start = float(np.clip(final - rng.uniform(8, 28), 5, 95))
    trend = np.linspace(start, final, 12) + rng.normal(0, 2.5, 12)
    trend = np.clip(trend, 0, 100)
    for m, val in zip(months, trend):
        history_rows.append({"ProfileID": prof["ProfileID"], "SnapshotDate": m.date(),
                              "ReadinessScore": round(float(val), 1)})
df_history = pd.DataFrame(history_rows)

# ---------------------------------------------------------------
# Courses
# ---------------------------------------------------------------
course_catalog = {
    "Python": ["Python for Data Analysis", "Advanced Python Programming"],
    "SQL": ["SQL for Data Professionals", "Advanced Query Optimization"],
    "Statistics": ["Applied Statistics", "Statistical Inference Bootcamp"],
    "Machine Learning": ["Machine Learning Specialization", "Deep Learning Foundations"],
    "Data Visualization": ["Power BI Mastery", "Data Storytelling with Tableau"],
    "Cloud Platforms": ["AWS Data Analytics", "Azure for Data Engineers"],
    "Communication": ["Business Communication for Analysts", "Executive Storytelling"],
}
statuses = ["Completed", "In Progress", "Recommended"]
course_rows = []
for _, prof in df_profiles.iterrows():
    n_courses = int(rng.integers(2, 6))
    chosen_cats = rng.choice(SKILL_CATEGORIES, size=n_courses, replace=False)
    for cat in chosen_cats:
        course = rng.choice(course_catalog[cat])
        gap = profile_skill_matrix[prof["ProfileID"]][cat] < goal_requirements[prof["CareerGoal"]][cat]
        status = rng.choice(statuses, p=[0.5, 0.2, 0.3]) if gap else rng.choice(statuses, p=[0.7, 0.15, 0.15])
        completion_date = (datetime(2025, 1, 1) + timedelta(days=int(rng.integers(0, 520)))).date() \
            if status == "Completed" else None
        course_rows.append({
            "ProfileID": prof["ProfileID"], "CourseName": course, "SkillCategory": cat,
            "Status": status, "CompletionDate": completion_date,
        })
df_courses = pd.DataFrame(course_rows)

# ---------------------------------------------------------------
# Certifications
# ---------------------------------------------------------------
cert_catalog = ["Microsoft Certified: Power BI Data Analyst Associate", "AWS Certified Data Analytics",
                "Google Professional Data Engineer", "TensorFlow Developer Certificate",
                "Tableau Desktop Specialist", "Azure Data Fundamentals"]
cert_rows = []
for _, prof in df_profiles.iterrows():
    n_certs = int(rng.integers(0, 3))
    for cert in rng.choice(cert_catalog, size=n_certs, replace=False):
        issue_date = (datetime(2024, 6, 1) + timedelta(days=int(rng.integers(0, 700)))).date()
        cert_rows.append({"ProfileID": prof["ProfileID"], "CertificationName": cert, "IssueDate": issue_date})
df_certifications = pd.DataFrame(cert_rows)

# ---------------------------------------------------------------
# Recommendations (personalized upskilling) — for the table visual
# ---------------------------------------------------------------
rec_rows = []
for _, prof in df_profiles.iterrows():
    pid, goal = prof["ProfileID"], prof["CareerGoal"]
    gaps = [(cat, goal_requirements[goal][cat] - profile_skill_matrix[pid][cat])
            for cat in SKILL_CATEGORIES if profile_skill_matrix[pid][cat] < goal_requirements[goal][cat]]
    gaps.sort(key=lambda x: -x[1])
    for cat, gap in gaps[:3]:
        priority = "High" if gap > 25 else ("Medium" if gap > 12 else "Low")
        rec_rows.append({
            "ProfileID": pid, "RecommendedCourse": rng.choice(course_catalog[cat]),
            "SkillCategory": cat, "Priority": priority,
            "ExpectedImpact": round(float(gap * 0.4), 1),
        })
df_recommendations = pd.DataFrame(rec_rows)

# ---------------------------------------------------------------
# Classification model: predict "CareerReady" (1) vs "At Risk" (0)
# Label threshold on readiness score; features = current skill
# levels + experience + courses completed + certifications
# ---------------------------------------------------------------
courses_completed = df_courses[df_courses.Status == "Completed"].groupby("ProfileID").size()
certs_count = df_certifications.groupby("ProfileID").size()

feature_rows = []
for _, prof in df_profiles.iterrows():
    pid, goal = prof["ProfileID"], prof["CareerGoal"]
    row = {}
    for cat in SKILL_CATEGORIES:
        ratio = profile_skill_matrix[pid][cat] / goal_requirements[goal][cat]
        row[f"{cat}_RatioToGoal"] = round(float(np.clip(ratio + rng.normal(0, 0.04), 0, 1.5)), 3)
    row["YearsExperience"] = prof["YearsExperience"]
    row["CoursesCompleted"] = int(courses_completed.get(pid, 0))
    row["Certifications"] = int(certs_count.get(pid, 0))
    row["Label"] = 1 if prof["ReadinessScore"] >= 75 else 0
    feature_rows.append(row)
df_features = pd.DataFrame(feature_rows)

X = df_features.drop(columns="Label")
y = df_features["Label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=7, stratify=y)

clf = RandomForestClassifier(n_estimators=200, max_depth=6, min_samples_leaf=3, random_state=7)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, zero_division=0)
rec = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print(f"Accuracy: {acc:.4f}  Precision: {prec:.4f}  Recall: {rec:.4f}  F1: {f1:.4f}")
print(f"Train size: {len(X_train)}  Test size: {len(X_test)}")

df_model_metrics = pd.DataFrame([
    {"Metric": "Model Type", "Value": "Random Forest Classifier"},
    {"Metric": "Target Label", "Value": "CareerReady (Readiness Score >= 75)"},
    {"Metric": "Accuracy", "Value": round(acc, 4)},
    {"Metric": "Precision", "Value": round(prec, 4)},
    {"Metric": "Recall", "Value": round(rec, 4)},
    {"Metric": "F1 Score", "Value": round(f1, 4)},
    {"Metric": "Training Samples", "Value": len(X_train)},
    {"Metric": "Test Samples", "Value": len(X_test)},
    {"Metric": "Features Used", "Value": ", ".join(X.columns)},
])

# ---------------------------------------------------------------
# Calendar dimension (supports the time-period slicer)
# ---------------------------------------------------------------
cal = pd.DataFrame({"Date": pd.date_range("2025-01-01", "2026-06-30", freq="D")})
cal["Year"] = cal.Date.dt.year
cal["MonthNumber"] = cal.Date.dt.month
cal["MonthName"] = cal.Date.dt.strftime("%b %Y")
cal["Quarter"] = "Q" + cal.Date.dt.quarter.astype(str) + " " + cal.Date.dt.year.astype(str)
cal["Date"] = cal["Date"].dt.date

# ---------------------------------------------------------------
# Skill category dimension (for the skill-category slicer)
# ---------------------------------------------------------------
df_skill_categories = pd.DataFrame({"SkillCategory": SKILL_CATEGORIES})

# ---------------------------------------------------------------
# Save everything for inspection / reuse by the Excel-build step
# ---------------------------------------------------------------
import pickle
with open("/home/claude/pbi/data_bundle.pkl", "wb") as f:
    pickle.dump({
        "profiles": df_profiles, "skills": df_skills, "requirements": df_requirements,
        "history": df_history, "courses": df_courses, "certifications": df_certifications,
        "recommendations": df_recommendations, "model_metrics": df_model_metrics,
        "calendar": cal, "skill_categories": df_skill_categories,
    }, f)

print("Profiles:", len(df_profiles), "| Skills rows:", len(df_skills),
      "| History rows:", len(df_history), "| Courses:", len(df_courses),
      "| Certifications:", len(df_certifications), "| Recommendations:", len(df_recommendations))
