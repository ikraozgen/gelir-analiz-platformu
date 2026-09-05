import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client, Client

# --- Sayfa Konfigürasyonu ---
st.set_page_config(
    page_title="Gelir & Pasif Gelir Platformu ✨",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Canlı, Renkli & Animasyonlu Özel CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Ana Arka Plan ve Yumuşak Işıltı */
.stApp {
    background: linear-gradient(135deg, #FDFBFB 0%, #EBEDEE 100%);
}

/* Canlı Gradient Başlık Animasyonu */
@keyframes gradientAnimation {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.gradient-title {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(-45deg, #FF6B8B, #FF8E53, #9B51E0, #6C5CE7, #FD79A8);
    background-size: 300% 300%;
    animation: gradientAnimation 6s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
    display: inline-block;
}

.sub-title {
    font-size: 1.05rem;
    color: #636E72;
    font-weight: 500;
    margin-bottom: 1.8rem;
}

/* Renkli ve Işıltılı KPI Kartları */
.kpi-card {
    border-radius: 18px;
    padding: 22px 16px;
    color: white !important;
    text-align: center;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.kpi-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.18);
}

.kpi-title {
    font-size: 0.92rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    opacity: 0.95;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 1.9rem;
    font-weight: 800;
    letter-spacing: -0.5px;
}

/* KPI Kart Gradientleri */
.card-pink { background: linear-gradient(135deg, #FF758C 0%, #FF7EB3 100%); }
.card-purple { background: linear-gradient(135deg, #A18CD1 0%, #FBC2EB 100%); }
.card-blue { background: linear-gradient(135deg, #4FACFE 0%, #00F2FE 100%); }
.card-sunset { background: linear-gradient(135deg, #FA709A 0%, #FEE140 100%); }

/* Canlı Gönder Butonu */
.stButton > button {
    background: linear-gradient(135deg, #FF6B8B 0%, #9B51E0 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 28px !important;
    box-shadow: 0 10px 20px -5px rgba(255, 107, 139, 0.4) !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.01) !important;
    box-shadow: 0 15px 25px -5px rgba(155, 81, 224, 0.5) !important;
}

/* Şık Kart Çerçevesi */
.glass-box {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(255, 255, 255, 0.9);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
    margin-bottom: 24px;
}
</style>
""", unsafe_allow_html=True)

# --- Supabase Bağlantı Bilgileri (Kalıcı ve Güvenli) ---
SUPABASE_URL = "https://zxysmzuquiuqahnfewly.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp4eXNtenVxdWl1cWFobmZld2x5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg1OTI0MDMsImV4cCI6MjEwNDE2ODQwM30.Rf2LnGHy4lad7YkK_Nz9kvyqtfYzMTp4LLy32UXv3sI"

if "supabase" in st.secrets:
    SUPABASE_URL = st.secrets["supabase"].get("url", SUPABASE_URL)
    SUPABASE_KEY = st.secrets["supabase"].get("key", SUPABASE_KEY)

@st.cache_resource
def get_supabase_client(url: str, key: str):
    try:
        return create_client(url, key)
    except Exception as e:
        return None

supabase: Client = get_supabase_client(SUPABASE_URL, SUPABASE_KEY)

# --- Sol Menü Tasarımı ---
st.sidebar.markdown("### 🌸 Platform Menüsü")
sayfa = st.sidebar.radio(
    "Nereye gitmek istersin?",
    ["📝 Gelir Bildir (Anket Formu)", "📊 Canlı & Renkli Analiz Paneli"]
)

st.sidebar.markdown("---")
if supabase:
    st.sidebar.markdown("🟢 **Sistem Canlı & Veritabanı Bağlı** ✨")
else:
    st.sidebar.markdown("🔴 **Bağlantı Bekleniyor**")

st.sidebar.markdown(
    """
    <div style='background: white; border-radius: 12px; padding: 12px; border: 1px solid #FFE3EC; font-size: 0.85rem; color: #636E72; margin-top: 15px;'>
        💡 <b>Tamamen Anonimdir:</b><br>
        Ad, soyad, telefon veya kimlik bilgisi toplanmaz. Rahatça doldurabilirsin!
    </div>
    """,
    unsafe_allow_html=True
)

# Türkiye İlleri ve Sektörler
ILLER = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir",
    "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli",
    "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari",
    "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir",
    "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir",
    "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat",
    "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman",
    "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"
]

SEKTORLER = [
    "Bankacılık ve Finans", "Üretim ve Sanayi", "Bilişim ve Yazılım", "Sağlık ve İlaç",
    "Eğitim", "Pazarlama ve E-Ticaret", "İnşaat ve Mimarlık", "Lojistik ve Tedarik Zinciri",
    "Otomotiv", "Hukuk ve Danışmanlık", "Kamu", "Diğer"
]

# ==========================================
# SAYFA 1: GELİR BİLDİRİM FORMU
# ==========================================
if sayfa == "📝 Gelir Bildir (Anket Formu)":
    st.markdown('<div class="gradient-title">Anonim Gelir ve Pasif Gelir Bildirimi ✨</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">Bu platform tamamen <b>anonimdir</b>. Hiçbir kimlik bilgin kaydedilmez. '
        'Toplanan veriler Türkiye\'deki gerçek gelir ve finansal özgürlük trendlerini haritalamak için kullanılır. 💕</div>',
        unsafe_allow_html=True
    )

    with st.form("gelir_formu", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 📍 Genel Bilgilerin")
            yas_grubu = st.selectbox("Yaş Grubu *", ["18-24", "25-34", "35-44", "45-54", "55+"], index=1)
            sehir = st.selectbox("Yaşadığın İl *", ILLER, index=ILLER.index("İstanbul") if "İstanbul" in ILLER else 0)
            ilce = st.text_input("Yaşadığın İlçe *", placeholder="Örn: Çekmeköy, Kadıköy, Nilüfer...")
            tecrube = st.number_input("Sektördeki Toplam Tecrüben (Yıl) *", min_value=0, max_value=50, value=2, step=1)

        with col2:
            st.markdown("##### 💼 Meslek ve Gelir Bilgilerin")
            sektor = st.selectbox("Çalıştığın Sektör *", SEKTORLER, index=0)
            meslek = st.text_input("Meslek / Unvan *", placeholder="Örn: Kalite Kontrol Mühendisi, Veri Analisti...")
            aylik_gelir = st.number_input("Aylık Ortalama Net Gelirin (TL) *", min_value=0.0, max_value=10000000.0, value=45000.0, step=1000.0)
            pasif_var_mi = st.radio("Pasif Gelirin Var mı? (Kira, Borsa, Faiz vb.) *", ["Hayır", "Evet"], horizontal=True)

        pasif_tutar = 0.0
        pasif_kaynaklar_str = ""

        if pasif_var_mi == "Evet":
            st.markdown("---")
            st.markdown("##### 💰 Pasif Gelir Detayların")
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                pasif_tutar = st.number_input("Aylık Ortalama Pasif Gelir Tutarı (TL) *", min_value=0.0, max_value=10000000.0, value=10000.0, step=1000.0)
            with p_col2:
                secilen_kaynaklar = st.multiselect(
                    "Pasif Gelir Kaynakların *",
                    ["Borsa / Hisse Senedi 📈", "Gayrimenkul / Kira 🏠", "Mevduat / Faiz 🏦", "Fon / Altın 🪙", "Freelance / Ek İş 💻", "Kripto Varlıklar ⚡", "Diğer ✨"]
                )
                pasif_kaynaklar_str = ", ".join(secilen_kaynaklar)

        st.markdown("<br>", unsafe_allow_html=True)
        gonder = st.form_submit_button("🌸 Verileri Güvenli & Anonim Olarak Gönder", use_container_width=True)

        if gonder:
            if not ilce.strip() or not meslek.strip():
                st.error("Lütfen ilçe ve meslek/unvan alanlarını doldurunuz.")
            elif pasif_var_mi == "Evet" and not pasif_kaynaklar_str:
                st.error("Pasif gelirin olduğunu belirttin, lütfen en az bir kaynak seç!")
            elif not supabase:
                st.error("Veritabanı bağlantısında bir problem var.")
            else:
                yeni_kayit = {
                    "yas_grubu": yas_grubu,
                    "sehir": sehir,
                    "ilce": ilce.strip(),
                    "sektor": sektor,
                    "meslek": meslek.strip(),
                    "tecrube_yili": int(tecrube),
                    "aylik_net_gelir": float(aylik_gelir),
                    "pasif_gelir_var_mi": (pasif_var_mi == "Evet"),
                    "pasif_gelir_tutari": float(pasif_tutar),
                    "pasif_gelir_kaynagi": pasif_kaynaklar_str
                }
                try:
                    res = supabase.table("gelir_verileri").insert(yeni_kayit).execute()
                    st.success("🎉 Harika! Bilgilerin tamamen anonim olarak veritabanına eklendi. Katkın için teşekkürler! 💕")
                    st.balloons()
                except Exception as e:
                    st.error(f"Kayıt eklenirken hata oluştu: {e}")

# ==========================================
# SAYFA 2: CANLI & RENKLİ ANALİZ PANELİ
# ==========================================
elif sayfa == "📊 Canlı & Renkli Analiz Paneli":
    st.markdown('<div class="gradient-title">Canlı Finans & Gelir Trendleri 📊</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Katılımcılardan toplanan verilerle gerçek zamanlı üretilen dinamik içgörüler. ✨</div>', unsafe_allow_html=True)

    if not supabase:
        st.warning("⚠️ Veritabanı bağlantısı kurulamadı.")
    else:
        try:
            response = supabase.table("gelir_verileri").select("*").execute()
            rows = response.data

            if not rows:
                st.markdown("""
                <div style='background: white; border-radius: 20px; padding: 40px; text-align: center; border: 2px dashed #FF8E53; margin-top: 20px;'>
                    <h2 style='color: #FF6B8B;'>🌸 Veri Havuzu Henüz Tertemiz!</h2>
                    <p style='color: #636E72; font-size: 1.1rem;'>Veritabanındaki tüm eski test verileri silindi. Formu ilk dolduran sen veya arkadaşların olabilir! ✨</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                df = pd.DataFrame(rows)
                df["aylik_net_gelir"] = pd.to_numeric(df["aylik_net_gelir"], errors="coerce")
                df["pasif_gelir_tutari"] = pd.to_numeric(df["pasif_gelir_tutari"], errors="coerce").fillna(0)

                toplam_katilimci = len(df)
                ort_gelir = df["aylik_net_gelir"].mean()
                pasif_oran = (df["pasif_gelir_var_mi"].sum() / toplam_katilimci) * 100
                ort_pasif = df[df["pasif_gelir_var_mi"] == True]["pasif_gelir_tutari"].mean() if pasif_oran > 0 else 0

                # --- RENKLİ GRADIENT KPI KARTLARI ---
                k1, k2, k3, k4 = st.columns(4)
                with k1:
                    st.markdown(f"""
                    <div class="kpi-card card-pink">
                        <div class="kpi-title">👥 Toplam Katılımcı</div>
                        <div class="kpi-value">{toplam_katilimci:,}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with k2:
                    st.markdown(f"""
                    <div class="kpi-card card-purple">
                        <div class="kpi-title">💵 Ort. Net Maaş</div>
                        <div class="kpi-value">{ort_gelir:,.0f} ₺</div>
                    </div>
                    """, unsafe_allow_html=True)

                with k3:
                    st.markdown(f"""
                    <div class="kpi-card card-blue">
                        <div class="kpi-title">📈 Pasif Gelir Oranı</div>
                        <div class="kpi-value">%{pasif_oran:.1f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with k4:
                    st.markdown(f"""
                    <div class="kpi-card card-sunset">
                        <div class="kpi-title">💰 Ort. Pasif Gelir</div>
                        <div class="kpi-value">{ort_pasif:,.0f} ₺</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # --- CANLI RENKLİ GRAFİKLER ---
                g_col1, g_col2 = st.columns(2)

                # Canlı Renk Paletleri
                canli_renkler = ["#FF6B8B", "#A18CD1", "#4FACFE", "#FA709A", "#6C5CE7", "#00B894", "#FDCB6E", "#E17055"]

                with g_col1:
                    st.markdown("#### 🏢 Sektörlere Göre Ortalama Gelir")
                    sektor_df = df.groupby("sektor")["aylik_net_gelir"].mean().reset_index().sort_values("aylik_net_gelir", ascending=True)
                    fig_sektor = px.bar(
                        sektor_df,
                        x="aylik_net_gelir",
                        y="sektor",
                        orientation="h",
                        labels={"aylik_net_gelir": "Ortalama Net Gelir (TL)", "sektor": "Sektör"},
                        color="aylik_net_gelir",
                        color_continuous_scale="Sunset"
                    )
                    fig_sektor.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="Plus Jakarta Sans", size=12),
                        height=400,
                        margin=dict(l=10, r=10, t=20, b=20)
                    )
                    st.plotly_chart(fig_sektor, use_container_width=True)

                with g_col2:
                    st.markdown("#### 🥧 Pasif Gelir Kaynakları Dağılımı")
                    kaynaklar_listesi = []
                    for k in df[df["pasif_gelir_var_mi"] == True]["pasif_gelir_kaynagi"].dropna():
                        for item in str(k).split(","):
                            temiz = item.strip().replace("📈", "").replace("🏠", "").replace("🏦", "").replace("🪙", "").replace("💻", "").replace("⚡", "").replace("✨", "").strip()
                            if temiz:
                                kaynaklar_listesi.append(temiz)

                    if kaynaklar_listesi:
                        kaynak_df = pd.Series(kaynaklar_listesi).value_counts().reset_index()
                        kaynak_df.columns = ["Kaynak", "Adet"]
                        fig_kaynak = px.pie(
                            kaynak_df,
                            names="Kaynak",
                            values="Adet",
                            hole=0.45,
                            color_discrete_sequence=canli_renkler
                        )
                        fig_kaynak.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
                        fig_kaynak.update_layout(
                            plot_bgcolor="rgba(0,0,0,0)",
                            paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(family="Plus Jakarta Sans"),
                            height=400,
                            margin=dict(l=10, r=10, t=20, b=20)
                        )
                        st.plotly_chart(fig_kaynak, use_container_width=True)
                    else:
                        st.info("Henüz pasif gelir kaynağı verisi eklenmedi.")

                g_col3, g_col4 = st.columns(2)

                with g_col3:
                    st.markdown("#### 🎂 Yaş Gruplarına Göre Gelir Dağılımı")
                    yas_sirasi = ["18-24", "25-34", "35-44", "45-54", "55+"]
                    yas_df = df.groupby("yas_grubu")["aylik_net_gelir"].mean().reindex(yas_sirasi).dropna().reset_index()
                    fig_yas = px.bar(
                        yas_df,
                        x="yas_grubu",
                        y="aylik_net_gelir",
                        labels={"yas_grubu": "Yaş Grubu", "aylik_net_gelir": "Ortalama Gelir (TL)"},
                        color="aylik_net_gelir",
                        color_continuous_scale="Purp"
                    )
                    fig_yas.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="Plus Jakarta Sans"),
                        height=360,
                        margin=dict(l=10, r=10, t=20, b=20)
                    )
                    st.plotly_chart(fig_yas, use_container_width=True)

                with g_col4:
                    st.markdown("#### 📍 En Çok Katılım Olan Şehirler")
                    il_df = df["sehir"].value_counts().head(5).reset_index()
                    il_df.columns = ["Şehir", "Katılımcı Sayısı"]
                    fig_il = px.bar(
                        il_df,
                        x="Şehir",
                        y="Katılımcı Sayısı",
                        color="Katılımcı Sayısı",
                        color_continuous_scale="Tealgrn"
                    )
                    fig_il.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="Plus Jakarta Sans"),
                        height=360,
                        margin=dict(l=10, r=10, t=20, b=20)
                    )
                    st.plotly_chart(fig_il, use_container_width=True)

                # --- GELİŞMİŞ VE RENKLİ VERİ TABLOSU ---
                st.markdown("---")
                st.markdown("#### 📋 Anonim Katılımcı Havuzu (Filtrelenebilir)")
                secilen_sektor = st.selectbox("Sektöre Göre Filtrele:", ["Tümü ✨"] + list(df["sektor"].unique()))
                filtreli_df = df if secilen_sektor == "Tümü ✨" else df[df["sektor"] == secilen_sektor]
                
                gosterim_kolonlari = ["sehir", "ilce", "sektor", "meslek", "tecrube_yili", "aylik_net_gelir", "pasif_gelir_var_mi", "pasif_gelir_tutari", "pasif_gelir_kaynagi"]
                st.dataframe(
                    filtreli_df[gosterim_kolonlari].sort_values("aylik_net_gelir", ascending=False),
                    use_container_width=True,
                    hide_index=True
                )

        except Exception as e:
            st.error(f"Veriler çekilirken hata oluştu: {e}")
