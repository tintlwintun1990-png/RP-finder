import streamlit as st
import swisseph as swe
from datetime import datetime
import pytz

st.set_page_config(page_title="Sai Kong Kham KP Pro", page_icon="🔮")

# --- Logic: ဂြိုဟ်သွားတွက်ချက်ခြင်း ---
def get_transit_data(jd):
    planets = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, 
        "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER, 
        "Venus": swe.VENUS, "Saturn": swe.SATURN
    }
    transit_results = {}
    lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
    
    for name, code in planets.items():
        res, ret = swe.calc_ut(jd, code)
        sign_idx = int(res[0] / 30)
        transit_results[name] = lords[sign_idx]
    return transit_results

# --- Logic: ဆန္ဒဂဏန်းမှ Sub-lord ရှာခြင်း ---
def get_kp_sub(number):
    total_arc = 360.0
    pos = (number - 1) * (total_arc / 249.0) + 0.01
    lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
    stars = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    sub_idx = (number % 9)
    return lords[int(pos/30)%12], stars[sub_idx]

# --- UI Design ---
st.title("🔮 KP Professional Analyzer")
st.subheader("Sai Kong Kham - Digital Astrology")

tab1, tab2 = st.tabs(["Ruling Planets (အခါရွေး)", "KP Horary (မေးခွန်း ၁၀ ခု)"])

with tab1:
    now = datetime.now(pytz.timezone('Asia/Yangon'))
    st.info(f"⏰ လက်ရှိအချိန်: {now.strftime('%I:%M:%S %p')}")
    st.write("လက်ရှိကောင်းကင်ရှိ ဂြိုဟ်အခြေအနေကို ကြည့်ရှုနေပါသည်။")

with tab2:
    # ၁။ မေးခွန်း ၁၀ ခု သတ်မှတ်ခြင်း
    questions = [
        "၁။ ကျွန်တော့်ရဲ့ ရည်မှန်းချက် အောင်မြင်နိုင်မလား?",
        "၂။ အလုပ်အကိုင် အခွင့်အလမ်းသစ် ရနိုင်မလား?",
        "၃။ ငွေကြေး စီးပွား အဆင်ပြေ ချောမွေ့ပါ့မလား?",
        "၄။ ချစ်ရေးချစ်ရာ နှင့် အိမ်ထောင်ရေး ကံကောင်းမလား?",
        "၅။ ကျန်းမာရေး အခြေအနေ ကောင်းမွန်လာမလား?",
        "၆။ အမှုအခင်း ကိစ္စများ အနိုင်ရနိုင်မလား?",
        "၇။ နိုင်ငံရပ်ခြား ခရီးသွားရမည့် အစီအစဉ် အောင်မြင်မလား?",
        "၈။ အိမ်/ခြံ/မြေ/ကား အရောင်းအဝယ် ဖြစ်ပါ့မလား?",
        "၉။ စာမေးပွဲ သို့မဟုတ် ပြိုင်ပွဲများ အောင်မြင်မလား?",
        "၁၀။ ပျောက်ဆုံးပစ္စည်း သို့မဟုတ် ကြွေးမြီများ ပြန်ရမလား?"
    ]
    
    selected_q = st.selectbox("သိလိုသော မေးခွန်းကို ရွေးချယ်ပါ", questions)
    num = st.number_input("ဆန္ဒဂဏန်း (၁ မှ ၂၄၉) ရိုက်ထည့်ပါ", min_value=1, max_value=249, value=1)
    
    if st.button("စိစစ်ချက်ရလဒ် ကြည့်မည်"):
        now = datetime.now(pytz.timezone('Asia/Yangon'))
        jd = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)
        
        sign_lord, sub_lord = get_kp_sub(num)
        transit_data = get_transit_data(jd)
        
        st.divider()
        st.write(f"### 📋 {selected_q}")
        
        # စိစစ်ချက် Logic
        # Sub-lord က Transit ထဲက Benefics (Jupiter, Venus, Mercury) နဲ့ တိုက်ဆိုင်ရင် ပိုခိုင်မာတယ်
        is_strong = sub_lord in transit_data.values()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("ဆန္ဒဂဏန်း Sub-lord", sub_lord)
        with col2:
            st.metric("လက်ရှိ Moon Sign Lord", transit_data["Moon"])

        st.divider()
        st.write("### 💡 ဟောကိန်းစိစစ်ချက်")
        
        if is_strong:
            st.success("✅ **အဖြေ: အောင်မြင်ပါမည်။**")
            st.write("ဆန္ဒဂဏန်းနှင့် လက်ရှိဂြိုဟ်သွား လွန်စွာကိုက်ညီနေပါသည်။ အခွင့်အလမ်းကောင်းများ မကြာမီ ရောက်ရှိလာပါလိမ့်မည်။")
        else:
            if sub_lord in ["Saturn", "Ketu"]:
                st.warning("⏳ **အဖြေ: နှောင့်နှေးမှု ရှိနိုင်ပါသည်။**")
                st.write("အတားအဆီး သို့မဟုတ် အချိန်ကြန့်ကြာမှု အနည်းငယ် ရှိနိုင်သဖြင့် စိတ်ရှည်သည်းခံပြီး ကြိုးစားပါ။")
            else:
                st.info("💡 **အဖြေ: အသင့်အတင့် ရှိပါသည်။**")
                st.write("ကြိုးစားအားထုတ်မှုပေါ် မူတည်ပြီး ရလဒ်ထွက်ပေါ်ပါလိမ့်မည်။ ဝေဖန်ပိုင်းခြားပြီး ဆောင်ရွက်ပါ။")

st.divider()
st.caption("Developed by Sai Kong Kham - KP Astrology Division")
