from components.chatbot_ui import chatbot_popup
import streamlit as st
import pandas as pd
from datetime import datetime


def render_emi_calculator():
    # ---------- Inject Footer CSS (same style as About Us & Case Studies) ----------
    st.markdown("""
        <style>
            .footer {
                text-align: center;
                color: #004D00;
                background-color: #EDE9D5;
                padding: 1.5rem 0;
                margin-top: 3rem;
                border-top: 2px solid #E2725B;
                font-family: 'Segoe UI', sans-serif;
            }
            .footer a {
                color: #E2725B;
                text-decoration: none;
                font-weight: 600;
            }
            .footer a:hover {
                text-decoration: underline;
            }
        </style>
    """, unsafe_allow_html=True)

    # ---------- Header ----------
    st.title("🏦 EMI Calculator")
    st.caption("Plan your home loan with a clear breakdown of EMI, interest, and total cost.")

    # ---------- Inputs ----------
    st.markdown("### Enter Loan Details")

    col1, col2 = st.columns(2)
    with col1:
        loan_amount_lakhs = st.number_input(
            "Loan Amount (₹ in Lakhs)",
            min_value=1.0,
            max_value=1000.0,
            value=50.0,
            step=1.0,
            key="emi_loan_amount",
        )
        interest_rate_annual = st.number_input(
            "Annual Interest Rate (%)",
            min_value=1.0,
            max_value=20.0,
            value=8.5,
            step=0.1,
            key="emi_interest_rate",
        )
    with col2:
        tenure_years = st.number_input(
            "Loan Tenure (Years)",
            min_value=1,
            max_value=40,
            value=20,
            step=1,
            key="emi_tenure_years",
        )
        frequency = st.selectbox(
            "Payment Frequency",
            options=["Monthly", "Quarterly", "Yearly"],
            index=0,
            key="emi_frequency",
        )

    col3, col4 = st.columns(2)
    with col3:
        down_payment_lakhs = st.number_input(
            "Down Payment (₹ in Lakhs)",
            min_value=0.0,
            max_value=500.0,
            value=10.0,
            step=1.0,
            key="emi_down_payment",
        )
    with col4:
        processing_fee_percent = st.number_input(
            "Processing Fee (%)",
            min_value=0.0,
            max_value=5.0,
            value=1.0,
            step=0.1,
            key="emi_processing_fee",
        )

    # ---------- Calculate EMI ----------
    if st.button("💰 Calculate EMI", use_container_width=True):
        principal = (loan_amount_lakhs - down_payment_lakhs) * 100000

        if principal <= 0:
            st.error("Down payment cannot be greater than or equal to the loan amount.")
            return

        rate_per_period = interest_rate_annual / 100.0

        if frequency == "Monthly":
            rate_per_period /= 12.0
            num_payments = tenure_years * 12
        elif frequency == "Quarterly":
            rate_per_period /= 4.0
            num_payments = tenure_years * 4
        else:
            num_payments = tenure_years

        # EMI formula
        if rate_per_period == 0:
            emi = principal / num_payments
        else:
            emi = (
                principal
                * rate_per_period
                * (1 + rate_per_period) ** num_payments
                / ((1 + rate_per_period) ** num_payments - 1)
            )

        total_payment = emi * num_payments
        total_interest = total_payment - principal
        processing_fee_amount = principal * (processing_fee_percent / 100.0)
        total_cost = total_payment + processing_fee_amount

        # ---------- Summary Section ----------
        st.markdown("### EMI Summary")

        st.markdown(
            f"""
            <div style="
                padding: 1.5rem;
                border-radius: 1rem;
                background: linear-gradient(135deg, #2563EB, #1D4ED8);
                color: white;
                text-align: center;
                margin-bottom: 1.5rem;
            ">
                <div style="text-transform: uppercase; font-size: 0.85rem; opacity: 0.9;">
                    {frequency} EMI
                </div>
                <div style="font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0;">
                    ₹{emi:,.2f}
                </div>
                <div style="font-size: 0.9rem; opacity: 0.85;">
                    Calculated on: {datetime.now().strftime("%Y-%m-%d %H:%M IST")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Payment", f"₹{total_payment:,.0f}")
        with c2:
            st.metric("Total Interest Paid", f"₹{total_interest:,.0f}")
        with c3:
            st.metric("Total Cost (Incl. Fee)", f"₹{total_cost:,.0f}")

        # ---------- Amortization Schedule ----------
        st.markdown("### 📊 Amortization Schedule (First 12 Periods)")

        schedule_rows = []
        balance = principal

        for period in range(1, int(num_payments) + 1):
            interest_payment = balance * rate_per_period
            principal_payment = emi - interest_payment
            balance = max(0, balance - principal_payment)

            schedule_rows.append(
                {
                    "Period": period,
                    "Payment": round(emi, 2),
                    "Principal Component": round(principal_payment, 2),
                    "Interest Component": round(interest_payment, 2),
                    "Remaining Balance": round(balance, 2),
                }
            )

        df_schedule = pd.DataFrame(schedule_rows)

        st.dataframe(df_schedule.head(12), use_container_width=True)

        csv_data = df_schedule.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Schedule as CSV",
            data=csv_data,
            file_name=f"emi_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

        chatbot_popup()

        # ---------- FOOTER ----------
        st.markdown("---")
        st.markdown("""
            <div class='footer'>
                © 2025 <b>StreetBase</b> | All Rights Reserved <br>
                Built with ❤️ using <a href='https://streamlit.io/' target='_blank'>Streamlit</a> and AI
            </div>
        """, unsafe_allow_html=True)
