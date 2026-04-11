import streamlit as st
import tldextract
import pandas as pd
import re
import requests
import webbrowser
from datetime import datetime
import plotly.express as px

# 1. PAGE CONFIG & SESSION STATE (Must be at the very top)
st.set_page_config(layout="wide", page_title="PhishGuard AI")

if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []

# 2. GET CURRENT PAGE
current_page = st.query_params.get("page", "Home")

# 3. GLOBAL CSS & NAVBAR
st.markdown(f"""
    <style>
    /* Navbar CSS */
    header {{visibility: hidden;}}
    .nav-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #0e1117;
        padding: 10px 44px;
        position: fixed;
        height: 66px;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 9999;
        border-bottom: 1px solid #1f2937;
    }}
    .nav-logo {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 24px;
        font-weight: bold;
        color: #00f2ff;
        text-decoration: none;
    }}
    .nav-links {{
        display: flex;
        gap: 25px;
    }}
    .nav-links a {{
        color: #ffffff;
        text-decoration: none;
        font-size: 16px;
        font-weight: 400;
        transition: 0.3s;
    }}
    .nav-links a:hover, .active-link {{
        color: #00f2ff !important;
    }}
    .main-content {{
        margin-top: 86px;
    }}
    
    /* App UI CSS */
    .stApp {{
        background-color: #FFFFFF;
        bottom: 0 !important;
    }}
    .main-header {{
        text-align: center;
        color: #1a2b4b;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        margin-top: 50px;
    }}
    .sub-text {{
        text-align: center;
        color: #6c757d;
        margin-bottom: 40px;
    }}
    div.stButton > button:first-child {{
        background-color: #4a80f0;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        display: block;
        margin: 0 auto;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        display: flex;
        justify-content: center;
        gap: 50px;
        border-bottom: none;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 60px;
        background-color: transparent;
        border: none;
        font-size: 18px;
        color: #6c757d;
    }}
    .stTabs [aria-selected="true"] {{
        color: #4a80f0 !important;
        border-bottom: 3px solid #4a80f0 !important;
    }}
    header, footer {{
        visibility: hidden !important;
        height: 1px !important;
    }}
    .main .block-container {{
        padding-bottom: 0rem !important;
        padding-top: 3rem !important;
    }}
    .custom-footer {{
        background-color: #f8f9fa;
        color: #6c757d;
        text-align: center;
        padding: 40px 20px;
        border-top: 1px solid #e9ecef;
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-top:43px;
        margin-left: -50vw;
        margin-right: -50vw;
        margin-bottom: -154px; 
        padding-bottom: 65px;
    }}
    .footer-links a {{
        color: #4a80f0;
        text-decoration: none;
        margin: 0 15px;
        font-weight: 500;
    }}
    </style>

    <div class="nav-container">
        <a href="/?page=Home" target="_self" class="nav-logo">PhishGuard</a>
        <div class="nav-links">
            <a href="/?page=Home" target="_self" class="{'active-link' if current_page == 'Home' else ''}">Home</a>
            <a href="/?page=Scan" target="_self" class="{'active-link' if current_page == 'Scan' else ''}">Scan</a>
            <a href="/?page=Performance" target="_self" class="{'active-link' if current_page == 'Performance' else ''}">Performance</a>
            <a href="/?page=Charts" target="_self" class="{'active-link' if current_page == 'Charts' else ''}">Charts</a>
            <a href="/?page=Logout" target="_self">Log Out</a>
        </div>
    </div>
    <div class="main-content"></div>
""", unsafe_allow_html=True)


# 4. FUNCTION DEFINITIONS
def display_performance_metrics():
    # --- 1. MAIN PERFORMANCE TABLE ---
    st.markdown("""
<style>
.metrics-container { background-color: #0e1117; padding: 30px; border-radius: 15px; border: 1px solid #1f2937; margin-top: 30px; }
.metrics-table { width: 100%; border-collapse: collapse; color: #ffffff; font-family: 'Segoe UI', sans-serif; }
.metrics-table th { text-align: left; padding: 15px; color: #00f2ff; border-bottom: 2px solid #1f2937; font-size: 14px; }
.metrics-table td { padding: 15px; border-bottom: 1px solid #1f2937; font-size: 14px; }
.highlight-text { color: #00f2ff; font-weight: bold; }
.status-badge { background-color: #00f2ff22; color: #00f2ff; padding: 5px 12px; border-radius: 20px; font-size: 12px; border: 1px solid #00f2ff; }

/* CSS for the 3 Confusion Matrix Cards */
.cm-card-wrapper {
    background-color: #0b1018;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 20px 10px;
    text-align: center;
    height: 100%;
}
.hm-table { margin: 0 auto; border-collapse: collapse; font-size: 11px; color: #8b9bb4; }
.hm-table td { padding: 0; }
.hm-cell {
    width: 162px; height: 151px;
    display: flex; align-items: center; justify-content: center;
    font-weight: bold; font-size: 16px; margin: 1px;
}
.hm-metric-row {
    display: flex; justify-content: space-around; margin-top: 25px;
}
.hm-badge {
    background-color: rgba(255,255,255,0.03);
    padding: 6px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;
}
</style>

<div class="metrics-container">
    <table class="metrics-table">
        <tr><th>Model</th><th>Accuracy</th><th>F1-Score</th><th>Recall</th><th>Precision</th><th>Status</th></tr>
        <tr><td>Gradient Boosting Classifier</td><td class="highlight-text">97.4%</td><td class="highlight-text">97.7%</td><td class="highlight-text">98.9%</td><td class="highlight-text">96.6%</td><td><span class="status-badge">SELECTED</span></td></tr>
        <tr><td>XGBoost Classifier</td><td class="highlight-text">97.1%</td><td class="highlight-text">97.4%</td><td class="highlight-text">98.3%</td><td class="highlight-text">96.5%</td><td><span class="status-badge">SELECTED</span></td></tr>
        <tr><td>Multi-layer Perceptron (MLP)</td><td class="highlight-text">96.9%</td><td class="highlight-text">98.9%</td><td class="highlight-text">98.2%</td><td class="highlight-text">96.3%</td><td><span class="status-badge">SELECTED</span></td></tr>
        <tr><td>Random Forest</td><td>96.7%</td><td>97.1%</td><td>97.4%</td><td>96.7%</td><td>-</td></tr>
    </table>
</div>
<div style="margin-top: 40px; margin-bottom: 20px;">
    <h3 style='color: #00f2ff;'>🎯 Confusion Matrices - Top 3 Models</h3>
</div>
    """, unsafe_allow_html=True)

    # --- 2. THE 3 CONFUSION MATRIX CARDS ---
    col1, col2, col3 = st.columns(3)

    # CARD 1: Gradient Boosting (Cyan)
    with col1:
        st.markdown("""
<div class="cm-card-wrapper">
    <h4 style="color: #00f2ff; margin-bottom: 5px; font-size: 16px;>Gradient Boosting Classifier</h4>
    <p style="color: #00f2ff; font-size: 12px; margin-bottom: 20px; opacity: 0.8;">Gradient Boosting Classifier</p>
    <div style="display: flex; align-items: center; justify-content: center;">
        <div style="transform: rotate(-90deg); color: #8b9bb4; font-size: 11px; margin-right: -25px;"></div>
        <table class="hm-table">
            <tr>
                <td style="text-align: right; padding-right: 8px;">Phishing</td>
                <td><div class="hm-cell" style="background-color: #00f2ff; color: #000;">933</div></td>
                <td><div class="hm-cell" style="background-color: #111827; color: #00f2ff;">43</div></td>
            </tr>
            <tr>
                <td style="text-align: right; padding-right: 8px;">Legitimate</td>
                <td><div class="hm-cell" style="background-color: #111827; color: #00f2ff;">14</div></td>
                <td><div class="hm-cell" style="background-color: #00f2ff; color: #000;">1221</div></td>
            </tr>
            <tr>
                <td></td><td style="padding-top: 8px;">Phishing</td><td style="padding-top: 8px;">Legitimate</td>
            </tr>
        </table>
    </div>
    <div style="color: #8b9bb4; font-size: 11px; margin-top: 5px;">Predicted Label</div>
    <div class="hm-metric-row">
        <div class="hm-badge" style="border: 1px solid #00f2ff; color: #00f2ff;">✓ Accuracy: 97.4%</div>
        <div class="hm-badge" style="border: 1px solid #00f2ff; color: #00f2ff;">✓ F1-Score: 97.7%</div>
    </div>
</div>
        """, unsafe_allow_html=True)

    # CARD 2: XGBoost (Light Blue)
    with col2:
        st.markdown("""
<div class="cm-card-wrapper">
    <h4 style="color: #4ea8de; margin-bottom: 5px; font-size: 16px;">XGBoost Classifier</h4>
    <p style="color: #4ea8de; font-size: 12px; margin-bottom: 20px; opacity: 0.8;">XGBoost Classifier</p>
    <div style="display: flex; align-items: center; justify-content: center;">
        <div style="transform: rotate(-90deg); color: #8b9bb4; font-size: 11px; margin-right: -25px;"></div>
        <table class="hm-table">
            <tr>
                <td style="text-align: right; padding-right: 8px;">Phishing</td>
                <td><div class="hm-cell" style="background-color: #4ea8de; color: #000;">932</div></td>
                <td><div class="hm-cell" style="background-color: #111827; color: #4ea8de;">44</div></td>
            </tr>
            <tr>
                <td style="text-align: right; padding-right: 8px;">Legitimate</td>
                <td><div class="hm-cell" style="background-color: #111827; color: #4ea8de;">21</div></td>
                <td><div class="hm-cell" style="background-color: #4ea8de; color: #000;">1214</div></td>
            </tr>
            <tr>
                <td></td><td style="padding-top: 8px;">Phishing</td><td style="padding-top: 8px;">Legitimate</td>
            </tr>
        </table>
    </div>
    <div style="color: #8b9bb4; font-size: 11px; margin-top: 5px;">Predicted Label</div>
    <div class="hm-metric-row">
        <div class="hm-badge" style="border: 1px solid #4ea8de; color: #4ea8de;">✓ Accuracy: 97.1%</div>
        <div class="hm-badge" style="border: 1px solid #4ea8de; color: #4ea8de;">✓ F1-Score: 97.4%</div>
    </div>
</div>
        """, unsafe_allow_html=True)

    # CARD 3: Multi-layer Perceptron (Green)
    with col3:
        st.markdown("""
<div class="cm-card-wrapper" style="border-color: #20c997; box-shadow: 0 0 15px rgba(32, 201, 151, 0.15);">
    <h4 style="color: #20c997; margin-bottom: 5px; font-size: 16px;">Multi-layer Perceptron</h4>
    <p style="color: #20c997; font-size: 12px; margin-bottom: 20px; opacity: 0.8;">Multi-layer Perceptron</p>
    <div style="display: flex; align-items: center; justify-content: center;">
        <div style="transform: rotate(-90deg); color: #8b9bb4; font-size: 11px; margin-right: -25px;"></div>
        <table class="hm-table">
            <tr>
                <td style="text-align: right; padding-right: 8px;">Phishing</td>
                <td><div class="hm-cell" style="background-color: #20c997; color: #000;">929</div></td>
                <td><div class="hm-cell" style="background-color: #111827; color: #20c997;">47</div></td>
            </tr>
            <tr>
                <td style="text-align: right; padding-right: 8px;">Legitimate</td>
                <td><div class="hm-cell" style="background-color: #111827; color: #20c997;">22</div></td>
                <td><div class="hm-cell" style="background-color: #20c997; color: #000;">1213</div></td>
            </tr>
            <tr>
                <td></td><td style="padding-top: 8px;">Phishing</td><td style="padding-top: 8px;">Legitimate</td>
            </tr>
        </table>
    </div>
    <div style="color: #8b9bb4; font-size: 11px; margin-top: 5px;">Predicted Label</div>
    <div class="hm-metric-row">
        <div class="hm-badge" style="border: 1px solid #20c997; color: #20c997;">✓ Accuracy: 96.9%</div>
        <div class="hm-badge" style="border: 1px solid #20c997; color: #20c997;">✓ F1-Score: 97.5%</div>
    </div>
</div>
        """, unsafe_allow_html=True)
        
        
        # graph comparsion
def display_metrics_chart():
    st.markdown("""
        <div style="margin-top: 30px; margin-bottom: 20px;">
            <h2 style='color: #00f2ff;'>📈 Model Comparison Trend Analysis</h2>
            <p style="color: #6c757d;">Interactive performance breakdown across all evaluated machine learning models.</p>
        </div>
    """, unsafe_allow_html=True)

    # 1. The Data
    data = {
        "Model": ["Gradient Boosting", "XGBoost", "MLP", "Random Forest", "SVM"],
        "Accuracy": [97.4, 97.1, 96.9, 96.7, 96.4],
        "F1-Score": [97.7, 97.4, 98.9, 97.1, 96.8],
        "Recall": [98.9, 98.3, 98.2, 97.4, 98.0],
        "Precision": [96.6, 96.5, 96.3, 96.7, 95.7]
    }
    df = pd.DataFrame(data)
    
    # 2. Reshape data for Plotly
    df_melted = df.melt(id_vars="Model", var_name="Metric", value_name="Score (%)")

    # 3. Create the Interactive Line Chart
    fig = px.line(
        df_melted, 
        x="Model", 
        y="Score (%)", 
        color="Metric", 
        markers=True, # This adds the dots on the lines!
        color_discrete_sequence=["#00f2ff", "#4ea8de", "#20c997", "#8b9bb4"] # Matching your brand colors
    )

    # 4. Apply Dark Theme Styling & Grid Tweaks
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff",
        title_font_color="#00f2ff",
        legend_title_text='Evaluation Metrics',
        yaxis=dict(range=[95, 100], gridcolor="#1f2937"), # Adjusted zoom to 95-100% for better line visibility
        xaxis=dict(showgrid=False), # Hiding vertical grid lines for a cleaner look
        margin=dict(l=0, r=0, t=30, b=0),
        hovermode="x unified" # Shows all metrics at once when hovering over a model
    )
    
    # Make the lines and dots slightly thicker for a premium feel
    fig.update_traces(line=dict(width=3), marker=dict(size=8))

    # 5. Add a dark container around the chart
    with st.container():
        st.markdown('<div style="background-color: #0e1117; padding: 20px; border-radius: 15px; border: 1px solid #1f2937;">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def agentic_email_report(text):
    text = text.lower()
    red_flags = []
    
    govt_keywords = ["govt", "government", "income tax", "official", "department"]
    if any(word in text for word in govt_keywords):
        red_flags.append({"type": "AUTHORITY", "finding": "The sender is claiming to be an official Government entity."})

    urgency_keywords = ["urgent", "immediate", "last warning", "penalty", "expired"]
    if any(word in text for word in urgency_keywords):
        red_flags.append({"type": "URGENCY", "finding": "High-pressure language detected to force quick action."})

    financial_keywords = ["subscription", "fees", "payment", "bank", "fine", "transfer"]
    if any(word in text for word in financial_keywords):
        red_flags.append({"type": "FINANCIAL", "finding": "The email requests a financial transaction or subscription fee."})

    count = len(red_flags)
    if count == 0:
        return "SAFE", "Minimal indicators of phishing found.", "green", red_flags
    elif count == 1:
        return "ELEVATED", "One suspicious pattern detected. Exercise caution.", "orange", red_flags
    elif count == 2:
        return "HIGH", "Multiple phishing indicators found. Likely a scam.", "red", red_flags
    else:
        return "CRITICAL", "Extreme risk. Classic Government impersonation scam detected.", "black", red_flags

def optimized_investigation(url):
    ext = tldextract.extract(url)
    findings = []
    base_score = 100
    site_type = "General"
    
    if len(url) > 50:
        base_score -= 30
        findings.append("⚠️ URL is too long (Commonly used to hide real domain)")
    if url.startswith("http://"):
        base_score -= 20
        findings.append("⚠️ Uses HTTP instead of HTTPS (Insecure connection)")

    suspicious_tlds = ['xyz', 'top', 'live', 'tk', 'ml', 'cf']
    if ext.suffix in suspicious_tlds:
        base_score -= 25
        findings.append(f"⚠️ Uses a high-risk TLD (.{ext.suffix})")

    categories = {
        "Banking/Finance": ["bank", "pay", "secure", "login", "wallet", "crypto", "hdfc", "sbi"],
        "E-commerce": ["amazon", "flipkart", "shop", "offer", "discount", "sale","store"],
        "Social Media": ["facebook", "insta", "login", "verification", "meta","instagram"]
    }

    found_category = False
    for cat, keywords in categories.items():
        if any(key in url.lower() for key in keywords):
            site_type = cat
            found_category = True
            if ext.domain not in keywords and any(key in ext.domain for key in keywords):
                base_score -= 40
                findings.append(f"🚨 Brand Impersonation: Detected {cat} keywords on an unauthorized domain.")
            break

    final_score = max(0, base_score)
    return final_score, findings, site_type


# 5. --- ROUTING LOGIC (The Switch) ---

if current_page == "Home":
    st.markdown("<h1 class='main-header'>CheckPhish Detects and Monitors Phishing and Scam Sites</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-text'>With CheckPhish, you can scan suspicious URLs and monitor for typosquats and lookalikes variants of a domain.</p>", unsafe_allow_html=True)
    
    # --- NEW CENTERED SCAN BUTTON ADDED HERE ---
    st.markdown("""
        <div style="text-align: center; margin-bottom: 50px;">
            <a href="/?page=Scan" target="_self" style="background-color: #4a80f0; color: white; padding: 12px 30px; border-radius: 8px; text-decoration: none; font-weight: 400; font-size: 16px; transition: 0.3s;">
                Start Scanning
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.write("---")
        col_text, col_img = st.columns([1, 1], gap="large")
        with col_text:
            st.markdown("### 🌐 Free Domain Monitoring")
            st.write("""
            **Stay one step ahead of malicious actors with advanced domain monitoring!**
            
            PhishGuard scans the internet for typosquat variants of your domain. 
            We protect your brand for free against variants like:
            - **Letter replacement** (amazan.in)
            - **Homoglyphs** (g00gle.com)
            - **TLD Squatting** (paypal.tk)
            """)
            st.link_button("Monitor Now →", "https://yourprojectlink.com")

        with col_img:
            st.markdown("#### Live Typosquat Detection Log")
            data = {
                "Source URL": ["amazan.com", "g00gle.net", "paypql.in", "hdfcbink.com"],
                "Category": ["Replacement", "Homoglyph", "Typosquat", "Visual Lookalike"],
                "Risk": ["🔴 High", "🔴 High", "🟡 Medium", "🔴 High"]
            }
            st.table(data)

    with st.container():
        st.write("---")
        st.markdown("### 🛡️ Protection:")
        st.info("PhishGuard is a FREE tool designed to safeguard your web and email domains against typosquatting attacks. With its powerful features of domain monitoring, email link protection, and a phishing scanner, you get one place that delivers protection against typosquats, all for free!")

    with st.container():
        st.write("---") 
        col_main, col_blog, col_guides = st.columns([2, 1, 1], gap="large")
        with col_main:
            st.markdown("<h2 style='color: #1a2b4b;'>Ready to get started on PhishGuard?</h2>", unsafe_allow_html=True)
            st.write("Don't let typosquatting attacks compromise your online security. Get started today and take proactive steps towards protecting your domains across web and email.")
            st.button("Sign Up →", "https://yourprojectlink.com", use_container_width=False)
        with col_blog:
            st.markdown("### 📄") 
            st.markdown("**Read Our Blog**")
            st.write("Get the latest research and thought leadership about typosquatting, domain monitoring, and phishing protection.")
            st.markdown("[Learn More →](#)", unsafe_allow_html=True)
        with col_guides:
            st.markdown("### 📄") 
            st.markdown("**Easy Product Guides**")
            st.write("Self-guided documentation gives you step-by-step support to quick integrations or issue resolution.")
            st.markdown("[Go to Community →](#)", unsafe_allow_html=True)

elif current_page == "Scan":
    col1, col2, col3 = st.columns([2, 5, 2])
    with col1:
        st.markdown("### 🔍 PhishScan")

    tab1, tab2, tab3, tab4 = st.tabs(["📧 Email Scanner", "🌐 URL Scanner", "🎯 Typosquat Monitoring", "🛡️ Takedown"])

    with tab1:
        st.markdown("<br><h4 style='text-align: center;'>Email Threat Investigation</h4>", unsafe_allow_html=True)
        email_text = st.text_area("Investigation Subject", placeholder="Paste email content here...", height=200, label_visibility="collapsed")
        if st.button("Start AI Investigation"):
            if email_text:
                status, summary, color, flags = agentic_email_report(email_text)
                st.write("---")
                if status in ["HIGH", "CRITICAL"]:
                    st.error("🚨 ACTION REQUIRED: This email shows classic signs of a phishing attempt. Do not click any links or provide personal data.")
                else:
                    st.info("💡 ADVISORY: While no major threats were found, always verify the sender's actual email address manually.")

                st.subheader("🛡️ Recommended Safety Steps")
                recs = [
                    "Check the 'Reply-To' address to ensure it matches the official domain.",
                    "Never share OTPs or passwords over email.",
                    "If this is from a 'Govt Dept', visit their official website directly instead of using provided links."
                ]
                for rec in recs:
                    st.markdown(f"✅ {rec}")

                with st.expander("ℹ️ Technical Methodology"):
                    st.caption("**Analysis Technique:** Heuristic Social Engineering Detection \n**Engine:** Natural Language Processing (NLP) Lexicon Matching \n**Risk Model:** Weighted Threat Attribution")
                
                st.markdown(f"""
                    <div style="background-color:{color}; padding:20px; border-radius:10px; text-align:center;">
                        <h1 style="color:white; margin:0;">{status} RISK</h1>
                        <p style="color:white; margin:0; opacity:0.8;">{summary}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📋 Agentic Evidence Log")
                if flags:
                    for flag in flags:
                        with st.expander(f"🚩 {flag['type']} ALERT"):
                            st.write(flag['finding'])
                else:
                    st.success("The AI Investigator found no obvious social engineering patterns.")
            else:
                st.warning("Please provide email content for the investigation.")

    with tab2:
        st.markdown("<br><h4 style='text-align: center;'>Scan a suspicious URL</h4>", unsafe_allow_html=True)
        st.markdown("Enter URL to Scan")
        url_input = st.text_input("URL Input", placeholder="https://amazon-shop-sale.xyz", label_visibility="collapsed")
        
        if st.button("Scan URL"):
            if url_input:
                with st.spinner("Checking if site is live..."):
                    if not is_site_reachable(url_input):
                        st.error("🚫 Site is not live or unreachable. Analysis aborted.")
                        st.stop()
            else:
                st.markdown("Invalid input or empty ",unsafe_allow_html=True)
                st.stop()

            score, findings, category = optimized_investigation(url_input)
            
            st.write("---")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(label="Security Score", value=f"{score}%", delta=f"{score-100}%" if score < 100 else "Secure")
                st.write(f"**Detected Category:** {category}")
                st.write("---")
                st.header("Visit Website")
            
            with col2:
                if score > 70:
                    st.success("SECURE SITE")
                elif score > 40:
                    st.warning("MODERATE RISK")
                else:
                    st.error("DANGEROUS / PHISHING")
            
            final_url = url_input if url_input.startswith(('http://', 'https://')) else f"https://{url_input}"
            if score < 50:
                st.warning("⚠️ Warning: This site was flagged as high risk. Proceed with caution.")
            
            st.link_button(f"Go to {url_input} →", final_url)

            if findings:
                st.markdown("### Why this score?")
                for item in findings:
                    st.write(item)
            
            if score >= 80:
                status = "SAFE"
            elif score >= 50:
                status = "SUSPICIOUS 🟠"
            else:
                status = "SAFE ✅"
            
            if "scan_history" in st.session_state and st.session_state.scan_history:
                st.session_state.setdefault("scan_history",[])
            
            new_scan = {
                "Timestamp": datetime.now().strftime("%H:%M:%S"),
                "Type": "URL", 
                "Input": url_input, 
                "Risk Level": status, 
                "Score": f"{score}%"
            }
            scan_history = st.session_state.setdefault("scan_history", [])
            scan_history.insert(0, new_scan)
            st.session_state.scan_history = scan_history[:5]
            
    with st.container():
        st.write("---")
        st.markdown("### 🕒 Recent Scan Activity")
        if st.session_state.scan_history:
            df_history = pd.DataFrame(st.session_state.scan_history)
            st.table(df_history)
            if st.button("Clear History"):
                st.session_state.scan_history = []
                st.rerun()
        else:
            st.info("No recent scans found. Start scanning to see your history here!")

elif current_page == "Performance":
    display_performance_metrics()
    st.info("💡 Technical Note: These metrics are derived from a 70/30 train-test split.")

elif current_page == "Charts":
    display_metrics_chart()

elif current_page == "Logout":
    st.session_state.clear()
    st.query_params.clear()
    st.success("Logged out successfully. Please refresh the page.")

# 6. GLOBAL FOOTER (Shows only on Home and Scan)
if current_page in ["Home", "Scan"]:
    st.write("<br><br>", unsafe_allow_html=True)
    st.write("---") 
    f1, f2, f3, f4 = st.columns(4)

    with f1:
        st.markdown("**🔍 PhishGuard AI**")
        st.caption("Advanced AI detection for social engineering.")
    with f2:
        st.markdown("**Products**")
        st.caption("URL & Email Scanner")
        st.caption("Email Investigation")
    with f3:
        st.markdown("**Resources**")
        st.caption("API DOCS")
        st.caption("Security Blog")
    with f4:
        st.markdown("**Company**")
        st.caption("About Project")
        st.caption("About US")
        st.caption("Contact Support")

    st.markdown("""
        <div class="custom-footer">
            <div class="footer-links">
                <a href="#">Twitter</a>
                <a href="#">LinkedIn</a>
                <a href="#">GitHub</a>
            </div>
            <p style="margin-top: 20px;">© 2026 PhishGuard AI - Project. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)