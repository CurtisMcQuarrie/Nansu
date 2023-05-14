# Nansu Dev Journal

## 05.13.23
[x] Payments Update
    [x] Remove the Accounts column
    [x] Add the account name to the title
    [x] Disable the `view` button (temporarily)
[] Transactions Update
    [] Add a way to view the transactions without the `view` button
        - Maybe try out the tabs idea
    [] `view` button will instead filter the transactions related to the payment
[] Payments-Transactions Connection
    [] When adding a payment that's reocurring, add the transactions to the Transactions model
    [] Same as above but with deleting
    [] When updating a payment amount, change the transactions as well
[] Payments View Button
    [] Enable the `view` button in payments
    [] Have the `view` button go to the transactions view but with a filter applied

## 02.19.23
[] create transactions when payments are added
[] change transactions view to be a tab instead
[] prevent modifications for specific sensitive columns
[x] add title for each widget