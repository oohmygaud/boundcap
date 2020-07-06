import React from 'react'
import { mount, route } from 'navi'
import Dashboard from "../components/Dashboard";
import Register from "../components/Register";
import Login from "../components/Login";

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
    
  '/getting-started': route({
    title: "Getting Started",
    getView: async () => {
      // This simulates some async content loading, so that
      // you can test the site's loading bar.
      await new Promise(resolve => setTimeout(resolve, 1000))

      return import('./getting-started.mdx')
    }
  }),
})