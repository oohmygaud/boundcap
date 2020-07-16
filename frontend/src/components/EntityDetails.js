import React, { useState, useEffect } from "react";
import useFetch from "use-http";
import Grid from "@material-ui/core/Grid";
import FormGroup from "@material-ui/core/FormGroup";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import Card from "@material-ui/core/Card";

const EntityDetails = ({ id }) => {
  const [entity, setEntity] = useState();
  const [email, setEmail] = useState();
  console.log(entity);
  const api = useFetch("/api");
  const { get, post, response, loading, error } = api;

  useEffect(() => {
    loadEntity();
  }, []);

  async function loadEntity() {
    setEntity(await get(`/entities/${id}`));
  }

  async function addUser(e, email) {
    e.preventDefault();
    const response = await post("/user_permissions/allow_user_by_email/", {
        entity: entity.id,
        email: email
    })
    if (response.ok) window.location.pathname = `/entities/${id}`;

    return false
  }

  if (loading || !entity) return <h3>Loading...</h3>;
  return (
    <div>
      <Grid
        container
        style={{ padding: "1em" }}
        spacing={2}
        direction="row"
        justify="center"
        alignItems="center"
      >
        <Grid item xs={12}>
            <center>
          <h3>{entity.title}</h3>
          </center>
        </Grid>
        <Grid item xs={3}>
          <h6>Allowed Users:</h6>
          
          {entity.allowed_users.map((user) => (
            <div key={user.id}>{user.user_data.email}</div>
          ))}
        </Grid>
        <Grid item xs={4}>
          <Card style={{ padding: "1em", textAlign: "center" }}>
            <form onSubmit={(e) => addUser(e, email)}>
              <h5>Add An Allowed User</h5>
              <FormGroup>
                <TextField
                  id="email"
                  label="Email"
                  variant="outlined"
                  margin="normal"
                  onChange={(e) => setEmail(e.target.value)}
                  value={email}
                />
              </FormGroup>
              {
                  error ? 
                  <div style={{ marginBottom: '0.5em' }}>
                      <small style={{ color: "red" }}>Invalid email - user does not exist</small></div> : null
              }
              <Button type="submit" variant="contained" color="primary">
                Submit
              </Button>
            </form>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

export default EntityDetails;
