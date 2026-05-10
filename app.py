# We import streamlit to build the interactive web dashboard
import streamlit as st
# We import pandas to load and manipulate the CSV data
import pandas as pd
# We import matplotlib to create basic charts like bar and line plots
import matplotlib.pyplot as plt
# We import seaborn to create styled line plots as required by the activity
import seaborn as sns
# We import plotly to make an interactive pie chart the user can hover over
import plotly.express as px

# --- Page configuration ---
# We set the layout to "wide" so the charts have more horizontal space
st.set_page_config(
    page_title="University Student Dashboard",
    page_icon="🎓",
    layout="wide"
)

# --- Title and team information ---
# We show the team names here and also in the sidebar so they appear in the deployment
st.title("University Student Data Dashboard")
st.markdown(
    "**Team:** Diego Navarro Gómez · Juan Félix · Dinelis García · Kimberly Ochoa"
)
st.markdown(
    "**Course:** Data Mining | Universidad de la Costa | Prof. José Escorcia-Gutierrez, Ph.D."
)
st.markdown("---")


# --- Load data ---
# We use @st.cache_data so the CSV file is only read once,
# not every time the user changes a filter
@st.cache_data
def load_data():
    df = pd.read_csv("university_student_data.csv")
    return df


df = load_data()


# --- Sidebar filters ---
# We put filters in the sidebar so they don't take space away from the charts
st.sidebar.header("Filters")
st.sidebar.markdown("**Team members:**")
st.sidebar.markdown("- Diego Navarro Gómez")
st.sidebar.markdown("- Juan Félix")
st.sidebar.markdown("- Dinelis García")
st.sidebar.markdown("- Kimberly Ochoa")
st.sidebar.markdown("---")

# Year range slider: lets the user pick a start and end year
year_min = int(df["Year"].min())
year_max = int(df["Year"].max())
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

# Term selector: the user can view all data or just Spring or Fall
term_options = ["All"] + sorted(df["Term"].unique().tolist())
selected_term = st.sidebar.selectbox("Select Term", term_options)

# Department selector: used to highlight a department in the pie chart
dept_options = ["All", "Engineering", "Business", "Arts", "Science"]
selected_dept = st.sidebar.selectbox("Select Department", dept_options)


# --- Apply filters ---
# We first filter by year range (always applied)
filtered_df = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# We only filter by term if the user chose something other than "All"
if selected_term != "All":
    filtered_df = filtered_df[filtered_df["Term"] == selected_term]


# --- KPI Cards ---
# We show the most important numbers at the top so the user gets a quick summary
# before looking at the detailed charts
st.subheader("Key Metrics (based on current filters)")

avg_retention = filtered_df["Retention Rate (%)"].mean()
avg_satisfaction = filtered_df["Student Satisfaction (%)"].mean()
total_enrolled = int(filtered_df["Enrolled"].sum())
total_applications = int(filtered_df["Applications"].sum())

# Four columns so the metric cards appear in a single horizontal row
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Avg Retention Rate", f"{avg_retention:.1f}%")
kpi2.metric("Avg Satisfaction Score", f"{avg_satisfaction:.1f}%")
kpi3.metric("Total Enrolled", f"{total_enrolled:,}")
kpi4.metric("Total Applications", f"{total_applications:,}")

st.markdown("---")


# === ROW 1: Line charts — trends over time ===
col1, col2 = st.columns(2)

# --- Chart 1: Retention Rate over Time (line chart) ---
# We use a line chart because we want to see how retention changes year by year.
# groupby("Year") averages both Spring and Fall values into a single yearly point.
with col1:
    st.subheader("Retention Rate Trend Over Time")
    retention_by_year = (
        filtered_df.groupby("Year")["Retention Rate (%)"]
        .mean()
        .reset_index()
    )
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(
        retention_by_year["Year"],
        retention_by_year["Retention Rate (%)"],
        marker="o",
        color="steelblue",
        linewidth=2
    )
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Retention Rate (%)")
    ax1.set_title("Average Retention Rate by Year")
    # Grid lines make it easier to read exact values from the chart
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.set_ylim(80, 95)  # We fix the y-axis so small changes are visible
    st.pyplot(fig1)
    plt.close(fig1)

# --- Chart 2: Student Satisfaction over Time (seaborn lineplot) ---
# sns.lineplot() is used here as required by the activity instructions.
# It shows trends and automatically handles grouped data.
with col2:
    st.subheader("Student Satisfaction Over Time")
    satisfaction_by_year = (
        filtered_df.groupby("Year")["Student Satisfaction (%)"]
        .mean()
        .reset_index()
    )
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.lineplot(
        data=satisfaction_by_year,
        x="Year",
        y="Student Satisfaction (%)",
        marker="o",
        color="coral",
        ax=ax2
    )
    ax2.set_title("Average Student Satisfaction by Year")
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.set_ylim(70, 95)  # Fixed y-axis so the trend is clearly visible
    st.pyplot(fig2)
    plt.close(fig2)

st.markdown("---")


# === ROW 2: Bar charts — category comparisons ===
col3, col4 = st.columns(2)

# --- Chart 3: Spring vs Fall Comparison (bar chart) ---
# A bar chart is the best choice here because we are comparing two discrete categories.
# We always use the year-filtered data (not term-filtered) so both bars are visible.
with col3:
    st.subheader("Spring vs Fall: Average Enrolled Students")
    # We apply only the year filter here so both terms always appear
    term_df = df[
        (df["Year"] >= year_range[0]) &
        (df["Year"] <= year_range[1])
    ]
    term_group = (
        term_df.groupby("Term")["Enrolled"]
        .mean()
        .reset_index()
    )
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    # Different colors help the user distinguish Spring from Fall at a glance
    bar_colors = ["#4C72B0" if t == "Fall" else "#DD8452" for t in term_group["Term"]]
    ax3.bar(term_group["Term"], term_group["Enrolled"], color=bar_colors, width=0.5)
    ax3.set_xlabel("Term")
    ax3.set_ylabel("Average Enrolled Students")
    ax3.set_title("Average Enrollment per Term")
    ax3.grid(axis="y", linestyle="--", alpha=0.5)
    # We add value labels on top of each bar for quick reading
    for bar in ax3.patches:
        ax3.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            f"{bar.get_height():.0f}",
            ha="center", va="bottom", fontsize=11
        )
    st.pyplot(fig3)
    plt.close(fig3)

# --- Chart 4: Department Enrollment (interactive pie chart) ---
# A pie chart works well to show the proportion of students in each department.
# We use plotly so the user can hover to see exact numbers.
with col4:
    st.subheader("Enrollment by Department")
    dept_totals = {
        "Engineering": int(filtered_df["Engineering Enrolled"].sum()),
        "Business": int(filtered_df["Business Enrolled"].sum()),
        "Arts": int(filtered_df["Arts Enrolled"].sum()),
        "Science": int(filtered_df["Science Enrolled"].sum()),
    }
    # If a specific department is selected we "pull" its slice out to highlight it
    pull_values = [
        0.1 if d == selected_dept else 0
        for d in dept_totals.keys()
    ]
    fig4 = px.pie(
        names=list(dept_totals.keys()),
        values=list(dept_totals.values()),
        title="Total Enrollment Distribution by Department",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.3  # Donut style as suggested by the activity
    )
    # pull must be set via update_traces, not as a px.pie() parameter
    fig4.update_traces(textposition="inside", textinfo="percent+label", pull=pull_values)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")


# --- Chart 5: Applications vs Enrolled over Time (dual-axis line chart) ---
# We use a dual y-axis because Applications (~2500-3500) and Enrolled (~600-800)
# have very different scales — putting them on the same axis makes Enrolled invisible.
# We apply only the year filter here (not the term filter) to always show the full year view.
st.subheader("Applications vs Enrolled Students Over Time")
apps_source = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]
# We use sum() to get the real annual total (Spring + Fall combined),
# which is consistent with the KPI cards that also sum both terms
apps_df = (
    apps_source.groupby("Year")[["Applications", "Enrolled"]]
    .sum()
    .reset_index()
)

years_list = apps_df["Year"].tolist()  # Convert to plain list to avoid xticklabel issues

fig5, ax5 = plt.subplots(figsize=(12, 4))

# Left axis: Applications
ax5.plot(years_list, apps_df["Applications"].tolist(),
         marker="o", color="#4C72B0", linewidth=2, label="Applications")
ax5.set_xlabel("Year")
ax5.set_ylabel("Applications", color="#4C72B0")
ax5.tick_params(axis="y", labelcolor="#4C72B0")
ax5.set_xticks(years_list)  # Force one tick per year so labels align exactly

# Right axis: Enrolled — separate scale so the trend is visible
ax5b = ax5.twinx()
ax5b.plot(years_list, apps_df["Enrolled"].tolist(),
          marker="s", color="#55A868", linewidth=2, linestyle="--", label="Enrolled")
ax5b.set_ylabel("Enrolled", color="#55A868")
ax5b.tick_params(axis="y", labelcolor="#55A868")

ax5.set_title("Applications vs Enrolled Students per Year")
ax5.grid(axis="y", linestyle="--", alpha=0.4)

# We combine both legends into one so the chart is not cluttered
lines1, labels1 = ax5.get_legend_handles_labels()
lines2, labels2 = ax5b.get_legend_handles_labels()
ax5.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.tight_layout()
st.pyplot(fig5)
plt.close(fig5)


# --- Footer ---
st.markdown("---")
st.caption(
    "Data Mining Activity I | Universidad de la Costa | Prof. José Escorcia-Gutierrez, Ph.D."
)
