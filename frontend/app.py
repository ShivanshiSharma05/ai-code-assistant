import streamlit as st
import requests
import pandas as pd


# ==================================
# PAGE CONFIGURATION
# ==================================

st.set_page_config(
    page_title="AI Code Assistant",
    page_icon="🤖",
    layout="wide"
)


# ==================================
# BACKEND API
# ==================================

API_URL = "http://127.0.0.1:8000"


# ==================================
# PAGE TITLE
# ==================================

st.title("🤖 AI Code Assistant")

st.write(
    "AI-powered repository intelligence platform that analyzes "
    "GitHub repositories, detects risks, prioritizes files, and "
    "generates actionable recommendations for developers."
)

st.divider()


# ==================================
# SIDEBAR
# ==================================

st.sidebar.header("⚙️ Settings")

st.sidebar.info(
    "Enter a public GitHub repository in the format:\n\n"
    "`owner/repository`"
)

st.sidebar.markdown("---")

st.sidebar.subheader("✨ Features")

st.sidebar.write("""
- Repository Analysis
- Code Quality Scoring
- Risk Detection
- File Prioritization
- Developer Action Plan
""")


# ==================================
# GITHUB REPOSITORY INPUT
# ==================================

st.header("📂 GitHub Repository Analysis")

repo_name = st.text_input(
    "Repository",
    placeholder="example: ShivanshiSharma05/ai-code-assistant"
)


analyze_button = st.button(
    "🚀 Analyze Repository",
    use_container_width=True
)


# ==================================
# ANALYZE REPOSITORY
# ==================================

if analyze_button:

    if not repo_name.strip():

        st.warning(
            "Please enter a GitHub repository."
        )

    else:

        with st.spinner(
            "🔍 Fetching repository and analyzing files..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/analyze-repo/",
                    json={
                        "repo": repo_name.strip()
                    },
                    timeout=120
                )


                # ==================================
                # HTTP ERROR HANDLING
                # ==================================

                if response.status_code != 200:

                    st.error(
                        f"Backend Error: {response.status_code}"
                    )

                    try:

                        error_data = response.json()

                        st.write(error_data)

                    except Exception:

                        st.write(response.text)


                else:

                    data = response.json()


                    # ==================================
                    # BACKEND ERROR CHECK
                    # ==================================

                    if "error" in data:

                        st.error(data["error"])

                        if "details" in data:

                            st.write(
                                data["details"]
                            )


                    else:

                        st.success(
                            "Repository analysis completed successfully!"
                        )


                        # ==================================
                        # GET ANALYSIS OUTPUT
                        # ==================================

                        output = data.get(
                            "output",
                            {}
                        )


                        if not output:

                            st.warning(
                                "No analysis results were returned."
                            )

                        else:

                            # ==================================
                            # CALCULATE SUMMARY DIRECTLY
                            # ==================================

                            total_files = 0

                            high_risk_files = 0

                            medium_risk_files = 0

                            low_risk_files = 0


                            for result in output.values():

                                if not isinstance(result, dict):
                                    continue

                                total_files += 1

                                risk_level = str(
                                    result.get(
                                        "risk_level",
                                        "LOW"
                                    )
                                ).upper()


                                if risk_level == "HIGH":

                                    high_risk_files += 1


                                elif risk_level == "MEDIUM":

                                    medium_risk_files += 1


                                else:

                                    low_risk_files += 1


                            # ==================================
                            # ANALYSIS RESULTS
                            # ==================================

                            st.divider()

                            st.header(
                                "📊 Analysis Results"
                            )


                            # ==================================
                            # SUMMARY METRICS
                            # ==================================

                            col1, col2, col3, col4 = st.columns(4)


                            with col1:

                                st.metric(
                                    "📁 Files Analyzed",
                                    total_files
                                )


                            with col2:

                                st.metric(
                                    "🔴 High Risk",
                                    high_risk_files
                                )


                            with col3:

                                st.metric(
                                    "🟠 Medium Risk",
                                    medium_risk_files
                                )


                            with col4:

                                st.metric(
                                    "🟢 Low Risk",
                                    low_risk_files
                                )


                            # ==================================
                            # RISK DISTRIBUTION
                            # ==================================

                            st.divider()

                            st.subheader(
                                "📈 Repository Risk Distribution"
                            )


                            chart_data = pd.DataFrame(
                                {
                                    "Risk Level": [
                                        "High Risk",
                                        "Medium Risk",
                                        "Low Risk"
                                    ],
                                    "Files": [
                                        high_risk_files,
                                        medium_risk_files,
                                        low_risk_files
                                    ]
                                }
                            )


                            st.bar_chart(
                                chart_data.set_index(
                                    "Risk Level"
                                )
                            )


                            # ==================================
                            # DEVELOPER PRIORITY QUEUE
                            # ==================================

                            st.divider()

                            st.header(
                                "🔥 Developer Priority Queue"
                            )

                            st.write(
                                "Files ranked by risk and priority score."
                            )


                            priority_files = []


                            for file_name, result in output.items():

                                if not isinstance(result, dict):
                                    continue


                                priority_score = result.get(
                                    "priority_score",
                                    0
                                )


                                risk_level = result.get(
                                    "risk_level",
                                    "LOW"
                                )


                                quality_score = result.get(
                                    "quality_score",
                                    0
                                )


                                complexity = result.get(
                                    "complexity",
                                    "Unknown"
                                )


                                priority_files.append(
                                    {
                                        "File": file_name,
                                        "Risk Level": risk_level,
                                        "Priority Score": priority_score,
                                        "Quality Score": quality_score,
                                        "Complexity": complexity
                                    }
                                )


                            # SORT BY PRIORITY

                            priority_files = sorted(
                                priority_files,
                                key=lambda x: x["Priority Score"],
                                reverse=True
                            )


                            if priority_files:

                                priority_df = pd.DataFrame(
                                    priority_files
                                )

                                st.dataframe(
                                    priority_df,
                                    use_container_width=True,
                                    hide_index=True
                                )

                            else:

                                st.info(
                                    "No priority data available."
                                )


                            # ==================================
                            # DEVELOPER ACTION PLAN
                            # ==================================

                            st.divider()

                            st.header(
                                "🎯 Developer Action Plan"
                            )

                            st.write(
                                "AI-generated prioritization plan to help "
                                "developers decide what to fix first."
                            )


                            fix_immediately = []

                            improve_soon = []

                            healthy_files = []


                            # ==================================
                            # CATEGORIZE FILES
                            # ==================================

                            for file_name, result in output.items():

                                if not isinstance(result, dict):
                                    continue


                                risk_level = str(
                                    result.get(
                                        "risk_level",
                                        "LOW"
                                    )
                                ).upper()


                                priority_score = result.get(
                                    "priority_score",
                                    0
                                )


                                bugs = result.get(
                                    "bugs",
                                    "No issues detected"
                                )


                                complexity = result.get(
                                    "complexity",
                                    "Unknown"
                                )


                                recommendation = result.get(
                                    "recommendation",
                                    result.get(
                                        "optimization",
                                        "Review this file"
                                    )
                                )


                                file_data = {

                                    "file_name": file_name,

                                    "priority_score": priority_score,

                                    "bugs": bugs,

                                    "complexity": complexity,

                                    "recommendation": recommendation
                                }


                                if risk_level == "HIGH":

                                    fix_immediately.append(
                                        file_data
                                    )


                                elif risk_level == "MEDIUM":

                                    improve_soon.append(
                                        file_data
                                    )


                                else:

                                    healthy_files.append(
                                        file_data
                                    )


                            # ==================================
                            # FIX IMMEDIATELY
                            # ==================================

                            st.subheader(
                                "🔥 Fix Immediately"
                            )


                            if fix_immediately:

                                fix_immediately = sorted(
                                    fix_immediately,
                                    key=lambda x: x[
                                        "priority_score"
                                    ],
                                    reverse=True
                                )


                                for item in fix_immediately:

                                    with st.expander(
                                        f"🚨 {item['file_name']} "
                                        f"(Priority: "
                                        f"{item['priority_score']})"
                                    ):

                                        st.error(
                                            f"🐛 Issue: "
                                            f"{item['bugs']}"
                                        )

                                        st.write(
                                            f"⚡ Complexity: "
                                            f"{item['complexity']}"
                                        )

                                        st.info(
                                            f"💡 Recommended Action: "
                                            f"{item['recommendation']}"
                                        )


                            else:

                                st.success(
                                    "🎉 No high-risk files detected."
                                )


                            # ==================================
                            # IMPROVE SOON
                            # ==================================

                            st.subheader(
                                "⚠️ Improve Soon"
                            )


                            if improve_soon:

                                improve_soon = sorted(
                                    improve_soon,
                                    key=lambda x: x[
                                        "priority_score"
                                    ],
                                    reverse=True
                                )


                                for item in improve_soon:

                                    with st.expander(
                                        f"⚠️ {item['file_name']} "
                                        f"(Priority: "
                                        f"{item['priority_score']})"
                                    ):

                                        st.warning(
                                            f"🐛 Issue: "
                                            f"{item['bugs']}"
                                        )

                                        st.write(
                                            f"⚡ Complexity: "
                                            f"{item['complexity']}"
                                        )

                                        st.info(
                                            f"💡 Recommended Action: "
                                            f"{item['recommendation']}"
                                        )


                            else:

                                st.success(
                                    "🎉 No medium-risk files detected."
                                )


                            # ==================================
                            # HEALTHY FILES
                            # ==================================

                            st.subheader(
                                "✅ Healthy Files"
                            )


                            if healthy_files:

                                st.write(
                                    f"🎉 {len(healthy_files)} files are "
                                    f"currently classified as low risk."
                                )


                                with st.expander(
                                    "View Healthy Files"
                                ):

                                    for item in healthy_files:

                                        st.write(
                                            f"✅ {item['file_name']} "
                                            f"(Priority: "
                                            f"{item['priority_score']})"
                                        )


                            else:

                                st.warning(
                                    "No low-risk files detected."
                                )


                            # ==================================
                            # DETAILED FILE ANALYSIS
                            # ==================================

                            st.divider()

                            st.header(
                                "📄 Detailed File Analysis"
                            )


                            for file_name, result in output.items():

                                if not isinstance(result, dict):
                                    continue


                                with st.expander(
                                    f"📄 {file_name}"
                                ):


                                    # BUGS

                                    bugs = result.get(
                                        "bugs",
                                        "No data available"
                                    )

                                    st.write(
                                        "### 🐛 Bugs"
                                    )

                                    st.write(bugs)


                                    # COMPLEXITY

                                    complexity = result.get(
                                        "complexity",
                                        "Unknown"
                                    )

                                    st.write(
                                        "### ⚡ Complexity"
                                    )

                                    st.write(complexity)


                                    # OPTIMIZATION

                                    optimization = result.get(
                                        "optimization",
                                        "No recommendation available"
                                    )

                                    st.write(
                                        "### 🚀 Optimization"
                                    )

                                    st.write(optimization)


                                    # QUALITY SCORE

                                    quality_score = result.get(
                                        "quality_score",
                                        "N/A"
                                    )

                                    st.write(
                                        "### ⭐ Quality Score"
                                    )

                                    st.metric(
                                        "Quality Score",
                                        quality_score
                                    )


                                    # RISK LEVEL

                                    risk_level = result.get(
                                        "risk_level",
                                        "LOW"
                                    )

                                    st.write(
                                        "### ⚠️ Risk Level"
                                    )

                                    st.write(risk_level)


                                    # PRIORITY SCORE

                                    priority_score = result.get(
                                        "priority_score",
                                        0
                                    )

                                    st.write(
                                        "### 🔥 Priority Score"
                                    )

                                    st.metric(
                                        "Priority Score",
                                        priority_score
                                    )


                                    # RISK REASONS

                                    risk_reasons = result.get(
                                        "risk_reasons",
                                        []
                                    )


                                    if risk_reasons:

                                        st.write(
                                            "### 🔎 Risk Reasons"
                                        )


                                        for reason in risk_reasons:

                                            st.write(
                                                f"- {reason}"
                                            )


                                    # RECOMMENDATION

                                    recommendation = result.get(
                                        "recommendation",
                                        optimization
                                    )

                                    st.write(
                                        "### 💡 Recommendation"
                                    )

                                    st.info(
                                        recommendation
                                    )


            # ==================================
            # CONNECTION ERROR
            # ==================================

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Cannot connect to backend API."
                )

                st.info(
                    "Make sure FastAPI is running."
                )


            # ==================================
            # TIMEOUT ERROR
            # ==================================

            except requests.exceptions.Timeout:

                st.error(
                    "⏳ Analysis timed out. Try again."
                )


            # ==================================
            # GENERAL ERROR
            # ==================================

            except Exception as e:

                st.error(
                    f"Unexpected Error: {str(e)}"
                )


# ==================================
# FOOTER
# ==================================

st.divider()

st.caption(
    "🤖 AI Code Assistant | Repository Intelligence Platform"
)