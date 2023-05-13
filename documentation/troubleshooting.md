# Troubleshooting

## Window Layouts

- **MainWindow**
    - **central_widget** (QStackedWidget)
        - **accounts_widget** (AccountsWidget)
            - **outer_layout** (QHBoxLayout)
                - title (Label)
                - **inner_layout** (QHBoxLayout)
                    - table (QTableView)
                    - **btns_layout** (QVLayout)
                        - buttons
        - **payments_widget** (PaymentsWidget)
            - **outer_layout** (QHBoxLayout)
                    - title (Label)
                    - **inner_layout** (QHBoxLayout)
                        - table (QTableView)
                        - **btns_layout** (QVLayout)
                            - buttons
        - **transactions_widget** (TransactionsWidget)
            - **outer_layout** (QHBoxLayout)
                - title (Label)
                - **inner_layout** (QHBoxLayout)
                    - table (QTableView)
                    - **btns_layout** (QVLayout)
                        - buttons