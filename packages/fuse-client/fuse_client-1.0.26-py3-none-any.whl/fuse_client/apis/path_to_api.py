import typing_extensions

from fuse_client.paths import PathValues
from fuse_client.apis.paths.v1_financial_connections_accounts_details import V1FinancialConnectionsAccountsDetails
from fuse_client.apis.paths.v1_financial_connections_owners import V1FinancialConnectionsOwners
from fuse_client.apis.paths.v1_financial_connections_accounts_statement import V1FinancialConnectionsAccountsStatement
from fuse_client.apis.paths.v1_financial_connections_accounts import V1FinancialConnectionsAccounts
from fuse_client.apis.paths.v1_financial_connections_asset_report_create import V1FinancialConnectionsAssetReportCreate
from fuse_client.apis.paths.v1_financial_connections_asset_report_refresh import V1FinancialConnectionsAssetReportRefresh
from fuse_client.apis.paths.v1_financial_connections_asset_report import V1FinancialConnectionsAssetReport
from fuse_client.apis.paths.v1_financial_connections_balances import V1FinancialConnectionsBalances
from fuse_client.apis.paths.v1_transactions_enrich import V1TransactionsEnrich
from fuse_client.apis.paths.v1_entities_entity_id import V1EntitiesEntityId
from fuse_client.apis.paths.v1_accounts_account_id_events import V1AccountsAccountIdEvents
from fuse_client.apis.paths.v1_accounts_account_id_finance_score import V1AccountsAccountIdFinanceScore
from fuse_client.apis.paths.v1_financial_connections_public_token_exchange import V1FinancialConnectionsPublicTokenExchange
from fuse_client.apis.paths.v1_financial_connections_sync import V1FinancialConnectionsSync
from fuse_client.apis.paths.v1_financial_connections_institutions_institution_id import V1FinancialConnectionsInstitutionsInstitutionId
from fuse_client.apis.paths.v1_financial_connections_financial_connection_id_to_delete import V1FinancialConnectionsFinancialConnectionIdToDelete
from fuse_client.apis.paths.v1_financial_connections_financial_connection_id import V1FinancialConnectionsFinancialConnectionId
from fuse_client.apis.paths.v1_financial_connections_migrate import V1FinancialConnectionsMigrate
from fuse_client.apis.paths.v1_financial_connections_investments_holdings import V1FinancialConnectionsInvestmentsHoldings
from fuse_client.apis.paths.v1_financial_connections_investments_transactions import V1FinancialConnectionsInvestmentsTransactions
from fuse_client.apis.paths.v1_financial_connections_liabilities import V1FinancialConnectionsLiabilities
from fuse_client.apis.paths.v1_link_token import V1LinkToken
from fuse_client.apis.paths.v1_risk_report_consumer import V1RiskReportConsumer
from fuse_client.apis.paths.v1_risk_report_consumer_customization import V1RiskReportConsumerCustomization
from fuse_client.apis.paths.v1_risk_report_consumer_customization_consumer_risk_report_customization_id import V1RiskReportConsumerCustomizationConsumerRiskReportCustomizationId
from fuse_client.apis.paths.v1_risk_report_consumer_consumer_risk_report_id import V1RiskReportConsumerConsumerRiskReportId
from fuse_client.apis.paths.v1_session import V1Session
from fuse_client.apis.paths.v1_financial_connections_transactions import V1FinancialConnectionsTransactions

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.V1_FINANCIAL_CONNECTIONS_ACCOUNTS_DETAILS: V1FinancialConnectionsAccountsDetails,
        PathValues.V1_FINANCIAL_CONNECTIONS_OWNERS: V1FinancialConnectionsOwners,
        PathValues.V1_FINANCIAL_CONNECTIONS_ACCOUNTS_STATEMENT: V1FinancialConnectionsAccountsStatement,
        PathValues.V1_FINANCIAL_CONNECTIONS_ACCOUNTS: V1FinancialConnectionsAccounts,
        PathValues.V1_FINANCIAL_CONNECTIONS_ASSET_REPORT_CREATE: V1FinancialConnectionsAssetReportCreate,
        PathValues.V1_FINANCIAL_CONNECTIONS_ASSET_REPORT_REFRESH: V1FinancialConnectionsAssetReportRefresh,
        PathValues.V1_FINANCIAL_CONNECTIONS_ASSET_REPORT: V1FinancialConnectionsAssetReport,
        PathValues.V1_FINANCIAL_CONNECTIONS_BALANCES: V1FinancialConnectionsBalances,
        PathValues.V1_TRANSACTIONS_ENRICH: V1TransactionsEnrich,
        PathValues.V1_ENTITIES_ENTITY_ID: V1EntitiesEntityId,
        PathValues.V1_ACCOUNTS_ACCOUNT_ID_EVENTS: V1AccountsAccountIdEvents,
        PathValues.V1_ACCOUNTS_ACCOUNT_ID_FINANCE_SCORE: V1AccountsAccountIdFinanceScore,
        PathValues.V1_FINANCIAL_CONNECTIONS_PUBLIC_TOKEN_EXCHANGE: V1FinancialConnectionsPublicTokenExchange,
        PathValues.V1_FINANCIAL_CONNECTIONS_SYNC: V1FinancialConnectionsSync,
        PathValues.V1_FINANCIAL_CONNECTIONS_INSTITUTIONS_INSTITUTION_ID: V1FinancialConnectionsInstitutionsInstitutionId,
        PathValues.V1_FINANCIAL_CONNECTIONS_FINANCIAL_CONNECTION_ID_TO_DELETE: V1FinancialConnectionsFinancialConnectionIdToDelete,
        PathValues.V1_FINANCIAL_CONNECTIONS_FINANCIAL_CONNECTION_ID: V1FinancialConnectionsFinancialConnectionId,
        PathValues.V1_FINANCIAL_CONNECTIONS_MIGRATE: V1FinancialConnectionsMigrate,
        PathValues.V1_FINANCIAL_CONNECTIONS_INVESTMENTS_HOLDINGS: V1FinancialConnectionsInvestmentsHoldings,
        PathValues.V1_FINANCIAL_CONNECTIONS_INVESTMENTS_TRANSACTIONS: V1FinancialConnectionsInvestmentsTransactions,
        PathValues.V1_FINANCIAL_CONNECTIONS_LIABILITIES: V1FinancialConnectionsLiabilities,
        PathValues.V1_LINK_TOKEN: V1LinkToken,
        PathValues.V1_RISK_REPORT_CONSUMER: V1RiskReportConsumer,
        PathValues.V1_RISK_REPORT_CONSUMER_CUSTOMIZATION: V1RiskReportConsumerCustomization,
        PathValues.V1_RISK_REPORT_CONSUMER_CUSTOMIZATION_CONSUMER_RISK_REPORT_CUSTOMIZATION_ID: V1RiskReportConsumerCustomizationConsumerRiskReportCustomizationId,
        PathValues.V1_RISK_REPORT_CONSUMER_CONSUMER_RISK_REPORT_ID: V1RiskReportConsumerConsumerRiskReportId,
        PathValues.V1_SESSION: V1Session,
        PathValues.V1_FINANCIAL_CONNECTIONS_TRANSACTIONS: V1FinancialConnectionsTransactions,
    }
)

path_to_api = PathToApi(
    {
        PathValues.V1_FINANCIAL_CONNECTIONS_ACCOUNTS_DETAILS: V1FinancialConnectionsAccountsDetails,
        PathValues.V1_FINANCIAL_CONNECTIONS_OWNERS: V1FinancialConnectionsOwners,
        PathValues.V1_FINANCIAL_CONNECTIONS_ACCOUNTS_STATEMENT: V1FinancialConnectionsAccountsStatement,
        PathValues.V1_FINANCIAL_CONNECTIONS_ACCOUNTS: V1FinancialConnectionsAccounts,
        PathValues.V1_FINANCIAL_CONNECTIONS_ASSET_REPORT_CREATE: V1FinancialConnectionsAssetReportCreate,
        PathValues.V1_FINANCIAL_CONNECTIONS_ASSET_REPORT_REFRESH: V1FinancialConnectionsAssetReportRefresh,
        PathValues.V1_FINANCIAL_CONNECTIONS_ASSET_REPORT: V1FinancialConnectionsAssetReport,
        PathValues.V1_FINANCIAL_CONNECTIONS_BALANCES: V1FinancialConnectionsBalances,
        PathValues.V1_TRANSACTIONS_ENRICH: V1TransactionsEnrich,
        PathValues.V1_ENTITIES_ENTITY_ID: V1EntitiesEntityId,
        PathValues.V1_ACCOUNTS_ACCOUNT_ID_EVENTS: V1AccountsAccountIdEvents,
        PathValues.V1_ACCOUNTS_ACCOUNT_ID_FINANCE_SCORE: V1AccountsAccountIdFinanceScore,
        PathValues.V1_FINANCIAL_CONNECTIONS_PUBLIC_TOKEN_EXCHANGE: V1FinancialConnectionsPublicTokenExchange,
        PathValues.V1_FINANCIAL_CONNECTIONS_SYNC: V1FinancialConnectionsSync,
        PathValues.V1_FINANCIAL_CONNECTIONS_INSTITUTIONS_INSTITUTION_ID: V1FinancialConnectionsInstitutionsInstitutionId,
        PathValues.V1_FINANCIAL_CONNECTIONS_FINANCIAL_CONNECTION_ID_TO_DELETE: V1FinancialConnectionsFinancialConnectionIdToDelete,
        PathValues.V1_FINANCIAL_CONNECTIONS_FINANCIAL_CONNECTION_ID: V1FinancialConnectionsFinancialConnectionId,
        PathValues.V1_FINANCIAL_CONNECTIONS_MIGRATE: V1FinancialConnectionsMigrate,
        PathValues.V1_FINANCIAL_CONNECTIONS_INVESTMENTS_HOLDINGS: V1FinancialConnectionsInvestmentsHoldings,
        PathValues.V1_FINANCIAL_CONNECTIONS_INVESTMENTS_TRANSACTIONS: V1FinancialConnectionsInvestmentsTransactions,
        PathValues.V1_FINANCIAL_CONNECTIONS_LIABILITIES: V1FinancialConnectionsLiabilities,
        PathValues.V1_LINK_TOKEN: V1LinkToken,
        PathValues.V1_RISK_REPORT_CONSUMER: V1RiskReportConsumer,
        PathValues.V1_RISK_REPORT_CONSUMER_CUSTOMIZATION: V1RiskReportConsumerCustomization,
        PathValues.V1_RISK_REPORT_CONSUMER_CUSTOMIZATION_CONSUMER_RISK_REPORT_CUSTOMIZATION_ID: V1RiskReportConsumerCustomizationConsumerRiskReportCustomizationId,
        PathValues.V1_RISK_REPORT_CONSUMER_CONSUMER_RISK_REPORT_ID: V1RiskReportConsumerConsumerRiskReportId,
        PathValues.V1_SESSION: V1Session,
        PathValues.V1_FINANCIAL_CONNECTIONS_TRANSACTIONS: V1FinancialConnectionsTransactions,
    }
)
