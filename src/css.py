class Cssdash:
    themes = {
        "Corporate Bonds": {
        "primary": "#002b36",
        "secondary": "#268bd2",
        "background": "#001f27",
        "accent1": "#2aa198",
        "accent2": "#b58900",
        "text": "#fdf6e3"
        },
        "Neon Cyberpunk": {
            "primary": "#0f0c29",
            "secondary": "#ff00ff",
            "background": "#100e1d",
            "accent1": "#00ffff",
            "accent2": "#ff00ff",
            "text": "#e0e0ff"
        },
        "Lava Explosion": {
            "primary": "#2a0000",
            "secondary": "#ff3c00",
            "background": "#1a0000",
            "accent1": "#ff7b00",
            "accent2": "#ff0000",
            "text": "#ffd9d9"
        },
        "Electric Ocean": {
            "primary": "#001f3f",
            "secondary": "#00ffff",
            "background": "#001a33",
            "accent1": "#0074D9",
            "accent2": "#7FDBFF",
            "text": "#aaffff"
        },
        "Acid Jungle": {
            "primary": "#001100",
            "secondary": "#00cc00",
            "background": "#000800",
            "accent1": "#00aa00",
            "accent2": "#008800",
            "text": "#e0ffe0"
        },
        "Galactic Purple": {
            "primary": "#0d000d",
            "secondary": "#cc00ff",
            "background": "#080008",
            "accent1": "#9900ff",
            "accent2": "#ff00cc",
            "text": "#f0e0ff"
        },
        "Retro Dark": {
        "primary": "#001100",  # Fond très sombre
        "secondary": "#00ff00",  # Vert rétro
        "background": "#000800",  # Noir
        "accent1": "#00cc00",
        "accent2": "#008800",
        "text": "#00ff00"  # Texte vert vif
        },
        "Crypto Fever": {
        "primary": "#0a0a2a",  # Fond bleu très foncé
        "secondary": "#ff8c00",  # Orange fluo
        "background": "#000022",  # Bleu nuit
        "accent1": "#00ffff",   # Cyan
        "accent2": "#ff00ff",   # Magenta
        "text": "#ffffff"       # Texte blanc
        }
    }

    @classmethod
    def get_css(cls, colors):
        return f"""
        <style>
            /* Fond principal et conteneurs */
            .stApp, .main, .block-container {{
                background-color: {colors['background']} !important;
                color: {colors['text']} !important;
            }}
        
            /* Texte général */
            p, div, h1, h2, h3, h4, h5, h6, span, label {{
                color: {colors['text']} !important;
            }}
        
            /* Inputs et sélecteurs */
            .stTextInput>div>div>input, 
            .stNumberInput>div>div>input,
            .stSelectbox>div>div>select,
            .stTextArea>div>div>textarea {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border-color: {colors['secondary']} !important;
            }}
        
            /* Métriques et indicateurs */
            .stMetric {{
                border-left: 0.4rem solid {colors['secondary']};
                padding: 1rem;
                border-radius: 0.5rem;
                background-color: {colors['primary']};
                color: {colors['text']};
                box-shadow: 0 0 15px {colors['accent1']};
            }}
        
            /* Onglets */
            .stTabs {{
                margin-bottom: 1rem;
            }}
            
            .stTabs [role="tablist"] {{
                gap: 0.5rem;
                padding: 0.25rem;
                background: transparent;
            }}
            
            .stTabs button[role="tab"] {{
                all: unset;
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border-radius: 0.5rem 0.5rem 0 0 !important;
                border: 1px solid {colors['secondary']} !important;
                padding: 0.5rem 1.5rem !important;
                transition: all 0.3s ease !important;
                font-weight: normal !important;
                margin: 0 !important;
                cursor: pointer;
                position: relative;
                overflow: hidden;
            }}
            
            .stTabs button[role="tab"]:not([aria-selected="true"]):hover {{
                background-color: {colors['accent1']} !important;
                color: {colors['primary']} !important;
                transform: translateY(-2px);
            }}
            
            .stTabs button[aria-selected="true"] {{
                background-color: {colors['secondary']} !important;
                color: {colors['primary']} !important;
                font-weight: bold !important;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
                border-bottom: 3px solid {colors['accent1']} !important;
            }}
            
            .stTabs button[aria-selected="true"]::after {{
                content: '';
                position: absolute;
                bottom: -1px;
                left: 0;
                width: 100%;
                height: 3px;
                background: {colors['accent1']};
                animation: tabUnderline 0.3s ease-out;
            }}
            
            .stTabs [role="tabpanel"] {{
                padding: 1.5rem !important;
                background: {colors['primary']} !important;
                border-radius: 0 0.5rem 0.5rem 0.5rem !important;
                border: 1px solid {colors['secondary']} !important;
                margin-top: -1px !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
            }}
            
            @keyframes tabUnderline {{
                from {{ transform: scaleX(0); }}
                to {{ transform: scaleX(1); }}
            }}
        
            /* En-tête */
            .css-1vq4p4l {{
                padding: 2rem 1rem;
                background-color: {colors['primary']};
                color: {colors['text']};
                border-bottom: 2px solid {colors['accent1']};
            }}
        
            /* Alertes */
            .stAlert {{
                background-color: {colors['primary']};
                border: 1px solid {colors['secondary']};
                color: {colors['text']};
            }}
        
            /* Boutons */
            .stButton>button {{
                background-color: {colors['primary']};
                color: {colors['text']};
                border: 1px solid {colors['secondary']};
                border-radius: 0.5rem;
                transition: all 0.3s;
            }}
            .stButton>button:hover {{
                background-color: {colors['secondary']};
                color: {colors['primary']};
                box-shadow: 0 0 15px {colors['accent2']};
            }}
        
            /* DataFrames */
            .stDataFrame {{
                border: 1px solid {colors['secondary']};
                border-radius: 0.5rem;
                background-color: {colors['primary']} !important;
            }}
        
            /* Graphiques Plotly */
            .js-plotly-plot .plotly {{
                background-color: {colors['primary']} !important;
            }}
        
            /* Barre latérale */
            [data-testid="stSidebar"] {{
                background-color: {colors['primary']} !important;
            }}
        
            /* Contraste amélioré pour les thèmes problématiques */
            .stMarkdown strong, .stMarkdown b {{
                color: {colors['accent1']} !important;
            }}
            
            /* Écran de chargement */
            .loading-screen {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: {colors['background']};
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 9999;
                opacity: 1;
                transition: opacity 0.5s ease;
            }}
            
            .loading-content {{
                text-align: center;
                max-width: 400px;
                padding: 2rem;
                border-radius: 15px;
                background: rgba(15, 12, 41, 0.85);
                box-shadow: 0 0 30px {colors['accent1']}, 
                            0 0 50px rgba(0, 255, 255, 0.3);
            }}
            .loading-logo {{
            width: 180px;
            height: 180px;
            position: relative;
            margin: 0 auto 20px;
            }}
            
            .logo-circle:nth-child(2) {{
                border-top-color: {colors['accent2']};
                animation-delay: -0.5s;
                width: 160px;
                height: 160px;
                top: 10px;
                left: 10px;
            }}
            
            
            .loading-text {{
                color: {colors['accent1']};
                font-size: 1.6rem;
                margin-top: 10px;
                font-family: 'Arial', sans-serif;
                text-transform: uppercase;
                letter-spacing: 3px;
                text-shadow: 0 0 8px rgba(0, 255, 255, 0.7);
                animation: glow 2s infinite alternate;
            }}
            
            .loading-subtext {{
                color: {colors['text']};
                font-size: 1rem;
                margin-top: 15px;
                opacity: 0.8;
            }}
            
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            
            @keyframes pulse {{
                0% {{ transform: scale(0.95); opacity: 0.9; }}
                50% {{ transform: scale(1.05); opacity: 1; }}
                100% {{ transform: scale(0.95); opacity: 0.9; }}
            }}
            
            @keyframes glow {{
                0% {{ text-shadow: 0 0 5px {colors['accent1']}; opacity: 0.8; }}
                100% {{ text-shadow: 0 0 20px {colors['accent1']}, 0 0 30px {colors['accent1']}; opacity: 1; }}
            }}
            
            @keyframes text-pulse {{
                0% {{ opacity: 0.7; transform: translate(-50%, -50%) scale(0.95); }}
                100% {{ opacity: 1; transform: translate(-50%, -50%) scale(1.05); }}
            }}
            
            /* ===== CORRECTIONS AJOUTÉES POUR LES ÉLÉMENTS D'INTERFACE ===== */
            /* Barre latérale - Titres */
            .css-1vq4p4l h1, 
            .css-1vq4p4l h2, 
            .css-1vq4p4l h3, 
            .css-1vq4p4l h4, 
            .css-1vq4p4l h5, 
            .css-1vq4p4l h6 {{
                color: {colors['accent1']} !important;
            }}
            
            /* Barre latérale - Texte général */
            .css-1vq4p4l, 
            .css-1vq4p4l p, 
            .css-1vq4p4l div, 
            .css-1vq4p4l span, 
            .css-1vq4p4l label {{
                color: {colors['text']} !important;
            }}
            
            /* Sélecteurs (Selectbox) */
            .stSelectbox > label {{
                color: {colors['text']} !important;
                font-weight: bold;
            }}
            
            .stSelectbox > div > div > select {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['secondary']} !important;
            }}
            
            .stSelectbox > div > div > div > svg {{
                fill: {colors['accent1']} !important;
            }}
            
            /* Date pickers */
            .stDateInput > label {{
                color: {colors['text']} !important;
                font-weight: bold;
            }}
            
            .stDateInput > div > div > input {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['secondary']} !important;
            }}
            
            .stDateInput > div > div > button {{
                color: {colors['accent1']} !important;
            }}
            
            /* Multiselect */
            .stMultiSelect > label {{
                color: {colors['text']} !important;
                font-weight: bold;
            }}
            
            .stMultiSelect > div > div > div {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['secondary']} !important;
            }}
            
            .stMultiSelect span[data-baseweb="tag"] {{
                background-color: {colors['accent1']} !important;
                color: {colors['primary']} !important;
            }}
            
            /* Boutons */
            .stButton > button {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['secondary']} !important;
                font-weight: bold;
            }}
            
            .stButton > button:hover {{
                background-color: {colors['secondary']} !important;
                color: {colors['primary']} !important;
                box-shadow: 0 0 15px {colors['accent2']} !important;
            }}
            
            /* Alertes */
            .stAlert {{
                background-color: {colors['primary']} !important;
                border: 1px solid {colors['secondary']} !important;
            }}
            
            .stAlert h3 {{
                color: {colors['accent1']} !important;
            }}
            
            .stAlert p {{
                color: {colors['text']} !important;
            }}
            
            /* Zone de texte */
            .stTextArea > label {{
                color: {colors['text']} !important;
                font-weight: bold;
            }}
            
            .stTextArea > div > div > textarea {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['secondary']} !important;
            }}
            
            /* Barre de progression */
            .stProgress > div > div > div {{
                background-color: {colors['accent1']} !important;
            }}
            
            /* Spinner */
            .stSpinner > div > div {{
                border-color: {colors['accent1']} !important;
                border-right-color: transparent !important;
            }}
            
            /* Placeholder texte */
            ::placeholder {{
                color: {colors['accent2']} !important;
                opacity: 0.7 !important;
            }}
            
            /* Tooltips */
            .stTooltip {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['secondary']} !important;
            }}
            
            /* Contenu des tooltips */
            .stTooltip p {{
                color: {colors['text']} !important;
            }}
            
            /* Sélecteur de thème */
            .stRadio > label {{
                color: {colors['text']} !important;
                font-weight: bold;
            }}
            
            .stRadio [role="radiogroup"] {{
                background-color: {colors['primary']} !important;
                border: 1px solid {colors['secondary']} !important;
                padding: 10px;
                border-radius: 8px;
            }}
            
            .stRadio [role="radio"] {{
                color: {colors['text']} !important;
            }}
            
            .stRadio [role="radio"][aria-checked="true"] {{
                background-color: {colors['accent1']} !important;
                color: {colors['primary']} !important;
                font-weight: bold;
            }}
            
            /* ===== CORRECTIONS SPÉCIFIQUES POUR LES SÉLECTEURS ===== */
            /* Cible tous les widgets de sélection */
            div[data-baseweb="select"] > div:first-child {{
                background-color: {colors['primary']} !important;
                border-color: {colors['secondary']} !important;
                color: {colors['text']} !important;
            }}
            
            /* Texte dans les sélecteurs */
            div[data-baseweb="select"] div {{
                color: {colors['text']} !important;
            }}
            
            /* Icônes des sélecteurs */
            div[data-baseweb="select"] svg {{
                fill: {colors['accent1']} !important;
            }}
            
            /* Options du menu déroulant */
            div[data-baseweb="popover"] div {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
            }}
            
            /* Options au survol */
            div[data-baseweb="popover"] li:hover {{
                background-color: {colors['accent1']} !important;
                color: {colors['primary']} !important;
            }}
            
            /* Sélecteur de mode dans la sidebar */
            .stSidebar div[data-baseweb="select"] {{
                background-color: {colors['background']} !important;
            }}
            
            /* Multiselect - éléments sélectionnés */
            span[data-baseweb="tag"] {{
                background-color: {colors['accent1']} !important;
                color: {colors['primary']} !important;
            }}
            
            /* Date picker - calendrier */
            .rdrMonth {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
            }}
            
            /* Boutons du date picker */
            .rdrDayToday span:after {{
                background-color: {colors['accent1']} !important;
            }}
            
            /* Inputs de date */
            input[data-baseweb="input"] {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border-color: {colors['secondary']} !important;
            }}
            
            /* Forcer la couleur du texte dans tous les widgets */
            .st-bb, .st-at, .st-ae, .st-af, .st-ag, .stSelectbox label, .stDateInput label, .stMultiSelect label {{
                color: {colors['text']} !important;
            }}
            
            /* Conteneur principal de la sidebar */
            [data-testid="stSidebar"] > div:first-child {{
                background-color: {colors['primary']} !important;
            }}
            
            /* ===== CORRECTIONS AJOUTÉES POUR LES ÉLÉMENTS RÉSISTANTS ===== */
            /* Start date & End date - renforcement */
            div[data-testid="stDateInput"] > div > div > input {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['secondary']} !important;
            }}

            div[data-testid="stDateInput"] > div > div > button {{
                background-color: {colors['primary']} !important;
                color: {colors['accent1']} !important;
            }}

            div[data-testid="stDateInput"] svg {{
                fill: {colors['accent1']} !important;
            }}

            /* Threshold (input numérique) - renforcement */
            div[data-testid="stNumberInput"] > div > div > input {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['secondary']} !important;
            }}

            div[data-testid="stNumberInput"] > div > div > button {{
                background-color: {colors['primary']} !important;
                color: {colors['accent1']} !important;
            }}

            div[data-testid="stNumberInput"] svg {{
                fill: {colors['accent1']} !important;
            }}

            /* Bouton Add Alert - renforcement */
            div[data-testid="stButton"] > button {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['secondary']} !important;
                font-weight: bold !important;
            }}

            div[data-testid="stButton"] > button:hover {{
                background-color: {colors['secondary']} !important;
                color: {colors['primary']} !important;
                box-shadow: 0 0 15px {colors['accent2']} !important;
            }}

            /* Labels des éléments résistants */
            div[data-testid="stDateInput"] label,
            div[data-testid="stNumberInput"] label,
            div[data-testid="stButton"] span {{
                color: {colors['text']} !important;
                font-weight: bold !important;
            }}

            /* ===== SURCHARGE POUR LES POPOVERS ===== */
            /* Calendrier des date pickers */
            div[data-baseweb="popover"] {{
                background-color: {colors['primary']} !important;
                border: 1px solid {colors['secondary']} !important;
            }}

            div[data-baseweb="popover"] li {{
                color: {colors['text']} !important;
            }}

            div[data-baseweb="popover"] li:hover {{
                background-color: {colors['accent1']} !important;
                color: {colors['primary']} !important;
            }}

            /* Jours sélectionnés dans le calendrier */
            .rdrDayToday .rdrDayNumber span:after {{
                background-color: {colors['accent1']} !important;
            }}

            .rdrSelected, .rdrInRange, .rdrStartEdge, .rdrEndEdge {{
                background-color: {colors['accent1']} !important;
            }}

            /* Boutons de navigation calendrier */
            .rdrNextButton i, .rdrPprevButton i {{
                border-color: {colors['accent1']} !important;
            }}

            /* ===== CORRECTIONS SUPPLÉMENTAIRES POUR LES WIDGETS ===== */
            /* Conteneurs des widgets */
            [data-testid="stForm"] {{
                border: 1px solid {colors['secondary']} !important;
                border-radius: 8px !important;
                padding: 12px !important;
                margin-bottom: 15px !important;
            }}

            /* Correction finale des textes récalcitrants */
            .stRadio label, .stSelectbox label, .stDateInput label, 
            .stNumberInput label, .stButton label, .stTextInput label {{
                color: {colors['text']} !important;
                font-weight: bold !important;
            }}

            /* Correction des icônes dans les inputs */
            input ~ div > div > svg {{
                fill: {colors['accent1']} !important;
            }}
            
            /* ===== SOLUTION NUCLÉAIRE ===== */
            /* Applique le style à TOUS les éléments enfants de stApp */
            .stApp * {{
                color: {colors['text']} !important;
                font-family: inherit !important;
            }}

            /* Force le style sur tous les inputs */
            input, select, textarea, button {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['secondary']} !important;
                border-radius: 4px !important;
                padding: 8px 12px !important;
            }}

            /* Style spécifique pour les boutons */
            button {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['secondary']} !important;
                font-weight: bold !important;
                transition: all 0.3s !important;
            }}

            button:hover {{
                background-color: {colors['secondary']} !important;
                color: {colors['primary']} !important;
                box-shadow: 0 0 10px {colors['accent2']} !important;
            }}

            /* Style pour les labels */
            label {{
                color: {colors['text']} !important;
                font-weight: bold !important;
                margin-bottom: 4px !important;
                display: block !important;
            }}

            /* Calendrier - solution radicale */
            .rdr-Month, 
            .rdr-Days, 
            .rdr-WeekDays {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
            }}

            .rdr-Day {{
                color: {colors['text']} !important;
            }}

            .rdr-Day:hover {{
                background-color: {colors['accent1']} !important;
                color: {colors['primary']} !important;
            }}

            .rdr-Day:active, 
            .rdr-Day:focus {{
                background-color: {colors['secondary']} !important;
                color: {colors['primary']} !important;
            }}

            /* Icônes - tout forcer */
            svg {{
                fill: {colors['accent1']} !important;
                stroke: {colors['accent1']} !important;
            }}

            /* Conteneurs - tout forcer */
            div[data-baseweb] {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
            }}

            /* Overlay pour les popups */
            [data-baseweb="popover"] {{
                background-color: {colors['primary']} !important;
                border: 2px solid {colors['secondary']} !important;
                box-shadow: 0 0 15px {colors['accent1']} !important;
            }}

            /* Éléments de liste */
            li {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
            }}

            li:hover {{
                background-color: {colors['accent1']} !important;
                color: {colors['primary']} !important;
            }}

            /* Solution finale pour les placeholders */
            ::placeholder {{
                color: {colors['accent2']} !important;
                opacity: 0.7 !important;
            }}
        .triangle {{
                width: 180px;
                height: 180px;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                animation: spin 1s linear infinite, pulse-danger 0.8s infinite alternate;
                z-index: 1;
                background: 
                    linear-gradient(45deg, 
                        #ff0000 25%, 
                        #000000 25%, 
                        #000000 50%, 
                        #ff0000 50%, 
                        #ff0000 75%, 
                        #000000 75%);
                background-size: 20px 20px;
                clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
            }}

        .eye {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 40px;
                height: 40px;
                background: #8b0000; /* Rouge foncé */
                border-radius: 50%;
                box-shadow: 
                    0 0 0 5px #ff0000,
                    0 0 20px #ff0000;
                animation: blink 0.8s infinite, glow-red 0.5s infinite alternate;
                z-index: 2;
                overflow: hidden;
            }}

        .eye::before {{
                content: '';
                position: absolute;
                top: 8px;
                right: 8px;
                width: 12px;
                height: 12px;
                background: #ff4500; /* Orange rougeâtre */
                border-radius: 50%;
                box-shadow: 0 0 10px #ff4500;
            }}
        @keyframes pulse-danger {{
                0% {{ opacity: 0.8; transform: translate(-50%, -50%) scale(1); }}
                100% {{ opacity: 1; transform: translate(-50%, -50%) scale(1.1); box-shadow: 0 0 30px #ff0000; }}
            }}
        @keyframes glow-red {{
                0% {{ box-shadow: 0 0 0 5px #ff0000, 0 0 20px #ff0000; }}
                100% {{ box-shadow: 0 0 0 10px #ff0000, 0 0 40px #ff0000; }}
            }}
        
        @keyframes blink {{
                0%, 45%, 55%, 100% {{ height: 40px; }}
                50% {{ height: 5px; }}
            }}

        /* Conserver l'animation spin existante mais la modifier légèrement */
        @keyframes spin {{
                0% {{ transform: translate(-50%, -50%) rotate(0deg); }}
                100% {{ transform: translate(-50%, -50%) rotate(360deg); }}
            }}
         @keyframes floatBlock {{
                0% {{ transform: translateY(-100px) rotate(0deg); opacity: 0; }}
                10% {{ opacity: 1; }}
                90% {{ opacity: 1; }}
                100% {{ transform: translateY(100vh) rotate(360deg); opacity: 0; }}
        }}

        .block-animation {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: -1;
            }}

        .block {{
                position: absolute;
                width: 20px;
                height: 20px;
                background: linear-gradient(45deg, {colors['accent2']}, {colors['accent1']});
                border-radius: 4px;
                animation: floatBlock 15s linear infinite;
                opacity: 0;
            }}

            /* Génération dynamique des blocs */
            .block:nth-child(1) {{ left: 5%; animation-delay: 0s; }}
            .block:nth-child(2) {{ left: 15%; animation-delay: 2s; }}
            .block:nth-child(3) {{ left: 25%; animation-delay: 4s; }}
            .block:nth-child(4) {{ left: 35%; animation-delay: 6s; }}
            .block:nth-child(5) {{ left: 45%; animation-delay: 8s; }}
            .block:nth-child(6) {{ left: 55%; animation-delay: 10s; }}
            .block:nth-child(7) {{ left: 65%; animation-delay: 12s; }}
            .block:nth-child(8) {{ left: 75%; animation-delay: 14s; }}
            .block:nth-child(9) {{ left: 85%; animation-delay: 16s; }}
            .block:nth-child(10) {{ left: 95%; animation-delay: 18s; }}

        </style>
        """