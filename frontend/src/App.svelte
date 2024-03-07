<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/List.svelte"
  import Detail from "./routes/Detail.svelte"
  import BoardCreate from "./routes/BoardCreate.svelte"
  import Navigation from "./components/Navigation.svelte"
  import UserCreate from "./routes/UserCreate.svelte"
  import UserLogin from "./routes/UserLogin.svelte"
  import BoardModify from "./routes/BoardModify.svelte"
  import CommentModify from "./routes/CommentModify.svelte"

  const routes = {
    '/': Home,
    '/detail/:board_id': Detail,
    '/board-create': BoardCreate,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/board-modify/:board_id': BoardModify,
    '/comment-modify/:comment_id': CommentModify,
  }
</script>

<Navigation />
<Router {routes}/>