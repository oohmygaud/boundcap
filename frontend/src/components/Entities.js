import React, { useState, useEffect } from "react";
import useFetch from "use-http";
import TextField from "@material-ui/core/TextField";
import Grid from "@material-ui/core/Grid";
import FormGroup from "@material-ui/core/FormGroup";
import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";

const Entities = () => {
  const [entities, setEntities] = useState();
  const [title, setTitle] = useState();
  const api = useFetch("/api");
  const { get, post, response, loading, error } = api;

  useEffect(() => {
    loadEntities();
  }, []);

  async function loadEntities() {
    const entitiesList = await get("/entities/");
    if (response.ok) setEntities(entitiesList);
  }

  async function createEntity(e, title) {
    e.preventDefault();
    const userEntity = await post("/entities/", { title });
    const userId = await get("/auth/profile/");
    await post("/user_permissions/", {
      user: userId.id,
      entity: userEntity.id,
    });
    window.location.pathname = "/entities";
    return false;
  }

  if (loading || !entities) return <h3>Loading...</h3>;

  return (
    <div>
      <Grid
        container
        style={{ padding: "1em" }}
        spacing={4}
        direction="row"
        justify="center"
        >
        <Grid item xs={4}>
          <form style={{ textAlign: "center"}} onSubmit={(e) => createEntity(e, title)}>
            <h4>Create A New Entity</h4>
            <FormGroup>
              <TextField
                id="title"
                label="Title"
                variant="outlined"
                margin="normal"
                onChange={(e) => setTitle(e.target.value)}
                value={title}
              />
            </FormGroup>
            <Button type="submit" variant="contained" color="primary">
              Submit
            </Button>
          </form>
        </Grid>
        <Grid item xs={4}>
          <center>
          <h4>Entities</h4>
          </center>
          
          <Grid container spacing={2} justify="center" alignItems="center" style={{ marginTop: '1em'}}>

            {entities.results.map((entity) => (
              <Grid item>
              <a href={"/entities/" + entity.id} key={entity.id}>
                <Card style={{ padding: '1em'}}>{entity.title}</Card>
              </a>
              </Grid>
            ))}
            </Grid>

        </Grid>
      </Grid>
    </div>
  );
};

export default Entities;
