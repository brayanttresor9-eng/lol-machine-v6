import streamlit as st
import stripe
import random

# CONFIG STREAMLIT
st.set_page_config(page_title="LOL Machine V6 🍀", page_icon="🍀", layout="wide")

# INIT DES VARIABLES DE SESSION
if 'user' not in st.session_state:
    st.session_state.user = None
if 'premium' not in st.session_state:
    st.session_state.premium = False
if 'blagues_vues' not in st.session_state:
    st.session_state.blagues_vues = 0
if 'stripe_url' not in st.session_state:
    st.session_state.stripe_url = None
if 'afficher_premium' not in st.session_state:
    st.session_state.afficher_premium = False

# LISTE DES 50 BLAGUES
BLAGUES = [
    "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon ils tombent dans le bateau.",
    "Que dit un escargot quand il croise une limace ? Oh la belle décapotable !",
    "Pourquoi les canards ont-ils les pattes si larges ? Pour éteindre les feux de forêt.",
    "Comment appelle-t-on un chat tombé dans un pot de peinture le jour de Noël ? Un chat-mallow.",
    "Pourquoi les poissons détestent l'ordinateur ? À cause d'Internet.",
    "Quel est le comble pour un électricien ? De ne pas être au courant.",
    "Que dit un zéro à un huit ? T'as mis ta ceinture !",
    "Pourquoi les squelettes ne se battent jamais entre eux ? Ils n'ont pas les tripes.",
    "Comment fait-on pour allumer un barbecue breton ? On utilise des breizh.",
    "Quel est l'animal le plus connecté ? Le porc USB.",
    # Ajoute les 40 autres blagues ici
]

# FONCTION STRIPE
def creer_session_stripe():
    try:
        stripe.api_key = st.secrets["STRIPE_KEY"]
        session = stripe.checkout.Session.create(
            success_url="https://lol-machine-v6.streamlit.app/?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://lol-machine-v6.streamlit.app/",
            payment_method_types=["card"],
            line_items=[{
                "price": "price_1TQyizDMScq27Uw6FhbJv1pS",
                "quantity": 1,
            }],
            mode="subscription",
        )
        return session.url, None  # On renvoie l'URL + pas d'erreur
    except Exception as e:
        return None, str(e)  # On renvoie pas d'URL + l'erreur

# BOUTON PREMIUM - EN DEHORS DU BOUTON BLAGUE
if not st.session_state.premium and st.session_state.afficher_premium:
    if st.button("DEVENIR PREMIUM 👑", use_container_width=True):
        with st.spinner('Connexion à Stripe...'):
            url, erreur = creer_session_stripe()
            if erreur:
                st.session_state.erreur_stripe = erreur  # ON SAUVE L'ERREUR
            else:
                st.session_state.stripe_url = url
            st.rerun()

# AFFICHER L'ERREUR SI ELLE EXISTE
if st.session_state.get('erreur_stripe'):
    st.error(f"ERREUR STRIPE BLOQUÉE: {st.session_state.erreur_stripe}")
    if st.button("Effacer l'erreur"):
        del st.session_state.erreur_stripe
        st.rerun()

# BOUTON ROUGE STRIPE
if st.session_state.get('stripe_url'):
    st.link_button(
        "👉 PAYER 5$/MOIS SUR STRIPE",
        st.session_state.stripe_url,
        use_container_width=True,
        type="primary"
    )
    st.success("Clique le bouton rouge ci-dessus pour payer 👆")
    st.session_state.stripe_url = None

# FOOTER
st.divider()
st.caption("Fait avec ❤️ par BRAYANT | LOL Machine V6")

       
