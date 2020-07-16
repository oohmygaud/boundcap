import React from 'react'
import { mount, route } from 'navi'
import Dashboard from "../components/Dashboard";
import Register from "../components/Register";
import Login from "../components/Login";
import Entities from "../components/Entities";
import EntityDetails from "../components/EntityDetails";
import TransactionDetails from "../components/TransactionDetails";

export default mount({
  "/": route({
    title: "Dashboard",
    view: <Dashboard />,
  }),
  "/register": route({
    title: "Register",
    view: <Register />,
  }),

  "/login": route({
    title: "Login",
    view: <Login />,
  }),

  "/entities": route({
    title: "Entities",
    view: <Entities />
  }),

  "/entities/:id": route({
    getView: ({ params }) => {
      return <EntityDetails {...params} />;
    }
  }),

  "/transactions/:id": route({
    getView: ({ params }) => {
      return <TransactionDetails {...params} />
    }
  })

})