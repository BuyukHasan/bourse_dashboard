import streamlit as st
from src.technical_analyzer import TechnicalAnalyzer
from datetime import datetime
from src.data_fetcher import DataFetcher
from src.visualizer import Visualizer

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
        
        # Bouton pour appliquer les changements
        if st.sidebar.button("Appliquer les changements"):
            self._reload_data()
    def _reload_data(self):
        """Recharge les données avec les nouveaux paramètres"""
        fetcher = DataFetcher(self.selected_ticker)
        new_df = fetcher.fetch_data(
            start=self.start_date, 
            end=self.end_date
        )
        
        if not new_df.empty:
            analyzer = TechnicalAnalyzer(new_df)
            analyzer.calcul_50_200_jours()
            analyzer.add_rsi()
            analyzer.calculate_volatility()
            self.df = new_df
            st.session_state.df = new_df  # Mettre à jour l'état de session
            st.rerun()  # Forcer le rafraîchissement
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
            st.plotly_chart(fig.fig, use_container_width=True, key=f"candlestick_{datetime.now().timestamp()}")
        
        with tab2:
            fig_vol = Visualizer(self.df, rows=1, columns=1)
            fig_vol.draw_volume()
            st.plotly_chart(fig_vol.fig, use_container_width=True, key=f"volume_{datetime.now().timestamp()}")
        
        with tab3:
            st.dataframe(
                self.df,
                height=400,
                use_container_width=True,
                column_order=["Date", "Open", "High", "Low", "Close", "Volume"],
                hide_index=False,
                key=f"dataframe_{datetime.now().timestamp()}"
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
        """Version avec suppression des éléments existants"""
        container = st.container()
        with container:
            self._create_sidebar_controls()
            self._display_kpis()
            self._create_analysis_tabs()
            self._add_data_download()
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