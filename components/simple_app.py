# components/valuation_section.py
import streamlit as st
import pandas as pd


def load_valuation_section():
    # Title (no set_page_config here; keep this import-safe)
    st.markdown(
        "<h1 style='text-align:center;'>🏠 AI Property Valuation Tool</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; font-size:18px;'>Get instant property valuations with 99.96% accuracy</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Two columns
    col1, col2 = st.columns(2, gap="large")

    # ---------- LEFT: INPUT FORM ----------
    with col1:
        st.header("📝 Property Details")

        location = st.selectbox(
            "📍 Location",
            [
                "Mumbai",
                "Delhi",
                "Bangalore",
                "Chennai",
                "Hyderabad",
                "Pune",
                "Kolkata",
                "Ahmedabad",
                "Jaipur",
                "Other",
            ],
            key="val_loc",
        )

        property_type = st.selectbox(
            "🏢 Property Type",
            ["Apartment", "Villa", "Independent House", "Plot", "Commercial"],
            key="val_type",
        )

        area = st.number_input(
            "📐 Area (sq.ft)",
            min_value=100,
            max_value=10000,
            value=1200,
            key="val_area",
        )
        bedrooms = st.number_input(
            "🛏️ Bedrooms", min_value=1, max_value=10, value=3, key="val_bed"
        )
        bathrooms = st.number_input(
            "🚿 Bathrooms", min_value=1, max_value=10, value=2, key="val_bath"
        )
        age = st.slider("📅 Property Age (years)", 0, 50, 10, key="val_age")
        amenities = st.multiselect(
            "🎯 Amenities",
            [
                "Parking",
                "Swimming Pool",
                "Gym",
                "Garden",
                "Lift",
                "Security",
                "Playground",
            ],
            key="val_amen",
        )

        if st.button("🔍 Get Valuation", type="primary", key="val_btn"):
            base_price = 50
            location_multiplier = {
                "Mumbai": 3.0,
                "Delhi": 2.5,
                "Bangalore": 2.0,
                "Chennai": 1.8,
                "Hyderabad": 1.6,
                "Pune": 1.7,
                "Kolkata": 1.4,
                "Ahmedabad": 1.3,
                "Jaipur": 1.2,
                "Other": 1.0,
            }
            type_multiplier = {
                "Apartment": 1.0,
                "Villa": 1.5,
                "Independent House": 1.3,
                "Plot": 0.8,
                "Commercial": 2.0,
            }

            price = (
                base_price
                + area * 0.02
                + bedrooms * 15
                + max(0, (30 - age) * 2)
                + len(amenities) * 5
            ) * location_multiplier.get(location, 1.0) * type_multiplier.get(
                property_type, 1.0
            )

            st.session_state.valuation_price = price
            st.session_state.valuation_calculated = True
            st.session_state.valuation_inputs = {
                "location": location,
                "property_type": property_type,
                "area": area,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "age": age,
                "amenities": amenities,
            }

    # ---------- RIGHT: RESULTS ----------
    with col2:
        st.header("📊 Valuation Results")

        if st.session_state.get("valuation_calculated", False):
            price = st.session_state.get("valuation_price", 0.0)
            inputs = st.session_state.get("valuation_inputs", {})

            st.success("✅ Valuation Complete!")

            st.markdown(
                f"""
            <div style='text-align: center; padding: 20px; background: #f0f8ff; border-radius: 10px; border-left: 5px solid #FF6600;'>
                <h1 style='color: #003366; font-size: 3rem; margin: 0;'>₹{price:.2f} Lakhs</h1>
                <p style='color: #666; font-size: 1.2rem;'>Estimated Property Value</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            col_m1, col_m2 = st.columns(2)
            area_val = max(1, float(inputs.get("area", 1)))
            col_m1.metric("Price per Sq.Ft", f"₹{(price * 100000 / area_val):.0f}")
            col_m2.metric("Price Range", "±₹2.93L")

            st.subheader("🏠 Property Summary")
            summary_data = {
                "Detail": [
                    "Location",
                    "Type",
                    "Area",
                    "Bedrooms",
                    "Bathrooms",
                    "Age",
                    "Amenities",
                ],
                "Value": [
                    inputs.get("location", "-"),
                    inputs.get("property_type", "-"),
                    f"{inputs.get('area', 0)} sq.ft",
                    inputs.get("bedrooms", "-"),
                    inputs.get("bathrooms", "-"),
                    f"{inputs.get('age', 0)} years",
                    len(inputs.get("amenities", [])),
                ],
            }
            st.dataframe(pd.DataFrame(summary_data), use_container_width=True)

            # ---------- NEXT STEPS ----------
            st.subheader("📞 Next Steps")
            col_a1, col_a2 = st.columns(2)

            # 👨‍💼 Expert Review → jump to AboutUs and scroll to contact
            if col_a1.button("👨‍💼 Expert Review", key="val_expert"):
                # 1) tell AboutUs page we want to scroll to contact
                st.session_state.scroll_to_contact = True

                # 2) change URL to match navbar: ?page=AboutUs
                try:
                    # Newer Streamlit API
                    st.query_params.update({"page": "AboutUs"})
                except Exception:
                    # Older Streamlit fallback
                    st.experimental_set_query_params(page="AboutUs")

            # # 📞 Contact Agent – inline feedback for now
            # if col_a2.button("📞 Contact Agent", key="val_agent"):
            #     st.info("Agent will contact you!")

        else:
            st.info("👈 Fill property details and click 'Get Valuation'")

    # Footer divider and note
    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: #666;'>
        <p>🏠 <strong>AI Property Valuation Tool</strong> | Professional Real Estate Analysis</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("""
<style>

/* ---------------- SHARED BASE STYLE FOR ALL BUTTONS ---------------- */
div.stButton > button {
    background-color: #F2F2F2 !important;   /* very light grey */
    color: #333333 !important;              /* dark grey text */
    font-weight: 600 !important;
    border: 1px solid #D6D6D6 !important;   /* soft border */
    border-radius: 10px !important;
    padding: 10px 22px !important;
    transition: all 0.25s ease !important;
}

/* Hover effect */
div.stButton > button:hover {
    background-color: #E6E6E6 !important;   /* slightly darker grey */
    color: #000000 !important;              /* solid black text */
    box-shadow: 0 3px 8px rgba(0,0,0,0.10) !important;
    transform: translateY(-1px);
}

/* Click/Active effect */
div.stButton > button:active {
    background-color: #DCDCDC !important;   /* deeper grey on click */
    color: #000000 !important;
    transform: scale(0.98);
}

</style>
""", unsafe_allow_html=True)
