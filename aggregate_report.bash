#!/bin/bash

# If no database name is provided, set it to the default name.
if [[ $# < 1 ]]; then
    DATABASE=expenses.db
else
    DATABASE=$1
fi

# Make sure the provided database actually exists.
if [ ! -f $DATABASE ]; then
    echo "Database $DATABASE doesn't exist."
    exit 1
fi

# Launch a sqlite session with prettyfied output and run the
# relevant SQL command
sqlite3 -header -column $DATABASE <<ENDOFSQLITE
.width 20 -12 11
Select description, sum(amount) as total_amount, count(rowid) as total_count
From expenses
Group By description
Order By total_amount desc;
ENDOFSQLITE
