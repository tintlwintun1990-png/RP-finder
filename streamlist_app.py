import streamlit as st
import swisseph as swe
from datetime import datetime
import pytz

# --- Golden Theme Configuration ---
st.set_page_config(page_title="Sai Kong Kham KP Pro", page_icon="🔮")

# Custom CSS for Golden Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #FFD700 !important;
    }
    .stButton>button {
        background-color: #FFD700;
        color: black;
        font-weight: bold;
        border-radius: 10px;
    }
    div[data-testid="stMetricValue"] {
        color: #FFD700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KP Constants ---
PLANETS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

# --- Planet Significators (ဆရာ့ပုံထဲကအတိုင်း) ---
PLANET_SIGNIFICATORS = {
    "Sun": [1, 10, 11], "Moon": [2, 4, 11], "Mars": [1, 6, 10],
    "Mercury": [3, 6, 11], "Jupiter": [2, 5, 9, 11], "Venus": [2, 7, 11],
    "Saturn": [8, 10, 12], "Rahu": [3, 6, 11], "Ketu": [7, 9, 12]
}

# --- Question Houses ---
QUESTION_HOUSES = {
    "၁။ ကျွန်တော့်ရဲ့ ရည်မှန်းချက် အောင်မြင်နိုင်မလား?": [1, 11],
    "၂။ အလုပ်အကိုင် အခွင့်အလမ်းသစ် ရနိုင်မလား?": [2, 6, 10, 11],
    "၃။ ငွေကြေး စီးပွား အဆင်ပြေ ချောမွေ့ပါ့မလား?": [2, 6, 11],
    "၄။ ချစ်ရေးချစ်ရာ နှင့် အိမ်ထောင်ရေး ကံကောင်းမလား?": [2, 5, 7, 11],
    "၅။ ကျန်းမာရေး အခြေအနေ ကောင်းမွန်လာမလား?": [1, 5, 11],
    "၆။ အမှုအခင်း ကိစ္စများ အနိုင်ရနိုင်မလား?": [1, 6, 11],
    "၇။ နိုင်ငံရပ်ခြား ခရီးသွားရမည့် အစီအစဉ် အောင်မြင်မလား?": [3, 9, 12],
    "၈။ အိမ်/ခြံ/မြေ/ကား အရောင်းအဝယ် ဖြစ်ပါ့မလား?": [4, 11, 12],
    "၉။ စာမေးပွဲ သို့မဟုတ် ပြိုင်ပွဲများ အောင်မြင်မလား?": [4, 9, 11],
    "၁၀။ ပျောက်ဆုံးပစ္စည်း သို့မဟုတ် ကြွေးမြီများ ပြန်ရမလား?": [2, 6, 11]
}

# --- Logic: KP 1-249 Star and Sub ---
def get_kp_1_249_details(number):
    # KP 1-249 table logic to find Star and Sub Lord
    star_idx = ((number - 1) // 9) % 9
    sub_idx = (number - 1) % 9
    return PLANETS[star_idx], PLANETS[sub_idx]

def get_transit_moon(jd):
    lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
    res, ret = swe.calc_ut(jd, swe.MOON)
    return lords[int(res[0]/30)]

# --- UI Layout ---
st.title("🌟 Sai Kong Kham - KP Pro")
st.subheader("Professional Astrology Software Division")

tab1, tab2 = st.tabs(["Ruling Planets (အခါရွေး)", "KP Horary (မေးခွန်းဟော)"])

with tab1:
    now = datetime.now(pytz.timezone('Asia/Yangon'))
    st.info(f"📅 လက်ရှိအချိန်: {now.strftime('%I:%M:%S %p')}")
    st.write("လက်ရှိ Transit အခြေအနေအရ အခါကောင်းများကို စစ်ဆေးနိုင်သည်။")

with tab2:
    st.write("### 🔮 ဆန္ဒဂဏန်းဖြင့် စိစစ်ချက်")
    selected_q = st.selectbox("သိလိုသော မေးခွန်းကို ရွေးပါ", list(QUESTION_HOUSES.keys()))
    num = st.number_input("ဆန္ဒဂဏန်း (၁ မှ ၂၄၉) ကို ရိုက်ပါ", min_value=1, max_value=249, value=1)
    
    if st.button("ဟောကိန်းရလဒ် စစ်ဆေးမည်"):
        now = datetime.now(pytz.timezone('Asia/Yangon'))
        jd = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)
        
        star_lord, sub_lord = get_kp_1_249_details(num)
        target_houses = QUESTION_HOUSES[selected_q]
        sub_lord_houses = PLANET_SIGNIFICATORS.get(sub_lord, [])
        t_moon_lord = get_transit_moon(jd)

        st.divider()
        st.write(f"### ✨ ရလဒ်စိစစ်ချက် (နံပါတ် - {num})")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("နက္ခတ်အရှင် (Star)", star_lord)
        col2.metric("အတန့်အရှင် (Sub)", sub_lord)
        col3.metric("Transit Moon", t_moon_lord)

        st.divider()
        
        is_success = any(h in target_houses for h in sub_lord_houses)

        if is_success:
            st.success("✅ **ဟောကိန်း: အောင်မြင်ပါမည်။**")
            st.write(f"အတန့်အရှင် {sub_lord} သည် လိုလားသော ဘာဝများ ({', '.join(map(str, target_houses))}) နှင့် ဆက်စပ်နေပါသည်။")
        else:
            st.warning("⚠️ **ဟောကိန်း: အတားအဆီး ရှိနိုင်ပါသည်။**")
            st.write("အတန့်အရှင်သည် မေးခွန်း၏ ဘာဝများနှင့် ဆက်စပ်မှု အားနည်းနေပါသည်။")

st.divider()
st.caption("© 2026 Sai Kong Kham Astrology - Premium Edition")
