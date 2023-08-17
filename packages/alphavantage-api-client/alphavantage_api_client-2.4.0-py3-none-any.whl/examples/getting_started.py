from alphavantage_api_client import AlphavantageClient, GlobalQuote, Quote, AccountingReport, CompanyOverview, Ticker
import logging
from decimal import Decimal

def sample_global_quote():
    client = AlphavantageClient()

    global_quote = client.get_global_quote("TSLA")
    if not global_quote.success:
        raise ValueError(f"{global_quote.error_message}")
    print(global_quote.model_dump_json())  # convenience method that will convert to json
    print(f"stock price: ${global_quote.get_price()}")  # convenience method to get stock price
    print(f"trade volume: {global_quote.get_volume()}")  # convenience method to get volume
    print(f"low price: ${global_quote.get_low_price()}")  # convenience method to get low price for the day


def sample_balance_sheet():
    client = AlphavantageClient()
    balance_sheet = client.get_balance_sheet("TSLA")
    if not balance_sheet.success:
        raise ValueError(f"{balance_sheet.error_message}")
    print(balance_sheet.get_most_recent_quarterly_report())  # get the newest quarterly statement
    print(balance_sheet.get_most_recent_annual_report())  # get the most recent annual report
    print(balance_sheet.quarterlyReports)  # get [] quarterly reports
    print(balance_sheet.annualReports)  # get [] annual reports


def sample_earnings_statement():
    client = AlphavantageClient()
    earnings = client.get_earnings("TSLA")
    if not earnings.success:
        raise ValueError(f"{earnings.error_message}")
    print(earnings.get_most_recent_quarterly_report())  # get the newest quarterly statement
    print(earnings.get_most_recent_annual_report())  # get the most recent annual report
    print(earnings.quarterlyReports)  # get [] quarterly reports
    print(earnings.annualReports)  # get [] annual reports


def sample_income_statement():
    client = AlphavantageClient()
    income_statement = client.get_income_statement("TSLA")
    if not income_statement.success:
        raise ValueError(f"{income_statement.error_message}")
    print(income_statement.get_most_recent_quarterly_report())  # get the newest quarterly statement
    print(income_statement.get_most_recent_annual_report())  # get the most recent annual report
    print(income_statement.quarterlyReports)  # get [] quarterly reports
    print(income_statement.annualReports)  # get [] annual reports


def sample_accounting_reports():
    client = AlphavantageClient()
    earnings = client.get_earnings("TSLA")
    cash_flow = client.get_cash_flow("TSLA")
    balance_sheet = client.get_balance_sheet("TSLA")
    income_statement = client.get_income_statement("TSLA")
    reports = [earnings, cash_flow, balance_sheet, income_statement]

    # show that each report is in the same type and how to access the annual and quarterly reports
    for accounting_report in reports:
        if not accounting_report.success:
            raise ValueError(f"{accounting_report.error_message}")
        print(accounting_report.model_dump_json())
        print(accounting_report.quarterlyReports)  # array of  all quarterly report
        print(accounting_report.annualReports)  # array of all annual reports
        print(accounting_report.get_most_recent_annual_report())  # get the most recent annual report
        print(accounting_report.get_most_recent_quarterly_report())  # get the most recent quarterly report;


def sample_intraday_quote():
    client = AlphavantageClient()
    quote = client.get_intraday_quote("TSLA")
    if not quote.success:
        raise ValueError(f"{quote.error_message}")
    print(quote.model_dump_json())
    print(f"success: {quote.success}")  # injected by this library to show success
    print(quote.data)  # all data from alpha vantage
    print(quote.get_most_recent_value())  # most recent quote
    print(quote.get_oldest_value())  # get the oldest quote


def sample_company_overview():
    client = AlphavantageClient()
    company_overview = client.get_company_overview("TSLA")
    if not company_overview.success:
        raise ValueError(f"{company_overview.error_message}")
    print(f"description: {company_overview.description}")
    print(f"name: {company_overview.name}")
    print(f" pe_ratio: {company_overview.pe_ratio}")
    print(f"shares_outstanding: {company_overview.shares_outstanding}")
    print(f"dividend_ratio: {company_overview.dividend_date}")
    print(f"dividend_yield: {company_overview.dividend_yield}")
    print(f"price_to_book_ratio: {company_overview.price_to_book_ratio}")
    # and more!


def sample_cash_flow():
    client = AlphavantageClient()
    cash_flow = client.get_cash_flow("TSLA")
    if not cash_flow.success:
        raise ValueError(f"{cash_flow.error_message}")
    print(cash_flow.get_most_recent_quarterly_report())  # get the newest quarterly statement
    print(cash_flow.get_most_recent_annual_report())  # get the most recent annual report
    print(cash_flow.quarterlyReports)  # get [] quarterly reports
    print(cash_flow.annualReports)  # get [] annual reports


def sample_retry_when_limit_reached():
    logging.basicConfig(level=logging.INFO)
    client = AlphavantageClient().use_simple_cache().should_retry_once()
    symbols = ["TSLA", "F", "C", "WFC", "ZIM", "PXD", "PXD", "POOL", "INTC", "INTU", "AAPL"]  # more than 5 calls so should fail
    for symbol in symbols:
        event = {
            "symbol": symbol
        }
        global_quote = client.get_global_quote(event)
        if not global_quote.success:
            raise ValueError(f"{global_quote.error_message}")

        if global_quote.limit_reached:
            raise ValueError(f"{global_quote.error_message}")
        print(f"symbol: {global_quote.symbol}, Price: {global_quote.get_price()}, success {global_quote.success}")

    client.clear_cache()  # when you are done making calls, clear cache


def sample_ticker_usage():
    """
    combine all financial statements (income, cash flow, earnings and balance sheet) for both
     quarterly and annual reports. There migth be times you want to store/visualize them together
     thus providing another dimensionality of the data
    Returns:

    """
    aapl = (Ticker()
            .create_client()
            .should_retry_once()  # auto retry when limit reached
            .from_symbol("AAPL")  # define the company of interest
            .fetch_accounting_reports()  # make the call to alpha vantage api
            .correlate_accounting_reports()  # combines all 4 financial statements
            )

    # get the individual financial statements if needed
    earnings = aapl.get_earnings()
    income_statement = aapl.get_income_statement()
    balance_sheet = aapl.get_balance_sheet()
    cash_flow = aapl.get_cash_flow()

    # get the combined financial statements and iterate easy
    correlated_financial_statements = aapl.get_correlated_reports() # both quarterly and annually

    for fiscal_date_ending in correlated_financial_statements:
        combined_financial_statements = correlated_financial_statements[fiscal_date_ending]
        print(f"{fiscal_date_ending} = {combined_financial_statements}")

def sample_direct_access():
    client = AlphavantageClient()
    event = {
        "symbol" : "AAPL",
        "function" : "GLOBAL_QUOTE"
    } # EACH ATTRIBUTE IS EXACTLY SUPPORTED BY END POINTS

    response = client.get_data_from_alpha_vantage(event)
    print(response) # a dictionary with exact response from Alpha Vantage End point you requested


def calculate_free_cash_flow_last_fiscal_year():
    client = AlphavantageClient()
    symbol = "TSLA"
    one_billion = Decimal(1000000000.00)
    cash_flow_statements = client.get_cash_flow(symbol)
    last_year_cash_flow_statement = cash_flow_statements.get_most_recent_annual_report()
    last_year_fcf = calc_free_cash_flow(last_year_cash_flow_statement, one_billion)
    fiscalDateEnding = last_year_cash_flow_statement.get('fiscalDateEnding', 'Not Provided')
    print(f"FCF as of {fiscalDateEnding} for {symbol} was ${last_year_fcf}b")


def calc_free_cash_flow(free_cash_flow_statement: dict, multiple: Decimal = Decimal(1)) -> Decimal:
    capitalExpenditures = free_cash_flow_statement.get('capitalExpenditures', Decimal('0.00'))
    capitalExpenditures = Decimal(capitalExpenditures) / multiple

    operatingCashflow = free_cash_flow_statement.get('operatingCashflow', Decimal('0.00'))
    operatingCashflow = Decimal(operatingCashflow) / multiple

    free_cash_flow = operatingCashflow - capitalExpenditures
    print(f"operatingCashflow = ${operatingCashflow}b, capitalExpenditures = ${capitalExpenditures}b ")


    return free_cash_flow

def calc_free_cash_flow_per_share():
    client = AlphavantageClient()
    symbol = "TSLA"
    one_billion = Decimal(1000000000.00)
    cash_flow_statements = client.get_cash_flow(symbol)
    last_year_cash_flow_statement = cash_flow_statements.get_most_recent_annual_report()
    last_year_fcf = calc_free_cash_flow(last_year_cash_flow_statement, one_billion)
    fiscalDateEnding = last_year_cash_flow_statement.get('fiscalDateEnding', 'Not Provided')
    print(f"FCF as of {fiscalDateEnding} for {symbol} was ${last_year_fcf}b")

    # get shares out standing
    company_overview = client.get_company_overview("tsla")
    shares_outstanding = Decimal(company_overview.shares_outstanding) / one_billion
    fcf_per_share = round(last_year_fcf / shares_outstanding, 2)
    print(f"Free Cash Flow per share for {symbol} was ${fcf_per_share} having shares outstanding of {shares_outstanding}b")

def get_earnings_calendar():
    client = AlphavantageClient()
    #symbols = ["IBM", "AAPL", "AMZN", "MSFT", "TSLA", "SYM"]
    symbols = ["MSFT"]
    for symbol in symbols:
        event = {
            "symbol": symbol,
            "horizon": "6month" #6 months so we are sure to get data
        }
        earnings_calendar = client.get_earnings_calendar(event)
        print(earnings_calendar)
            


if __name__ == "__main__":
    get_earnings_calendar()
