import streamlit as st
from src.technical_analyzer import TechnicalAnalyzer
from datetime import datetime
from src.data_fetcher import DataFetcher
from src.visualizer import Visualizer
from src.news_fetcher import NewsFetcher
from src.reddit_analyzer import RedditSentiment
from src.geo_data import GeoDataFetcher
from src.asset_categories import AssetCategories
from src.macro_data import MacroData
import plotly.express as px
import pandas as pd
import threading
from concurrent.futures import ThreadPoolExecutor
import plotly.graph_objects as go

class Dashboard:
    def __init__(self, data_frame):
        # Définir les catégories d'actifs étendues
        self.asset_categories = AssetCategories.get_all_categories()
        
        # Trouver le ticker initial à partir des données
        self.ticker = self._find_initial_ticker(data_frame)
        self.default_start_date = datetime.now().replace(year=datetime.now().year-1)
        self.default_end_date = datetime.now()
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
        
        start_value = st.session_state.get('dashboard_start_date', self.default_start_date)
        end_value = st.session_state.get('dashboard_end_date', self.default_end_date)
        
        self.start_date = st.sidebar.date_input(
            "Date de début:", 
            value=start_value,
            key="dashboard_start_date"
        )
        self.end_date = st.sidebar.date_input(
            "Date de fin:", 
            value=end_value,
            key="dashboard_end_date"
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
        """Load data with caching"""
        # Créer une clé de cache unique
        cache_key = f"{self.selected_ticker}_{self.start_date}_{self.end_date}"
        
        # Vérifier le cache
        if 'data_cache' in st.session_state and cache_key in st.session_state.data_cache:
            self.df = st.session_state.data_cache[cache_key]
            st.session_state.df = self.df
            st.rerun()
            return
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
        if 'data_cache' not in st.session_state:
            st.session_state.data_cache = {}
            st.session_state.data_cache[cache_key] = self.df
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
         # Mood Market (nouvelle section)
        st.markdown("---")
        self._display_market_mood()
        
        # Jauge Risque/Récompense
        self._display_risk_reward()

        # Ajouter après la jauge risque/récompense
        self._display_macro_context()
    def _display_macro_context(self):
        """Affiche le contexte macro-économique"""
        st.markdown("---")
        st.subheader("🌐 Contexte Macro-économique")
        
        with st.spinner("Chargement des données macro..."):
            macro_fetcher = MacroData()
            
            macro_df, errors = macro_fetcher.fetch_macro_data(period="1y")
            
            # Afficher les erreurs
            if errors:
                for indicator, error in errors.items():
                    st.warning(f"{indicator}: {error}")
                    
            if macro_df.empty:
                st.warning("Aucune donnée macro disponible")
                return
                
            # Afficher les indicateurs même avec peu de points
            cols = st.columns(4)
            indicators = list(macro_df.columns)[:4]
            
            for i, indicator in enumerate(indicators):
                try:
                    # Utiliser la dernière valeur disponible
                    value = macro_df[indicator].iloc[-1]
                    cols[i].metric(label=indicator, value=f"{value:.2f}")
                except:
                    cols[i].metric(label=indicator, value="N/A")
            
            # Afficher le graphique même avec peu de données
            st.markdown("**Tendances macro-économiques**")
            fig = Visualizer(macro_df, rows=1, columns=1)
            for indicator in macro_df.columns:
                fig._add_trace(
                    go.Scatter(
                        x=macro_df.index,
                        y=macro_df[indicator],
                        name=indicator,
                        mode='lines'
                    ),
                    overlay=True
                )
            fig.fig.update_layout(height=300)
            st.plotly_chart(fig.fig, use_container_width=True)
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
        @st.cache_data(ttl=86400)  # Cache de 24h
        def get_cached_geo_data(ticker):
            fetcher = GeoDataFetcher()
            return fetcher.get_geo_data(ticker)
        """Display geographical influence map with Plotly"""
        st.subheader("Influence géographique")
        
        fetcher = GeoDataFetcher()
        geo_data = get_cached_geo_data(self.selected_ticker)
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
    def _display_market_mood(self):
        """Affiche l'humeur du marché avec des emojis géants"""
        # Calcul des tendances
        last_5_days = self.df['Close'].pct_change(5).iloc[-1] * 100
        last_month = self.df['Close'].pct_change(20).iloc[-1] * 100
        
        # Détermination de l'humeur
        if last_5_days > 5:
            mood = "🚀"  # Hausse forte
            explanation = "Forte hausse récente"
        elif last_5_days < -5:
            mood = "😱"  # Krach
            explanation = "Fort recul récent"
        elif last_month > 10:
            mood = "📈"  # Tendance haussière
            explanation = "Bonne tendance mensuelle"
        elif last_month < -10:
            mood = "📉"  # Tendance baissière
            explanation = "Tendance mensuelle négative"
        else:
            mood = "🥱"  # Stagnation
            explanation = "Marché stagnant"
        
        # Affichage stylisé
        st.markdown(f"""
        <div style="text-align:center; margin: 30px 0;">
            <div style="font-size: 80px; margin-bottom: 10px;">{mood}</div>
            <div style="font-size: 20px; color: {st.session_state.theme_colors['accent1']}">
                {explanation}
            </div>
        </div>
        """, unsafe_allow_html=True)
    def _display_risk_reward(self):
        """Affiche la jauge risque/récompense"""
        volatility = self.df['Volatility'].iloc[-1] * 100  # Volatilité en %
        
        # Détermination du niveau de risque
        if volatility < 5:
            level = "🟢 Faible"
            position = 25
            color = "#00ff00"
        elif volatility < 15:
            level = "🟡 Modéré"
            position = 50
            color = "#ffff00"
        else:
            level = "🔴 Élevé"
            position = 85
            color = "#ff0000"
        
        # Affichage de la jauge
        st.markdown(f"""
        <div style="margin: 30px 0; text-align: center;">
            <div style="font-size: 20px; margin-bottom: 10px; color: {st.session_state.theme_colors['text']}">
                Ratio Risque/Récompense
            </div>
            <div style="background: #333; height: 30px; border-radius: 15px; position: relative; margin: 0 auto; max-width: 600px;">
                <div style="position: absolute; width: 100%; display: flex; justify-content: space-between; padding: 0 10px;">
                    <span>Élevé</span>
                    <span>Équilibré</span>
                    <span>Faible</span>
                </div>
                <div style="background: linear-gradient(to right, #ff0000, #ffff00, #00ff00); 
                            height: 100%; border-radius: 15px; opacity: 0.6;"></div>
                <div style="position: absolute; top: -5px; left: {position}%; 
                            transform: translateX(-50%); width: 10px; height: 40px; 
                            background: {color}; border-radius: 5px;"></div>
            </div>
            <div style="font-size: 24px; margin-top: 10px; color: {color}">
                {level} • Volatilité: {volatility:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
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