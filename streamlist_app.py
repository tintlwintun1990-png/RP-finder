import streamlit as st
import swisseph as swe
from datetime import datetime
import pytz

# Page Branding
st.set_page_config(page_title="Sai Kong Kham KP RP", page_icon="🔮")

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🔮 KP Ruling Planets</h1>", unsafe_allow_index=True)
st.markdown("<h3 style='text-align: center;'>Sai Kong Kham - Professional Analyzer</h3>", unsafe_allow_index=True)

# Main Calculation Logic
def get_rp():
    # Set Timezone
    tz = pytz.timezone('Asia/Yangon')
    now = datetime.now(tz)
    
    # Julian Day calculation
    jd = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)
    
    # Signs and Lords
    signs = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya", "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]
    lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
    stars = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

    # 1. Moon Details
    moon_pos = swe.calc_ut(jd, swe.MOON)[0][0]
    m_sign_idx = int(moon_pos / 30)
    m_star_idx = int((moon_pos * 3 / 40) % 9)
    
    # 2. Lagna Details (Using Magway location roughly)
    # Lat: 20.15, Lon: 94.94
    res = swe.houses_ex(jd, 20.15, 94.94, b'P')[0]
    asc_pos = res[0]
    l_sign_idx = int(asc_pos / 30)
    l_star_idx = int((asc_pos * 3 / 40) % 9)

    return {
        "time": now.strftime('%d-%m-%Y %I:%M:%S %p'),
        "m_lord": lords[m_sign_idx],
        "m_star": stars[m_star_idx],
        "l_lord": lords[l_sign_idx],
        "l_star": stars[l_star_idx],
        "day": now.strftime('%A')
    }

# UI Display
try:
    data = get_rp()
    st.info(f"📅 လက်ရှိအချိန်: **{data['time']}**")
    
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌙 Moon (စန္ဒြ)")
        st.write(f"**Sign Lord:** {data['m_lord']}")
        st.write(f"**Star Lord:** {data['m_star']}")
        
    with col2:
        st.subheader("🌅 Lagna (လဂ်)")
        st.write(f"**Sign Lord:** {data['l_lord']}")
        st.write(f"**Star Lord:** {data['l_star']}")

    st.warning(f"📅 **Day Lord (ဝါရအရှင်):** {data['day']}")
    
except Exception as e:
    st.error("တွက်ချက်မှုတွင် အမှားရှိနေပါသည်။ ခဏအကြာမှ ပြန်လည် Refresh လုပ်ပေးပါ။")

st.divider()
st.caption("© 2026 Sai Kong Kham Astrology Software Division")
