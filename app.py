import streamlit as st

# Toggle this to True to use real Claude API (make sure your API key is set in secrets)
USE_CLAUDE = False

# Custom CSS for card style
st.markdown(
    """
    <style>
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📄 Resume & Job Description Matcher")

# Input columns
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Resume")
    resume_text = st.text_area("Paste your resume here:", height=300)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Job Description")
    job_text = st.text_area("Paste the job description here:", height=300)
    st.markdown("</div>", unsafe_allow_html=True)

# Analyze button
if st.button("Analyze"):
    with st.spinner("Analyzing..."):
        if USE_CLAUDE:
            import anthropic

            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0.5,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Compare this resume:
{resume_text}

with this job:
{job_text}

Give feedback and match score.""",
                    }
                ],
            )
            feedback = response.content[0].text
        else:
            feedback = (
                "🤖 [MOCK] Your resume aligns moderately well with the job. "
                "Consider highlighting project outcomes and key skills."
            )

        st.subheader("📋 Feedback")
        st.write(feedback)

st.caption("⚠️ This tool does not store your data. Use responsibly.")
