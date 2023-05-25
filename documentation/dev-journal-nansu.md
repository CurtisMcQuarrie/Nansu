# Nansu Dev Journal

## 05.20.23
[] Payments-Transactions Connection
    [] When adding a payment that's reocurring, add the transactions to the Transactions model
    [] Same as above but with deleting
    [] When updating a payment amount, change the transactions as well
    [x] ~~Add a "Once" frequency to the payments~~
[] Graphs and Charts Update
    [] Add the ability to view the daily amount in an account
[] View Buttons Update
    [] Transactions view button should apply a filter to the Payments view
    [] Modify the view buttons for both Transaction and Payments
        - have them be more descriptive ("view payments", "view transactions")
    [] Add a button to Transactions and Payments views that can remove the filters if there is one

## 05.13.23
[x] Payments Update
    [x] Remove the Accounts column
    [x] Add the account name to the title
    [x] Disable the `view` button (temporarily)
[x] Transactions Update
    [x] Add a way to view the transactions without the `view` button
        - Maybe try out the tabs idea
    [x] `view` button will instead filter the transactions related to the payment
[x] Payments View Button
    [x] Enable the `view` button in payments
    [x] Have the `view` button go to the transactions view but with a filter applied
[] Future Fixes Update
    [] Add filtering capabilities directly to the table views
    [] Move the back button to somewhere a bit more meaningful and make it more descriptive
        - change to something like "view accounts" or "back to accounts" or just "accounts"
        - maybe move the back button to the dropdown menus or have it display beside the tabs
    [] Consider refactoring classes
    [] Look into testing
    [] Add more of a setup flow to creating an account
        - like allow the user to setup an initial amount
        - add additional info to the account
    [] Add Import and Export options



## 02.19.23
[] create transactions when payments are added
[] change transactions view to be a tab instead
[] prevent modifications for specific sensitive columns
[x] add title for each widget