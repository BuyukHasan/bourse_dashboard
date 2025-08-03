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
        fetcher = DataFetcher(self.selected_ticker)
        new_df = fetcher.fetch_data(start=self.start_date, end=self.end_date)
        
        if not new_df.empty:
            analyzer = TechnicalAnalyzer(new_df)
            analyzer.calcul_50_200_jours()
            analyzer.add_rsi()
            analyzer.calculate_volatility()
            self.df = new_df
            st.session_state.df = new_df
            st.rerun()
        else:
            st.sidebar.error("Aucune donnée disponible pour ces paramètres")
    
    def _display_kpis(self):
        col1, col2, col3 = st.columns(3)
        col1.metric(label="💰 Prix Actuel", value=f"{self.df['Clôt'].iloc[-1]:.2f} $")
        col2.metric(label="📈 Volatilité (30j)", value=f"{self.df['Volatilite'].iloc[-1]:.1%}")
        col3.metric(label="📊 Volume (dernier jour)", value=f"{self.df['Volume'].iloc[-1]:,}")

    def _create_analysis_tabs(self):
        tab1, tab2, tab3 = st.tabs(["Graphique Principal", "Volumes", "Données Brutes"])

        with tab1:
            fig = Visualizer(self.df, rows=1, columns=1)
            fig.draw_candlestick().MA_draw(overlay=True)
            st.plotly_chart(fig.fig, use_container_width=True)

        with tab2:
            fig_vol = Visualizer(self.df, rows=1, columns=1)
            fig_vol.draw_volume()
            st.plotly_chart(fig_vol.fig, use_container_width=True)

        with tab3:
            st.dataframe(
                self.df,
                height=400,
                use_container_width=True,
                column_order=["Ouv", "Haut", "Bas", "Clôt", "Volume"],
                hide_index=False
            )

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
        container = st.container()
        with container:
            self._create_sidebar_controls()
            self._create_alert_system()  # Ajout du système d'alertes
        
            if hasattr(self, 'df'):
                self._check_alerts()  # Vérification des alertes
                self._display_kpis()
                self._create_analysis_tabs()
                self._add_data_download()
    def _create_alert_system(self):
        """
        Système complet de gestion des alertes avec :
        - Création d'alertes
        - Stockage dans session_state
        - Vérification en temps réel
        - Affichage des notifications
        """
        st.sidebar.subheader("🔔 Système d'Alertes")
    
        # Initialisation de la structure de données
        if 'alertes' not in st.session_state:
            st.session_state.alertes = []
    
        # Formulaire de création d'alerte
        with st.sidebar.form("alerte_form"):
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
        
            seuil = st.number_input(
                "Seuil/valeur",
                min_value=0.0,
                max_value=1000.0 if indicateur == "Prix de clôture" else 100.0,
                value=30.0 if indicateur == "RSI" else 50.0,
                step=0.1,
                key="alerte_seuil"
            )
        
            submitted = st.form_submit_button("💾 Sauvegarder l'alerte")
        
            if submitted:
                nouvelle_alerte = {
                    'indicateur': indicateur,
                    'condition': condition,
                    'seuil': seuil,
                    'active': True,
                    'declenchee': False
                }
                st.session_state.alertes.append(nouvelle_alerte)
                st.sidebar.success("Alerte enregistrée!")
    
        # Liste des alertes existantes avec toggle
        if st.session_state.alertes:
            st.sidebar.markdown("---")
            st.sidebar.markdown("**Mes Alertes**")
        
            for i, alerte in enumerate(st.session_state.alertes[:5]):  # Limite à 5 alertes
                cols = st.sidebar.columns([1, 3, 1])
                cols[0].checkbox(
                    "",
                    value=alerte['active'],
                    key=f"alerte_active_{i}",
                    on_change=lambda i=i: self._toggle_alerte(i)
                )
                cols[1].markdown(
                    f"{alerte['indicateur']} {alerte['condition']} {alerte['seuil']}"
                )
                cols[2].button(
                    "🗑️", 
                    key=f"delete_{i}",
                    on_click=lambda i=i: self._remove_alerte(i)
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
            
                # Récupération de la valeur courante
                if alerte['indicateur'] == "RSI":
                    current_value = self.df['rsi'].iloc[-1]
                elif alerte['indicateur'] == "Prix de clôture":
                    current_value = self.df['Clôt'].iloc[-1]
                elif alerte['indicateur'] == "Volatilité":
                    current_value = self.df['Volatilite'].iloc[-1] * 100  # Conversion en %
            
                # Vérification des conditions
                if current_value is not None:
                    if alerte['condition'] == "Supérieur à" and current_value > alerte['seuil']:
                        message = f"🚨 {alerte['indicateur']} ({current_value:.2f}) > {alerte['seuil']}"
                    elif alerte['condition'] == "Inférieur à" and current_value < alerte['seuil']:
                        message = f"🚨 {alerte['indicateur']} ({current_value:.2f}) < {alerte['seuil']}"
                
                    # Gestion des croisements (exemple pour MA)
                    elif alerte['indicateur'] == "Croisement MA":
                        if alerte['condition'] == "Croise vers le haut" and \
                            self.df['MA_50'].iloc[-1] > self.df['MA_200'].iloc[-1] and \
                            self.df['MA_50'].iloc[-2] <= self.df['MA_200'].iloc[-2]:
                            message = "🚨 Croisement haussier (MA50 > MA200)"
                        elif alerte['condition'] == "Croise vers le bas" and \
                            self.df['MA_50'].iloc[-1] < self.df['MA_200'].iloc[-1] and \
                            self.df['MA_50'].iloc[-2] >= self.df['MA_200'].iloc[-2]:
                            message = "🚨 Croisement baissier (MA50 < MA200)"
            
                    # Affichage de l'alerte si condition remplie
                    if message and not alerte['declenchee']:
                        st.toast(message, icon="🔔")
                        st.session_state.alertes[i]['declenchee'] = True
                    elif not message and alerte['declenchee']:
                        st.session_state.alertes[i]['declenchee'] = False
                    
            except KeyError as e:
                st.error(f"Erreur: Colonne {str(e)} manquante pour l'alerte")
    def _create_news_tab(self):
        with st.expander("📰 Actualités Financières"):
            if st.checkbox("Afficher les données simulées"):
                # Version simulée
                news = NewsFetcher().get_company_news(self.selected_ticker)
                reddit_data = RedditSentiment().analyze_ticker(self.selected_ticker)
            
                st.write("**Actualités (simulées):**")
                for item in news:
                    st.write(f"- {item['title']} ({item['sentiment']})")
            
                st.write("**Sentiment Reddit (simulé):**")
                st.write(f"Positif: {reddit_data['positive']}/{reddit_data['total']}")
            else:
                st.info("Activez les données simulées ou configurez des clés API")
    
    @classmethod
    def test_dashboard(cls):
        """Lance une démo du dashboard
    
        Exemple:
        >>> Dashboard.test_dashboard()
        """
        df = DataFetcher("TSLA").fetch_data(period="6mo")
        analyzer = TechnicalAnalyzer(df)
        analyzer.calcul_50_200_jours()
    
        dashboard = cls(analyzer.df)
        dashboard.display()