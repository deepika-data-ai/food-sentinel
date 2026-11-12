import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq Client safely
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Page configuration
st.set_page_config(
    page_title="Masala Boulevard",
    page_icon="🍛",
    layout="wide"
)

# --- Sidebar Navigation & Admin Authentication ---
with st.sidebar:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=160)
    st.markdown("### Navigation")
    
    mode = st.radio(
        "Select Mode:",
        ["Public Customer Assistant", "Private Business Administration"]
    )

# --- Private Business Administration Mode ---
if mode == "Private Business Administration":
    st.markdown("# 🔒 Private Business Administration")
    st.markdown("Internal tools, order management, and operational analytics for Masala Boulevard.")
    
    # Password protection check
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        password = st.text_input("Enter Admin Password:", type="password")
        if st.button("Login"):
            if password == "masala2020":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
    else:
        st.success("Admin dashboard is active.")
        st.markdown("---")
        
        # Admin Sub-Tabs for Operations & Cost Analysis (Defined AFTER login)
        admin_tab1, admin_tab2 = st.tabs(["📊 Ingredient Price & Cost Tracker", "📋 Active Activity Logs"])
        
        with admin_tab1:
            st.markdown("### 🧮 Catering Ingredient Price & Cost Analysis")
            st.markdown("Track and analyze wholesale or retail price fluctuations for key ingredients like cooking oil, vegetables, and spices.")
            
            # Initialize session state for ingredient logs if not present
            if "ingredient_logs" not in st.session_state:
                st.session_state.ingredient_logs = []

            # Interactive pricing inputs
            col_ing1, col_ing2 = st.columns(2)
            with col_ing1:
                item_name = st.selectbox("Select Ingredient:", ["Cooking Oil (Sunflower/Vegetable - 20L)", "Cauliflower (per crate)", "Basmati Rice (20kg)", "Chicken (per 5kg)", "Paneer (per kg)", "Spices & Condiments Bundle"])
                current_price = st.number_input("Current Purchase Price (£):", min_value=0.0, value=25.0, step=0.5)
            with col_ing2:
                quantity_needed = st.number_input("Quantity Needed per Batch/Week:", min_value=1.0, value=2.0, step=1.0)
                supplier_notes = st.text_input("Supplier / Notes:", value="Local cash & carry / Wholesaler")
            
            total_estimated_cost = current_price * quantity_needed
            st.info(f"**Estimated Cost Impact:** £{total_estimated_cost:.2f} for {quantity_needed} unit(s) of {item_name}.")
            
            if st.button("Save Ingredient Log"):
                new_log = {
                    "Ingredient": item_name,
                    "Price (£)": current_price,
                    "Qty": quantity_needed,
                    "Total (£)": total_estimated_cost,
                    "Notes": supplier_notes
                }
                st.session_state.ingredient_logs.append(new_log)
                st.success(f"Successfully recorded price for {item_name} at £{current_price:.2f}!")

            # Display saved logs in a table
            st.markdown("### 📋 Saved Ingredient Price History")
            if st.session_state.ingredient_logs:
                st.dataframe(st.session_state.ingredient_logs, use_container_width=True)
                
                if st.button("Clear Logs"):
                    st.session_state.ingredient_logs = []
                    st.rerun()
            else:
                st.info("No ingredient logs saved yet. Add an item above and click save!")

        with admin_tab2:
            st.markdown("### 📈 Customer Engagement Logs")
            st.info("No active customer support tickets or critical error logs found.")

        st.markdown("---")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

# --- Public Customer Assistant Mode ---
else:
    st.markdown("# 🍛 Masala Boulevard Assistant")
    st.markdown("Authentic South Indian Home Catering — Greater Manchester (Est. 2020)")

    # --- 1. Quick Enquiries & Policies (Collapsible) ---
    with st.expander("📌 Quick Enquiries & Policies (Tap to expand)", expanded=False):
        st.markdown("""
        - **Minimum Notice:** At least 48–72 hours preferred for standard catering orders.
        - **Delivery / Collection:** Collection available in Sale, Greater Manchester (M33). Local delivery options can be discussed.
        - **Custom Orders:** Vegetarian, Non-Vegetarian, and Jain-friendly adjustments available upon request.
        """)

    # --- 2. Full Catering Menu (Collapsible Expander + Clean Tabs) ---
    with st.expander("🍛 View Full Catering Menu (Tap to expand)", expanded=False):
        tab_veg, tab_nonveg, tab_dessert = st.tabs(["🌿 Vegetarian", "🍗 Non-Vegetarian", "🍮 Desserts"])

        with tab_veg:
            v_col1, v_col2, v_col3 = st.columns(3)
            with v_col1:
                st.markdown("**🥟 Starters**")
                st.markdown("""
                - Aloo Samosa
                - Onion Samosa
                - Dal Kachori
                - Onion Kachori
                - Vegetable Cutlet
                - Soya Cutlet
                - Medu Vada
                - Masala Vada
                - Sambhar Vada
                - Curd Vada
                - Gobi 65
                - Gobi Manchurian
                - Veg Manchurian
                - Soya Pepper Fry
                - Aloo Bonda
                """)
            with v_col2:
                st.markdown("**🍲 Mains & Curries**")
                st.markdown("""
                - Sambhar
                - Vegetable Kurma
                - Pakoda Kurma
                - Morkulambu *(South Indian Kadhi)*
                - Cauliflower Walnut Kurma
                - Dal Makhani
                - Kadai Paneer
                - Paneer Butter Masala
                - Matar Paneer
                - Kadai Mushroom
                - Channa Masala
                - Dal
                """)
            with v_col3:
                st.markdown("**🍚 Rice, Tiffins & Sides**")
                st.markdown("""
                - Jeera Rice
                - Veg Pulav
                - Veg Biryani
                - Veg Tahiri
                - Veg Kothu Parotta
                - Veg Fried Rice
                - Veg Noodles
                - Veg Salna
                """)

        with tab_nonveg:
            nv_col1, nv_col2, nv_col3 = st.columns(3)
            with nv_col1:
                st.markdown("**🍢 Starters**")
                st.markdown("""
                - Chicken 65
                - Chicken Cutlet
                - Pepper Chicken
                - Chicken Chukka
                - Andhra Masala Chicken
                - Andhra Chilli Chicken *(Boneless Fried)*
                - Majestic Chicken *(Boneless Fried)*
                - Chicken Manchurian
                - Guntur Mirchi Chicken Fry
                - Lamb Chukka
                """)
            with nv_col2:
                st.markdown("**🍛 Mains & Curries**")
                st.markdown("""
                - Chicken Curry
                - Chicken Changezi
                - Butter Chicken
                - Varutharcha Chicken Curry
                - Lamb Curry
                - Lamb Paya
                - Chicken Salna
                """)
            with nv_col3:
                st.markdown("**🥘 Biryani, Rice & Noodles**")
                st.markdown("""
                - Chicken Biryani *(Chennai Style)*
                - Lamb Biryani *(Chennai Style)*
                - Chicken Pulao
                - Andhra Chicken Pulao
                - Egg / Chicken Fried Rice
                - Egg / Chicken Noodles
                - Egg / Chicken Kothu Parotta
                """)

        with tab_dessert:
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                st.markdown("**🍯 Traditional Sweets & Halwa**")
                st.markdown("""
                - Gulab Jamun
                - Carrot Halwa
                - Bread Halwa
                - Shahi Tukra Rabri
                """)
            with d_col2:
                st.markdown("**🥣 Kheer Varieties**")
                st.markdown("""
                - Badam Kheer
                - Carrot Kheer
                - Poha / Semiya / Rice / Sabudana Kheer
                """)

    st.markdown("---")
    st.markdown("### 💬 Chat with Masala Boulevard Assistant")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! Welcome to Masala Boulevard. How can we help you with your catering or order today?"}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask a question about our menu, catering, or orders..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if client:
                try:
                    active_models = [m.id for m in client.models.list().data]
                    blocked_keywords = ("whisper", "guard", "canopylabs", "orpheus", "tts", "playai")
                    chat_models = [
                        m for m in active_models
                        if not any(word in m.lower() for word in blocked_keywords)
                    ]
                    selected_model = chat_models[0] if chat_models else "llama-3.1-8b-instant"

                    chat_completion = client.chat.completions.create(
                        model=selected_model,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant for Masala Boulevard, an authentic South Indian home catering business in Greater Manchester established in 2020. Provide warm, polite, and accurate info about the menu, catering, and orders."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    response = chat_completion.choices[0].message.content
                except Exception as e:
                    response = f"I'm here to help with your Masala Boulevard inquiry! (API note: {e})"
            else:
                response = "Hello! Thank you for your interest in Masala Boulevard catering. Please check our menu tabs above or reach out for custom orders!"
            
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})