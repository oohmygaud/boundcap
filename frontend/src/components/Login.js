import React, { useState } from "react";
import useFetch from "use-http";
import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import FormGroup from "@material-ui/core/FormGroup";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";

export default function Login() {
  const [login, setUsername] = useState();
  const [password, setPassword] = useState();
  const api = useFetch("/api", {
    cachePolicy: "no-cache",
  });

  const { get, post, response, loading, error } = api;

  async function login_user(e, login, password) {
    e.preventDefault();
    await post("/auth/login/", { login, password });
    if (response.ok) window.location.pathname = "/";
  }
  return (
    <Grid
        container
        justify="center"
        alignItems="center"
        direction="row"
        spacing={1}
        style={{ marginTop: "1em"}}
    >
      <Grid item xs={12} md={6} lg={3}>
        <Card style={{ marginTop: "0.5em", padding: "1em" }}>
          <Grid container direction="row" justify="center">
            <Grid item xs={6} md={4}>
              <h5 style={{ margin: "1em 0 0", textAlign: "right" }}>
                Not a user yet?
              </h5>
            </Grid>
            <Grid item xs={4} md={3}>
              <Button
                style={{ marginTop: "1.1em" }}
                href="/register"
                color="secondary"
              >
                Register
              </Button>
            </Grid>
          </Grid>
          <form onSubmit={(e) => login_user(e, login, password)}>
            <FormGroup>
              <TextField
                label="Username"
                type="username"
                variant="outlined"
                margin="normal"
                value={login}
                onChange={(e) => setUsername(e.target.value)}
              />
            </FormGroup>
            <FormGroup>
              <TextField
                label="Password"
                type="password"
                variant="outlined"
                margin="normal"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </FormGroup>
            <center>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                style={{ marginRight: "0.5em" }}
              >
                Login
              </Button>
            </center>
          </form>
        </Card>
      </Grid>
    </Grid>
  );
}
