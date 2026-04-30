import streamlit as st
import stripe
import random

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
]

def creer_session_stripe():
    try:
        stripe.api_key = st.secrets["STRIPE_KEY"]
        session = stripe.checkout.Session.create(
            success_url="https://brayanttresor9-eng-lol-machine-v6-code-cfngds.streamlit.app/?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://brayanttresor9-eng-lol-machine-v6-code-cfngds.streamlit.app/",
            payment_method_types=["card"],
            line_items=[{
                "price": "price_1TQyhLDmScq27Uw61o6wMkiC",
                "quantity": 1,
            }],
            mode="subscription",
        )
        return session.url, None
    except Exception as e:
        return None, str(e)

# VERIFICATION PAIEMENT AU RETOUR DE STRIPE
query_params = st.query_params
if "session_id" in query_params and not st.session_state.premium:
    try:
        stripe.api_key = st.secrets["STRIPE_KEY"]
        session = stripe.checkout.Session.retrieve(query_params["session_id"])
        if session.payment_status == "paid":
            st.session_state.premium = True
            st.balloons()
            st.success("🎉 Paiement réussi ! Tu es maintenant Premium !")
    except Exception as e:
        st.error(f"Erreur de vérification: {e}")

# UI DE L'APP
st.title("LOL Machine V6 🍀")
st.caption("La machine à blagues qui vaut 5$/mois")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Statut")
    if st.session_state.premium:
        st.success("Premium 👑")
    else:
        st.warning("Gratuit")
with col2:
    st.subheader("Blagues lues")
    st.metric(label="Total", value=st.session_state.blagues_vues)

st.divider()

# BOUTON PRINCIPAL BLAGUE
if st.button("RACONTE UNE BLAGUE 🍀", use_container_width=True, type="primary"):
    if st.session_state.premium:
        st.success(random.choice(BLAGUES))
        st.session_state.blagues_vues += 1
        st.session_state.afficher_premium = False
    else:
        st.error("❌ Réservé aux membres Premium !")
        st.info("Débloque 50 blagues illimitées pour seulement 5$/mois")
        st.session_state.afficher_premium = True

# BOUTON PREMIUM
if not st.session_state.premium and st.session_state.afficher_premium:
    if st.button("DEVENIR PREMIUM 👑", use_container_width=True):
        with st.spinner('Connexion à Stripe...'):
            url, erreur = creer_session_stripe()
            if erreur:
                st.session_state.erreur_stripe = erreur
            else:
                st.session_state.stripe_url = url
            st.rerun()

# AFFICHER L'ERREUR SI ELLE EXISTE
if st.session_state.get('erreur_stripe'):
    st.error(f"ERREUR STRIPE: {st.session_state.erreur_stripe}")
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

st.divider()
st.caption("Fait avec ❤️ par BRAYANT | LOL Machine V6")
