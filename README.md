# University Student Data Dashboard

**Data Mining — Activity I: Data Visualization and Dashboard Deployment**  
Universidad de la Costa | Prof. José Escorcia-Gutierrez, Ph.D.

---

## Team Members

| Name | Group |
|------|-------|
| Diego Navarro Gómez | 18690 |
| Juan Félix | 18038 |
| Dinelis García | 18038 |
| Kimberly Ochoa | 19027 |

---

## Purpose

This dashboard lets users explore university student data from 2015 to 2024.  
It shows key metrics like **retention rate**, **student satisfaction**, and **enrollment trends** through interactive charts and filters.

---

## How to Run Locally

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

4. Open your browser at `http://localhost:8501`

---

## Files in This Repository

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit dashboard code |
| `university_student_data.csv` | Dataset with student records from 2015 to 2024 |
| `requirements.txt` | Python libraries needed to run the app |
| `notebook_exploratory_analysis.ipynb` | Google Colab notebook with exploratory analysis |
| `README.md` | This file |

---

## Dataset Columns

| Column | Description |
|--------|-------------|
| Year | Academic year (2015–2024) |
| Term | Semester — Spring or Fall |
| Applications | Total student applications received that year/term |
| Admitted | Number of students admitted |
| Enrolled | Number of students who confirmed enrollment |
| Retention Rate (%) | Percentage of students who stayed enrolled |
| Student Satisfaction (%) | Average student satisfaction score |
| Engineering Enrolled | Students enrolled in the Engineering department |
| Business Enrolled | Students enrolled in the Business department |
| Arts Enrolled | Students enrolled in the Arts department |
| Science Enrolled | Students enrolled in the Science department |

---

## Dashboard Features

- **Filters** (sidebar): Year range slider, Term selector (Spring / Fall / All), Department selector
- **KPI Cards**: Average retention rate, average satisfaction, total enrolled, total applications
- **Line Chart**: Retention rate trend over time
- **Seaborn Line Chart**: Student satisfaction trend over time
- **Bar Chart**: Spring vs Fall enrollment comparison
- **Donut / Pie Chart** (interactive): Enrollment distribution by department
- **Dual Y-Axis Line Chart**: Applications vs enrolled students per year (each metric on its own scale)

---

## Main Findings

- Retention rate grew steadily from **85% in 2015** to **90% in 2024**, showing that the university is getting better at keeping students.
- Student satisfaction also improved from **78% to 88%** over the same period, which likely contributes to better retention.
- **Engineering** is consistently the most enrolled department, while **Science** enrollment has slightly decreased in recent years.
- Spring and Fall terms show nearly identical enrollment numbers, meaning the university is stable across both semesters.

**Actionable Insight:** Since Science enrollment is declining, the university could investigate whether course offerings, career prospects, or student satisfaction in that department are lower than in others, and take action to improve them.
