import React, { useState, useEffect } from "react";
import useFetch from "use-http";
import Button from "@material-ui/core/Button";
import MaterialTable from "material-table";
import { forwardRef } from 'react';
import moment from 'moment';

import ArrowDownward from '@material-ui/icons/ArrowDownward';
import ChevronLeft from '@material-ui/icons/ChevronLeft';
import ChevronRight from '@material-ui/icons/ChevronRight';
import Clear from '@material-ui/icons/Clear';
import Edit from '@material-ui/icons/Edit';
import FirstPage from '@material-ui/icons/FirstPage';
import LastPage from '@material-ui/icons/LastPage';
import Search from '@material-ui/icons/Search';
import ViewColumn from '@material-ui/icons/ViewColumn';

const tableIcons = {

    Edit: forwardRef((props, ref) => <Edit {...props} ref={ref} />),
    FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref} />),
    LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref} />),
    NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
    PreviousPage: forwardRef((props, ref) => <ChevronLeft {...props} ref={ref} />),
    ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
    Search: forwardRef((props, ref) => <Search {...props} ref={ref} />),
    SortArrow: forwardRef((props, ref) => <ArrowDownward {...props} ref={ref} />),
    ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref} />)
  };

const Dashboard = () => {
  const [transactions, setTransactions] = useState();
  const api = useFetch("/api");
  const [profile, setProfile] = useState();
  const { get, post, response, loading, error } = api;
  useEffect(() => {
    const asyncPageLoaded = async () => {
      await getProfile();
      await loadTransactions();
    };
    asyncPageLoaded();
  }, []);

  async function logout_user(e) {
    e.preventDefault();
    await post("/auth/logout/");
    if (response.ok) window.location.pathname = "/login/";
  }

  async function getProfile() {
    await get("/auth/profile/");
    if (response.ok) setProfile(response.data);
  }

  async function getTransactionDetail(id) {
    window.location.pathname = "/transactions/" + id
    return false
  }

  async function loadTransactions() {
    const transactionsList = await get("/transactions/");
    if (response.ok) setTransactions(transactionsList);
  }

  if(loading || !transactions)
    return <h3>Loading...</h3>
  console.log("transactions", transactions)

  return (
    <div>
      {profile ? (
        <li>
          <Button onClick={(e) => logout_user(e)}>Logout</Button>
        </li>
      ) : (
        ""
      )}
      <MaterialTable
        columns={[
          { title: "Import date", field: "import_date" },
          { title: "Account", field: "account" },
          { title: "Category", field: "category" },
          { title: "Amount", field: "amount", render: rowData => '$' + rowData.amount},
          { title: "Merchant", field: "merchant" },
        ]}
        data={transactions.results.map((t) => ({
          id: t.id,
          import_date: moment(t.import_date).format('MM-DD-YYYY'),
          account: t.account_data.title,
          category: t.category,
          amount: t.amount_in_cents / 100,
          merchant: t.merchant,
        }))}
        title="Transactions"
        icons={tableIcons}
        actions={[
          {
            icon: Edit,
            tooltip: 'Edit Transaction',
            onClick: (event, rowData) => getTransactionDetail(rowData.id)
          }
        ]}
        options={{
          actionsColumnIndex: -1
        }}
      />
    </div>
  );
};

export default Dashboard;
