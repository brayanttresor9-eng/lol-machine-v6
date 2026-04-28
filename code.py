import streamlit as st
import stripe

stripe.api_key = st.secrets["STRIPE_KEY"]

st.set_page_config(page_title="LOL Machine V6 🍀", page_icon="🍀", layout="wide")

if 'user' not in st.session_state: st.session_state.user = None
if 'premium' not in st.session_state: st.session_state.premium = False

def creer_session_stripe():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{'price': 'price_1TQyhLDmScq27Uw61o6wMkiC', 'quantity': 1}],
            mode='subscription',
            success_url='https://brayanttresor9-eng-lol-machine-v6-code-cfngds.streamlit.app?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://brayanttresor9-eng-lol-machine-v6-code-cfngds.streamlit.app',
        )
        return checkout_session.url
    except Exception as e:
        st.error(f"Erreur Stripe: {e}")
        return None


st.set_page_config(page_title="LOL Machine V6 🍀", page_icon="🍀", layout="wide")

stripe.api_key ="st.secrets[STRIPE_KEY] "


if 'user' not in st.session_state: st.session_state.user = None
if 'premium' not in st.session_state: st.session_state.premium = False

def creer_session_stripe():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{'price': 'price_1TQyhLDmScq27Uw61o6wMkiC', 'quantity': 1}], # Remplace price_...
            mode='subscription',
            success_url='http://localhost:8501?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:8501',
        )
        return checkout_session.url
    except Exception as e:
        st.error(f"Erreur Stripe: {e}")
        return None

st.title("LOL Machine V6 🍀")

with st.sidebar:
    st.header("Compte")
    if st.session_state.user is None:
        pseudo = st.text_input("Pseudo")
        if st.button("Entrer"):
            st.session_state.user = pseudo
            st.rerun()
    else:
        st.success(f"Salut {st.session_state.user}")
        if st.session_state.premium:
            st.info("Status : 👑 PREMIUM")
        else:
            if st.button("👑 Passer Premium 1.99€/mois"):
                url = creer_session_stripe()
                if url: st.markdown(f'[Payer maintenant]({url})')

st.write("L'app tourne ! 🍀")
if st.button("RACONTE UNE BLAGUE"):
    st.success("Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon ils tombent dans le bateau 🤿")

# Check retour Stripe
if "session_id" in st.query_params:
    st.session_state.premium = True
    st.balloons()
    st.success("Paiement validé ! T'es Premium 👑")
