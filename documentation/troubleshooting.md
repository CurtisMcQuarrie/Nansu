# Troubleshooting
## Best Resources
https://doc.qt.io/
    - actual QT documentation.
    - sadly it is written w.r.t. the c++ implementation.

## Model Manipulation
Manipulating the data in a model is very incremental.

For example, to add a single entry into the model you must follow these steps.
1. Get the row count...


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
        - **tabs_widget** (QTabsWidget)
            - **payments_tab** (PaymentsWidget)
                - **outer_layout** (QHBoxLayout)
                        - title (Label)
                        - **inner_layout** (QHBoxLayout)
                            - table (QTableView)
                            - **btns_layout** (QVLayout)
                                - buttons
            - **transactions_tab** (TransactionsWidget)
                - **outer_layout** (QHBoxLayout)
                    - title (Label)
                    - **inner_layout** (QHBoxLayout)
                        - table (QTableView)
                        - **btns_layout** (QVLayout)
                            - buttons