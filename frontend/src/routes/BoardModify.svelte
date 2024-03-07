<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    export let params = {}
    const board_id = params.board_id

    let error = {detail:[]}
    let subject = ''
    let content = ''

    fastapi("get", "/api/board/detail/" + board_id, {}, (json) => {
        subject = json.subject
        content = json.content
    })

    function update_board(event) {
        event.preventDefault()
        let url = "/api/board/update"
        let params = {
            board_id: board_id,
            subject: subject,
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
    <h5 class="my-3 border-bottom pb-2">수정하기</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" bind:value="{subject}">
        </div>
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click="{update_board}">수정하기</button>
    </form>
</div>
