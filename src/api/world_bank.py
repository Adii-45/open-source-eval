"""
World Bank API Client
Fetches macroeconomic indicators from the World Bank Open Data API
"""

import requests
import pandas as pd
from typing import List, Dict
import time


class WorldBankAPI:
    """Client for interacting with World Bank API"""
    
    BASE_URL = "https://api.worldbank.org/v2"
    
    # World Bank Indicator Codes organized by category
    INDICATORS = {
        # POPULATION & DEMOGRAPHICS
        "population_total": "SP.POP.TOTL",
        "population_female": "SP.POP.TOTL.FE.IN",
        "population_male": "SP.POP.TOTL.MA.IN",
        "population_growth": "SP.POP.GROW",
        "life_expectancy_total": "SP.DYN.LE00.IN",
        "life_expectancy_female": "SP.DYN.LE00.FE.IN",
        "life_expectancy_male": "SP.DYN.LE00.MA.IN",
        "birth_rate": "SP.DYN.CBRT.IN",
        "death_rate": "SP.DYN.CDRT.IN",
        "fertility_rate": "SP.DYN.TFRT.IN",
        "contraceptive_prevalence": "SP.DYN.CONM.ZS",
        "rural_population": "SP.RUR.TOTL",
        "urban_population": "SP.URB.TOTL",
        "rural_population_pct": "SP.RUR.TOTL.ZS",
        "urban_population_pct": "SP.URB.TOTL.IN.ZS",
        "population_0_14": "SP.POP.0014.TO.ZS",
        "population_15_64": "SP.POP.1564.TO.ZS",
        "population_65_plus": "SP.POP.65UP.TO.ZS",
        
        # ECONOMY & GDP
        "gdp": "NY.GDP.MKTP.CD",
        "gdp_constant": "NY.GDP.MKTP.KD",
        "gdp_growth": "NY.GDP.MKTP.KD.ZG",
        "gdp_per_capita": "NY.GDP.PCAP.CD",
        "gdp_per_capita_constant": "NY.GDP.PCAP.KD",
        "gdp_per_capita_growth": "NY.GDP.PCAP.KD.ZG",
        "gni": "NY.GNP.MKTP.CD",
        "gni_per_capita": "NY.GNP.PCAP.CD",
        "adjusted_net_savings": "NY.ADJ.SVNG.GN.ZS",
        "exports": "NE.EXP.GNFS.CD",
        "imports": "NE.IMP.GNFS.CD",
        "exports_pct_gdp": "NE.EXP.GNFS.ZS",
        "imports_pct_gdp": "NE.IMP.GNFS.ZS",
        "net_oda": "BN.TRF.KOGT.CD",
        
        # PRICES, INFLATION & MONEY
        "inflation": "FP.CPI.TOTL.ZG",
        "cpi_index": "FP.CPI.TOTL",
        "real_interest_rate": "FR.INR.RINR",
        "lending_interest_rate": "FR.INR.LNDP",
        "deposit_interest_rate": "FR.INR.DPST",
        "money_supply_m2": "FM.LBL.MQMY.GD.ZS",
        "bank_assets_to_gdp": "GFDD.EI.01",
        "stock_market_cap": "GFDD.SM.01",
        
        # EMPLOYMENT & LABOR MARKET
        "unemployment": "SL.UEM.TOTL.ZS",
        "unemployment_female": "SL.UEM.TOTL.FE.ZS",
        "unemployment_male": "SL.UEM.TOTL.MA.ZS",
        "labor_force_total": "SL.TLF.TOTL.IN",
        "labor_force_female_pct": "SL.TLF.TOTL.FE.ZS",
        "employment_agriculture": "SL.AGR.EMPL.ZS",
        "employment_industry": "SL.IND.EMPL.ZS",
        "employment_services": "SL.SRV.EMPL.ZS",
        "labor_force_participation": "SL.TLF.CACT.ZS",
        "employment_to_population": "SL.TLF.ACTI.ZS",
        
        # EDUCATION
        "literacy_rate": "SE.ADT.LITR.ZS",
        "primary_enrollment": "SE.PRM.ENRR",
        "secondary_enrollment": "SE.SEC.ENRR",
        "tertiary_enrollment": "SE.TER.ENRR",
        "primary_completion": "SE.PRM.CMPT.ZS",
        "lower_secondary_completion": "SE.SEC.CMPT.LO.ZS",
        "upper_secondary_completion": "SE.SEC.CMPT.UP.ZS",
        "education_expenditure_gdp": "SE.XPD.TOTL.GD.ZS",
        "education_expenditure_gni": "SE.XPD.TOTL.ZS",
        "stem_enrollment": "UIS.FOSEP.56.F500",
        
        # HEALTH
        "health_expenditure_gdp": "SH.XPD.CHEX.GD.ZS",
        "health_expenditure_per_capita": "SH.XPD.CHEX.PC.CD",
        "hospital_beds": "SH.MED.BEDS.ZS",
        "maternal_mortality": "SH.STA.MMRT",
        "child_mortality": "SH.DYN.MORT",
        "neonatal_mortality": "SH.DYN.NMRT",
        "hiv_prevalence_0_14": "SH.HIV.0014.ZS",
        "hiv_prevalence_15_24": "SH.HIV.1524.ZS",
        "tuberculosis_incidence": "SH.TBS.INCD",
        "immunization_measles": "SH.IMM.MEAS",
        "immunization_dpt": "SH.IMM.IDPT",
        "alcohol_consumption": "SH.ALC.PCAP.LI",
        "smoking_female": "SH.PRV.SMOK.FE",
        "smoking_male": "SH.PRV.SMOK.MA",
        
        # POVERTY & INEQUALITY
        "poverty_headcount": "SI.POV.DDAY",
        "poverty_umic": "SI.POV.UMIC",
        "poverty_lmic": "SI.POV.LMIC",
        "poverty_national": "SI.POV.NAHC",
        "income_share_lowest_10": "SI.DST.FRST.10",
        "income_share_highest_20": "SI.DST.05TH.20",
        "income_share_middle_20": "SI.DST.03RD.20",
        "gini_index": "SI.POV.GINI",
        
        # ENVIRONMENT & CLIMATE
        "co2_per_capita": "EN.ATM.CO2E.PC",
        "co2_emissions": "EN.ATM.CO2E.KT",
        "co2_liquid_fuel": "EN.ATM.CO2E.LF.ZS",
        "greenhouse_gas": "EN.ATM.GHGT.KT.CE",
        "methane_emissions": "EN.ATM.METH.KT.CE",
        "nitrous_oxide": "EN.ATM.NOXE.KT.CE",
        "pm25_pollution": "EN.ATM.PM25.MC.M3",
        "fish_stocks_overexploited": "EN.FSH.THRD.NO",
        "forest_area_km2": "AG.LND.FRST.K2",
        "forest_area_pct": "AG.LND.FRST.ZS",
        "agricultural_land": "AG.LND.AGRI.ZS",
        "renewable_water": "ER.H2O.FWTL.K3",
        
        # ENERGY
        "energy_per_capita": "EG.USE.PCAP.KG.OE",
        "energy_total": "EG.USE.COMM.KT.OE",
        "electricity_access": "EG.ELC.ACCS.ZS",
        "renewable_electricity": "EG.ELC.RNEW.ZS",
        "electricity_fossil": "EG.ELC.FOSL.ZS",
        "electricity_oil": "EG.ELC.PETR.ZS",
        "electricity_coal": "EG.ELC.COAL.ZS",
        "electricity_nuclear": "EG.ELC.NUCL.ZS",
        
        # TRADE, BUSINESS & INDUSTRY
        "ease_of_business": "IC.BUS.EASE.XQ",
        "startup_costs": "IC.REG.COST.PC.FE.ZS",
        "contract_enforcement_days": "IC.LGL.DURS",
        "merchandise_trade": "TM.VAL.MRCH.CD.WT",
        "merchandise_exports": "TX.VAL.MRCH.XD.WT",
        "merchandise_imports": "TM.VAL.MRCH.XD.WT",
        "agriculture_value_added": "NV.AGR.TOTL.ZS",
        "industry_value_added": "NV.IND.TOTL.ZS",
        "services_value_added": "NV.SRV.TOTL.ZS",
        
        # DIGITAL, INFRASTRUCTURE & INNOVATION
        "internet_users": "IT.NET.USER.ZS",
        "mobile_subscriptions": "IT.CEL.SETS.P2",
        "mobile_broadband": "IT.CEL.SETS.P3",
        "rail_lines": "IS.RRS.TOTL.KM",
        "air_passengers": "IS.AIR.PSGR",
        "patent_applications_residents": "IP.PAT.RESD",
        "patent_applications_nonresidents": "IP.PAT.NRES",
        "trademark_applications": "IP.TMK.TOTL",
        "industrial_design_applications": "IP.IDS.TOTL"
    }
    
    # Indicator categories for organized display
    INDICATOR_CATEGORIES = {
        "POPULATION & DEMOGRAPHICS": {
            "Population, total": "population_total",
            "Female population": "population_female",
            "Male population": "population_male",
            "Population growth (%)": "population_growth",
            "Life expectancy at birth (total)": "life_expectancy_total",
            "Life expectancy (female)": "life_expectancy_female",
            "Life expectancy (male)": "life_expectancy_male",
            "Birth rate": "birth_rate",
            "Death rate": "death_rate",
            "Fertility rate": "fertility_rate",
            "Contraceptive prevalence": "contraceptive_prevalence",
            "Rural population": "rural_population",
            "Urban population": "urban_population",
            "Rural population (% of total)": "rural_population_pct",
            "Urban population (% of total)": "urban_population_pct",
            "Population ages 0-14 (%)": "population_0_14",
            "Population ages 15-64 (%)": "population_15_64",
            "Population 65+ (%)": "population_65_plus"
        },
        "ECONOMY & GDP": {
            "GDP (current US$)": "gdp",
            "GDP (constant 2015 US$)": "gdp_constant",
            "GDP growth (%)": "gdp_growth",
            "GDP per capita (current US$)": "gdp_per_capita",
            "GDP per capita (constant 2015 US$)": "gdp_per_capita_constant",
            "GDP per capita growth (%)": "gdp_per_capita_growth",
            "GNI (current US$)": "gni",
            "GNI per capita (current US$)": "gni_per_capita",
            "Adjusted net savings (% of GNI)": "adjusted_net_savings",
            "Exports of goods and services (US$)": "exports",
            "Imports of goods and services (US$)": "imports",
            "Exports (% of GDP)": "exports_pct_gdp",
            "Imports (% of GDP)": "imports_pct_gdp",
            "Net official development assistance": "net_oda"
        },
        "PRICES, INFLATION & MONEY": {
            "Inflation, consumer prices (%)": "inflation",
            "CPI (index)": "cpi_index",
            "Real interest rate": "real_interest_rate",
            "Lending interest rate": "lending_interest_rate",
            "Deposit interest rate": "deposit_interest_rate",
            "Money supply (M2 % of GDP)": "money_supply_m2",
            "Bank assets to GDP (%)": "bank_assets_to_gdp",
            "Stock market capitalization (% of GDP)": "stock_market_cap"
        },
        "EMPLOYMENT & LABOR MARKET": {
            "Unemployment rate (%)": "unemployment",
            "Unemployment (female)": "unemployment_female",
            "Unemployment (male)": "unemployment_male",
            "Labor force, total": "labor_force_total",
            "Female labor force (% of total)": "labor_force_female_pct",
            "Employment in agriculture (%)": "employment_agriculture",
            "Employment in industry (%)": "employment_industry",
            "Employment in services (%)": "employment_services",
            "Labor force participation rate": "labor_force_participation",
            "Employment-to-population ratio": "employment_to_population"
        },
        "EDUCATION": {
            "Literacy rate, adult (%)": "literacy_rate",
            "Primary school enrollment": "primary_enrollment",
            "Secondary school enrollment": "secondary_enrollment",
            "Tertiary school enrollment": "tertiary_enrollment",
            "Primary completion rate": "primary_completion",
            "Lower secondary completion rate": "lower_secondary_completion",
            "Upper secondary completion rate": "upper_secondary_completion",
            "Government expenditure on education": "education_expenditure_gdp",
            "Education expenditure (% of GNI)": "education_expenditure_gni",
            "STEM enrollment ratio": "stem_enrollment"
        },
        "HEALTH": {
            "Health expenditure (% of GDP)": "health_expenditure_gdp",
            "Health expenditure per capita (US$)": "health_expenditure_per_capita",
            "Hospital beds per 1,000 people": "hospital_beds",
            "Maternal mortality ratio": "maternal_mortality",
            "Mortality rate, under-5": "child_mortality",
            "Neonatal mortality rate": "neonatal_mortality",
            "HIV prevalence (ages 0–14)": "hiv_prevalence_0_14",
            "HIV prevalence (ages 15–24)": "hiv_prevalence_15_24",
            "Tuberculosis incidence": "tuberculosis_incidence",
            "Immunization, measles (%)": "immunization_measles",
            "Immunization, DPT (%)": "immunization_dpt",
            "Alcohol consumption per capita": "alcohol_consumption",
            "Smoking prevalence (female)": "smoking_female",
            "Smoking prevalence (male)": "smoking_male"
        },
        "POVERTY & INEQUALITY": {
            "Poverty headcount ratio ($2.15/day)": "poverty_headcount",
            "Poverty at upper-middle-income lines": "poverty_umic",
            "Poverty at lower-middle-income lines": "poverty_lmic",
            "Poverty national headcount ratio": "poverty_national",
            "Income share held by lowest 10%": "income_share_lowest_10",
            "Income share held by highest 20%": "income_share_highest_20",
            "Income share middle 20%": "income_share_middle_20",
            "Gini index": "gini_index"
        },
        "ENVIRONMENT & CLIMATE": {
            "CO2 emissions (tons per capita)": "co2_per_capita",
            "CO2 emissions (kt)": "co2_emissions",
            "CO2 emissions from liquid fuel (%)": "co2_liquid_fuel",
            "Greenhouse gas emissions (kt CO2 eq.)": "greenhouse_gas",
            "Methane emissions": "methane_emissions",
            "Nitrous oxide emissions": "nitrous_oxide",
            "PM2.5 air pollution (µg/m³)": "pm25_pollution",
            "Fish stocks overexploited (%)": "fish_stocks_overexploited",
            "Forest area (sq. km)": "forest_area_km2",
            "Forest area (% of land)": "forest_area_pct",
            "Agricultural land (%)": "agricultural_land",
            "Renewable water resources": "renewable_water"
        },
        "ENERGY": {
            "Energy use per capita (kg oil equivalent)": "energy_per_capita",
            "Total energy use (kt of oil equivalent)": "energy_total",
            "Access to electricity (%)": "electricity_access",
            "Renewable electricity output (%)": "renewable_electricity",
            "Electricity from fossil fuels (%)": "electricity_fossil",
            "Electricity from oil (%)": "electricity_oil",
            "Electricity from coal (%)": "electricity_coal",
            "Electricity from nuclear (%)": "electricity_nuclear"
        },
        "TRADE, BUSINESS & INDUSTRY": {
            "Ease of doing business index": "ease_of_business",
            "Start-up costs (% of income per capita)": "startup_costs",
            "Time to enforce contracts (days)": "contract_enforcement_days",
            "Merchandise trade (% of GDP)": "merchandise_trade",
            "Merchandise exports": "merchandise_exports",
            "Merchandise imports": "merchandise_imports",
            "Agriculture value added (% of GDP)": "agriculture_value_added",
            "Industry value added (% of GDP)": "industry_value_added",
            "Services value added (% of GDP)": "services_value_added"
        },
        "DIGITAL, INFRASTRUCTURE & INNOVATION": {
            "Internet users (% of population)": "internet_users",
            "Mobile subscriptions (per 100 people)": "mobile_subscriptions",
            "Mobile broadband subscriptions": "mobile_broadband",
            "Rail lines (total km)": "rail_lines",
            "Air transport, passengers carried": "air_passengers",
            "Patent applications (residents)": "patent_applications_residents",
            "Patent applications (non-residents)": "patent_applications_nonresidents",
            "Trademark applications": "trademark_applications",
            "Industrial design applications": "industrial_design_applications"
        }
    }
    
    # Popular countries for quick selection
    POPULAR_COUNTRIES = {
        # G7 Countries
        "USA": "United States",
        "JPN": "Japan",
        "DEU": "Germany",
        "GBR": "United Kingdom",
        "FRA": "France",
        "ITA": "Italy",
        "CAN": "Canada",
        
        # BRICS Nations
        "BRA": "Brazil",
        "RUS": "Russian Federation",
        "IND": "India",
        "CHN": "China",
        "ZAF": "South Africa",
        
        # Major European Economies
        "ESP": "Spain",
        "NLD": "Netherlands",
        "CHE": "Switzerland",
        "POL": "Poland",
        "SWE": "Sweden",
        "BEL": "Belgium",
        "AUT": "Austria",
        "NOR": "Norway",
        "DNK": "Denmark",
        "IRL": "Ireland",
        "FIN": "Finland",
        "PRT": "Portugal",
        "GRC": "Greece",
        "CZE": "Czech Republic",
        "ROU": "Romania",
        "HUN": "Hungary",
        
        # Asia-Pacific
        "KOR": "Korea, Rep.",
        "AUS": "Australia",
        "IDN": "Indonesia",
        "THA": "Thailand",
        "SGP": "Singapore",
        "MYS": "Malaysia",
        "PHL": "Philippines",
        "VNM": "Vietnam",
        "PAK": "Pakistan",
        "BGD": "Bangladesh",
        "NZL": "New Zealand",
        "HKG": "Hong Kong SAR, China",
        "TWN": "Taiwan, China",
        
        # Middle East & North Africa
        "SAU": "Saudi Arabia",
        "TUR": "Turkey",
        "EGY": "Egypt, Arab Rep.",
        "IRN": "Iran, Islamic Rep.",
        "IRQ": "Iraq",
        "ARE": "United Arab Emirates",
        "ISR": "Israel",
        "QAT": "Qatar",
        "KWT": "Kuwait",
        "DZA": "Algeria",
        "MAR": "Morocco",
        "JOR": "Jordan",
        "LBN": "Lebanon",
        
        # Latin America
        "MEX": "Mexico",
        "ARG": "Argentina",
        "COL": "Colombia",
        "CHL": "Chile",
        "PER": "Peru",
        "VEN": "Venezuela, RB",
        "ECU": "Ecuador",
        "URY": "Uruguay",
        "CRI": "Costa Rica",
        "PAN": "Panama",
        
        # Africa
        "NGA": "Nigeria",
        "KEN": "Kenya",
        "ETH": "Ethiopia",
        "GHA": "Ghana",
        "TZA": "Tanzania",
        "UGA": "Uganda",
        "CIV": "Cote d'Ivoire",
        "SEN": "Senegal",
        "CMR": "Cameroon",
        "AGO": "Angola",
        
        # Other Major Economies
        "UKR": "Ukraine",
        "KAZ": "Kazakhstan",
        "LKA": "Sri Lanka",
        "MNG": "Mongolia",
        "ISL": "Iceland"
    }
    
    def __init__(self):
        self.session = requests.Session()
    
    def fetch_indicator(
        self,
        indicator_code: str,
        country_codes: List[str],
        start_year: int = 2000,
        end_year: int = 2023
    ) -> pd.DataFrame:
        """
        Fetch indicator data for specified countries and years
        
        Args:
            indicator_code: World Bank indicator code
            country_codes: List of ISO country codes (e.g., ['USA', 'CHN'])
            start_year: Starting year for data
            end_year: Ending year for data
            
        Returns:
            DataFrame with columns: country, country_code, year, value
        """
        all_data = []
        
        for country_code in country_codes:
            try:
                data = self._fetch_country_indicator(
                    indicator_code, 
                    country_code, 
                    start_year, 
                    end_year
                )
                all_data.extend(data)
                time.sleep(0.1)  # Rate limiting - be nice to the API
            except Exception as e:
                print(f"Error fetching data for {country_code}: {e}")
                continue
        
        if not all_data:
            return pd.DataFrame(columns=['country', 'country_code', 'year', 'value'])
        
        df = pd.DataFrame(all_data)
        df = df.sort_values(['country', 'year']).reset_index(drop=True)
        return df
    
    def _fetch_country_indicator(
        self,
        indicator_code: str,
        country_code: str,
        start_year: int,
        end_year: int
    ) -> List[Dict]:
        """Fetch data for a single country"""
        
        url = f"{self.BASE_URL}/country/{country_code}/indicator/{indicator_code}"
        params = {
            "date": f"{start_year}:{end_year}",
            "format": "json",
            "per_page": 1000
        }
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        json_data = response.json()
        
        # World Bank API returns [metadata, data] array
        if len(json_data) < 2 or json_data[1] is None:
            return []
        
        data_records = []
        for entry in json_data[1]:
            if entry['value'] is not None:
                data_records.append({
                    'country': entry['country']['value'],
                    'country_code': entry['countryiso3code'],
                    'year': int(entry['date']),
                    'value': float(entry['value'])
                })
        
        return data_records
    
    def fetch_by_indicator_key(
        self,
        indicator_key: str,
        country_codes: List[str],
        start_year: int = 2000,
        end_year: int = 2023
    ) -> pd.DataFrame:
        """
        Fetch data for any indicator using its key name
        
        Args:
            indicator_key: Key from INDICATORS dict (e.g., 'gdp', 'population_total')
            country_codes: List of ISO country codes
            start_year: Starting year
            end_year: Ending year
            
        Returns:
            DataFrame with indicator data
        """
        if indicator_key not in self.INDICATORS:
            raise ValueError(f"Unknown indicator key: {indicator_key}")
        
        return self.fetch_indicator(
            self.INDICATORS[indicator_key],
            country_codes,
            start_year,
            end_year
        )
    
    
    def get_all_countries(self) -> Dict[str, str]:
        """
        Fetch list of all countries from World Bank API
        
        Returns:
            Dictionary mapping country codes to country names
        """
        url = f"{self.BASE_URL}/country"
        params = {
            "format": "json",
            "per_page": 500
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            json_data = response.json()
            
            if len(json_data) < 2:
                return self.POPULAR_COUNTRIES
            
            countries = {}
            for country in json_data[1]:
                # Filter out regions and aggregates
                if country['capitalCity']:  # Only actual countries have capitals
                    code = country['iso2Code']
                    name = country['name']
                    if len(code) == 2 or len(code) == 3:  # Valid country codes
                        countries[code] = name
            
            return countries if countries else self.POPULAR_COUNTRIES
            
        except Exception as e:
            print(f"Error fetching countries: {e}")
            return self.POPULAR_COUNTRIES


# Singleton instance
wb_api = WorldBankAPI()
