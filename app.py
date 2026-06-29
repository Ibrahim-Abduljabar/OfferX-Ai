import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("API_kkk")

st.set_page_config(page_title="OfferX AI 💼", layout="centered")
st.title("💼 OfferX AI")
st.write("منصة لإنشاء أكثر من عرض وظيفي للـ HR باستخدام الذكاء الاصطناعي.")

if not GROQ_API_KEY:
    st.error("🚨 لم يتم العثور على المفتاح API_kkk في Secrets.")
    st.stop()


def generate_offer(data):
    prompt = f"""
اكتب عرض وظيفي رسمي واحترافي للموظف التالي:

الاسم: {data['name']}
المسمى الوظيفي: {data['title']}
الراتب: {data['salary']}
تاريخ البدء: {data['start_date']}
المزايا: {data['benefits']}
الشروط: {data['conditions']}

خله منسّق، رسمي، قابل للإرسال كـ Offer Letter.
    """

    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    data_json = resp.json()

    if "choices" not in data_json:
        return f"❌ خطأ في الاتصال بالـ API:\n{data_json}"

    return data_json["choices"][0]["message"]["content"]


if "offers" not in st.session_state:
    st.session_state.offers = []

with st.form("offer_form", clear_on_submit=True):
    st.subheader("✨ إنشاء عرض وظيفي جديد")

    name = st.text_input("اسم الموظف")
    title = st.text_input("المسمى الوظيفي")
    salary = st.text_input("الراتب")
    start_date = st.text_input("تاريخ البدء")
    benefits = st.text_area("المزايا")
    conditions = st.text_area("الشروط")

    submitted = st.form_submit_button("إنشاء العرض")

    if submitted:
        if not all([name, title, salary, start_date]):
            st.warning("⚠️ عبّ البيانات الأساسية أول.")
        else:
            data = {
                "name": name,
                "title": title,
                "salary": salary,
                "start_date": start_date,
                "benefits": benefits,
                "conditions": conditions
            }

            with st.spinner("⏳ جاري إنشاء العرض..."):
                offer_text = generate_offer(data)

            st.session_state.offers.append(
                {"data": data, "text": offer_text}
            )

            st.success("✅ تم إنشاء العرض وإضافته للقائمة.")


st.divider()
st.subheader("📂 كل العروض الوظيفية")

if not st.session_state.offers:
    st.info("لسه ما فيه عروض. أنشئ أول عرض من فوق.")
else:
    for i, offer in enumerate(st.session_state.offers, 1):
        with st.expander(f"Offer #{i} - {offer['data']['name']} / {offer['data']['title']}"):
            st.markdown("### 📌 البيانات الأساسية")
            st.write(f"- الاسم: {offer['data']['name']}")
            st.write(f"- المسمى الوظيفي: {offer['data']['title']}")
            st.write(f"- الراتب: {offer['data']['salary']}")
            st.write(f"- تاريخ البدء: {offer['data']['start_date']}")
            st.write(f"- المزايا: {offer['data']['benefits']}")
            st.write(f"- الشروط: {offer['data']['conditions']}")

            st.markdown("---")
            st.markdown("### 📝 نص العرض الوظيفي")
            st.write(offer["text"])
