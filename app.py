import sqlite3
from datetime import date
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Talha Tracker - Emaan | Health | Wealth",
    page_icon="🧭",
    layout="centered",
)

# -------------------------------------------------------------
# DATABASE SETUP (Local SQLite for easy testing; persists data)
# -------------------------------------------------------------
conn = sqlite3.connect("talha_tracker.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS daily_records (
        date TEXT PRIMARY KEY,
        fajr INTEGER, dhuhr INTEGER, asr INTEGER, maghrib INTEGER, isha INTEGER,
        morning_adhkar INTEGER, evening_adhkar INTEGER, quran_pages INTEGER, reflection TEXT,
        custom_emaan_3 TEXT, custom_emaan_4 TEXT,
        gym_done INTEGER, is_sunday_rest INTEGER,
        creatine INTEGER, egg INTEGER, shake INTEGER,
        water_3l INTEGER, body_weight REAL, sleep_hours REAL,
        agency_mode TEXT,
        outreach_done INTEGER, zero_spend INTEGER, client_delivered INTEGER, learning_done INTEGER,
        revenue REAL, expense REAL, expense_category TEXT, agency_focus TEXT
    )
"""
)
conn.commit()


def load_day_data(selected_date_str):
    cursor.execute(
        "SELECT * FROM daily_records WHERE date = ?", (selected_date_str,)
    )
    return cursor.fetchone()


def save_day_data(data_tuple):
    cursor.execute(
        """
        INSERT INTO daily_records VALUES (
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )
        ON CONFLICT(date) DO UPDATE SET
            fajr=excluded.fajr, dhuhr=excluded.dhuhr, asr=excluded.asr, maghrib=excluded.maghrib, isha=excluded.isha,
            morning_adhkar=excluded.morning_adhkar, evening_adhkar=excluded.evening_adhkar,
            quran_pages=excluded.quran_pages, reflection=excluded.reflection,
            custom_emaan_3=excluded.custom_emaan_3, custom_emaan_4=excluded.custom_emaan_4,
            gym_done=excluded.gym_done, is_sunday_rest=excluded.is_sunday_rest,
            creatine=excluded.creatine, egg=excluded.egg, shake=excluded.shake,
            water_3l=excluded.water_3l, body_weight=excluded.body_weight, sleep_hours=excluded.sleep_hours,
            agency_mode=excluded.agency_mode,
            outreach_done=excluded.outreach_done, zero_spend=excluded.zero_spend,
            client_delivered=excluded.client_delivered, learning_done=excluded.learning_done,
            revenue=excluded.revenue, expense=excluded.expense,
            expense_category=excluded.expense_category, agency_focus=excluded.agency_focus
    """,
        data_tuple,
    )
    conn.commit()


# -------------------------------------------------------------
# APP HEADER & MAIN NAVIGATION
# -------------------------------------------------------------
st.title("Talha's Daily System")
tab_emaan, tab_health, tab_wealth, tab_records = st.tabs(
    ["🕌 Emaan", "💪 Health", "💼 Wealth", "📊 View Records"]
)

# =============================================================
# TAB 1: EMAAN
# =============================================================
with tab_emaan:
    st.subheader("Emaan Tracker")
    emaan_date = st.date_input("Select Date for Emaan", value=date.today(), key="emaan_date")
    record = load_day_data(str(emaan_date))

    st.markdown("### 1. Salah")
    col1, col2, col3, col4, col5 = st.columns(5)
    fajr = col1.checkbox("Fajr", value=bool(record[1]) if record else False)
    dhuhr = col2.checkbox("Zohr", value=bool(record[2]) if record else False)
    asr = col3.checkbox("Asr", value=bool(record[3]) if record else False)
    maghrib = col4.checkbox(
        "Magrib", value=bool(record[4]) if record else False
    )
    isha = col5.checkbox("Isha", value=bool(record[5]) if record else False)

    st.markdown("### 2. Adhkar & Quran")
    c_adhkar1, c_adhkar2 = st.columns(2)
    morning_adhkar = c_adhkar1.checkbox(
        "Morning Adhkar", value=bool(record[6]) if record else False
    )
    evening_adhkar = c_adhkar2.checkbox(
        "Evening Adhkar", value=bool(record[7]) if record else False
    )

    quran_pages = st.checkbox(
        "5 Pages of Quran Daily (+2 pages monthly target)",
        value=bool(record[8]) if record else False,
    )
    reflection = st.text_input(
        "Short Daily Reflection (1-line):",
        value=record[9] if record and record[9] else "",
        placeholder="One key takeaway or mindset note for today...",
    )

    st.markdown("### 3 & 4. Custom Slot (For later)")
    custom_emaan_3 = st.text_input(
        "Option 3 (Placeholder / Custom Note):",
        value=record[10] if record and record[10] else "",
    )
    custom_emaan_4 = st.text_input(
        "Option 4 (Placeholder / Custom Note):",
        value=record[11] if record and record[11] else "",
    )

    if st.button("Save Emaan Entry", type="primary", use_container_width=True):
        # Fetch current record state to avoid overwriting other tabs
        current = load_day_data(str(emaan_date)) or [str(emaan_date)] + [0] * 27
        updated = list(current)
        updated[0] = str(emaan_date)
        updated[1], updated[2], updated[3], updated[4], updated[5] = (
            int(fajr),
            int(dhuhr),
            int(asr),
            int(maghrib),
            int(isha),
        )
        updated[6], updated[7], updated[8], updated[9] = (
            int(morning_adhkar),
            int(evening_adhkar),
            int(quran_pages),
            reflection,
        )
        updated[10], updated[11] = custom_emaan_3, custom_emaan_4
        save_day_data(tuple(updated))
        st.success(f"Emaan log saved for {emaan_date}!")

# =============================================================
# TAB 2: HEALTH
# =============================================================
with tab_health:
    st.subheader("Health Tracker")
    health_date = st.date_input(
        "Select Date for Health", value=date.today(), key="health_date"
    )
    record = load_day_data(str(health_date))

    st.markdown("### 1. Gym / Training")
    is_sunday = health_date.weekday() == 6
    col_gym1, col_gym2 = st.columns(2)
    gym_done = col_gym1.checkbox(
        "Gym Daily Session",
        value=bool(record[12]) if record else False,
        disabled=is_sunday,
    )
    sunday_rest = col_gym2.checkbox(
        "Sunday Rest Day", value=True if is_sunday else (bool(record[13]) if record else False)
    )

    st.markdown("### 2. Daily Diet & Fuel")
    col_d1, col_d2, col_d3 = st.columns(3)
    creatine = col_d1.checkbox(
        "Creatine", value=bool(record[14]) if record else False
    )
    egg = col_d2.checkbox("Egg", value=bool(record[15]) if record else False)
    shake = col_d3.checkbox(
        "SHAKE", value=bool(record[16]) if record else False
    )

    water_3l = st.checkbox(
        "3+ Liters Water Target Reached",
        value=bool(record[17]) if record else False,
    )

    st.markdown("### 3. Metrics")
    col_m1, col_m2 = st.columns(2)
    body_weight = col_m1.number_input(
        "Weekly Body Weight (kg):",
        min_value=40.0,
        max_value=120.0,
        value=float(record[18]) if (record and record[18]) else 63.0,
        step=0.1,
    )
    sleep_hours = col_m2.slider(
        "Sleep (Hours):",
        min_value=4.0,
        max_value=12.0,
        value=float(record[19]) if (record and record[19]) else 7.5,
        step=0.5,
    )

    if st.button("Save Health Entry", type="primary", use_container_width=True):
        current = load_day_data(str(health_date)) or [str(health_date)] + [0] * 27
        updated = list(current)
        updated[0] = str(health_date)
        updated[12], updated[13] = int(gym_done), int(sunday_rest)
        updated[14], updated[15], updated[16], updated[17] = (
            int(creatine),
            int(egg),
            int(shake),
            int(water_3l),
        )
        updated[18], updated[19] = float(body_weight), float(sleep_hours)
        save_day_data(tuple(updated))
        st.success(f"Health log saved for {health_date}!")

# =============================================================
# TAB 3: WEALTH
# =============================================================
with tab_wealth:
    st.subheader("Wealth & Business Tracker")
    wealth_date = st.date_input(
        "Select Date for Wealth", value=date.today(), key="wealth_date"
    )
    record = load_day_data(str(wealth_date))

    st.markdown("### Agency Status Mode")
    current_mode = record[20] if (record and record[20]) else "Active Outreach Mode"
    agency_mode = st.radio(
        "Choose what you are currently focusing on:",
        options=[
            "Active Outreach Mode (Hunting Clients)",
            "Client Execution Mode (Working with active clients)",
            "Hybrid (Both)",
        ],
        index=0
        if "Outreach" in current_mode
        else (1 if "Execution" in current_mode else 2),
    )

    st.markdown("### Checkboxes")
    outreach_done = False
    client_delivered = False

    # Dynamic conditions based on agency status
    if "Outreach" in agency_mode or "Hybrid" in agency_mode:
        outreach_done = st.checkbox(
            "Agency Outreach Completed",
            value=bool(record[21]) if record else False,
        )

    if "Execution" in agency_mode or "Hybrid" in agency_mode:
        client_delivered = st.checkbox(
            "Client Work / Project Milestone Delivered",
            value=bool(record[23]) if record else False,
        )

    zero_spend = st.checkbox(
        "Zero Unnecessary Spending Day",
        value=bool(record[22]) if record else False,
    )
    learning_done = st.checkbox(
        "Learning / Skill Session Done",
        value=bool(record[24]) if record else False,
    )

    st.markdown("### Inputs & Cash Flow")
    col_rev, col_exp = st.columns(2)
    revenue = col_rev.number_input(
        "Daily Inflow / Revenue (₹ / $):",
        min_value=0.0,
        value=float(record[25]) if (record and record[25]) else 0.0,
        step=100.0,
    )
    expense = col_exp.number_input(
        "Daily Expenses:",
        min_value=0.0,
        value=float(record[26]) if (record and record[26]) else 0.0,
        step=50.0,
    )

    expense_cat = st.selectbox(
        "Expense Category:",
        ["None", "Food", "Tools/Software", "Transport", "Personal", "Other"],
        index=["None", "Food", "Tools/Software", "Transport", "Personal", "Other"].index(
            record[27] if (record and record[27]) else "None"
        ),
    )

    agency_focus = st.text_input(
        "Daily Agency Focus:",
        value=record[28] if (record and record[28]) else "",
        placeholder="e.g., Built dental bot prototype, followed up with 3 leads",
    )

    if st.button("Save Wealth Entry", type="primary", use_container_width=True):
        current = load_day_data(str(wealth_date)) or [str(wealth_date)] + [0] * 27
        updated = list(current)
        updated[0] = str(wealth_date)
        updated[20] = agency_mode
        updated[21], updated[22], updated[23], updated[24] = (
            int(outreach_done),
            int(zero_spend),
            int(client_delivered),
            int(learning_done),
        )
        updated[25], updated[26], updated[27], updated[28] = (
            float(revenue),
            float(expense),
            expense_cat,
            agency_focus,
        )
        save_day_data(tuple(updated))
        st.success(f"Wealth log saved for {wealth_date}!")

# =============================================================
# TAB 4: RECORDS & CALENDAR VIEW
# =============================================================
with tab_records:
    st.subheader("Stored Logs History")
    cursor.execute(
        "SELECT date, fajr+dhuhr+asr+maghrib+isha as prayers, creatine+egg+shake as diet_score, revenue, expense FROM daily_records ORDER BY date DESC"
    )
    rows = cursor.fetchall()
    if rows:
        st.table(
            [
                {
                    "Date": r[0],
                    "Prayers (out of 5)": f"{r[1]}/5",
                    "Diet Fuel Logged": f"{r[2]}/3",
                    "Revenue": f"{r[3]}",
                    "Expense": f"{r[4]}",
                }
                for r in rows
            ]
        )
    else:
        st.info("No logs saved yet. Pick a date above and save an entry!")
