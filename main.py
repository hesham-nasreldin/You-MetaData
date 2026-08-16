import streamlit as st
import yt_dlp

strings = {
    "en": {
        "title": "YouTube Metadata",
        "urlLabel": "Video URL",
        "fetchBtn": "Get Metadata",
        "resultTitle": "Video Information",
        "labelTitle": "Title",
        "labelChannel": "Channel",
        "labelDate": "Upload Date",
        "errorNoUrl": "Please provide a video URL.",
        "errorFetch": "Error fetching metadata.",
    },
    "ar": {
        "title": "بيانات الفيديو",
        "urlLabel": "رابط الفيديو",
        "fetchBtn": "جلب المعلومات",
        "resultTitle": "معلومات الفيديو",
        "labelTitle": "العنوان",
        "labelChannel": "القناة",
        "labelDate": "تاريخ الرفع",
        "errorNoUrl": "يرجى إدخال رابط الفيديو.",
        "errorFetch": "حدث خطأ أثناء جلب البيانات.",
    },
}


st.set_page_config(page_title="YouTube Metadata", layout="centered")

# Language selector
lang_label = "Language / اللغة"
lang = st.selectbox(lang_label, options=["English", "العربية"])
lang_code = "ar" if lang == "العربية" else "en"

# Inject RTL and font for Arabic
if lang_code == "ar":
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
        html, body, [data-testid="stAppViewContainer"] {direction: rtl; text-align: right; font-family: 'Cairo', sans-serif}
        .stButton>button {float: none}
        </style>
        """,
        unsafe_allow_html=True,
    )


st.title(strings[lang_code]["title"])

with st.form(key="meta_form"):
    url_text = st.text_area(
        label=strings[lang_code]["urlLabel"],
        value="",
        help="Enter one video URL per line",
        placeholder="https://www.youtube.com/watch?v=...\nhttps://youtu.be/...",
        height=120,
    )
    submit = st.form_submit_button(strings[lang_code]["fetchBtn"])

if submit:
    urls = [u.strip() for u in (url_text or "").splitlines() if u.strip()]
    if not urls:
        st.error(strings[lang_code]["errorNoUrl"])
    else:
        results = []
        ydl_opts = {"quiet": True, "extract_flat": True}
        for u in urls:
            with st.spinner(f"Fetching: {u}"):
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(u, download=False)

                    title = info.get("title") or "-"
                    channel = info.get("uploader") or "-"
                    raw_date = info.get("upload_date")
                    if raw_date and len(raw_date) == 8:
                        upload_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
                    else:
                        upload_date = "-"

                    results.append(
                        {
                            "url": u,
                            strings[lang_code]["labelTitle"]: title,
                            strings[lang_code]["labelChannel"]: channel,
                            strings[lang_code]["labelDate"]: upload_date,
                            "error": "",
                        }
                    )
                except yt_dlp.utils.DownloadError as e:
                    results.append(
                        {
                            "url": u,
                            strings[lang_code]["labelTitle"]: "",
                            strings[lang_code]["labelChannel"]: "",
                            strings[lang_code]["labelDate"]: "",
                            "error": f"DownloadError: {e}",
                        }
                    )
                except Exception as e:
                    results.append(
                        {
                            "url": u,
                            strings[lang_code]["labelTitle"]: "",
                            strings[lang_code]["labelChannel"]: "",
                            strings[lang_code]["labelDate"]: "",
                            "error": str(e),
                        }
                    )

        st.subheader(strings[lang_code]["resultTitle"])
        # Display results as a table
        st.dataframe(results)
