import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Import local modules
from src.data_fetcher import DataFetcher
from src.technical_analyzer import TechnicalAnalyzer
from src.visualizer import Visualizer
from src.news_fetcher import NewsFetcher
from src.reddit_analyzer import RedditSentiment
from src.geo_data import GeoDataFetcher
from src.asset_categories import AssetCategories
from src.macro_data import MacroData

class Dashboard:
    """Class to create financial dashboard"""
    
    def __init__(self, data_frame):
        """
        Initialize dashboard with data frame
        
        Args:
            data_frame (pd.DataFrame): Input financial data
        """
        # Get extended asset categories
        self.asset_categories = AssetCategories.get_all_categories()
        
        # Find initial ticker from data
        self.ticker = self._find_initial_ticker(data_frame)
        self.default_start_date = datetime.now().replace(year=datetime.now().year-1)
        self.default_end_date = datetime.now()
        self.df = data_frame
        if 'theme_colors' not in st.session_state:
            st.session_state.theme_colors = self._get_theme_colors("Neon Cyberpunk")
    
    def _find_initial_ticker(self, df):
        """Find initial ticker from data"""
        # If DataFrame contains 'Ticker' column, use first value
        if 'Ticker' in df.columns:
            return df['Ticker'].iloc[0]
        # Otherwise, use first ticker in categories
        return self.asset_categories["Technology"][0]
        
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
                "primary": "#001100",  # Darker
                "secondary": "#00cc00",  # Bright but less aggressive green
                "background": "#000800",  # Darker background
                "accent1": "#00aa00",
                "accent2": "#008800",
                "text": "#e0ffe0"  # Very light green text
            },
            "Galactic Purple": {
                "primary": "#0d000d",
                "secondary": "#cc00ff",
                "background": "#080008",  # Darker
                "accent1": "#9900ff",
                "accent2": "#ff00cc",
                "text": "#f0e0ff"  # Light purple text
            }
        }
        return themes.get(theme_name, themes["Neon Cyberpunk"]) 
        
    def _create_sidebar_controls(self):
        """Create sidebar controls for dashboard"""
        # Find current ticker's category
        current_category = None
        for category, tickers in self.asset_categories.items():
            if self.ticker in tickers:
                current_category = category
                break
        
        if current_category is None:
            current_category = "Stocks"
        
        # Selection widgets
        selected_category = st.sidebar.selectbox(
            "Category", 
            list(self.asset_categories.keys()),
            index=list(self.asset_categories.keys()).index(current_category)
        )
        
        ticker_options = self.asset_categories[selected_category]
    
        # Verify if current ticker is in options
        if self.ticker in ticker_options:
            ticker_index = ticker_options.index(self.ticker)
        else:
            ticker_index = 0  # Take first ticker by default
        
        self.selected_ticker = st.sidebar.selectbox(
            "Ticker", 
            ticker_options,
            index=ticker_index  # Use calculated index
        )
        
        start_value = st.session_state.get('dashboard_start_date', self.default_start_date)
        end_value = st.session_state.get('dashboard_end_date', self.default_end_date)
        
        self.start_date = st.sidebar.date_input(
            "Start date:", 
            value=start_value,
            key="dashboard_start_date"
        )
        self.end_date = st.sidebar.date_input(
            "End date:", 
            value=end_value,
            key="dashboard_end_date"
        )
        
        if st.sidebar.button("Apply changes"):
            self._reload_data()
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("🎨 Theme Customization")
        new_theme = st.sidebar.selectbox(
            "Visual theme",
            ["Neon Cyberpunk", "Lava Explosion", "Electric Ocean", "Acid Jungle", "Galactic Purple"],
            index=0,
            key="dashboard_theme_selector"
        )
    
        if new_theme != st.session_state.get('current_theme'):
            st.session_state.theme = new_theme
            st.session_state.current_theme = new_theme
            st.rerun()
    
    def _reload_data(self):
        """Load data with caching"""
        # Create unique cache key
        cache_key = f"{self.selected_ticker}_{self.start_date}_{self.end_date}"
        
        # Check cache
        if 'data_cache' in st.session_state and cache_key in st.session_state.data_cache:
            self.df = st.session_state.data_cache[cache_key]
            st.session_state.df = self.df
            st.rerun()
            return
            
        """Load data synchronously"""
        with st.status(f"**Loading data for {self.selected_ticker}...**", expanded=True) as status:
            st.write("Retrieving data from Yahoo Finance")
            progress_bar = st.progress(0)
            
            try:
                # Convert dates to string format
                start_str = self.start_date.strftime("%Y-%m-%d")
                end_str = self.end_date.strftime("%Y-%m-%d")
                
                fetcher = DataFetcher(self.selected_ticker)
                progress_bar.progress(30)
                new_df = fetcher.fetch_data(start=start_str, end=end_str)
                
                if new_df.empty:
                    status.update(label="No data available for these parameters", state="error")
                    st.error("Check selected ticker and dates")
                    return
                    
                st.write("Processing data (calculating technical indicators)")
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
                status.update(label="Data updated successfully!", state="complete")
                st.rerun()
                
            except Exception as e:
                status.update(label="Error during loading", state="error")
                st.error(f"Error: {str(e)}")
        if 'data_cache' not in st.session_state:
            st.session_state.data_cache = {}
            st.session_state.data_cache[cache_key] = self.df
            
    def _display_kpis(self):
        """Display key indicators with improved style"""
        cols = st.columns(4)
    
        price_change = self.df['Close'].pct_change().iloc[-1] * 100
        cols[0].metric(
            label="💰 Current price",
            value=f"{self.df['Close'].iloc[-1]:.2f} $",
            delta=f"{price_change:.2f}%",
            delta_color="normal",
            help="Last closing price with daily variation"
        )
    
        volatility = self.df['Volatility'].iloc[-1] * 100
        volatility_icon = "📈" if volatility < 5 else "📉" if volatility > 15 else "📊"
        cols[1].metric(
            label=f"{volatility_icon} Volatility (30d)",
            value=f"{volatility:.1f}%",
            help="Annualized 30-day volatility"
        )
    
        volume = self.df['Volume'].iloc[-1]
        cols[2].metric(
            label="📦 Daily volume",
            value=f"{volume/1e6:.1f}M",
            help="Traded volume in millions"
        )
    
        if 'rsi' in self.df.columns:
            rsi_value = self.df['rsi'].iloc[-1]
            rsi_status = "Buy" if rsi_value < 30 else "Sell" if rsi_value > 70 else "Neutral"
            cols[3].metric(
                label=f"📊 RSI (14d) - {rsi_status}",
                value=f"{rsi_value:.1f}",
                help="Relative Strength Index - <30: Oversold, >70: Overbought"
            )
        
        # Market Mood (new section)
        st.markdown("---")
        self._display_market_mood()
        
        # Risk/Reward gauge
        self._display_risk_reward()

        # Add after risk/reward gauge
        self._display_macro_context()
        
    def _display_macro_context(self):
        """Display macroeconomic context"""
        st.markdown("---")
        st.subheader("🌐 Macro-economic Context")
        
        with st.spinner("Loading macro data..."):
            macro_fetcher = MacroData()
            
            macro_df, errors = macro_fetcher.fetch_macro_data(period="1y")
            
            # Display errors
            if errors:
                for indicator, error in errors.items():
                    st.warning(f"{indicator}: {error}")
                    
            if macro_df.empty:
                st.warning("No macro data available")
                return
                
            # Display indicators even with few points
            cols = st.columns(4)
            indicators = list(macro_df.columns)[:4]
            
            for i, indicator in enumerate(indicators):
                try:
                    # Use last available value
                    value = macro_df[indicator].iloc[-1]
                    cols[i].metric(label=indicator, value=f"{value:.2f}")
                except:
                    cols[i].metric(label=indicator, value="N/A")
            
            # Display chart even with little data
            st.markdown("**Macro-economic trends**")
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
            "📈 Main Chart", 
            "📊 Technical Analysis", 
            "🔍 Raw Data",
            "📰 News & Sentiment",
            "🌍 Geographical Influence" 
        ])

        with tab1:
            st.markdown("#### Price evolution with moving averages")
            fig = Visualizer(self.df, rows=1, columns=1)
            fig.draw_candlestick().MA_draw(overlay=True)
            fig.show(title=f"Analysis of {self.selected_ticker}")
        
            st.markdown("##### Recent trends")
            col1, col2 = st.columns(2)
            with col1:
                last_5_days = self.df['Close'].pct_change(5).iloc[-1] * 100
                st.metric("Last 5 days", f"{last_5_days:.2f}%")
            with col2:
                last_month = self.df['Close'].pct_change(20).iloc[-1] * 100
                st.metric("1 month", f"{last_month:.2f}%")

        with tab2:
            st.markdown("#### Complete technical analysis")
            cols = st.columns(2)
        
            with cols[0]:
                st.markdown("##### Key indicators")
                fig1 = Visualizer(self.df, rows=2, columns=1, row_heights=[0.7, 0.3])
                fig1.draw_candlestick().Rsi_draw(show_zones=True)
                fig1.show()
            
            with cols[1]:
                st.markdown("##### Volume and volatility")
                fig2 = Visualizer(self.df, rows=2, columns=1, row_heights=[0.5, 0.5])
                fig2.draw_volume().draw_cumulative_returns()
                fig2.show()

        with tab3:
            st.markdown("#### Historical data")
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
        @st.cache_data(ttl=86400)  # 24h cache
        def get_cached_geo_data(ticker):
            fetcher = GeoDataFetcher()
            return fetcher.get_geo_data(ticker)
            
        """Display geographical influence map with Plotly"""
        st.subheader("Geographical Influence")
        
        fetcher = GeoDataFetcher()
        geo_data = get_cached_geo_data(self.selected_ticker)
        df_geo = fetcher.to_dataframe(geo_data)
        
        if df_geo.empty:
            st.warning("No geographical data available for this ticker")
            return
        
        # Create map with Plotly
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
            title=f"Geographical exposure of {self.selected_ticker}"
        )
        
        # Customize style according to theme
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
        
        # Display data as table
        with st.expander("View detailed data"):
            st.dataframe(
                df_geo[['country', 'weight']].sort_values('weight', ascending=False),
                column_config={
                    "country": "Country",
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
        st.subheader("📰 News and Sentiment Analysis")
    
        news = NewsFetcher().get_company_news(self.selected_ticker)
        reddit_data = RedditSentiment().analyze_ticker(self.selected_ticker)
    
        news_scores = [item['score'] for item in news]
        avg_news_score = sum(news_scores) / len(news_scores) if news_scores else 0
    
        reddit_score = (reddit_data['positive'] - reddit_data['negative']) / reddit_data['total']
    
        global_score = (avg_news_score + reddit_score) / 2
        
        st.markdown("### Investment Recommendation")
        if global_score > 0.3:
            st.success("✅ **Favorable to buy** - Very positive sentiment")
        elif global_score > -0.2:
            st.info("🟢 **Moderate opportunity** - Generally neutral sentiment")
        else:
            st.warning("⚠️ **Caution** - Dominant negative sentiment")
        
        st.metric("Confidence score", f"{global_score:.2f}/1.0")
        
        st.markdown("### Latest news")
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
        
        st.markdown("### Social media sentiment")
        st.progress((reddit_data['positive'] / reddit_data['total']))
        st.caption(f"Positive: {reddit_data['positive']} | Neutral: {reddit_data['neutral']} | Negative: {reddit_data['negative']}")
        
    def _display_market_mood(self):
        """Display market mood with giant emojis"""
        # Calculate trends
        last_5_days = self.df['Close'].pct_change(5).iloc[-1] * 100
        last_month = self.df['Close'].pct_change(20).iloc[-1] * 100
        
        # Determine mood
        if last_5_days > 5:
            mood = "🚀"  # Strong rise
            explanation = "Strong recent gain"
        elif last_5_days < -5:
            mood = "😱"  # Crash
            explanation = "Strong recent decline"
        elif last_month > 10:
            mood = "📈"  # Bullish trend
            explanation = "Good monthly trend"
        elif last_month < -10:
            mood = "📉"  # Bearish trend
            explanation = "Negative monthly trend"
        else:
            mood = "🥱"  # Stagnation
            explanation = "Stagnant market"
        
        # Stylized display
        st.markdown(f"""
        <div style="text-align:center; margin: 30px 0;">
            <div style="font-size: 80px; margin-bottom: 10px;">{mood}</div>
            <div style="font-size: 20px; color: {st.session_state.theme_colors['accent1']}">
                {explanation}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    def _display_risk_reward(self):
        """Display risk/reward gauge"""
        volatility = self.df['Volatility'].iloc[-1] * 100  # Volatility in %
        
        # Determine risk level
        if volatility < 5:
            level = "🟢 Low"
            position = 25
            color = "#00ff00"
        elif volatility < 15:
            level = "🟡 Moderate"
            position = 50
            color = "#ffff00"
        else:
            level = "🔴 High"
            position = 85
            color = "#ff0000"
        
        # Display gauge
        st.markdown(f"""
        <div style="margin: 30px 0; text-align: center;">
            <div style="font-size: 20px; margin-bottom: 10px; color: {st.session_state.theme_colors['text']}">
                Risk/Reward Ratio
            </div>
            <div style="background: #333; height: 30px; border-radius: 15px; position: relative; margin: 0 auto; max-width: 600px;">
                <div style="position: absolute; width: 100%; display: flex; justify-content: space-between; padding: 0 10px;">
                    <span>High</span>
                    <span>Balanced</span>
                    <span>Low</span>
                </div>
                <div style="background: linear-gradient(to right, #ff0000, #ffff00, #00ff00); 
                            height: 100%; border-radius: 15px; opacity: 0.6;"></div>
                <div style="position: absolute; top: -5px; left: {position}%; 
                            transform: translateX(-50%); width: 10px; height: 40px; 
                            background: {color}; border-radius: 5px;"></div>
            </div>
            <div style="font-size: 24px; margin-top: 10px; color: {color}">
                {level} • Volatility: {volatility:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    def _add_data_download(self):
        """Add data download button"""
        csv_data = self.df.to_csv(index=False).encode('utf-8')
        today = datetime.now().strftime("%Y-%m-%d")
        st.download_button(
            label="📥 Download data",
            data=csv_data,
            file_name=f'stock_data_{today}.csv',
            mime='text/csv',
            key=f"download_btn_{datetime.now().timestamp()}"
        )
    

    def display(self):
        """Display dashboard with alert system"""
        container = st.container()
        with container:
            self._create_sidebar_controls()
            self._create_alert_system()
            
            # Verify if data is loaded
            if not hasattr(self, 'df') or self.df.empty:
                st.warning("Loading initial data...")
                self._reload_data()
                return
    
            if hasattr(self, 'df'):
                self._check_alerts()
                self._display_kpis()
                self._create_analysis_tabs()
                self._add_data_download()
                
    def _create_alert_system(self):
        """Visually improved alert system"""
        with st.sidebar.expander("🔔 Alert System", expanded=True):
            if 'alerts' not in st.session_state:
                st.session_state.alerts = []
        
            with st.form("alert_form", clear_on_submit=True):
                cols = st.columns(2)
                with cols[0]:
                    indicator = st.selectbox(
                        "Indicator",
                        ["RSI", "Closing Price", "Volatility", "MA Crossover"],
                        key="alert_indicator"
                    )
                    condition = st.selectbox(
                        "Condition",
                        ["Above", "Below", "Crosses above", "Crosses below"],
                        key="alert_condition"
                    )
            
                with cols[1]:
                    threshold = st.number_input(
                        "Threshold",
                        min_value=0.0,
                        max_value=1000.0 if indicator == "Closing Price" else 100.0,
                        value=30.0 if indicator == "RSI" else 50.0,
                        step=0.1,
                        key="alert_threshold"
                    )
                    color = st.color_picker(
                        "Alert color",
                        value="#FF4B4B",
                        key="alert_color"
                    )
            
                if st.form_submit_button("➕ Add alert", use_container_width=True):
                    new_alert = {
                        'indicator': indicator,
                        'condition': condition,
                        'threshold': threshold,
                        'color': color,
                        'active': True,
                        'triggered': False
                    }
                    st.session_state.alerts.append(new_alert)
                    st.success("Alert saved!")
        
            if st.session_state.alerts:
                st.markdown("---")
                st.markdown("**My active alerts**")
            
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
                elif alert['indicator'] == "Closing Price":
                    current_value = self.df['Close'].iloc[-1]
                elif alert['indicator'] == "Volatility":
                    current_value = self.df['Volatility'].iloc[-1] * 100
            
                if current_value is not None:
                    if alert['condition'] == "Above" and current_value > alert['threshold']:
                        message = f"🚨 {alert['indicator']} ({current_value:.2f}) > {alert['threshold']}"
                    elif alert['condition'] == "Below" and current_value < alert['threshold']:
                        message = f"🚨 {alert['indicator']} ({current_value:.2f}) < {alert['threshold']}"
                
                    elif alert['indicator'] == "MA Crossover":
                        if alert['condition'] == "Crosses above" and \
                            self.df['MA_50'].iloc[-1] > self.df['MA_200'].iloc[-1] and \
                            self.df['MA_50'].iloc[-2] <= self.df['MA_200'].iloc[-2]:
                            message = "🚨 Bullish crossover (MA50 > MA200)"
                        elif alert['condition'] == "Crosses below" and \
                            self.df['MA_50'].iloc[-1] < self.df['MA_200'].iloc[-1] and \
                            self.df['MA_50'].iloc[-2] >= self.df['MA_200'].iloc[-2]:
                            message = "🚨 Bearish crossover (MA50 < MA200)"
            
                    if message and not alert['triggered']:
                        st.toast(message, icon="🔔")
                        st.session_state.alerts[i]['triggered'] = True
                    elif not message and alert['triggered']:
                        st.session_state.alerts[i]['triggered'] = False
                    
            except KeyError as e:
                st.error(f"Error: Missing column {str(e)} for alert")
                
    @classmethod
    def test_dashboard(cls):
        """Launch a dashboard demo"""
        df = DataFetcher("TSLA").fetch_data(period="6mo")
        analyzer = TechnicalAnalyzer(df)
        analyzer.compute_50_200_days()
    
        dashboard = cls(analyzer.df)
        dashboard.display()