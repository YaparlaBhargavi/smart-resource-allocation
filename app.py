import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np
from streamlit_option_menu import option_menu

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Smart Resource Allocation System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================= ENHANCED CSS =================
st.markdown(
    """
<style>
/* ===== GLOBAL ===== */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ===== MAIN CONTAINER ===== */
.main {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(25px);
    border-radius: 20px;
    padding: 25px;
}

/* ===== HEADER ===== */
h1, h2, h3, h4, h5 {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.8rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 1rem;
    animation: gradientShift 3s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ===== FIX TEXT VISIBILITY ===== */
p, span, label, div {
    color: #e5e7eb !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #0f172a);
    color: white;
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* ===== RADIO & SLIDER TEXT ===== */
.stRadio label, .stSlider label {
    color: white !important;
}

/* ===== METRIC CARDS ===== */
.metric-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    border-radius: 18px;
    padding: 20px;
    color: white;
    border: 1px solid rgba(255,255,255,0.1);
    transition: 0.3s;
    animation: slideInUp 0.5s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    background: rgba(255,255,255,0.12);
}

.critical-card {
    background: linear-gradient(135deg, rgba(249, 115, 22, 0.2), rgba(239, 68, 68, 0.2));
    border-left: 4px solid #f97316;
}

.success-card {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(16, 185, 129, 0.2));
    border-left: 4px solid #22c55e;
}

.info-card {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(99, 102, 241, 0.2));
    border-left: 4px solid #3b82f6;
}

.stat-number {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 10px 0;
    background: linear-gradient(135deg, #fff, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    opacity: 0.8;
}

@keyframes slideInUp {
    from {
        transform: translateY(30px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

/* ===== PRIORITY BADGES ===== */
.priority-high {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.8rem;
    display: inline-block;
    animation: pulse 2s infinite;
}

.priority-medium {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.8rem;
    display: inline-block;
}

.priority-low {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.8rem;
    display: inline-block;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

/* ===== CHART CONTAINER ===== */
.chart-container {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(25px);
    border-radius: 20px;
    padding: 20px;
    margin-top: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    transition: transform 0.3s;
}

.chart-container:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

/* ===== NAVBAR ===== */
.nav-link {
    color: white !important;
    font-weight: 500;
    transition: 0.3s;
}

.nav-link:hover {
    transform: translateY(-2px);
}

.nav-link-selected {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}

/* ===== TABLE ===== */
table {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 10px;
    overflow: hidden;
    width: 100%;
}

th {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    padding: 12px !important;
    font-weight: 600 !important;
}

td {
    padding: 10px !important;
    border-bottom: 1px solid rgba(255,255,255,0.1) !important;
}

tr:hover td {
    background: rgba(99, 102, 241, 0.2) !important;
}

/* ===== BUTTON ===== */
.stButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.5rem 1rem;
    font-weight: 600;
    transition: all 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 20px rgba(99, 102, 241, 0.4);
}

/* ===== DIVIDER ===== */
.custom-divider {
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
    border-radius: 5px;
    margin: 20px 0;
    animation: gradientShift 3s ease infinite;
}

/* ===== FOOTER ===== */
.footer {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    border-radius: 15px;
    padding: 15px;
    text-align: center;
    color: white;
    margin-top: 30px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* ===== SCROLL BAR ===== */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #8b5cf6, #6366f1);
}

/* ===== METRIC CONTAINER ===== */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    border-radius: 15px;
    padding: 10px;
}

[data-testid="stMetricLabel"] {
    color: white !important;
}

[data-testid="stMetricValue"] {
    color: #a78bfa !important;
    font-size: 2rem !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ================= GLOBAL FUNCTIONS =================
def add_priority_badge(val):
    """Add HTML badge for priority levels"""
    if val == "High":
        return f'<span class="priority-high">{val}</span>'
    elif val == "Medium":
        return f'<span class="priority-medium">{val}</span>'
    elif val == "Low":
        return f'<span class="priority-low">{val}</span>'
    return val


# ================= SIDEBAR =================
with st.sidebar:
    st.markdown(
        '<div style="text-align: center; padding: 10px;">', unsafe_allow_html=True
    )
    st.markdown('<div style="font-size: 3rem;">🎯</div>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: white;">Resource Hub</h3>', unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.header("📊 Controls")

    data_option = st.radio(
        "Select Data",
        ["✨ Enhanced (50 issues)", "📝 Basic (20 issues)"],
        help="Choose the dataset size",
    )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    severity_filter = st.slider(
        "⚠️ Minimum Severity", 1, 10, 5, help="Filter issues by minimum severity level"
    )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        f"""
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 15px;">
        <div style="text-align: center;">
            <div>🕒 Last Updated</div>
            <div style="font-size: 0.85rem; font-weight: bold;">{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ================= ENHANCED DATA GENERATION =================
def generate_enhanced_data(n=50):
    np.random.seed(42)

    locations = [
        "Downtown",
        "Eastside",
        "Westside",
        "Northside",
        "Southside",
        "Central",
        "Harbor",
    ]
    categories = [
        "Infrastructure",
        "Medical",
        "Natural Disaster",
        "Emergency",
        "Security",
    ]
    statuses = ["Active", "In Progress", "Pending", "Resolved"]

    issues = pd.DataFrame(
        {
            "IssueID": [f"ISS{i:03d}" for i in range(1, n + 1)],
            "Title": [f"Emergency Response {i}" for i in range(1, n + 1)],
            "Location": np.random.choice(locations, n),
            "Severity": np.random.randint(1, 11, n),
            "Category": np.random.choice(categories, n),
            "Status": np.random.choice(statuses, n, p=[0.4, 0.3, 0.2, 0.1]),
            "ReportedTime": [
                datetime.now().replace(hour=np.random.randint(0, 24)) for _ in range(n)
            ],
        }
    )

    volunteers = pd.DataFrame(
        {
            "Name": [f"Volunteer_{i}" for i in range(1, 21)],
            "Location": np.random.choice(locations, 20),
            "Skills": np.random.choice(
                ["Medical", "Engineering", "Logistics", "Rescue", "Communication"], 20
            ),
            "Availability": np.random.choice(["Yes", "No"], 20, p=[0.7, 0.3]),
            "Capacity": np.random.randint(1, 8, 20),
            "Experience": np.random.randint(1, 15, 20),
        }
    )

    return issues, volunteers


def generate_basic_data(n=20):
    np.random.seed(42)

    issues = pd.DataFrame(
        {
            "IssueID": [f"ISS{i}" for i in range(1, n + 1)],
            "Location": np.random.choice(["A", "B", "C", "D"], n),
            "Severity": np.random.randint(1, 11, n),
            "Category": np.random.choice(["Infrastructure", "Medical", "Emergency"], n),
            "Status": np.random.choice(["Active", "In Progress", "Resolved"], n),
        }
    )

    volunteers = pd.DataFrame(
        {
            "Name": [f"Vol{i}" for i in range(1, 16)],
            "Location": np.random.choice(["A", "B", "C", "D"], 15),
            "Availability": np.random.choice(["Yes", "No"], 15, p=[0.7, 0.3]),
            "Capacity": np.random.randint(1, 6, 15),
        }
    )

    return issues, volunteers


# Load data based on selection
is_enhanced = "Enhanced" in data_option
issues, volunteers = (
    generate_enhanced_data(50) if is_enhanced else generate_basic_data(20)
)


# ================= PROCESSING LOGIC =================
def get_priority(severity):
    if severity >= 8:
        return "High"
    elif severity >= 5:
        return "Medium"
    else:
        return "Low"


issues["Priority"] = issues["Severity"].apply(get_priority)


# Advanced matching algorithm
def match_volunteers(issue, volunteers_df):
    available = volunteers_df[volunteers_df["Availability"] == "Yes"]

    # Perfect location match
    perfect_match = available[available["Location"] == issue["Location"]]
    if not perfect_match.empty:
        # Sort by capacity and get best fit
        best_match = perfect_match.sort_values("Capacity", ascending=False).iloc[0]
        return best_match["Name"], "🎯 Perfect Match"

    # No match found
    return "Not Assigned", "❌ No Match"


# Apply matching
assignments = []
match_scores = []
for _, row in issues.iterrows():
    assigned, score = match_volunteers(row, volunteers)
    assignments.append(assigned)
    match_scores.append(score)

issues["Assigned Volunteer"] = assignments
issues["Match Quality"] = match_scores

# Filter by severity if needed
filtered_issues = issues[issues["Severity"] >= severity_filter]

# ================= MAIN HEADER =================
st.markdown(
    '<h1 class="main-header">🎯 Smart Resource Allocation System</h1>',
    unsafe_allow_html=True,
)
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ================= NAVIGATION =================
selected = option_menu(
    menu_title=None,
    options=[
        "📊 Dashboard",
        "🚨 Issue Management",
        "👥 Volunteer Directory",
        "🎯 Resource Allocation",
        "📈 Analytics",
    ],
    icons=["house", "exclamation-triangle", "people", "git-pull", "graph-up"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "#a78bfa", "font-size": "18px"},
        "nav-link": {
            "font-size": "15px",
            "text-align": "center",
            "margin": "0px 5px",
            "--hover-color": "rgba(99, 102, 241, 0.2)",
            "border-radius": "10px",
            "color": "white",
        },
        "nav-link-selected": {
            "background": "linear-gradient(135deg, #6366f1, #8b5cf6)",
            "color": "white",
        },
    },
)

# ================= DASHBOARD =================
if selected == "📊 Dashboard":
    st.markdown("### 📈 Real-time Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="stat-label">📋 Total Issues</div>
            <div class="stat-number">{len(issues)}</div>
            <div style="font-size: 0.75rem;">Active incidents</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        high_priority = len(issues[issues["Priority"] == "High"])
        st.markdown(
            f"""
        <div class="metric-card critical-card">
            <div class="stat-label">⚠️ High Priority</div>
            <div class="stat-number">{high_priority}</div>
            <div style="font-size: 0.75rem;">Critical issues</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        assigned = len(issues[issues["Assigned Volunteer"] != "Not Assigned"])
        st.markdown(
            f"""
        <div class="metric-card success-card">
            <div class="stat-label">✅ Assigned Issues</div>
            <div class="stat-number">{assigned}</div>
            <div style="font-size: 0.75rem;">{assigned / len(issues) * 100:.0f}% coverage</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        available_vols = len(volunteers[volunteers["Availability"] == "Yes"])
        st.markdown(
            f"""
        <div class="metric-card info-card">
            <div class="stat-label">👥 Available</div>
            <div class="stat-number">{available_vols}</div>
            <div style="font-size: 0.75rem;">Volunteers ready</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Charts Row
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Priority Distribution")
        priority_counts = issues["Priority"].value_counts()
        fig = px.pie(
            values=priority_counts.values,
            names=priority_counts.index,
            color=priority_counts.index,
            color_discrete_map={
                "High": "#ef4444",
                "Medium": "#f59e0b",
                "Low": "#10b981",
            },
            hole=0.4,
        )
        fig.update_layout(
            showlegend=True,
            height=400,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📍 Issues by Location")
        location_counts = issues["Location"].value_counts().head(8)
        fig = px.bar(
            x=location_counts.values,
            y=location_counts.index,
            orientation="h",
            color=location_counts.values,
            color_continuous_scale="Viridis",
            title="Top Locations",
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            xaxis_title="Number of Issues",
            yaxis_title="Location",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Match Quality Distribution
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🎯 Match Quality Distribution")
    col1, col2, col3 = st.columns(3)
    with col1:
        perfect = len(issues[issues["Match Quality"] == "🎯 Perfect Match"])
        st.metric(
            "Perfect Matches", perfect, delta=f"{perfect / len(issues) * 100:.0f}%"
        )
    with col2:
        unassigned = len(issues[issues["Assigned Volunteer"] == "Not Assigned"])
        st.metric(
            "Unassigned Issues",
            unassigned,
            delta=f"{unassigned / len(issues) * 100:.0f}%",
            delta_color="inverse",
        )
    with col3:
        coverage = (
            len(issues[issues["Assigned Volunteer"] != "Not Assigned"])
            / len(issues)
            * 100
        )
        st.metric("Coverage Rate", f"{coverage:.0f}%", delta="Active")
    st.markdown("</div>", unsafe_allow_html=True)

    # Recent Issues
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📋 Recent Critical Issues")

    display_df = (
        filtered_issues[
            [
                "IssueID",
                "Location",
                "Severity",
                "Priority",
                "Assigned Volunteer",
                "Match Quality",
            ]
        ]
        .head(10)
        .copy()
    )
    display_df["Priority"] = display_df["Priority"].apply(add_priority_badge)

    st.markdown(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= ISSUE MANAGEMENT =================
elif selected == "🚨 Issue Management":
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📋 Issue Management Dashboard")

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        priority_filter = st.multiselect(
            "🎨 Priority Filter",
            options=issues["Priority"].unique(),
            default=issues["Priority"].unique(),
        )
    with col2:
        if "Category" in issues.columns:
            category_filter = st.multiselect(
                "📂 Category Filter", options=issues["Category"].unique()
            )
    with col3:
        if "Status" in issues.columns:
            status_filter = st.multiselect(
                "🔄 Status Filter", options=issues["Status"].unique()
            )

    # Apply filters
    filtered = issues.copy()
    if priority_filter:
        filtered = filtered[filtered["Priority"].isin(priority_filter)]
    if "Category" in issues.columns and category_filter:
        filtered = filtered[filtered["Category"].isin(category_filter)]
    if "Status" in issues.columns and status_filter:
        filtered = filtered[filtered["Status"].isin(status_filter)]

    # Display filtered data
    display_filtered = filtered.copy()
    display_filtered["Priority"] = display_filtered["Priority"].apply(
        add_priority_badge
    )

    st.markdown(
        display_filtered.to_html(escape=False, index=False), unsafe_allow_html=True
    )

    # Export button
    if st.button("📥 Export to CSV", use_container_width=True):
        csv = filtered.to_csv(index=False)
        st.download_button(
            "Download CSV",
            csv,
            f"issues_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ================= VOLUNTEER DIRECTORY =================
elif selected == "👥 Volunteer Directory":
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🌟 Volunteer Directory")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👥 Total Volunteers", len(volunteers))
    with col2:
        available = len(volunteers[volunteers["Availability"] == "Yes"])
        st.metric(
            "✅ Available Now",
            available,
            delta=f"{available / len(volunteers) * 100:.0f}%",
        )
    with col3:
        total_capacity = (
            volunteers[volunteers["Availability"] == "Yes"]["Capacity"].sum()
            if "Capacity" in volunteers.columns
            else 0
        )
        st.metric("💪 Total Capacity", f"{total_capacity} issues/day")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Volunteer table with styling
    st.dataframe(
        volunteers.style.background_gradient(cmap="Blues"), use_container_width=True
    )

    # Volunteer workload summary
    if "Assigned Volunteer" in issues.columns:
        st.subheader("📊 Volunteer Workload")
        workload = pd.merge(
            volunteers,
            issues[issues["Assigned Volunteer"] != "Not Assigned"]
            .groupby("Assigned Volunteer")
            .size()
            .reset_index(name="Current Load"),
            left_on="Name",
            right_on="Assigned Volunteer",
            how="left",
        ).fillna(0)

        if "Capacity" in workload.columns:
            workload["Utilization"] = (
                workload["Current Load"] / workload["Capacity"] * 100
            ).round(1)
            workload["Utilization"] = workload["Utilization"].apply(lambda x: f"{x}%")

        st.dataframe(
            workload[
                [
                    "Name",
                    "Location",
                    "Skills",
                    "Availability",
                    "Current Load",
                    "Utilization",
                ]
            ],
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ================= RESOURCE ALLOCATION =================
elif selected == "🎯 Resource Allocation":
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🔄 Resource Allocation Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Current Assignments")
        assignment_summary = (
            issues[issues["Assigned Volunteer"] != "Not Assigned"]
            .groupby("Assigned Volunteer")
            .size()
            .reset_index(name="Assigned Issues")
        )
        st.dataframe(
            assignment_summary.style.background_gradient(cmap="Greens"),
            use_container_width=True,
        )

    with col2:
        st.subheader("📈 Volunteer Utilization")
        if "Assigned Volunteer" in issues.columns:
            utilization = pd.merge(
                volunteers,
                issues[issues["Assigned Volunteer"] != "Not Assigned"]
                .groupby("Assigned Volunteer")
                .size()
                .reset_index(name="Current Load"),
                left_on="Name",
                right_on="Assigned Volunteer",
                how="left",
            ).fillna(0)

            if "Capacity" in utilization.columns:
                utilization["Utilization %"] = (
                    utilization["Current Load"] / utilization["Capacity"] * 100
                ).round(1)
                st.dataframe(
                    utilization[
                        [
                            "Name",
                            "Location",
                            "Capacity",
                            "Current Load",
                            "Utilization %",
                        ]
                    ].style.background_gradient(
                        subset=["Utilization %"], cmap="RdYlGn", vmin=0, vmax=100
                    ),
                    use_container_width=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)

# ================= ANALYTICS =================
elif selected == "📈 Analytics":
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📈 Advanced Analytics Dashboard")

    tab1, tab2 = st.tabs(["📊 Visual Analytics", "🎯 Performance Metrics"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Severity Distribution")
            fig = px.histogram(
                issues,
                x="Severity",
                nbins=10,
                color="Priority",
                color_discrete_map={
                    "High": "#ef4444",
                    "Medium": "#f59e0b",
                    "Low": "#10b981",
                },
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            if "Category" in issues.columns:
                st.subheader("Issues by Category")
                category_counts = issues["Category"].value_counts()
                fig = px.pie(
                    values=category_counts.values, names=category_counts.index, hole=0.3
                )
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white"),
                )
                st.plotly_chart(fig, use_container_width=True)

        if "ReportedTime" in issues.columns:
            st.subheader("Hourly Distribution")
            issues["Hour"] = pd.to_datetime(issues["ReportedTime"]).dt.hour
            hourly_dist = issues["Hour"].value_counts().sort_index()
            fig = px.line(x=hourly_dist.index, y=hourly_dist.values, markers=True)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                xaxis_title="Hour of Day",
                yaxis_title="Number of Issues",
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("🎯 Key Performance Indicators")

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        with kpi1:
            response_rate = (
                len(issues[issues["Assigned Volunteer"] != "Not Assigned"])
                / len(issues)
                * 100
            )
            st.metric("Response Rate", f"{response_rate:.1f}%", delta="Target: 90%")

        with kpi2:
            avg_severity = issues["Severity"].mean()
            st.metric("Avg Severity", f"{avg_severity:.1f}/10", delta="Moderate")

        with kpi3:
            high_priority_pct = (
                len(issues[issues["Priority"] == "High"]) / len(issues) * 100
            )
            st.metric(
                "High Priority %", f"{high_priority_pct:.1f}%", delta="Needs attention"
            )

        with kpi4:
            if (
                "Capacity" in volunteers.columns
                and len(volunteers[volunteers["Availability"] == "Yes"]) > 0
            ):
                volunteer_utilization = (
                    len(issues[issues["Assigned Volunteer"] != "Not Assigned"])
                    / (
                        len(volunteers[volunteers["Availability"] == "Yes"])
                        * volunteers[volunteers["Availability"] == "Yes"][
                            "Capacity"
                        ].mean()
                    )
                    * 100
                )
                st.metric(
                    "Resource Utilization",
                    f"{volunteer_utilization:.1f}%",
                    delta="Optimal",
                )
            else:
                st.metric("Resource Utilization", "N/A", delta="No data")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown(
    """
<div class="footer">
    <div style="font-size: 1rem;">🚀 Smart Resource Allocation System v3.0</div>
    <div style="font-size: 0.8rem; margin-top: 8px;">Powered by AI • Real-time Analytics • Intelligent Matching</div>
    <div style="font-size: 0.7rem; margin-top: 5px;">🎯 Optimizing resource distribution for emergency response</div>
</div>
""",
    unsafe_allow_html=True,
)
