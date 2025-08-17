

class AssetCategories:
    CATEGORIES = {
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
            "UCO", "SCO", "BOIL", "KOLD", "WEat", "CORN", "SOYB", "CANE", "CPER", "PALL", 
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
    @classmethod
    def get_all_categories(cls):
        return cls.CATEGORIES

    @classmethod
    def get_all_tickers(cls):
        """Retourne une liste unique de tous les tickers"""
        all_tickers = []
        for category in cls.CATEGORIES.values():
            all_tickers.extend(category)
        return sorted(set(all_tickers))

    @classmethod
    def get_tickers_by_category(cls, category_name):
        """Retourne les tickers d'une catégorie spécifique"""
        return cls.CATEGORIES.get(category_name, [])