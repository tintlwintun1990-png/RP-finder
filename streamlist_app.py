import streamlit as st
import swisseph as swe
from datetime import datetime
import pytz

# --- Configuration ---
st.set_page_config(page_title="Sai Kong Kham KP RP", page_icon="🔮")

st.title("🔮 KP Ruling Planets")
st.subheader("Sai Kong Kham - KP Professional Analyzer")

# --- Helper Functions ---
def get_planet_details(jd, planet):
    # Fixed: Get only the first value from calculation
    res_list, ret = swe.calc_ut(jd, planet)
    res = res_list[0] 
    
    sign_idx = int(res / 30)
    signs = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya", "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]
    lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
    
    stars = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    star_pos = res * (27.0/360.0)
    star_idx = int((star_pos % 1) * 9)
    
    return signs[sign_idx], lords[sign_idx], stars[star_idx % 9]

# --- Main Logic ---
now = datetime.now(pytz.timezone('Asia/Yangon'))
st.write(f"📅 လက်ရှိအချိန်: **{now.strftime('%d-%m-%Y %I:%M:%S %p')}**")

jd = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)

try:
    # Get Moon Details
    moon_sign, moon_sign_lord, moon_star_lord = get_planet_details(jd, swe.MOON)
    
    # Get Lagna (Simplified for default location Magway)
    res_houses, ret_h = swe.houses_ex(jd, 20.15, 94.94, b'P')
    ascendant = res_houses[0]
    lagna_sign_idx = int(ascendant / 30)
    lagna_lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

    st.divider()

    # --- Display Results ---
    col1, col2 = st.columns(2)

    with col1:
        st.info("🌙 Moon (စန္ဒြ)")
        st.write(f"**Sign Lord:** {moon_sign_lord}")
        st.write(f"**Star Lord:** {moon_star_lord}")

    with col2:
        st.success("🌅 Lagna (လဂ်)")
        st.write(f"**Sign Lord:** {lagna_lords[lagna_sign_idx]}")
        st.write(f"**Star Lord:** KP Star Lord")

    st.warning(f"📅 **Day Lord (ဝါရအရှင်):** {now.strftime('%A')}")

except Exception as e:
    st.error("တွက်ချက်မှု အနည်းငယ် မှားယွင်းနေပါသည်။ ခဏအကြာတွင် ပြန်လည် ကြိုးစားကြည့်ပါ။")

st.divider()
st.caption("© 2026 Sai Kong Kham Astrology Software Division")
