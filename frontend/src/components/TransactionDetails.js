import React, { useState, useEffect } from "react";
import useFetch from "use-http";
import Button from "@material-ui/core/Button";
import Autocomplete from "@material-ui/lab/Autocomplete";
import { TextField } from "@material-ui/core";

const TransactionDetail = ({ id }) => {
  const [transaction, setTransaction] = useState();
  const [category, setCategory] = useState();
  const [categoryList, setCategoryList] = useState();
  const api = useFetch("/api");
  const { get, post, put, response, loading, error } = api;

  useEffect(() => {
    loadTransaction();
    loadCategories();
  }, []);

  async function editCategory(e) {
    e.preventDefault();
    await put(`/transactions/${id}`, {
      external_id: transaction.external_id,
      account: transaction.account,
      category: category,
      amount_in_cents: transaction.amount_in_cents,
      is_transfer: transaction.is_transfer,
      is_spending: transaction.is_spending,
      internally_editted: true,
    });
  }

  async function loadCategories() {
    setCategoryList(await get("/categories/?limit=100"));
  }

  async function loadTransaction() {
    setTransaction(await get(`/transactions/${id}`));
  }

  if (loading || !transaction || !categoryList) return <h3>Loading...</h3>;
  console.log(transaction, categoryList);
  return (
    <div>
      <form onSubmit={(e) => editCategory()}>
        <h4>Transaction Details</h4>
        <div>Account: {transaction.account_data.title}</div>
        <div>${transaction.amount_in_cents / 100}</div>
        <div>Merchant: {transaction.merchant}</div>

        <Autocomplete
          id="category"
          options={categoryList.results.map((cat) => cat.title)}
          defaultValue={transaction.category_title}
          style={{ width: 300 }}
          renderInput={(params) => (
            <TextField
              {...params}
              variant="outlined"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            />
          )}
        />

        <Button type="submit" variant="contained" color="primary">
          Submit
        </Button>
      </form>
    </div>
  );
};

export default TransactionDetail;
