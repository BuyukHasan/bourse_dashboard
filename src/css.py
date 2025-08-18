class Cssdash:
    """Class to manage CSS themes and styles"""
    
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
        "primary": "#001100",  # Very dark background
        "secondary": "#00ff00",  # Retro green
        "background": "#000800",  # Black
        "accent1": "#00cc00",
        "accent2": "#008800",
        "text": "#00ff00"  # Bright green text
        },
        "Crypto Fever": {
        "primary": "#0a0a2a",  # Very dark blue background
        "secondary": "#ff8c00",  # Fluorescent orange
        "background": "#000022",  # Night blue
        "accent1": "#00ffff",   # Cyan
        "accent2": "#ff00ff",   # Magenta
        "text": "#ffffff"       # White text
        }
    }

    @classmethod
    def get_css(cls, colors):
        """Generate CSS styles based on theme colors"""
        return f"""
        <style>
            /* Main background and containers */
            .stApp, .main, .block-container {{
                background-color: {colors['background']} !important;
                color: {colors['text']} !important;
            }}
        
            /* General text */
            p, div, h1, h2, h3, h4, h5, h6, span, label {{
                color: {colors['text']} !important;
            }}
        
            /* Inputs and selectors */
            .stTextInput>div>div>input, 
            .stNumberInput>div>div>input,
            .stSelectbox>div>div>select,
            .stTextArea>div>div>textarea {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border-color: {colors['secondary']} !important;
            }}
        
            /* Metrics and indicators */
            .stMetric {{
                border-left: 0.4rem solid {colors['secondary']};
                padding: 1rem;
                border-radius: 0.5rem;
                background-color: {colors['primary']};
                color: {colors['text']};
                box-shadow: 0 0 15px {colors['accent1']};
            }}
        
            /* Tabs */
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
        
            /* Header */
            .css-1vq4p4l {{
                padding: 2rem 1rem;
                background-color: {colors['primary']};
                color: {colors['text']};
                border-bottom: 2px solid {colors['accent1']};
            }}
        
            /* Alerts */
            .stAlert {{
                background-color: {colors['primary']};
                border: 1px solid {colors['secondary']};
                color: {colors['text']};
            }}
        
            /* Buttons */
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
        
            /* Plotly charts */
            .js-plotly-plot .plotly {{
                background-color: {colors['primary']} !important;
            }}
        
            /* Sidebar */
            [data-testid="stSidebar"] {{
                background-color: {colors['primary']} !important;
            }}
        
            /* Improved contrast for problematic themes */
            .stMarkdown strong, .stMarkdown b {{
                color: {colors['accent1']} !important;
            }}
            
            /* Loading screen */
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
            
            /* ===== ADDED CORRECTIONS FOR UI ELEMENTS ===== */
            /* Sidebar - Titles */
            .css-1vq4p4l h1, 
            .css-1vq4p4l h2, 
            .css-1vq4p4l h3, 
            .css-1vq4p4l h4, 
            .css-1vq4p4l h5, 
            .css-1vq4p4l h6 {{
                color: {colors['accent1']} !important;
            }}
            
            /* Sidebar - General text */
            .css-1vq4p4l, 
            .css-1vq4p4l p, 
            .css-1vq4p4l div, 
            .css-1vq4p4l span, 
            .css-1vq4p4l label {{
                color: {colors['text']} !important;
            }}
            
            /* Selectors (Selectbox) */
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
            
            /* Buttons */
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
            
            /* Alerts */
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
            
            /* Text area */
            .stTextArea > label {{
                color: {colors['text']} !important;
                font-weight: bold;
            }}
            
            .stTextArea > div > div > textarea {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['secondary']} !important;
            }}
            
            /* Progress bar */
            .stProgress > div > div > div {{
                background-color: {colors['accent1']} !important;
            }}
            
            /* Spinner */
            .stSpinner > div > div {{
                border-color: {colors['accent1']} !important;
                border-right-color: transparent !important;
            }}
            
            /* Placeholder text */
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
            
            /* Tooltip content */
            .stTooltip p {{
                color: {colors['text']} !important;
            }}
            
            /* Theme selector */
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
            
            /* ===== SPECIFIC CORRECTIONS FOR SELECTORS ===== */
            /* Target all selection widgets */
            div[data-baseweb="select"] > div:first-child {{
                background-color: {colors['primary']} !important;
                border-color: {colors['secondary']} !important;
                color: {colors['text']} !important;
            }}
            
            /* Text in selectors */
            div[data-baseweb="select"] div {{
                color: {colors['text']} !important;
            }}
            
            /* Selector icons */
            div[data-baseweb="select"] svg {{
                fill: {colors['accent1']} !important;
            }}
            
            /* Dropdown menu options */
            div[data-baseweb="popover"] div {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
            }}
            
            /* Hover options */
            div[data-baseweb="popover"] li:hover {{
                background-color: {colors['accent1']} !important;
                color: {colors['primary']} !important;
            }}
            
            /* Mode selector in sidebar */
            .stSidebar div[data-baseweb="select"] {{
                background-color: {colors['background']} !important;
            }}
            
            /* Multiselect - selected items */
            span[data-baseweb="tag"] {{
                background-color: {colors['accent1']} !important;
                color: {colors['primary']} !important;
            }}
            
            /* Date picker - calendar */
            .rdrMonth {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
            }}
            
            /* Date picker buttons */
            .rdrDayToday span:after {{
                background-color: {colors['accent1']} !important;
            }}
            
            /* Date inputs */
            input[data-baseweb="input"] {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border-color: {colors['secondary']} !important;
            }}
            
            /* Force text color in all widgets */
            .st-bb, .st-at, .st-ae, .st-af, .st-ag, .stSelectbox label, .stDateInput label, .stMultiSelect label {{
                color: {colors['text']} !important;
            }}
            
            /* Main sidebar container */
            [data-testid="stSidebar"] > div:first-child {{
                background-color: {colors['primary']} !important;
            }}
            
            /* ===== ADDED CORRECTIONS FOR RESISTANT ELEMENTS ===== */
            /* Start date & End date - reinforcement */
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

            /* Threshold (numeric input) - reinforcement */
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

            /* Add Alert button - reinforcement */
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

            /* Labels for resistant elements */
            div[data-testid="stDateInput"] label,
            div[data-testid="stNumberInput"] label,
            div[data-testid="stButton"] span {{
                color: {colors['text']} !important;
                font-weight: bold !important;
            }}

            /* ===== OVERLOAD FOR POPOVERS ===== */
            /* Date picker calendar */
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

            /* Selected days in calendar */
            .rdrDayToday .rdrDayNumber span:after {{
                background-color: {colors['accent1']} !important;
            }}

            .rdrSelected, .rdrInRange, .rdrStartEdge, .rdrEndEdge {{
                background-color: {colors['accent1']} !important;
            }}

            /* Calendar navigation buttons */
            .rdrNextButton i, .rdrPprevButton i {{
                border-color: {colors['accent1']} !important;
            }}

            /* ===== ADDITIONAL CORRECTIONS FOR WIDGETS ===== */
            /* Widget containers */
            [data-testid="stForm"] {{
                border: 1px solid {colors['secondary']} !important;
                border-radius: 8px !important;
                padding: 12px !important;
                margin-bottom: 15px !important;
            }}

            /* Final correction for recalcitrant texts */
            .stRadio label, .stSelectbox label, .stDateInput label, 
            .stNumberInput label, .stButton label, .stTextInput label {{
                color: {colors['text']} !important;
                font-weight: bold !important;
            }}

            /* Correction of icons in inputs */
            input ~ div > div > svg {{
                fill: {colors['accent1']} !important;
            }}
            
            /* ===== NUCLEAR SOLUTION ===== */
            /* Apply style to ALL children of stApp */
            .stApp * {{
                color: {colors['text']} !important;
                font-family: inherit !important;
            }}

            /* Force style on all inputs */
            input, select, textarea, button {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
                border: 1px solid {colors['secondary']} !important;
                border-radius: 4px !important;
                padding: 8px 12px !important;
            }}

            /* Specific style for buttons */
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

            /* Style for labels */
            label {{
                color: {colors['text']} !important;
                font-weight: bold !important;
                margin-bottom: 4px !important;
                display: block !important;
            }}

            /* Calendar - radical solution */
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

            /* Icons - force everything */
            svg {{
                fill: {colors['accent1']} !important;
                stroke: {colors['accent1']} !important;
            }}

            /* Containers - force everything */
            div[data-baseweb] {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
            }}

            /* Overlay for popups */
            [data-baseweb="popover"] {{
                background-color: {colors['primary']} !important;
                border: 2px solid {colors['secondary']} !important;
                box-shadow: 0 0 15px {colors['accent1']} !important;
            }}

            /* List items */
            li {{
                background-color: {colors['primary']} !important;
                color: {colors['text']} !important;
            }}

            li:hover {{
                background-color: {colors['accent1']} !important;
                color: {colors['primary']} !important;
            }}

            /* Final solution for placeholders */
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
                background: #8b0000; /* Dark red */
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
                background: #ff4500; /* Reddish orange */
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

        /* Keep existing spin animation but modify slightly */
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

            /* Dynamic block generation */
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
        .stDataFrame th, .stDataFrame td {{
            background-color: {colors['primary']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['secondary']} !important;
        }}

        .stDataFrame tr:hover {{
            background-color: {colors['accent1']} !important;
            color: {colors['primary']} !important;
        }}

        @keyframes floatBlock {{
            0% {{ transform: translateY(-100px) rotate(0deg); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateY(100vh) rotate(360deg); opacity: 0; }}
        }}
        </style>
        """