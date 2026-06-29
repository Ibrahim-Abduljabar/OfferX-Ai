import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# مفتاحك أنت
GROQ_API_KEY = os.getenv("API_kkk")

st.set_page_config(page_title="OfferX AI: مساعدك في كتابة عروض العمل 💼", layout="centered")
st.title("OfferX AI")
st.write("أدخل بيانات الموظف لإنشاء عرض وظيفي احترافي.")

if not GROQ_API_KEY:
    st.error("🚨 لم يتم العثور على مفتاح API_kkk في البيئة.")
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

اجعل العرض منسقًا، رسميًا، وقابلًا للإرسال كـ Offer Letter.
    """

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "llama-3.3-70b-versatile",  # الموديل الجديد المدعوم
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ خطأ في الاتصال بـ API: {e}"


# حفظ العروض
if "offers" not in st.session_state:
    st.session_state.offers = []

st.subheader("إنشاء عرض وظيفي جديد")

with st.form("offer_form", clear_on_submit=True):
    name = st.text_input("اسم الموظف")
    title = st.text_input("المسمى الوظيفي")
    salary = st.text_input("الراتب")
    start_date = st.text_input("تاريخ البدء")
    benefits = st.text_area("المزايا")
    conditions = st.text_area("الشروط")

    submitted = st.form_submit_button("✨ أنشئ العرض")

    if submitted:
        if not all([name, title, salary, start_date]):
            st.warning("⚠️ يرجى تعبئة البيانات الأساسية.")
        else:
            data = {
                "name": name,
                "title": title,
                "salary": salary,
                "start_date": start_date,
                "benefits": benefits,
                "conditions": conditions
            }

            with st.spinner("جاري إنشاء العرض..."):
                offer_text = generate_offer(data)

            st.session_state.offers.append({"data": data, "text": offer_text})
            st.success("✅ تم إنشاء العرض وإضافته للقائمة.")


st.divider()
st.subheader("📂 كل العروض الوظيفية")

if not st.session_state.offers:
    st.info("لا توجد عروض بعد. أنشئ أول عرض من النموذج أعلاه.")
else:
    for i, offer in enumerate(st.session_state.offers, 1):
        with st.expander(f"Offer #{i} - {offer['data']['name']} / {offer['data']['title']}"):
            st.markdown("### البيانات الأساسية")
            st.write(f"- الاسم: {offer['data']['name']}")
            st.write(f"- المسمى الوظيفي: {offer['data']['title']}")
            st.write(f"- الراتب: {offer['data']['salary']}")
            st.write(f"- تاريخ البدء: {offer['data']['start_date']}")
            st.write(f"- المزايا: {offer['data']['benefits']}")
            st.write(f"- الشروط: {offer['data']['conditions']}")

            st.markdown("---")
            st.markdown("### نص العرض الوظيفي")
            st.write(offer["text"])
