import streamlit as st
from src.technical_analyzer import TechnicalAnalyzer
from datetime import datetime
from src.data_fetcher import DataFetcher
from src.visualizer import Visualizer
from src.news_fetcher import NewsFetcher
from src.reddit_analyzer import RedditSentiment
from src.geo_data import GeoDataFetcher
import plotly.express as px
import pandas as pd
import threading
from concurrent.futures import ThreadPoolExecutor

class Dashboard:
    def __init__(self, data_frame):
        # Définir les catégories d'actifs étendues
        self.asset_categories = {
        "Technologie": [
            "AAPL", "MSFT", "GOOGL", "META", "NVDA", "TSLA", "ADBE", "INTC", "CSCO", 
            "ORCL", "IBM", "QCOM", "TXN", "AVGO", "AMD", "CRM", "ADP", "INTU", "NOW", 
            "AMAT", "MU", "ADI", "LRCX", "KLAC", "CDNS", "SNPS", "ANET", "FTNT", "NXPI", 
            "MRVL", "PANW", "PYPL", "SQ", "SHOP", "ZM", "TEAM", "OKTA", "CRWD", "ZS", "NET"
        ],
        "Services Publics": [
            "NEE", "DUK", "SO", "D", "EXC", "AEP", "PEG", "ED", "EIX", "ES", "FE", 
            "PPL", "WEC", "XEL", "AEE", "ETR", "CMS", "AWK", "ATO", "SRE", "CNP", 
            "PCG", "NI", "DTE", "LNT", "D", "PEG", "EVRG", "AGR", "BEP", "BIPC"
        ],
        "Santé": [
            "JNJ", "PFE", "UNH", "MRK", "ABT", "TMO", "BMY", "AMGN", "GILD", "CVS", 
            "LLY", "ABBV", "MDT", "VRTX", "REGN", "DHR", "SYK", "BDX", "ISRG", "ZTS", 
            "HCA", "CI", "ANTM", "HUM", "IQV", "EW", "IDXX", "ALGN", "MRNA", "BNTX", 
            "VTRS", "BAX", "BIIB", "ILMN", "DGX", "LH", "UHS", "HOLX", "DXCM", "STE"
        ],
        "Consommation": [
            "PG", "KO", "PEP", "WMT", "COST", "MO", "PM", "MDLZ", "CL", "KHC", "EL", 
            "KMB", "STZ", "CLX", "SJM", "CHD", "CAG", "HSY", "GIS", "ADM", "TSN", 
            "MKC", "CPB", "LW", "TAP", "BF-B", "MNST", "FLO", "SYY", "KR", "K", "COTY",
            "TGT", "HD", "LOW", "DG", "DLTR", "FIVE", "BURL", "ROST", "TJX"
        ],
        "Finances": [
            "JPM", "BAC", "V", "MA", "WFC", "C", "GS", "AXP", "MS", "BLK", "SCHW", 
            "PYPL", "COF", "USB", "PNC", "TFC", "TD", "CME", "ICE", "AON", "MMC", 
            "AJG", "SPGI", "MCO", "FIS", "FISV", "NDAQ", "CBOE", "MKTX", "RJF", "RY",
            "BNS", "BMO", "ALLY", "KEY", "CFG", "HBAN", "MTB", "RF", "ZION"
        ],
        "Industriel": [
            "GE", "HON", "MMM", "BA", "CAT", "UNP", "DE", "RTX", "LMT", "GD", "NOC", 
            "ITW", "EMR", "ETN", "WM", "RSG", "WM", "FDX", "UPS", "CSX", "NSC", "CP", 
            "CNI", "DAL", "UAL", "LUV", "AAL", "DOV", "FTV", "IR", "OTIS", "TT", "PH", 
            "ROK", "SWK", "AME", "GNRC", "JCI", "PWR", "WAB", "XYL", "WSO", "FAST"
        ],
        "ETF Large Cap": [
            "SPY", "IVV", "VOO", "VTI", "SCHX", "IWB", "ITOT", "VTV", "IWD", "SCHV", 
            "VUG", "IWF", "SCHG", "QUAL", "MTUM", "USMV", "SPLG", "SPLV", "RSP", "VIG",
            "DIA", "IWM", "IJH", "IJR", "VB", "VO", "VV", "MGK", "MGV", "VONE"
        ],
        "ETF Techno": [
            "QQQ", "XLK", "VGT", "SMH", "ARKK", "SOXX", "FTEC", "IGV", "FDN", "SKYY", 
            "WCLD", "PSI", "XNTK", "AIQ", "BOTZ", "ROBT", "ARKW", "ARKF", "FINX", "IPAY",
            "XSW", "PSJ", "PSCT", "PTF", "TECL", "SOXL", "ROM", "USD", "FXL", "QTEC"
        ],
        "ETF Dividendes": [
            "SCHD", "VYM", "DGRO", "SDY", "NOBL", "VIG", "DVY", "HDV", "SPYD", "FVD", 
            "DIV", "PEY", "PFM", "KBWD", "QYLD", "XYLD", "RYLD", "DIVO", "SPHD", "JEPI",
            "NUSI", "SRET", "ALTY", "GTO", "RDIV", "FDL", "DHS", "FVD", "SDOG", "DIVB"
        ],
        "Obligations Corporate": [
            "LQD", "VCIT", "HYG", "JNK", "PFF", "VCLT", "VCIT", "VCSH", "IGIB", "IGSB", 
            "SHYG", "SJNK", "HYLB", "USHY", "ANGL", "FALN", "HYLS", "HYXU", "IHY", "PHB",
            "QLTA", "SLQD", "BSCQ", "BSJP", "BSJO", "BSJN", "BSJM", "BSJL", "BSJK", "BSJI"
        ],
        "Obligations Gouvernement": [
            "GOVT", "TLT", "IEF", "SHY", "SPTS", "VGIT", "VGLT", "VGSH", "IEI", "SHV", 
            "BIL", "SCHO", "SCHR", "SPTL", "TLO", "GVI", "ITE", "FIBR", "FTSM", "GOVZ",
            "EDV", "ZROZ", "TLH", "IEF", "VGIT", "VGSH", "SCHR", "SPTI", "FIBR", "GOVI"
        ],
        "Matières Premières": [
            "GLD", "SLV", "USO", "UNG", "DBA", "PDBC", "GSG", "IAU", "SLVO", "USL", 
            "UCO", "SCO", "BOIL", "KOLD", "WEAT", "CORN", "SOYB", "CANE", "CPER", "PALL", 
            "PPLT", "DBB", "DBC", "COMT", "FTGC", "BCD", "BCM", "JJG", "JJC", "LD"
        ],
        "Cryptomonnaies": [
            "BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "XRP-USD", "SOL-USD", "DOT-USD", 
            "DOGE-USD", "AVAX-USD", "SHIB-USD", "MATIC-USD", "ATOM-USD", "LTC-USD", 
            "UNI-USD", "LINK-USD", "ALGO-USD", "XLM-USD", "VET-USD", "ICP-USD", "FIL-USD",
            "TRX-USD", "ETC-USD", "XMR-USD", "EGLD-USD", "AAVE-USD", "XTZ-USD", "EOS-USD",
            "NEO-USD", "ZEC-USD", "DASH-USD"
        ],
        "Immobilier (REITs)": [
            "O", "AMT", "PLD", "CCI", "EQIX", "DLR", "PSA", "SPG", "AVB", "EQR", 
            "VTR", "WELL", "WY", "EXR", "MAA", "ESS", "UDR", "SBAC", "IRM", "ARE",
            "REG", "KIM", "FRT", "VICI", "STOR", "NSA", "LAMR", "GLPI", "CPT", "ACC"
        ],
        "Énergie": [
            "XOM", "CVX", "SHEL", "TTE", "COP", "EOG", "PXD", "MPC", "PSX", "VLO",
            "OXY", "HES", "DVN", "FANG", "CTRA", "EQT", "MRO", "HAL", "SLB", "BKR",
            "NOV", "FTI", "LNG", "ET", "EPD", "WMB", "OKE", "KMI", "TRP", "ENB"
        ],
        "Communication": [
            "DIS", "NFLX", "CMCSA", "T", "VZ", "TMUS", "CHTR", "EA", "TTWO", "ATVI",
            "ROKU", "LYV", "NWSA", "FOXA", "IPG", "OMC", "WPP", "DISH", "SIRI", "LGF-A",
            "IAC", "MTCH", "BIDU", "JD", "BABA", "TME", "YY", "DOYU", "HUYA", "IQ"
        ]
    }
        
        # Trouver le ticker initial à partir des données
        self.ticker = self._find_initial_ticker(data_frame)
        self.default_start_date = datetime.now().replace(year=datetime.now().year-1)
        self.df = data_frame
        if 'theme_colors' not in st.session_state:
            st.session_state.theme_colors = self._get_theme_colors("Neon Cyberpunk")
    
    def _find_initial_ticker(self, df):
        """Trouver le ticker initial à partir des données"""
        # Si le DataFrame contient une colonne 'Ticker', utiliser la première valeur
        if 'Ticker' in df.columns:
            return df['Ticker'].iloc[0]
        # Sinon, utiliser le premier ticker dans les catégories
        return self.asset_categories["Technologie"][0]
        
    def _get_theme_colors(self, theme_name):
        """Return color palette for selected theme"""
        themes = {
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
                "primary": "#001100",  # Plus foncé
                "secondary": "#00cc00",  # Vert vif mais moins agressif
                "background": "#000800",  # Fond plus sombre
                "accent1": "#00aa00",
                "accent2": "#008800",
                "text": "#e0ffe0"  # Texte vert très clair
            },
            "Galactic Purple": {
                "primary": "#0d000d",
                "secondary": "#cc00ff",
                "background": "#080008",  # Plus sombre
                "accent1": "#9900ff",
                "accent2": "#ff00cc",
                "text": "#f0e0ff"  # Texte violet clair
            }
        }
        return themes.get(theme_name, themes["Neon Cyberpunk"]) 
        
    def _create_sidebar_controls(self):
        # Trouver la catégorie du ticker actuel
        current_category = None
        for category, tickers in self.asset_categories.items():
            if self.ticker in tickers:
                current_category = category
                break
        
        if current_category is None:
            current_category = "Actions"
        
        # Widgets de sélection
        selected_category = st.sidebar.selectbox(
            "Catégorie", 
            list(self.asset_categories.keys()),
            index=list(self.asset_categories.keys()).index(current_category)
        )
        
        ticker_options = self.asset_categories[selected_category]
    
        # Vérifie si le ticker actuel est dans les options
        if self.ticker in ticker_options:
            ticker_index = ticker_options.index(self.ticker)
        else:
            ticker_index = 0  # Prend le premier ticker par défaut
        
        self.selected_ticker = st.sidebar.selectbox(
            "Ticker", 
            ticker_options,
            index=ticker_index  # Utilise l'index calculé
        )
        
        self.start_date = st.sidebar.date_input(
            "Date de début:", 
            value=self.default_start_date,
            key="unique_start_date"
        )
        self.end_date = st.sidebar.date_input(
            "Date de fin:", 
            value=datetime.now(),
            key="unique_end_date"
        )
        
        if st.sidebar.button("Appliquer les changements"):
            self._reload_data()
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("🎨 Personnalisation du thème")
        new_theme = st.sidebar.selectbox(
            "Thème visuel",
            ["Neon Cyberpunk", "Lava Explosion", "Electric Ocean", "Acid Jungle", "Galactic Purple"],
            index=0,
            key="dashboard_theme_selector"
        )
    
        if new_theme != st.session_state.get('current_theme'):
            st.session_state.theme = new_theme
            st.session_state.current_theme = new_theme
            st.rerun()
    
    # Remplacer la méthode _reload_data
    def _reload_data(self):
        """Load data synchronously"""
        with st.status(f"**Chargement des données pour {self.selected_ticker}...**", expanded=True) as status:
            st.write("Récupération des données depuis Yahoo Finance")
            progress_bar = st.progress(0)
            
            try:
                # Convertir les dates au format string
                start_str = self.start_date.strftime("%Y-%m-%d")
                end_str = self.end_date.strftime("%Y-%m-%d")
                
                fetcher = DataFetcher(self.selected_ticker)
                progress_bar.progress(30)
                new_df = fetcher.fetch_data(start=start_str, end=end_str)
                
                if new_df.empty:
                    status.update(label="Aucune donnée disponible pour ces paramètres", state="error")
                    st.error("Vérifiez le ticker et les dates sélectionnées")
                    return
                    
                st.write("Traitement des données (calcul des indicateurs techniques)")
                progress_bar.progress(60)
                analyzer = TechnicalAnalyzer(new_df)
                analyzer.compute_50_200_days()
                analyzer.add_rsi()
                analyzer.calculate_volatility()
                analyzer.add_signal_column()
                analyzer.add_performance_column()
                analyzer.add_returns_columns()
                progress_bar.progress(90)
                
                self.df = analyzer.df
                st.session_state.df = self.df
                progress_bar.progress(100)
                status.update(label="Données mises à jour avec succès !", state="complete")
                st.rerun()
                
            except Exception as e:
                status.update(label="Erreur lors du chargement", state="error")
                st.error(f"Erreur : {str(e)}")
    def _display_kpis(self):
        """Display key indicators with improved style"""
        cols = st.columns(4)
    
        price_change = self.df['Close'].pct_change().iloc[-1] * 100
        cols[0].metric(
            label="💰 Prix actuel",
            value=f"{self.df['Close'].iloc[-1]:.2f} $",
            delta=f"{price_change:.2f}%",
            delta_color="normal",
            help="Dernier prix de clôture avec variation journalière"
        )
    
        volatility = self.df['Volatility'].iloc[-1] * 100
        volatility_icon = "📈" if volatility < 5 else "📉" if volatility > 15 else "📊"
        cols[1].metric(
            label=f"{volatility_icon} Volatilité (30j)",
            value=f"{volatility:.1f}%",
            help="Volatilité annualisée sur 30 jours"
        )
    
        volume = self.df['Volume'].iloc[-1]
        cols[2].metric(
            label="📦 Volume journalier",
            value=f"{volume/1e6:.1f}M",
            help="Volume échangé en millions"
        )
    
        if 'rsi' in self.df.columns:
            rsi_value = self.df['rsi'].iloc[-1]
            rsi_status = "Achat" if rsi_value < 30 else "Vente" if rsi_value > 70 else "Neutre"
            cols[3].metric(
                label=f"📊 RSI (14j) - {rsi_status}",
                value=f"{rsi_value:.1f}",
                help="Indice de force relative - <30: Survente, >70: Surachat"
            )

    def _create_analysis_tabs(self):
        """Create analysis tabs with enriched content"""
        tab1, tab2, tab3, tab4 , tab5 = st.tabs([
            "📈 Graphique principal", 
            "📊 Analyse technique", 
            "🔍 Données brutes",
            "📰 Actualités & Sentiment",
            "🌍 Influence géographique" 
        ])

        with tab1:
            st.markdown("#### Évolution des prix avec moyennes mobiles")
            fig = Visualizer(self.df, rows=1, columns=1)
            fig.draw_candlestick().MA_draw(overlay=True)
            fig.show(title=f"Analyse de {self.selected_ticker}")
        
            st.markdown("##### Tendances récentes")
            col1, col2 = st.columns(2)
            with col1:
                last_5_days = self.df['Close'].pct_change(5).iloc[-1] * 100
                st.metric("5 derniers jours", f"{last_5_days:.2f}%")
            with col2:
                last_month = self.df['Close'].pct_change(20).iloc[-1] * 100
                st.metric("1 mois", f"{last_month:.2f}%")

        with tab2:
            st.markdown("#### Analyse technique complète")
            cols = st.columns(2)
        
            with cols[0]:
                st.markdown("##### Indicateurs clés")
                fig1 = Visualizer(self.df, rows=2, columns=1, row_heights=[0.7, 0.3])
                fig1.draw_candlestick().Rsi_draw(show_zones=True)
                fig1.show()
            
            with cols[1]:
                st.markdown("##### Volume et volatilité")
                fig2 = Visualizer(self.df, rows=2, columns=1, row_heights=[0.5, 0.5])
                fig2.draw_volume().draw_cumulative_returns()
                fig2.show()

        with tab3:
            st.markdown("#### Données historiques")
            st.data_editor(
                self.df.sort_index(ascending=False),
                column_config={
                    "Open": st.column_config.NumberColumn(format="$%.2f"),
                    "High": st.column_config.NumberColumn(format="$%.2f"),
                    "Low": st.column_config.NumberColumn(format="$%.2f"),
                    "Close": st.column_config.NumberColumn(format="$%.2f"),
                    "Volume": st.column_config.NumberColumn(format="%.0f"),
                    "rsi": st.column_config.NumberColumn(format="%.1f"),
                    "Volatility": st.column_config.NumberColumn(format="%.2%")
                },
                hide_index=False,
                use_container_width=True,
                height=600
            )
        
        with tab4:
            self._display_news_analysis()
        
        with tab5:  
            self._display_geo_influence()
    def _display_geo_influence(self):
        """Display geographical influence map with Plotly"""
        st.subheader("Influence géographique")
        
        fetcher = GeoDataFetcher()
        geo_data = fetcher.get_geo_data(self.selected_ticker)
        df_geo = fetcher.to_dataframe(geo_data)
        
        if df_geo.empty:
            st.warning("Aucune donnée géographique disponible pour ce ticker")
            return
        
        # Créer la carte avec Plotly
        fig = px.scatter_geo(
            df_geo,
            lat='lat',
            lon='lon',
            size='size',
            color='weight',
            color_continuous_scale=px.colors.sequential.Plasma,
            hover_name='country',
            hover_data={'weight': ':.2%', 'lat': False, 'lon': False, 'size': False},
            projection='natural earth',
            title=f"Exposition géographique de {self.selected_ticker}"
        )
        
        # Personnaliser le style selon le thème
        fig.update_layout(
            geo=dict(
                bgcolor='rgba(0,0,0,0)',
                landcolor='lightgray',
                showcountries=True,
                countrycolor='gray'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=st.session_state.theme_colors['text']),
            margin=dict(l=0, r=0, t=40, b=0),
            coloraxis_colorbar=dict(
                title="Influence",
                tickformat=".0%"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Afficher les données sous forme de tableau
        with st.expander("Voir les données détaillées"):
            st.dataframe(
                df_geo[['country', 'weight']].sort_values('weight', ascending=False),
                column_config={
                    "country": "Pays",
                    "weight": st.column_config.ProgressColumn(
                        "Influence",
                        format="%.2f%%",
                        min_value=0,
                        max_value=1
                    )
                },
                hide_index=True,
                use_container_width=True
            )
    def _display_news_analysis(self):
        """Display news and sentiment analysis"""
        st.subheader("📰 Actualités et analyse de sentiment")
    
        news = NewsFetcher().get_company_news(self.selected_ticker)
        reddit_data = RedditSentiment().analyze_ticker(self.selected_ticker)
    
        news_scores = [item['score'] for item in news]
        avg_news_score = sum(news_scores) / len(news_scores) if news_scores else 0
    
        reddit_score = (reddit_data['positive'] - reddit_data['negative']) / reddit_data['total']
    
        global_score = (avg_news_score + reddit_score) / 2
        
        st.markdown("### Recommandation d'investissement")
        if global_score > 0.3:
            st.success("✅ **Favorable à l'achat** - Sentiment très positif")
        elif global_score > -0.2:
            st.info("🟢 **Opportunité modérée** - Sentiment généralement neutre")
        else:
            st.warning("⚠️ **Prudence** - Sentiment négatif dominant")
        
        st.metric("Score de confiance", f"{global_score:.2f}/1.0")
        
        st.markdown("### Dernières actualités")
        for item in news:
            sentiment_color = {
                "positive": "green",
                "neutral": "orange",
                "negative": "red"
            }.get(item['sentiment'], "gray")
            
            st.markdown(f"""
            <div style="border-left: 3px solid {sentiment_color}; padding-left: 10px; margin-bottom: 15px;">
                <b>{item['title']}</b><br>
                <i>{item['source']} - {item['date']}</i><br>
                Sentiment: <span style="color: {sentiment_color}; font-weight: bold">{item['sentiment']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Sentiment des réseaux sociaux")
        st.progress((reddit_data['positive'] / reddit_data['total']))
        st.caption(f"Positif: {reddit_data['positive']} | Neutre: {reddit_data['neutral']} | Négatif: {reddit_data['negative']}")
        
    def _add_data_download(self):
        csv_data = self.df.to_csv(index=False).encode('utf-8')
        today = datetime.now().strftime("%Y-%m-%d")
        st.download_button(
            label="📥 Télécharger les données",
            data=csv_data,
            file_name=f'stock_data_{today}.csv',
            mime='text/csv',
            key=f"download_btn_{datetime.now().timestamp()}"
        )

    def display(self):
        """Version with alert system"""
        container = st.container()
        with container:
            self._create_sidebar_controls()
            self._create_alert_system()
            
            # Vérifier si les données sont chargées
            if not hasattr(self, 'df') or self.df.empty:
                st.warning("Chargement initial des données...")
                self._reload_data()
                return
    
            if hasattr(self, 'df'):
                self._check_alerts()
                self._display_kpis()
                self._create_analysis_tabs()
                self._add_data_download()
                
    def _create_alert_system(self):
        """Visually improved alert system"""
        with st.sidebar.expander("🔔 Système d'alertes", expanded=True):
            if 'alerts' not in st.session_state:
                st.session_state.alerts = []
        
            with st.form("alert_form", clear_on_submit=True):
                cols = st.columns(2)
                with cols[0]:
                    indicator = st.selectbox(
                        "Indicateur",
                        ["RSI", "Prix de clôture", "Volatilité", "Croisement MA"],
                        key="alert_indicator"
                    )
                    condition = st.selectbox(
                        "Condition",
                        ["Au-dessus", "En dessous", "Croise au-dessus", "Croise en dessous"],
                        key="alert_condition"
                    )
            
                with cols[1]:
                    threshold = st.number_input(
                        "Seuil",
                        min_value=0.0,
                        max_value=1000.0 if indicator == "Prix de clôture" else 100.0,
                        value=30.0 if indicator == "RSI" else 50.0,
                        step=0.1,
                        key="alert_threshold"
                    )
                    color = st.color_picker(
                        "Couleur d'alerte",
                        value="#FF4B4B",
                        key="alert_color"
                    )
            
                if st.form_submit_button("➕ Ajouter une alerte", use_container_width=True):
                    new_alert = {
                        'indicator': indicator,
                        'condition': condition,
                        'threshold': threshold,
                        'color': color,
                        'active': True,
                        'triggered': False
                    }
                    st.session_state.alerts.append(new_alert)
                    st.success("Alerte enregistrée !")
        
            if st.session_state.alerts:
                st.markdown("---")
                st.markdown("**Mes alertes actives**")
            
                for i, alert in enumerate(st.session_state.alerts[:5]):
                    with st.container(border=True):
                        cols = st.columns([1, 3, 1])
                        with cols[0]:
                            st.checkbox(
                                "Active",
                                value=alert['active'],
                                key=f"alert_active_{i}",
                                on_change=lambda i=i: self._toggle_alert(i),
                                label_visibility="collapsed"
                            )
                        with cols[1]:
                            st.markdown(f"""
                            **{alert['indicator']}** {alert['condition']} **{alert['threshold']}**
                            """)
                        with cols[2]:
                            st.button(
                                "🗑️", 
                                key=f"delete_{i}",
                                on_click=lambda i=i: self._remove_alert(i),
                                use_container_width=True
                            )
                            
    def _toggle_alert(self, index):
        """Enable/disable an alert"""
        st.session_state.alerts[index]['active'] = not st.session_state.alerts[index]['active']

    def _remove_alert(self, index):
        """Remove an alert"""
        st.session_state.alerts.pop(index)
        st.rerun()

    def _check_alerts(self):
        """Check if alert conditions are met"""
        if not hasattr(self, 'df') or 'alerts' not in st.session_state:
            return
    
        for i, alert in enumerate(st.session_state.alerts):
            if not alert['active']:
                continue
            
            try:
                current_value = None
                message = ""
            
                if alert['indicator'] == "RSI":
                    current_value = self.df['rsi'].iloc[-1]
                elif alert['indicator'] == "Prix de clôture":
                    current_value = self.df['Close'].iloc[-1]
                elif alert['indicator'] == "Volatilité":
                    current_value = self.df['Volatility'].iloc[-1] * 100
            
                if current_value is not None:
                    if alert['condition'] == "Au-dessus" and current_value > alert['threshold']:
                        message = f"🚨 {alert['indicator']} ({current_value:.2f}) > {alert['threshold']}"
                    elif alert['condition'] == "En dessous" and current_value < alert['threshold']:
                        message = f"🚨 {alert['indicator']} ({current_value:.2f}) < {alert['threshold']}"
                
                    elif alert['indicator'] == "Croisement MA":
                        if alert['condition'] == "Croise au-dessus" and \
                            self.df['MA_50'].iloc[-1] > self.df['MA_200'].iloc[-1] and \
                            self.df['MA_50'].iloc[-2] <= self.df['MA_200'].iloc[-2]:
                            message = "🚨 Croisement haussier (MA50 > MA200)"
                        elif alert['condition'] == "Croise en dessous" and \
                            self.df['MA_50'].iloc[-1] < self.df['MA_200'].iloc[-1] and \
                            self.df['MA_50'].iloc[-2] >= self.df['MA_200'].iloc[-2]:
                            message = "🚨 Croisement baissier (MA50 < MA200)"
            
                    if message and not alert['triggered']:
                        st.toast(message, icon="🔔")
                        st.session_state.alerts[i]['triggered'] = True
                    elif not message and alert['triggered']:
                        st.session_state.alerts[i]['triggered'] = False
                    
            except KeyError as e:
                st.error(f"Erreur: Colonne {str(e)} manquante pour l'alerte")
                
    @classmethod
    def test_dashboard(cls):
        """Launch a dashboard demo"""
        df = DataFetcher("TSLA").fetch_data(period="6mo")
        analyzer = TechnicalAnalyzer(df)
        analyzer.compute_50_200_days()
    
        dashboard = cls(analyzer.df)
        dashboard.display()