# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 09:18:54 2022

@author: RobWen
Version: 0.4.0
"""

# Packages
import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup

# Header
from .TickerRequest import *

class YahooRequest(TickerRequest):
    def __init__(self, ticker, headers_standard):
        super().__init__(ticker, headers_standard)
        self.__headers_standard = headers_standard

    ###########################
    ###                     ###
    ###     Yahoo Finance   ###
    ###        Requests     ###
    ###                     ###
    ###########################

    @property
    def statistics(self):
        return self.__yahoo_statistics_abfrage()

    @property
    def statistics_p(self):
        return self.__yahoo_statistics_df_p()

    #######################
    ###                 ###
    ###  Yahoo Finance  ###
    ###      Data       ###
    ###                 ###
    #######################

    # Führt eine Abfrage durch um das Symbol zu finden
    def __yahoo_statistics_abfrage(self):

        if self.__yahoo_statistics_df_() is None:
            if self.__yahoo_query_df() != None:
                self.ticker = self.__yahoo_query_df()

        return self.__yahoo_statistics_df_()

    def __yahoo_query_df(self):
        url = "https://query2.finance.yahoo.com/v1/finance/search"
        params = {'q': f'{self.ticker}', 'quotesCount': 1, 'newsCount': 0}

        r = requests.get(url, params=params, headers = self.__headers_standard)

        try:
            symbol = r.json()['quotes'][0]['symbol']
        except:
            return None

        return symbol

    ### Yahoo Finance Statistics                                 ###
    ### e.g. https://finance.yahoo.com/quote/NVDA/key-statistics ###
    ### Rückgabe None implementiert und getestet                 ###
    ### Ungültige Werte = NaN implementiert                      ###
    def __yahoo_statistics_df_(self):
        url = f'https://finance.yahoo.com/quote/{self.ticker}/key-statistics'

        with requests.session():
            page = requests.get(url, headers = self.__headers_standard)
            page = BeautifulSoup(page.content, 'html.parser')
            table = page.find_all('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})

            if len(table) == 0:
                self.__yahoo_statistics_df = None
            else:
                headlines = page.find_all('h3', {'class': 'Mt(20px)'})

                valuation_measures = []
                n = 9
                v = page.find_all('h2', {'class': 'Pt(20px)'})[0].text
                valuation_measures += n * [v]

                stock_price_history = []
                n = 7
                v = headlines[0].text
                stock_price_history += n * [v]

                share_statistics = []
                n = 12
                v = headlines[1].text
                share_statistics += n * [v]

                dividends_splits = []
                n = 10
                v = headlines[2].text
                dividends_splits += n * [v]

                fiscal_year = []
                n = 2
                v = headlines[3].text
                fiscal_year += n * [v]

                profitability = []
                n = 2
                v = headlines[4].text
                profitability += n * [v]

                management_effectiveness = []
                n = 2
                v = headlines[5].text
                management_effectiveness += n * [v]

                income_statement = []
                n = 8
                v = headlines[6].text
                income_statement += n * [v]

                balance_sheet = []
                n = 6
                v = headlines[7].text
                balance_sheet += n * [v]

                cash_flow_statement = []
                n = 2
                v = headlines[8].text
                cash_flow_statement += n * [v]

                outer_text = page.find_all('td', {
                    'class': 'Pos(st) Start(0) Bgc($lv2BgColor) fi-row:h_Bgc($hoverBgColor) Pend(10px) Miw(140px)'})
                inner_text = page.find_all('td', {
                    'class': 'Pos(st) Start(0) Bgc($lv2BgColor) fi-row:h_Bgc($hoverBgColor) Pend(10px)'})

                if len(outer_text) == 10 or len(inner_text) == 50:

                    arrays = [
                        np.array(valuation_measures + stock_price_history + share_statistics + dividends_splits
                               + fiscal_year + profitability + management_effectiveness + income_statement
                               + balance_sheet + cash_flow_statement),

                        np.array([outer_text[0].text[:-2],
                                  inner_text[0].text[:-2],
                                  inner_text[1].text[:-1],
                                  inner_text[2].text[:-2],
                                  inner_text[3].text[:-2],
                                  inner_text[4].text,
                                  inner_text[5].text,
                                  inner_text[6].text[:-2],
                                  inner_text[7].text[:-2],
                                  outer_text[1].text.strip(),
                                  inner_text[8].text[:-2],
                                  inner_text[9].text[:-2],
                                  inner_text[10].text[:-2],
                                  inner_text[11].text[:-2],
                                  inner_text[12].text[:-2],
                                  inner_text[13].text[:-2],
                                  outer_text[2].text[:-2],
                                  inner_text[14].text[:-2],
                                  inner_text[15].text[:-2],
                                  inner_text[16].text[:-2],
                                  inner_text[17].text[:-2],
                                  inner_text[18].text[:-2],
                                  inner_text[19].text[:-2],
                                  inner_text[20].text[:-2],
                                  inner_text[21].text[:-2],
                                  inner_text[22].text[:-2],
                                  inner_text[23].text[:-2],
                                  inner_text[24].text[:-2],
                                  outer_text[3].text[:-2],
                                  inner_text[25].text[:-2],
                                  inner_text[26].text[:-2],
                                  inner_text[27].text[:-2],
                                  inner_text[28].text[:-2],
                                  inner_text[29].text[:-2],
                                  inner_text[30].text[:-2],
                                  inner_text[31].text[:-2],
                                  inner_text[32].text[:-2],
                                  inner_text[33].text[:-2],
                                  outer_text[4].text[:-1],
                                  inner_text[34].text,
                                  outer_text[5].text[:-1],
                                  inner_text[35].text,
                                  outer_text[6].text,
                                  inner_text[36].text,
                                  outer_text[7].text,
                                  inner_text[37].text,
                                  inner_text[38].text,
                                  inner_text[39].text,
                                  inner_text[40].text.strip(),
                                  inner_text[41].text,
                                  inner_text[42].text,
                                  inner_text[43].text,
                                  outer_text[8].text,
                                  inner_text[44].text,
                                  inner_text[45].text,
                                  inner_text[46].text,
                                  inner_text[47].text,
                                  inner_text[48].text,
                                  outer_text[9].text,
                                  inner_text[49].text]), ]

                    array_table = []

                    for i in range(0, 60):
                        array_table.append(table[i].text.strip())

                    s = pd.DataFrame(array_table, index=arrays, columns=[self.ticker + ' Yahoo Statistics'])
                    s = s.loc[:, self.ticker + ' Yahoo Statistics'].replace(['N/A'], np.nan)

                    self.__yahoo_statistics_df = s.to_frame(name=self.ticker + ' Yahoo Statistics')

                else:
                    self.__yahoo_statistics_df = None

        return self.__yahoo_statistics_df

    ### Yahoo Finance Statistics - PreProcessing                 ###
    ### e.g. https://finance.yahoo.com/quote/NVDA/key-statistics ###
    ### Rückgabe None implementiert und getestet                 ###
    def __yahoo_statistics_df_p(self):

        def m_b_t(string):

            if type(string) != float:
                if string[-1] == 'B':
                    string = float(string[:-1]) * 10 ** 9
                elif string[-1] == 'M':
                    string = float(string[:-1]) * 10 ** 6
                elif string[-1] == 'T':
                    string = float(string[:-1]) * 10 ** 12
                else:
                    string = float(string[:-1])
            else:
                pass

            return string

        s = self.__yahoo_statistics_abfrage()

        if s is not None:
            s.iloc[0, 0] = m_b_t(s.iloc[0, 0])  # Market Cap
            s.iloc[1, 0] = m_b_t(s.iloc[1, 0])  # Enterprise Value
            s.iloc[2, 0] = float(s.iloc[2, 0])  # Trailing P/E
            s.iloc[3, 0] = float(s.iloc[3, 0])  # Forward P/E
            s.iloc[4, 0] = float(s.iloc[4, 0])  # PEG Ratio (5 yr expected)
            s.iloc[5, 0] = float(s.iloc[5, 0])  # Price/Sales (ttm)
            s.iloc[6, 0] = float(s.iloc[6, 0])  # Price/Book (mrq)
            s.iloc[7, 0] = float(s.iloc[7, 0])  # Enterprise Value/Revenue
            s.iloc[8, 0] = float(s.iloc[8, 0])  # Enterprise Value/EBITDA
            s.iloc[9, 0] = float(s.iloc[9, 0])  # Beta (5Y Monthly)
            s.iloc[10, 0] = m_b_t(s.iloc[10, 0])  # 52-Week Change
            s.iloc[11, 0] = m_b_t(s.iloc[11, 0])  # S&P500 52-Week Change
            s.iloc[12, 0] = float(s.iloc[12, 0])  # 52 Week High
            s.iloc[13, 0] = float(s.iloc[13, 0])  # 52 Week Low
            s.iloc[14, 0] = float(s.iloc[14, 0])  # 50-Day Moving Average
            s.iloc[15, 0] = float(s.iloc[15, 0])  # 200-Day Moving Average
            s.iloc[16, 0] = m_b_t(s.iloc[16, 0])  # Avg Vol (3 month)
            s.iloc[17, 0] = m_b_t(s.iloc[17, 0])  # Avg Vol (10 day)
            s.iloc[18, 0] = m_b_t(s.iloc[18, 0])  # Shares Outstanding
            s.iloc[19, 0] = m_b_t(s.iloc[19, 0])  # Implied Shares Outstanding
            s.iloc[20, 0] = m_b_t(s.iloc[20, 0])  # Float
            s.iloc[21, 0] = m_b_t(s.iloc[21, 0])  # % Held by Insiders
            s.iloc[22, 0] = m_b_t(s.iloc[22, 0])  # % Held by Institutions
            s.iloc[23, 0] = m_b_t(s.iloc[23, 0])  # Shares Short (Oct 14, 2021)
            s.iloc[24, 0] = float(s.iloc[24, 0])  # Short Ratio (Oct 14, 2021)
            s.iloc[25, 0] = m_b_t(s.iloc[25, 0])  # Short % of Float (Oct 14, 2021)
            s.iloc[26, 0] = m_b_t(s.iloc[26, 0])  # Short % of Shares Outstanding (Oct 14, 2021)
            s.iloc[27, 0] = m_b_t(s.iloc[27, 0])  # Shares Short (prior month Sep 14, 2021)
            s.iloc[28, 0] = float(s.iloc[28, 0])  # Forward Annual Dividend Rate
            s.iloc[29, 0] = m_b_t(s.iloc[29, 0])  # Forward Annual Dividend Yield
            s.iloc[30, 0] = float(s.iloc[30, 0])  # Trailing Annual Dividend Rate
            s.iloc[31, 0] = m_b_t(s.iloc[31, 0])  # Trailing Annual Dividend Yield
            s.iloc[32, 0] = float(s.iloc[32, 0])  # 5 Year Average Dividend Yield
            s.iloc[33, 0] = m_b_t(s.iloc[33, 0])  # Payout Ratio
            # s.iloc[34,0] = float(s.iloc[34,0]) # Dividend Date
            # s.iloc[35,0] = float(s.iloc[35,0]) # Ex-Dividend Date
            # s.iloc[36,0] = float(s.iloc[36,0]) # Last Split Factor
            # s.iloc[37,0] = float(s.iloc[37,0]) # Last Split Date
            # s.iloc[38,0] = float(s.iloc[38,0]) # Fiscal Year Ends
            # s.iloc[39,0] = float(s.iloc[39,0]) # Most Recent Quarter (mrq)
            s.iloc[40, 0] = m_b_t(s.iloc[40, 0])  # Profit Margin
            s.iloc[41, 0] = m_b_t(s.iloc[41, 0])  # Operating Margin (ttm)
            s.iloc[42, 0] = m_b_t(s.iloc[42, 0])  # Return on Assets (ttm)
            s.iloc[43, 0] = m_b_t(s.iloc[43, 0])  # Return on Equity (ttm)
            s.iloc[44, 0] = m_b_t(s.iloc[44, 0])  # Revenue (ttm)
            s.iloc[45, 0] = float(s.iloc[45, 0])  # Revenue Per Share (ttm)
            s.iloc[46, 0] = m_b_t(s.iloc[46, 0])  # Quarterly Revenue Growth (yoy)
            s.iloc[47, 0] = m_b_t(s.iloc[47, 0])  # Gross Profit (ttm)
            s.iloc[48, 0] = m_b_t(s.iloc[48, 0])  # EBITDA
            s.iloc[49, 0] = m_b_t(s.iloc[49, 0])  # Net Income Avi to Common (ttm)
            s.iloc[50, 0] = float(s.iloc[50, 0])  # Diluted EPS (ttm)
            s.iloc[51, 0] = m_b_t(s.iloc[51, 0])  # Quarterly Earnings Growth (yoy)
            s.iloc[52, 0] = m_b_t(s.iloc[52, 0])  # Total Cash (mrq)
            s.iloc[53, 0] = float(s.iloc[53, 0])  # Total Cash Per Share (mrq)
            s.iloc[54, 0] = m_b_t(s.iloc[54, 0])  # Total Debt (mrq)
            s.iloc[55, 0] = float(s.iloc[55, 0])  # Total Debt/Equity (mrq)
            s.iloc[56, 0] = float(s.iloc[56, 0])  # Current Ratio (mrq)
            s.iloc[57, 0] = float(s.iloc[57, 0])  # Book Value Per Share (mrq)
            s.iloc[58, 0] = m_b_t(s.iloc[58, 0])  # Operating Cash Flow (ttm)
            s.iloc[59, 0] = m_b_t(s.iloc[59, 0])  # Levered Free Cash Flow (ttm)

            s = s.rename(
                columns={self.ticker + ' Yahoo Statistics': self.ticker + ' Yahoo Statistics PreProcessing'})

        else:
            s = None

        return s