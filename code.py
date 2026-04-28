import streamlit as st
import stripe
import random

# CONFIG STREAMLIT
st.set_page_config(page_title="LOL Machine V6 🍀", page_icon="🍀", layout="wide")

# CLÉ STRIPE DEPUIS LES SECRETS
stripe.api_key = st.secrets["STRIPE_KEY"]

# INIT DES VARIABLES DE SESSION
if 'user' not in st.session_state: 
    st.session_state.user = None
if 'premium' not in st.session_state: 
    st.session_state.premium = False
if 'blagues_vues' not in st.session_state: 
    st.session_state.blagues_vues = 0

# LISTE DES 50 BLAGUES
BLAGUES = [
    "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon ils tombent dans le bateau.",
    "Que dit un escargot quand il croise une limace ? Oh la belle décapotable !",
    "Comment appelle-t-on un chat tombé dans un pot de peinture le jour de Noël ? Un chat-mallow.",
    "Pourquoi les squelettes ne se battent jamais entre eux ? Ils n'ont pas le cran.",
    "Que fait une fraise sur un cheval ? Tagada tagada.",
    "C'est l'histoire d'un pingouin qui respire par les fesses. Un jour il s'assoit et il meurt.",
    "Pourquoi les poissons n'aiment pas jouer au tennis ? À cause du filet.",
    "Comment on appelle un boomerang qui ne revient pas ? Un bâton.",
    "Que dit un citron policier ? Plus un zeste.",
    "Pourquoi les livres ont-ils toujours chaud ? Parce qu'ils ont une couverture.",
    "Quel est le comble pour un électricien ? Ne pas être au courant.",
    "Pourquoi les vaches ferment-elles les yeux pendant la traite ? Pour faire du lait concentré.",
    "Qu'est-ce qui est jaune et qui attend ? Jonathan.",
    "Comment fait-on aboyer un chat ? On lui donne une tasse de lait et il lappe.",
    "Que dit une imprimante dans l'eau ? J'ai papier !",
    "Pourquoi Napoléon n'achetait jamais de maison ? Il avait déjà Bonaparte.",
    "Quel est le sport préféré des insectes ? Le cri-cri-quet.",
    "Pourquoi les canards sont toujours à l'heure ? Parce qu'ils sont dans l'étang.",
    "C'est quoi un petit pois avec une épée ? Un escrimeau.",
    "Comment appelle-t-on un alligator qui enquête ? Un investicat-gator.",
    "Pourquoi les moutons n'utilisent pas de shampoing ? Parce qu'ils ont la laine qui frise.",
    "Quel est le café préféré des informaticiens ? Le Java.",
    "Pourquoi les girafes n'existent pas ? C'est un cou monté.",
    "Qu'est-ce qu'une manifestation d'aveugles ? Un festival de cannes.",
    "Comment savoir qu'on est vieux ? Quand on te dit que t'es jeune.",
    "Pourquoi les fantômes sont de mauvais menteurs ? Parce qu'on voit à travers eux.",
    "Quel est le pays le plus chaud ? Le Chili.",
    "Que dit un fantôme quand il entre dans une pièce ? Salut, je suis transparent.",
    "Pourquoi les grenouilles sont-elles toujours à l'heure ? Elles mangent des vers.",
    "C'est l'histoire d'une chaise. Elle raconte une blague mais elle est pliante.",
    "Comment appelle-t-on un chien sans pattes ? On ne l'appelle pas, on va le chercher.",
    "Pourquoi les coqs n'ont pas de mains ? Parce que les poules ont pas de seins.",
    "Que fait un rat dans une échelle ? Il rat-compte les barreaux.",
    "Pourquoi le Père Noël n'a pas d'enfants ? Il ne vient qu'une fois par an.",
    "Quel est l'animal le plus connecté ? Le porc USB.",
    "Pourquoi les bananes utilisent de la crème solaire ? Parce qu'elles pèlent.",
    "Comment appelle-t-on un dinosaure qui ne s'arrête jamais de parler ? Un bla-bla-saurus.",
    "Pourquoi les abeilles vont chez le coiffeur ? Pour avoir une coupe au carré.",
    "Que dit un vampire à son psy ? J'ai des envies de meurtres.",
    "Pourquoi les toilettes belges ont 3 portes ? Grande, moyenne, et WC.",
    "C'est quoi le comble pour un jardinier ? Raconter des salades.",
    "Pourquoi les sumos se rasent les jambes ? Pour pas qu'on les prenne pour des féministes.",
    "Quel est le pain préféré du magicien ? La baguette.",
    "Pourquoi les frites ne croient pas en Dieu ? Parce qu'elles sont au ketchup.",
    "Comment appelle-t-on un rat qui fait de la magie ? Un rat-dini.",
    "Pourquoi les facteurs n'aiment pas l'hiver ? À cause des gelées matinales.",
    "Que dit un mur à un autre mur ? On se voit au coin.",
    "Pourquoi les sorcières volent sur un balai ? Parce que les aspirateurs sont trop lourds.",
    "C'est quoi une chorale d'enfants en hiver ? Un choeur de grelots.",
    "Pourquoi tu mets ton réveil à côté du café ? Pour me réveiller avec un expresso."
]

# FONCTION STRIPE CHECKOUT
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

# VÉRIFIE SI LE PAIEMENT EST VALIDÉ AU RETOUR DE STRIPE
query_params = st.query_params
if "session_id" in query_params:
    st.session_state.premium = True
    st.balloons()
    st.success("Paiement validé ! T'es Premium 👑")

# INTERFACE
st.title("LOL Machine V6 🍀")
st.caption("La machine à blagues qui vaut 5$/mois")

col1, col2 = st.columns(2)
with col1:
    st.metric("Statut", "👑 Premium" if st.session_state.premium else "Gratuit")
with col2:
    st.metric("Blagues lues", st.session_state.blagues_vues)

st.divider()
# BOUTON PRINCIPAL
if st.button("RACONTE UNE BLAGUE 🍀", use_container_width=True, type="primary"):
    if st.session_state.premium:
        st.success(random.choice(BLAGUES))
        st.session_state.blagues_vues += 1
    else:
        st.error("❌ Réservé aux membres Premium !")
        st.info("Débloque 50 blagues illimitées pour seulement 5$/mois")
        if st.button("DEVENIR PREMIUM 👑", use_container_width=True):
            url = creer_session_stripe()
            if url:
                st.link_button("👉 PAYER 5$/MOIS SUR STRIPE", url, use_container_width=True)
            else:
                st.error("Erreur Stripe. Vérifie ta clé dans Secrets.")

# FOOTER
st.divider()
st.caption("Fait avec ❤️ par BRAYANT | LOL Machine V6")

st.caption("Fait avec ❤️ par BRAYANT | LOL Machine V6")
       
