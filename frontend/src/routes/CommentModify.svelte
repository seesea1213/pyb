<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { push } from 'svelte-spa-router'

    export let params = {}
    const comment_id = params.comment_id

    let error = {detail:[]}
    let board_id = 0
    let content = ''

    fastapi("get", "/api/comment/detail/" + comment_id, {}, (json) => {
        board_id = json.board_id
        content = json.content
    })

    function update_comment(event) {
        event.preventDefault()
        let url = "/api/comment/update"
        let params = {
            comment_id: comment_id,
            content: content,
        }
        fastapi('put', url, params, 
            (json) => {
                push('/detail/'+board_id)
            },
            (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">댓글 수정</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click="{update_comment}">수정하기</button>
    </form>
</div>
