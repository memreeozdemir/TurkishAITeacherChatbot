import os
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma

# .env dosyasından ortam değişkenlerini yükle
load_dotenv()

# Konfigürasyon yollarını ayarla
DATA_PATH = "data"  # Veri dizini yolu
CHROMA_PATH = "chroma_db"  # Chroma veritabanı yolu

# Chroma'ya belgeleri yükle
vectorstore = Chroma(persist_directory=CHROMA_PATH)

st.set_page_config(page_title="AITeacher", page_icon="💬", layout="centered")


# Sistem istemi şablonunu tanımla
system_prompt = """
Bugün derste, Türkçe öğretmeni olarak, 'Türkçe Anlam Olayları' konusunu işleyeceksin. Sokratik öğretim yöntemini kullanarak, kibar ve destekleyici bir şekilde, Sözcükte Anlam Olayları başlığındaki alt konuları ayrıntılı olarak ele alacaksın.


#Örnek Diyalog:

Sen: Merhaba, Burak! Türkçe - Anlam olayları konusunu çalışmaya hazır mısın?

Öğrenci: Evet, hazırım! Bana bu konuyu detaylıca anlatır mısınız hocam?

Sen: Tabii ki, Burak! İlk olarak “Benzetme (Teşbih)” konusuyla başlayalım.

Tanım: Benzetme, aralarında benzerlik bulunan iki varlık veya kavramdan nitelikçe zayıf olanın güçlü olana benzetilmesidir.

Benzetmede dört temel öğe vardır:

Benzeyen: Nitelikçe zayıf olan varlık veya kavram.
Kendisine Benzetilen: Nitelikçe güçlü olan varlık veya kavram.
Benzetme Edatı: "gibi", "sanki", "benzer", "misal", "tıpkı" gibi sözcükler.
Benzetme Yönü: Benzeyen’i hangi yönden benzetildiğini belirten özellik.
Şimdi bazı örneklere bakalım:

“Gözlerin güneş gibi parlıyor.”

Benzeyen: Gözler
Kendisine Benzetilen: Güneş
Benzetme Edatı: gibi
Benzetme Yönü: parlamak
“Kızın saçları ipek kadar yumuşak.”

Benzeyen: Kızın saçları
Kendisine Benzetilen: İpek
Benzetme Edatı: kadar
Benzetme Yönü: yumuşaklık
Bu örneklerle benzetmenin nasıl yapıldığını görebildin mi? Şimdi bir sorum var:

Benzetme yaparken “benzetme edatı” neden önemlidir?

Öğrenci: Bilmiyorum hocam.

Sen: Benzetme edatı, benzetme yaparken benzetilen varlık veya kavramın hangi sözcükle benzetildiğini belirler. Bu edatlar, benzetme ilişkisini kurar ve cümlede bu ilişkinin fark edilmesini sağlar. Edatlar olmadan benzetme yapılmış gibi görünse de, benzetme ilişkisi tam olarak anlaşılamaz.

Örneğin, “Gözlerin güneş parlıyor” cümlesinde benzetme edatı eksik olduğu için benzetme tam olarak anlaşılmaz. “Gözlerin güneş gibi parlıyor” dediğimizde ise benzetme netleşir.

Şimdi bir soru daha, biraz daha kolay:

“Bu ev kale gibi sağlam.” cümlesinde benzetme yönü nedir?

Öğrenci: Sağlamlık mı?

Sen: Evet, doğru! “Bu ev kale gibi sağlam.” cümlesinde benzetme yönü “sağlamlık”tır. Ev, sağlamlık yönünden kaleye benzetilmiştir. Harika bir cevap verdin!

Bir sonraki konuya geçelim mi yoksa başka bir sorum var mı?
-----------
Önemli: Bu örnek konu anlatımında kullanılan teknikleri göstermek amaçlı verildi. Aynı örnekleri kullanma.
ÖNEMLİ: Öğrenci rolü örnek olarak verildi. Sen sadece öğretmen rolünü uygulayacaksın. Öğrenci adına yanıt verme. Cevapları user verecek.

#Takip edilecek adımlar:
1.İlk olarak öğrenciyi selamlayacak ve dersin ana başlığını tanıtacaksın. Öğrenciye hazır olup olmadığını soracaksın.
2.Öğrencinin yanıtını bekleyeceksin. Hazırım derse, anlatıma başlayacaksın.
3.Konuyu tanımlayarak açıklayacak ve ardından konuyu pekiştirecek örnekler vereceksin.
4.Anlatımını tamamladıktan sonra, öğrenciye öğrendiklerini test etmek amacıyla bir soru soracak ve cevabını alacaksın.
5.Yanıtı doğru ya da yanlış olarak değerlendirdikten sonra, öğrenciye yapıcı ve teşvik edici bir geribildirimde bulunacaksın.
6.Bir başka soru sorarak öğrencinin konuya ne kadar hakim olduğunu ölçüp, konuyu tam anlamış olduğundan emin olacaksın. Konuyla ilgili en az iki soru sorulduğuna dikkat et.
7.Öğrencinin anladığını onayladıktan sonra, bir sonraki konuya geçeceksin. Eğer öğrenci anlamadığını belirtirse, konuyu daha ayrıntılı ve basitleştirerek anlatmaya devam edeceksin.
8.Bu adımlar ile dersin etkili, ilgi çekici ve Sokratik yöntemle işlenmesini sağlayacaksın.
"""
# OpenAI API istemcisini başlat
llm = ChatOpenAI(model="gpt-4o")

# Uygulama başlatıldığında sohbet geçmişini başlat
if "message_history" not in st.session_state:
    st.session_state["message_history"] = ChatMessageHistory()



def process_and_clear():
    user_input = st.session_state["user_input"]  # Mevcut kullanıcı girdisini al
    if user_input.strip():  # Girdi boş değilse işleme devam et
        # Kullanıcı mesajını hafızaya ekle
        user_message = HumanMessage(content=user_input)
        st.session_state["message_history"].add_message(user_message)

        # Sistem promptu ekle
        messages = [HumanMessage(content=system_prompt)] + st.session_state["message_history"].messages

        # LLM ile yanıt oluştur
        try:
            response = llm.invoke(messages)
        except Exception as e:
            st.error(f"Hata oluştu: {e}")
            return

        # AI yanıtını hafızaya ekle
        ai_response = AIMessage(content=response.content)
        st.session_state["message_history"].add_message(ai_response)

    else:
        st.warning("Lütfen mesajınızı yazın.")

    # Kullanıcı girdisini sıfırla
    st.session_state["user_input"] = ""

def apply_custom_styles():
    st.markdown("""
    <style>
    /* Öğrenci mesajları sağda */
    .user-message {
        text-align: right;
        background-color:rgba(0, 0, 0, 0.1);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Öğretmen mesajları solda */
    .teacher-message {
        text-align: left;
        background-color: rgba(0, 0, 0, 0.1);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
        margin-right: auto;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Text input ve butonları düzenle */
    .stTextInput > div > div > input {
        border-radius: 20px;
        width: 90%;
        margin-bottom: 20px;
    }
    .stButton > button {
        border-radius: 20px;
        font-size: 0.8em;
        width: 20%;
    }
    .stTextInput {
        position: fixed;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%);
    }
    .stButton {
        position: fixed;
        bottom: 80px;
        left: 80%;
        transform: translateX(-50%);
                
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_styles()

# Streamlit UI düzenlemeleri
st.title("Türkçe Anlam Olayları")
st.write("Merhaba, Türkçe Anlam Olayları konusuna çalışmaya hazır mısı?")

# Kullanıcı girişi ve sohbet geçmişini gösterme
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""  # Mesaj alanı başlangıçta boş

# Geçmiş mesajları göster
if st.session_state["message_history"].messages:
    for message in st.session_state["message_history"].messages:
        if isinstance(message, HumanMessage):
            st.markdown(f'<div class="user-message"><strong>Öğrenci:</strong> {message.content}</div>', unsafe_allow_html=True)
        elif isinstance(message, AIMessage):
            st.markdown(f'<div class="teacher-message"><strong>Öğretmen:</strong> {message.content}</div>', unsafe_allow_html=True)


# Mesajı gönderme butonu
user_input = st.text_input("Öğrenci: ", key="user_input")

if st.button("Mesajı Gönder", on_click=process_and_clear):
    pass