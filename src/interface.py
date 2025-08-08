import streamlit as st
from src.technical_analyzer import TechnicalAnalyzer
from datetime import datetime
from src.data_fetcher import DataFetcher
from src.visualizer import Visualizer
from src.news_fetcher import NewsFetcher
from src.reddit_analyzer import RedditSentiment

class Dashboard:
    def __init__(self, data_frame):
        self.tickers = ["AAPL", "TSLA", "MSFT", "AMZN", "GOOGL"]
        self.default_start_date = datetime.now().replace(year=datetime.now().year-1)
        self.df = data_frame
        
    def _set_global_style(self):
        """Configure le style global du dashboard"""
        primary_color = "#2c3e50"
        secondary_color = "#3498db"
        background_color = "#f8f9fa"
    
        st.set_page_config(
            page_title="Dashboard Boursier",
            layout="wide",
            page_icon="📊"
        )
    
        st.markdown(f"""
        <style>
            .css-18e3th9 {{
                background-color: {background_color};
            }}
            .css-1d391kg {{
                background-color: {primary_color};
                color: white;
            }}
            .stMetric {{
                border-left: 0.25rem solid {secondary_color};
                padding: 1rem;
                border-radius: 0.5rem;
                background-color: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .stTabs [data-baseweb="tab-list"] {{
                gap: 0.5rem;
            }}
            .stTabs [data-baseweb="tab"] {{
                padding: 0.5rem 1rem;
                border-radius: 0.5rem 0.5rem 0 0;
            }}
            .stTabs [aria-selected="true"] {{
                background-color: {secondary_color};
                color: white;
            }}
            .css-1vq4p4l {{
                padding: 2rem 1rem;
                background-color: {primary_color};
                color: white;
            }}
            .sidebar .sidebar-content {{
                background-color: {primary_color};
            }}
        </style>
        """, unsafe_allow_html=True)
        
    def _create_sidebar_controls(self):
        self.selected_ticker = st.sidebar.selectbox(
            "Choisissez une action :", 
            self.tickers,
            key="unique_ticker_select"
        )
        self.start_date = st.sidebar.date_input(
            "Date de début :", 
            value=self.default_start_date,
            key="unique_start_date"
        )
        self.end_date = st.sidebar.date_input(
            "Date de fin :", 
            value=datetime.now(),
            key="unique_end_date"
        )
        
        if st.sidebar.button("Appliquer les changements"):
            self._reload_data()
    
    def _reload_data(self):
        """Charge les données avec un indicateur de progression"""
        with st.spinner(f"Chargement des données pour {self.selected_ticker}..."):
            progress_bar = st.progress(0)
        
            try:
                fetcher = DataFetcher(self.selected_ticker)
                progress_bar.progress(20)
            
                new_df = fetcher.fetch_data(start=self.start_date, end=self.end_date)
                progress_bar.progress(50)
            
                if not new_df.empty:
                    analyzer = TechnicalAnalyzer(new_df)
                    analyzer.calcul_50_200_jours()
                    progress_bar.progress(70)
                    analyzer.add_rsi()
                    analyzer.calculate_volatility()
                    # Générer les colonnes nécessaires pour rendements
                    analyzer.Add_column_Signal()
                    analyzer.Add_column_Performance()
                    analyzer.Add_columns_rendements()
                    progress_bar.progress(90)
                
                    self.df = analyzer.df
                    st.session_state.df = analyzer.df
                    progress_bar.progress(100)
                
                    st.toast("Données mises à jour avec succès!", icon="✅")
                    st.rerun()
                else:
                    st.sidebar.error("Aucune donnée disponible pour ces paramètres")
            except Exception as e:
                st.sidebar.error(f"Erreur lors du chargement: {str(e)}")
            finally:
                progress_bar.empty()
    
    def _display_kpis(self):
        """Affiche les indicateurs clés avec style amélioré"""
        cols = st.columns(4)
    
        price_change = self.df['Clôt'].pct_change().iloc[-1] * 100
        cols[0].metric(
            label="💰 Prix Actuel",
            value=f"{self.df['Clôt'].iloc[-1]:.2f} $",
            delta=f"{price_change:.2f}%",
            delta_color="normal",
            help="Prix de clôture du dernier jour avec variation journalière"
        )
    
        volatility = self.df['Volatilite'].iloc[-1] * 100
        volatility_icon = "📈" if volatility < 5 else "📉" if volatility > 15 else "📊"
        cols[1].metric(
            label=f"{volatility_icon} Volatilité (30j)",
            value=f"{volatility:.1f}%",
            help="Volatilité annualisée sur 30 jours"
        )
    
        volume = self.df['Volume'].iloc[-1]
        cols[2].metric(
            label="📦 Volume Journalier",
            value=f"{volume/1e6:.1f}M",
            help="Volume échangé du dernier jour en millions"
        )
    
        if 'rsi' in self.df.columns:
            rsi_value = self.df['rsi'].iloc[-1]
            rsi_status = "Achat" if rsi_value < 30 else "Vente" if rsi_value > 70 else "Neutre"
            cols[3].metric(
                label=f"📊 RSI (14j) - {rsi_status}",
                value=f"{rsi_value:.1f}",
                help="Relative Strength Index - <30: Survente, >70: Surachat"
            )

    def _create_analysis_tabs(self):
        """Crée des onglets d'analyse avec contenu enrichi"""
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Graphique Principal", 
            "📊 Analyse Technique", 
            "🔍 Données Brutes",
            "📰 Actualités & Sentiment"
        ])

        with tab1:
            st.markdown("#### Évolution du prix avec moyennes mobiles")
            fig = Visualizer(self.df, rows=1, columns=1)
            fig.draw_candlestick().MA_draw(overlay=True)
            fig.show(title=f"Analyse de {self.selected_ticker}")
        
            st.markdown("##### Dernières tendances")
            col1, col2 = st.columns(2)
            with col1:
                last_5_days = self.df['Clôt'].pct_change(5).iloc[-1] * 100
                st.metric("5 derniers jours", f"{last_5_days:.2f}%")
            with col2:
                last_month = self.df['Clôt'].pct_change(20).iloc[-1] * 100
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
                st.markdown("##### Volumes et volatilité")
                fig2 = Visualizer(self.df, rows=2, columns=1, row_heights=[0.5, 0.5])
                fig2.draw_volume().draw_cumulative_returns()
                fig2.show()

        with tab3:
            st.markdown("#### Données historiques")
            st.data_editor(
                self.df.sort_index(ascending=False),
                column_config={
                    "Ouv": st.column_config.NumberColumn(format="$%.2f"),
                    "Haut": st.column_config.NumberColumn(format="$%.2f"),
                    "Bas": st.column_config.NumberColumn(format="$%.2f"),
                    "Clôt": st.column_config.NumberColumn(format="$%.2f"),
                    "Volume": st.column_config.NumberColumn(format="%.0f"),
                    "rsi": st.column_config.NumberColumn(format="%.1f"),
                    "Volatilite": st.column_config.NumberColumn(format="%.2%")
                },
                hide_index=False,
                use_container_width=True,
                height=600
            )
        
        with tab4:
            self._display_news_analysis()
            
    def _display_news_analysis(self):
        """Affiche l'analyse des actualités et du sentiment"""
        st.subheader("📰 Analyse des Actualités et Sentiment")
    
        news = NewsFetcher().get_company_news(self.selected_ticker)
        reddit_data = RedditSentiment().analyze_ticker(self.selected_ticker)
    
        news_scores = [item['score'] for item in news]
        avg_news_score = sum(news_scores) / len(news_scores) if news_scores else 0
    
        reddit_score = (reddit_data['positive'] - reddit_data['negative']) / reddit_data['total']
    
        global_score = (avg_news_score + reddit_score) / 2
        
        st.markdown("### Recommandation d'Investissement")
        if global_score > 0.3:
            st.success("✅ **Favorable à l'achat** - Sentiment très positif")
        elif global_score > -0.2:
            st.info("🟢 **Opportunité modérée** - Sentiment globalement neutre")
        else:
            st.warning("⚠️ **Prudence** - Sentiment négatif dominant")
        
        st.metric("Score de Confiance", f"{global_score:.2f}/1.0")
        
        st.markdown("### Dernières Actualités")
        for item in news:
            sentiment_color = {
                "positif": "green",
                "neutre": "orange",
                "négatif": "red"
            }.get(item['sentiment'], "gray")
            
            st.markdown(f"""
            <div style="border-left: 3px solid {sentiment_color}; padding-left: 10px; margin-bottom: 15px;">
                <b>{item['title']}</b><br>
                <i>{item['source']} - {item['date']}</i><br>
                Sentiment: <span style="color: {sentiment_color}; font-weight: bold">{item['sentiment']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Sentiment des Réseaux Sociaux")
        st.progress((reddit_data['positive'] / reddit_data['total']))
        st.caption(f"Positif: {reddit_data['positive']} | Neutre: {reddit_data['neutral']} | Négatif: {reddit_data['negative']}")
        
    def _add_data_download(self):
        csv_data = self.df.to_csv(index=False).encode('utf-8')
        today = datetime.now().strftime("%Y-%m-%d")
        st.download_button(
            label="📥 Télécharger les données",
            data=csv_data,
            file_name=f'donnees_bourse_{today}.csv',
            mime='text/csv',
            key=f"download_btn_{datetime.now().timestamp()}"
        )

    def display(self):
        """Version avec système d'alertes"""
        self._set_global_style()
    
        container = st.container()
        with container:
            self._create_sidebar_controls()
            self._create_alert_system()
    
            if hasattr(self, 'df'):
                self._check_alerts()
                self._display_kpis()
                self._create_analysis_tabs()
                self._add_data_download()
                
    def _create_alert_system(self):
        """Système d'alertes visuellement amélioré"""
        with st.sidebar.expander("🔔 Système d'Alertes", expanded=True):
            if 'alertes' not in st.session_state:
                st.session_state.alertes = []
        
            with st.form("alerte_form", clear_on_submit=True):
                cols = st.columns(2)
                with cols[0]:
                    indicateur = st.selectbox(
                        "Indicateur",
                        ["RSI", "Prix de clôture", "Volatilité", "Croisement MA"],
                        key="alerte_indicateur"
                    )
                    condition = st.selectbox(
                        "Condition",
                        ["Supérieur à", "Inférieur à", "Croise vers le haut", "Croise vers le bas"],
                        key="alerte_condition"
                    )
            
                with cols[1]:
                    seuil = st.number_input(
                        "Seuil",
                        min_value=0.0,
                        max_value=1000.0 if indicateur == "Prix de clôture" else 100.0,
                        value=30.0 if indicateur == "RSI" else 50.0,
                        step=0.1,
                        key="alerte_seuil"
                    )
                    couleur = st.color_picker(
                        "Couleur d'alerte",
                        value="#FF4B4B",
                        key="alerte_couleur"
                    )
            
                if st.form_submit_button("➕ Ajouter l'alerte", use_container_width=True):
                    nouvelle_alerte = {
                        'indicateur': indicateur,
                        'condition': condition,
                        'seuil': seuil,
                        'couleur': couleur,
                        'active': True,
                        'declenchee': False
                    }
                    st.session_state.alertes.append(nouvelle_alerte)
                    st.success("Alerte enregistrée!")
        
            if st.session_state.alertes:
                st.markdown("---")
                st.markdown("**Mes Alertes Actives**")
            
                for i, alerte in enumerate(st.session_state.alertes[:5]):
                    with st.container(border=True):
                        cols = st.columns([1, 3, 1])
                        with cols[0]:
                            st.checkbox(
                                "Active",
                                value=alerte['active'],
                                key=f"alerte_active_{i}",
                                on_change=lambda i=i: self._toggle_alerte(i),
                                label_visibility="collapsed"
                            )
                        with cols[1]:
                            st.markdown(f"""
                            **{alerte['indicateur']}** {alerte['condition']} **{alerte['seuil']}**
                            """)
                        with cols[2]:
                            st.button(
                                "🗑️", 
                                key=f"delete_{i}",
                                on_click=lambda i=i: self._remove_alerte(i),
                                use_container_width=True
                            )
                            
    def _toggle_alerte(self, index):
        """Active/désactive une alerte"""
        st.session_state.alertes[index]['active'] = not st.session_state.alertes[index]['active']

    def _remove_alerte(self, index):
        """Supprime une alerte"""
        st.session_state.alertes.pop(index)
        st.rerun()

    def _check_alerts(self):
        """Vérifie si les conditions d'alerte sont remplies"""
        if not hasattr(self, 'df') or 'alertes' not in st.session_state:
            return
    
        for i, alerte in enumerate(st.session_state.alertes):
            if not alerte['active']:
                continue
            
            try:
                current_value = None
                message = ""
            
                if alerte['indicateur'] == "RSI":
                    current_value = self.df['rsi'].iloc[-1]
                elif alerte['indicateur'] == "Prix de clôture":
                    current_value = self.df['Clôt'].iloc[-1]
                elif alerte['indicateur'] == "Volatilité":
                    current_value = self.df['Volatilite'].iloc[-1] * 100
            
                if current_value is not None:
                    if alerte['condition'] == "Supérieur à" and current_value > alerte['seuil']:
                        message = f"🚨 {alerte['indicateur']} ({current_value:.2f}) > {alerte['seuil']}"
                    elif alerte['condition'] == "Inférieur à" and current_value < alerte['seuil']:
                        message = f"🚨 {alerte['indicateur']} ({current_value:.2f}) < {alerte['seuil']}"
                
                    elif alerte['indicateur'] == "Croisement MA":
                        if alerte['condition'] == "Croise vers le haut" and \
                            self.df['MA_50'].iloc[-1] > self.df['MA_200'].iloc[-1] and \
                            self.df['MA_50'].iloc[-2] <= self.df['MA_200'].iloc[-2]:
                            message = "🚨 Croisement haussier (MA50 > MA200)"
                        elif alerte['condition'] == "Croise vers le bas" and \
                            self.df['MA_50'].iloc[-1] < self.df['MA_200'].iloc[-1] and \
                            self.df['MA_50'].iloc[-2] >= self.df['MA_200'].iloc[-2]:
                            message = "🚨 Croisement baissier (MA50 < MA200)"
            
                    if message and not alerte['declenchee']:
                        st.toast(message, icon="🔔")
                        st.session_state.alertes[i]['declenchee'] = True
                    elif not message and alerte['declenchee']:
                        st.session_state.alertes[i]['declenchee'] = False
                    
            except KeyError as e:
                st.error(f"Erreur: Colonne {str(e)} manquante pour l'alerte")
                
    @classmethod
    def test_dashboard(cls):
        """Lance une démo du dashboard"""
        df = DataFetcher("TSLA").fetch_data(period="6mo")
        analyzer = TechnicalAnalyzer(df)
        analyzer.calcul_50_200_jours()
    
        dashboard = cls(analyzer.df)
        dashboard.display()