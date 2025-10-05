# Progress reports
"""
Reports component for generating and displaying detailed analytics reports
Comprehensive progress analysis and insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def render_reports_page():
    """Render the main reports page"""
    st.title("📈 Progress Reports & Analytics")
    
    # Report type selector
    report_type = st.selectbox(
        "Select Report Type:",
        ["📊 Weekly Summary", "📅 Monthly Overview", "📚 Subject Deep Dive", "😊 Wellbeing Report"],
        key="report_type"
    )
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=7))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # Generate report button
    if st.button("📋 Generate Report", type="primary"):
        if report_type == "📊 Weekly Summary":
            render_weekly_summary(start_date, end_date)
        elif report_type == "📅 Monthly Overview":
            render_monthly_overview(start_date, end_date)
        elif report_type == "📚 Subject Deep Dive":
            render_subject_deep_dive(start_date, end_date)
        elif report_type == "😊 Wellbeing Report":
            render_wellbeing_report(start_date, end_date)
    
    # Export options
    render_export_options()

def render_weekly_summary(start_date, end_date):
    """Render weekly progress summary"""
    st.subheader("📊 Weekly Progress Summary")
    st.caption(f"Report period: {start_date} to {end_date}")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Study Time", "18h 45m", "+3h 20m")
    with col2:
        st.metric("Sessions Completed", "12", "+3")
    with col3:
        st.metric("Average Understanding", "8.2/10", "+0.5")
    
    # Study pattern analysis
    st.subheader("📈 Study Patterns")
    
    # Mock hourly study pattern
    hours = list(range(24))
    study_intensity = [
        0, 0, 0, 0, 0, 0, 0.2, 0.8, 1.0, 0.9, 0.7, 0.5,
        0.3, 0.4, 0.6, 0.8, 0.9, 0.7, 0.5, 0.3, 0.2, 0.1, 0, 0
    ]
    
    fig = px.bar(
        x=hours, 
        y=study_intensity,
        labels={'x': 'Hour of Day', 'y': 'Study Intensity'},
        title="Study Intensity by Hour of Day"
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # Subject performance
    render_subject_performance_table()
    
    # AI insights
    render_ai_weekly_insights()

def render_monthly_overview(start_date, end_date):
    """Render monthly overview report"""
    st.subheader("📅 Monthly Learning Overview")
    st.caption(f"Report period: {start_date} to {end_date}")
    
    # Monthly trends
    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    study_hours = [15, 18, 22, 19]
    understanding_avg = [7.2, 7.8, 8.1, 8.3]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=weeks, 
        y=study_hours,
        mode='lines+markers',
        name='Study Hours',
        yaxis='y',
        line=dict(color='blue', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=weeks,
        y=understanding_avg, 
        mode='lines+markers',
        name='Avg Understanding',
        yaxis='y2',
        line=dict(color='green', width=3)
    ))
    
    fig.update_layout(
        title="Monthly Progress Trends",
        yaxis=dict(title="Study Hours"),
        yaxis2=dict(title="Understanding Level", overlaying='y', side='right', range=[0, 10]),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Monthly achievements
    render_monthly_achievements()
    
    # Subject progress over time
    render_subject_progress_over_time()

def render_subject_deep_dive(start_date, end_date):
    """Render detailed subject analysis"""
    st.subheader("📚 Subject Deep Dive Analysis")
    
    # Subject selector
    subject = st.selectbox(
        "Select Subject:",
        ["Mathematics", "Physics", "Chemistry", "Literature", "History"]
    )
    
    st.caption(f"Analysis for {subject} | {start_date} to {end_date}")
    
    # Subject metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Time Spent", "6h 30m", "+45m")
    with col2:
        st.metric("Topics Covered", "8", "+2")
    with col3:
        st.metric("Avg Understanding", "8.5/10", "+0.3")
    with col4:
        st.metric("Sessions", "5", "+1")
    
    # Topic breakdown
    st.subheader("🎯 Topic Performance")
    
    # Mock topic data
    topics = [
        "Calculus Integration", "Differential Equations", "Linear Algebra",
        "Statistics", "Trigonometry"
    ]
    understanding_levels = [8.5, 7.2, 9.1, 6.8, 8.0]
    time_spent = [90, 75, 120, 60, 85]
    
    df = pd.DataFrame({
        'Topic': topics,
        'Understanding Level': understanding_levels,
        'Time Spent (mins)': time_spent,
        'Status': ['✅ Mastered', '📚 Learning', '✅ Mastered', '⚠️ Needs Work', '✅ Mastered'],
        'Difficulty': ['Medium', 'Hard', 'Easy', 'Hard', 'Medium']
    })
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Understanding progression
    render_understanding_progression(subject)
    
    # Recommendations for the subject
    render_subject_recommendations(subject)

def render_wellbeing_report(start_date, end_date):
    """Render emotional wellbeing and mental health report"""
    st.subheader("😊 Wellbeing & Mental Health Report")
    st.caption(f"Report period: {start_date} to {end_date}")
    
    # Wellbeing metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Positive Days", "5/7", "+1")
    with col2:
        st.metric("Stress Level", "Low", "↓ Improved")
    with col3:
        st.metric("Motivation Score", "8.2/10", "+0.8")
    
    # Emotion distribution
    st.subheader("😊 Emotional State Distribution")
    
    emotions = ['Happy', 'Excited', 'Neutral', 'Stressed', 'Confused']
    percentages = [35, 25, 20, 15, 5]
    
    fig = px.pie(
        values=percentages,
        names=emotions,
        title="Emotional States This Week",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Stress factors
    render_stress_analysis()
    
    # Wellbeing recommendations
    render_wellbeing_recommendations()
    
    # Mood calendar
    render_mood_calendar()

def render_subject_performance_table():
    """Render subject performance breakdown table"""
    st.subheader("📊 Subject Performance Breakdown")
    
    subjects_data = [
        {
            'Subject': 'Mathematics',
            'Time Spent': '5h 30m',
            'Understanding': '8.5/10',
            'Progress': '📈 Improving',
            'Next Focus': 'Integration techniques',
            'Confidence': 'High'
        },
        {
            'Subject': 'Physics', 
            'Time Spent': '4h 15m',
            'Understanding': '7.8/10',
            'Progress': '📈 Improving',
            'Next Focus': 'Quantum mechanics',
            'Confidence': 'Medium'
        },
        {
            'Subject': 'Chemistry',
            'Time Spent': '3h 45m', 
            'Understanding': '8.9/10',
            'Progress': '✅ Excellent',
            'Next Focus': 'Organic reactions',
            'Confidence': 'High'
        },
        {
            'Subject': 'Literature',
            'Time Spent': '2h 30m',
            'Understanding': '7.2/10', 
            'Progress': '⚠️ Needs attention',
            'Next Focus': 'Essay structure',
            'Confidence': 'Low'
        }
    ]
    
    df = pd.DataFrame(subjects_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_ai_weekly_insights():
    """Render AI-generated weekly insights"""
    st.subheader("🧠 AI-Generated Insights")
    
    insights = [
        {
            'type': 'success',
            'title': 'Great Progress!',
            'content': 'Your Mathematics understanding improved by 15% this week. The extra time on integration is paying off!'
        },
        {
            'type': 'info', 
            'title': 'Study Pattern',
            'content': 'You study most effectively between 9-11 AM. Consider scheduling challenging topics during this time.'
        },
        {
            'type': 'warning',
            'title': 'Attention Needed',
            'content': 'Literature requires more focus. Consider breaking reading sessions into smaller chunks.'
        },
        {
            'type': 'info',
            'title': 'Recommendation',
            'content': 'Take 5-minute breaks every 25 minutes to maintain concentration (Pomodoro technique).'
        }
    ]
    
    for insight in insights:
        if insight['type'] == 'success':
            st.success(f"**{insight['title']}**: {insight['content']}")
        elif insight['type'] == 'warning':
            st.warning(f"**{insight['title']}**: {insight['content']}")
        else:
            st.info(f"**{insight['title']}**: {insight['content']}")

def render_monthly_achievements():
    """Render monthly achievements and milestones"""
    st.subheader("🏆 Monthly Achievements")
    
    achievements = [
        "🎯 **Study Streak Champion** - 28 consecutive days of studying!",
        "📚 **Multi-Subject Master** - Excellent progress across 4 subjects",
        "⭐ **Understanding Expert** - Average understanding above 8/10", 
        "🕐 **Time Manager** - Consistently met weekly study time goals",
        "😊 **Positive Mindset** - Maintained high motivation throughout the month"
    ]
    
    for achievement in achievements:
        st.success(achievement)

def render_understanding_progression(subject):
    """Render understanding progression chart for a subject"""
    st.subheader(f"📈 {subject} Understanding Progression")
    
    # Mock progression data
    dates = pd.date_range(start=datetime.now() - timedelta(days=14), end=datetime.now(), freq='D')
    understanding_levels = [round(random.uniform(6.0, 9.5), 1) for _ in dates]
    
    # Add trend
    for i in range(1, len(understanding_levels)):
        understanding_levels[i] = max(understanding_levels[i-1] + random.uniform(-0.3, 0.5), 6.0)
    
    df = pd.DataFrame({
        'Date': dates,
        'Understanding Level': understanding_levels
    })
    
    fig = px.line(
        df,
        x='Date',
        y='Understanding Level', 
        title=f"{subject} Understanding Over Time",
        markers=True
    )
    fig.update_layout(height=400)
    fig.update_yaxis(range=[5, 10])
    st.plotly_chart(fig, use_container_width=True)

def render_stress_analysis():
    """Render stress level analysis"""
    st.subheader("📊 Stress Level Analysis")
    
    stress_factors = [
        {'Factor': 'Upcoming Exams', 'Impact': 'High', 'Frequency': 'Weekly'},
        {'Factor': 'Heavy Workload', 'Impact': 'Medium', 'Frequency': 'Daily'},
        {'Factor': 'Difficult Topics', 'Impact': 'Medium', 'Frequency': 'Occasional'},
        {'Factor': 'Time Management', 'Impact': 'Low', 'Frequency': 'Rare'}
    ]
    
    df = pd.DataFrame(stress_factors)
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_wellbeing_recommendations():
    """Render personalized wellbeing recommendations"""
    st.subheader("💡 Personalized Wellbeing Tips")
    
    recommendations = [
        "🧘 **Mindfulness**: Try 5 minutes of deep breathing before study sessions",
        "🚶 **Movement**: Take a 10-minute walk between subjects",
        "💤 **Sleep**: Maintain 7-8 hours of sleep for optimal learning",
        "🥗 **Nutrition**: Stay hydrated and eat brain-healthy snacks",
        "👥 **Social**: Study with friends or join study groups for motivation",
        "🎯 **Goals**: Set small, achievable daily goals to build confidence"
    ]
    
    for rec in recommendations:
        st.info(rec)

def render_mood_calendar():
    """Render mood tracking calendar"""
    st.subheader("📅 Mood Calendar")
    
    # Mock mood data for the past week
    dates = pd.date_range(start=datetime.now() - timedelta(days=6), end=datetime.now(), freq='D')
    moods = ['😊', '🎉', '😐', '😟', '😊', '🎉', '😊']
    
    cols = st.columns(7)
    for i, (date, mood) in enumerate(zip(dates, moods)):
        with cols[i]:
            st.markdown(f"**{date.strftime('%a')}**")
            st.markdown(f"**{mood}**")
            st.caption(date.strftime('%m/%d'))

def render_subject_progress_over_time():
    """Render subject progress over multiple weeks"""
    st.subheader("📈 Subject Progress Over Time")
    
    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    subjects = ['Math', 'Physics', 'Chemistry', 'Literature']
    
    fig = go.Figure()
    
    for subject in subjects:
        progress = [random.uniform(6, 9) for _ in weeks]
        fig.add_trace(go.Scatter(
            x=weeks,
            y=progress,
            mode='lines+markers',
            name=subject,
            line=dict(width=3)
        ))
    
    fig.update_layout(
        title="Understanding Level Progress by Subject",
        yaxis_title="Understanding Level",
        yaxis=dict(range=[0, 10]),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_subject_recommendations(subject):
    """Render specific recommendations for a subject"""
    st.subheader(f"💡 {subject} Recommendations")
    
    recommendations = {
        "Mathematics": [
            "Practice more word problems to improve application skills",
            "Use visual aids and diagrams for geometry concepts",
            "Review algebra fundamentals before tackling calculus",
            "Work on one problem type at a time to build confidence"
        ],
        "Physics": [
            "Connect mathematical formulas to real-world phenomena",
            "Practice drawing free body diagrams for mechanics problems",
            "Review units and dimensional analysis regularly",
            "Use simulation tools to visualize wave and particle behavior"
        ],
        "Chemistry": [
            "Master the periodic table patterns and trends",
            "Practice balancing chemical equations daily",
            "Use molecular models to understand 3D structures",
            "Connect macro observations to molecular explanations"
        ],
        "Literature": [
            "Read actively with annotation and note-taking",
            "Analyze themes and character development systematically",
            "Practice writing analytical essays with clear thesis statements",
            "Join discussion groups to explore different interpretations"
        ],
        "History": [
            "Create timelines to understand chronological relationships",
            "Focus on cause-and-effect relationships between events",
            "Use primary sources to understand historical perspectives",
            "Connect historical events to contemporary issues"
        ]
    }
    
    subject_recs = recommendations.get(subject, ["Keep studying and stay curious!"])
    
    for rec in subject_recs:
        st.info(f"• {rec}")

def render_export_options():
    """Render report export options"""
    st.subheader("📥 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export as PDF", use_container_width=True):
            st.success("PDF report generated! Check your downloads.")
    
    with col2:
        if st.button("📊 Export as Excel", use_container_width=True):
            # Create sample data for download
            sample_data = pd.DataFrame({
                'Date': pd.date_range(start='2025-09-22', end='2025-09-29'),
                'Subject': ['Math', 'Physics', 'Chemistry', 'Literature', 'Math', 'Physics', 'Chemistry', 'Literature'],
                'Study Time': [60, 45, 90, 30, 75, 60, 45, 40],
                'Understanding': [8, 7, 9, 6, 8, 8, 9, 7]
            })
            
            st.download_button(
                label="📊 Download Excel Report",
                data=sample_data.to_csv(index=False),
                file_name=f"study_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("📧 Email Report", use_container_width=True):
            st.info("Report will be sent to your registered email address.")
