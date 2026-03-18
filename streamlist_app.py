import streamlit as st
import swisseph as swe
from datetime import datetime
import pytz

# --- Configuration ---
st.set_page_config(page_title="Sai Kong Kham KP RP", page_icon="🔮")

# Custom CSS for Burmese Font & Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    h1, h3 { color: #2e4053; font-family: 'Pyidaungsu', sans-serif; }
    </style>
    """, unsafe_allow_index=True)

st.title("🔮 KP Ruling Planets (Real-time)")
st.subheader("Sai Kong Kham - KP Professional Analyzer")

# --- Helper Functions ---
def get_planet_details(jd, planet):
    res = swe.calc_ut(jd, planet)[0]
    sign_idx = int(res / 30)
    signs = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya", "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]
    lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
    
    # Star Lord Calculation (Vimshottari order)
    stars = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    star_pos = res * (27/360)
    star_idx = int((star_pos % 1) * 9) # Simplified for prototype
    
    return signs[sign_idx], lords[sign_idx], stars[star_idx % 9]

# --- Main Logic ---
now = datetime.now(pytz.timezone('Asia/Yangon'))
st.write(f"📅 လက်ရှိအချိန် (မြန်မာ): **{now.strftime('%d-%m-%Y %I:%M:%S %p')}**")

# Julian Day for SwissEph
jd = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)

# Get Data
moon_sign, moon_sign_lord, moon_star_lord = get_planet_details(jd, swe.MOON)
# Simplified Lagna (Lagna calculation needs coordinates, using 90E, 20N as default)
res_asc = swe.houses_ex(jd, 20.15, 94.94, b'P')[0][0]
lagna_sign_idx = int(res_asc / 30)
lagna_lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

st.divider()

# --- Display Results ---
col1, col2 = st.columns(2)

with col1:
    st.info("🌙 Moon (စန္ဒြ)")
    st.metric("Sign Lord", moon_sign_lord)
    st.metric("Star Lord", moon_star_lord)

with col2:
    st.success("🌅 Lagna (လဂ်)")
    st.metric("Sign Lord", lagna_lords[lagna_sign_idx])
    st.metric("Star Lord", "Saturn") # Static for prototype preview

day_lord = now.strftime('%A')
st.warning(f"📅 **Day Lord (ဝါရအရှင်):** {day_lord}")

st.divider()
st.info("💡 **ဟောကိန်းလမ်းညွှန်:** လက်ရှိ RP ထဲမှာ ကိုယ်လုပ်မယ့်ကိစ္စရဲ့ အိမ်အရှင်ဂြိုဟ်တွေ ပါဝင်နေရင် အောင်မြင်နိုင်ခြေ အလွန်များပါတယ်။")
st.caption("© 2026 Sai Kong Kham Astrology Software Division")
