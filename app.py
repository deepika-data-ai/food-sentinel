import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from transformers import pipeline
from groq import Groq

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Masala Boulevard",
    page_icon="🍛",
    layout="centered"
)

# ---------------------------------------------------------
# Navigation Sidebar (Mode Switch)
# ---------------------------------------------------------
st.sidebar.title("🍛 Masala Boulevard")
app_mode = st.sidebar.radio(
    "Select Mode:",
    ["Public Customer Assistant", "Private Business Admin"]
)

# Initialize Groq client
client = Groq()

# =========================================================
# MODE 1: PUBLIC CUSTOMER ASSISTANT
# =========================================================
if app_mode == "Public Customer Assistant":
    st.title("🍛 Masala Boulevard Assistant")
    st.caption("Authentic South Indian Catering — Greater Manchester")

    # FAQ Responses
    FAQ_RESPONSES = {
        "ordering_how": """
### 💐 How Ordering With Us Works

1. **Explore the Menu**: Check our latest menu postings and seasonal specials.
2. **Place Your Order**: Send us your item choices, quantities, and preferred pickup/delivery date.
3. **Confirmation**: We verify kitchen capacity and send confirmation with payment details.
4. **Fresh Preparation**: Your meal is cooked fresh following strict hygiene standards.
5. **Pickup / Delivery**: Collect your fresh order at the agreed time!
""",
        "menu_schedule": """
### 💐 Menu Schedule & Deadlines

* **Weekly Menu Updates**: Posted regularly on our official broadcast list/channels.
* **Weekend Orders**: Please place orders at least 24–48 hours in advance.
* **Large Catering / Parties**: Minimum 5–7 days advance notice required.
""",
        "party_guidelines": """
### 💐 Party Order Guidelines

* **Generous Portion Sizes**: Platters and catering trays catered for group gatherings.
* **Custom Spice Levels**: Mild, Medium, or Authentic South Indian spice levels available.
* **Fresh Delivery / Pickup**: Packaged safely in food-grade hot-holding containers.
""",
        "allergen_list": """
### ⚠️ Allergen Information & Safety

* **Common Kitchen Ingredients**: Mustard seeds, sesame, peanuts, cashew nuts, dairy (ghee/paneer), and wheat/gluten.
* **Gluten-Free Friendly**: Idli, Dosa batter, Sambhar, Rasam, and rice specialties.
* **Dietary Requests**: Please inform us of any severe allergies when placing your order.
""",
        "confirm_party": """
### 💐 Confirm Your Party Order

Please share the following details to confirm your catering booking:
1. **Full Name & Contact Number**:
2. **Event Date & Time**:
3. **Delivery or Pickup**:
4. **Guest Count & Menu Items**:
""",
        "know_about_us": """
### 💐 Know About Us

* **Established**: Business started in 2020
* **Council Registered**: Trafford Council registered
* **Hygiene Rating**: 5 Stars ⭐⭐⭐⭐⭐
* **Certifications**: Level 2 Food Hygiene course completed & Food Allergen and Safety completed
* **Insurance**: Liability insurance is available upon request
""",
        "pricing_policy": """
### 💐 Pricing Policy

* **Custom Quotes**: Prices are always based on the items chosen, prices of ingredients, and the complexity of the dish.
* **Menu Amendments**: Every time we amend the menu, we requote and send it to you.
* **Final Pricing**: We take time to do the pricing carefully. What we quote would be the final pricing—please kindly don't ask for discounts or round-offs 🙏.
""",
        "contact_info": """
### 💐 Contact Details

* **Name**: Deepika Prasana
* **Phone**: +447459943235
* **Email**: deepikaprasana@gmail.com
"""
    }

    # Preset Quick Action Buttons
    st.markdown("##### ⚡ Quick Enquiries")
    col1, col2 = st.columns(2)

    if "customer_messages" not in st.session_state:
        st.session_state.customer_messages = [
            {
                "role": "assistant",
                "content": "Hello! Welcome to **Masala Boulevard**. 🍛\n\nHow can we help you with your catering or order today? Select an option below or ask us a question!"
            }
        ]

    with col1:
        if st.button("💐 Know About Us"):
            st.session_state.customer_messages.append({"role": "user", "content": "Tell me about Masala Boulevard."})
            st.session_state.customer_messages.append({"role": "assistant", "content": FAQ_RESPONSES["know_about_us"]})
            st.rerun()

        if st.button("💐 How ordering works"):
            st.session_state.customer_messages.append({"role": "user", "content": "How does ordering work?"})
            st.session_state.customer_messages.append({"role": "assistant", "content": FAQ_RESPONSES["ordering_how"]})
            st.rerun()

        if st.button("💐 Menu schedule & deadlines"):
            st.session_state.customer_messages.append({"role": "user", "content": "What is your ordering deadline?"})
            st.session_state.customer_messages.append({"role": "assistant", "content": FAQ_RESPONSES["menu_schedule"]})
            st.rerun()

        if st.button("💐 Pricing Policy"):
            st.session_state.customer_messages.append({"role": "user", "content": "What is your pricing policy?"})
            st.session_state.customer_messages.append({"role": "assistant", "content": FAQ_RESPONSES["pricing_policy"]})
            st.rerun()

    with col2:
        if st.button("💐 Party order guidelines"):
            st.session_state.customer_messages.append({"role": "user", "content": "Tell me about party orders."})
            st.session_state.customer_messages.append({"role": "assistant", "content": FAQ_RESPONSES["party_guidelines"]})
            st.rerun()

        if st.button("⚠️ Allergen list"):
            st.session_state.customer_messages.append({"role": "user", "content": "Can I see allergen info?"})
            st.session_state.customer_messages.append({"role": "assistant", "content": FAQ_RESPONSES["allergen_list"]})
            st.rerun()

        if st.button("💐 Confirm party order"):
            st.session_state.customer_messages.append({"role": "user", "content": "How do I confirm my order?"})
            st.session_state.customer_messages.append({"role": "assistant", "content": FAQ_RESPONSES["confirm_party"]})
            st.rerun()

        if st.button("💐 Contact Details"):
            st.session_state.customer_messages.append({"role": "user", "content": "What are your contact details?"})
            st.session_state.customer_messages.append({"role": "assistant", "content": FAQ_RESPONSES["contact_info"]})
            st.rerun()

    st.divider()

    # Display Customer Chat History
    for msg in st.session_state.customer_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Free-text Customer Chat Input
    if user_prompt := st.chat_input("Ask a question about our menu, catering, or orders..."):
        st.session_state.customer_messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Responding..."):
                customer_system_prompt = f"""
                You are the friendly customer service assistant for 'Masala Boulevard' (run by Deepika Prasana), a home-based South Indian food catering business in Greater Manchester.
                
                User Inquiry: "{user_prompt}"

                Rules:
                - Focus ONLY on customer hospitality, menu items, ordering procedures, event catering, pricing policy, and our 5-star Trafford council registration credentials.
                - Never discuss internal business strategy, supplier profit margins, or cost analysis.
                - Be polite, warm, and professional.
                """

                completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": customer_system_prompt}],
                    model="openai/gpt-oss-20b",
                )
                response = completion.choices[0].message.content
                st.markdown(response)

        st.session_state.customer_messages.append({"role": "assistant", "content": response})

# =========================================================
# MODE 2: PRIVATE BUSINESS ADMIN (Owner Only)
# =========================================================
else:
    st.title("🔒 Owner Operations Portal")
    st.caption("Private strategy & cost advice for Masala Boulevard.")

    admin_password = st.text_input("Enter Admin PIN / Password:", type="password")

    if admin_password == "1234":
        st.success("Authenticated as Owner")

        @st.cache_resource
        def load_classifier():
            return pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-3")

        classifier = load_classifier()

        st.subheader("💡 Quick Cost & Operations Check")
        signal_input = st.text_area(
            "Paste ingredient price change, market news, or catering cost query:",
            placeholder="e.g., Sunflower oil is up 10% or cauliflower dropped to £1.19..."
        )

        if st.button("Analyze Impact 🚀", type="primary"):
            if signal_input:
                with st.spinner("Analyzing..."):
                    candidate_labels = ["Financial Cost Shift", "Customer Demand Shift", "Regulatory & Safety Warning"]
                    pred = classifier(signal_input, candidate_labels)
                    cat = pred['labels'][0]

                    admin_prompt = f"""
                    You are a practical, direct business advisor for 'Masala Boulevard', a home catering business in Greater Manchester.
                    The owner provided this note: "{signal_input}"
                    Detected Category: {cat}

                    Provide a short, easy-to-read response formatted in standard Markdown (DO NOT use HTML tags like <br> or markdown tables):
                    1. **Category**: Confirm the category.
                    2. **Impact**: 1 simple sentence on how this affects kitchen margins or orders.
                    3. **Practical Action Steps**: 2-3 short, clear bullet points on what to do next (e.g., substitute ingredient, adjust weekly tray pricing, bulk buy).

                    Keep it clear, simple, and directly relevant to a South Indian catering business.
                    """

                    completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": admin_prompt}],
                        model="openai/gpt-oss-20b",
                    )
                    
                    st.info(f"**Category:** {cat}")
                    st.markdown(completion.choices[0].message.content)
            else:
                st.warning("Please enter a note to analyze.")
    elif admin_password != "":
        st.error("Incorrect PIN.")