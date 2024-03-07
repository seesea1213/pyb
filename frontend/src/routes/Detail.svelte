<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { link, push } from 'svelte-spa-router'
    import { is_login, username } from "../lib/store"
    import { marked } from 'marked'
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    export let params = {}
    let board_id = params.board_id
    let board = {comments:[], voter:[], content: ''}
    let content = ""
    let error = {detail:[]}

    function get_board() {
        fastapi("get", "/api/board/detail/" + board_id, {}, (json) => {
            board = json
        })
    }

    get_board()

    function post_comment(event) {
        event.preventDefault()
        let url = "/api/comment/create/" + board_id
        let params = {
            content: content
        }
        fastapi("post", url, params, 
            (json) => {
                content = ""
                error = {detail:[]}
                get_board()
            },
            (err_json) => {
                error = err_json
            }
        )
    }

    function delete_board(_board_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/board/delete"
            let params = {
                board_id: _board_id
            }
            fastapi('delete', url, params, 
                (json) => {
                    push('/')
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }
    function delete_comment(comment_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/comment/delete"
            let params = {
                comment_id: comment_id
            }
            fastapi('delete', url, params, 
                (json) => {
                    get_board()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }
    function vote_board(_board_id) {
        if(window.confirm('정말로 추천하시겠습니까?')) {
            let url = "/api/board/vote"
            let params = {
                board_id: _board_id
            }
            fastapi('post', url, params, 
                (json) => {
                    get_board()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }
    function vote_comment(comment_id) {
        if(window.confirm('정말로 추천하시겠습니까?')) {
            let url = "/api/comment/vote"
            let params = {
                comment_id: comment_id
            }
            fastapi('post', url, params, 
                (json) => {
                    get_board()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

</script>

<div class="container my-4">
    <div class="border-bottom py-2">
        <h2 class="mb-2">{board.subject}</h2>
        <div class="d-flex justify-content-between align-items-center">
            <span class="text-muted">작성자: { board.user ? board.user.username : "" }</span>
            <!-- 수정된 날짜와 생성날짜 모두 출력
            <span class="badge text-dark p-2">
                {#if board.modify_date }
                {moment(board.modify_date).format("YYYY년 MM월 DD일 hh:mm a")} 수정됨 |
                {/if}
                {moment(board.create_date).format("YYYY년 MM월 DD일 hh:mm a")}
            </span>
            -->
            <!-- 수정된 날짜만 출력-->
            <span class="badge text-dark p-2">
                {#if board.modify_date}
                    {moment(board.modify_date).format("YYYY년 MM월 DD일 hh:mm a")} 수정됨
                {:else}
                    {moment(board.create_date).format("YYYY년 MM월 DD일 hh:mm a")}
                {/if}
            </span>
        </div>
    </div>

    <div class="card my-3"> 
        <div class="card-body">
            <div class="card-text mb-5">{@html marked.parse(board.content)}</div>
            <div class="d-flex justify-content-center">
                <button class="btn btn-sm btn-outline-secondary"
                on:click="{vote_board(board.id)}"> 
                추천
                <span class="badge rounded-pill bg-success">{ board.voter.length }</span>
                </button>
            </div>
        </div>
    </div>

    <h5 class="border-bottom my-3 py-2">{board.comments.length}개의 댓글</h5> 

    {#each board.comments as comment}
    <div class="card my-2">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2"> 
                <span class="text-muted">작성자: { comment.user ? comment.user.username : "" }</span> 
                <!-- 수정된 날짜와 생성날짜 모두 출력
                <span class="badge text-dark p-2">
                    {#if comment.modify_date }
                    {moment(comment.modify_date).format("YYYY년 MM월 DD일 hh:mm a")} 수정됨 |
                    {/if}
                    {moment(comment.create_date).format("YYYY년 MM월 DD일 hh:mm a")}
                </span>
                -->
                <!-- 수정된 날짜만 출력-->
                <span class="badge text-dark p-2">
                    {#if comment.modify_date}
                        {moment(comment.modify_date).format("YYYY년 MM월 DD일 hh:mm a")} 수정됨
                    {:else}
                        {moment(comment.create_date).format("YYYY년 MM월 DD일 hh:mm a")}
                    {/if}
                </span>
            </div>
            <div class="card-text">{@html marked.parse(comment.content)}</div>
        </div>
        <div class="d-flex justify-content-end mb-2">
            <button class="btn btn-sm btn-outline-secondary"
                    on:click="{vote_comment(comment.id)}"> 
                    추천
                    <span class="badge rounded-pill bg-success">{ comment.voter.length }</span>
            </button>
            {#if comment.user && $username === comment.user.username }
            <a use:link href="/comment-modify/{comment.id}" class="btn btn-sm btn-outline-secondary">수정</a>
            <button class="btn btn-sm btn-outline-secondary"
                on:click={() => delete_comment(comment.id) }>삭제</button>
            {/if}
        </div>
    </div>
    {/each}

    <Error error={error} /> 

    <form method="post" class="my-3">
        <div class="mb-3 input-group"> 
          <textarea id="comment-content" rows="3" bind:value={content} disabled={$is_login ? "" : "disabled"} class="form-control" />  
          <input type="submit" value="댓글등록" class="btn-secondary" on:click="{post_comment}" />
        </div>
    </form>

    <div class="d-flex justify-content-between">
        <div>
            <button class="btn btn-sm btn-outline-secondary" on:click="{() => {
                push('/')
            }}">목록</button>
        </div>
        <div>
            {#if board.user && $username === board.user.username }
            <a use:link href="/board-modify/{board.id}" class="btn btn-sm btn-outline-secondary">수정</a>
            <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => delete_board(board.id)}>삭제</button>
            {/if}
        </div>
        
    </div>
    
     
</div>