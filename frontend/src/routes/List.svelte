<script>
  import { page, keyword, is_login } from '../lib/store.js';
  import fastapi from "../lib/api";
  import { link } from 'svelte-spa-router';
  import moment from 'moment/min/moment-with-locales';
  moment.locale('ko');
  
    let board_list = [];
    let size = 10; // 한 페이지에 보여줄 아이템 수
    let total = 0; // 총 아이템 수
    let kw = '';
    let totalPage = 0; // 총 페이지 수 계산

    let currentPage;
    $: totalPage = Math.ceil(total / size); // 총 페이지 수
  
    $: currentPage, get_board_list(); // currentPage 변화에 따라 목록을 가져옴
    $: $keyword, get_board_list();
  
    // 페이지 번호 스토어 구독
    $: $page, currentPage = $page;
 
  
    async function get_board_list() {
      let params = { page: currentPage, size: size, keyword: $keyword };
      fastapi('get', '/api/board/list', params, 
        (json) => {
            board_list = json.board_list;
            total = json.total;
        }, 
        (error) => { console.error(error); }
      );
    }
  
    function goToPage(_page) {
      page.set(_page); // 스토어 업데이트
    }

    function handleSearch(event) {
        event.preventDefault(); // 기본 form 제출 동작 방지
        $keyword = kw; // 검색어 스토어 업데이트
        $page = 0; // 페이지를 처음으로 설정
        get_board_list(); // 검색 결과를 가져오는 함수 호출
    }
  </script>
  
  <div class="container">
    <div class="mx-auto col-4 my-4">
      <form on:submit={handleSearch}>
          <div class="input-group">
              <input type="text" class="form-control" bind:value="{kw}">
              <button class="btn btn-outline-secondary" type="submit">
                  검색
              </button>
          </div>
      </form>
    </div>
    <table class="table table-hover table-responsive">
        <thead class="table" style="border-top: 3px solid; border-bottom: 1px solid;">
        <tr>
            <th scope="col">#</th>
            <th scope="col">제목</th>
            <th scope="col">글쓴이</th>
            <th scope="col">작성일시</th>
        </tr>
        </thead>
        <tbody>
        {#each board_list as board, i (board.id)}
        <tr>
          <td>{total - (size * currentPage + i)}</td>
          <td>
              <a use:link href="/detail/{board.id}">{board.subject}</a>
              {#if board.comments.length > 0 }
                  <span class="text-danger small mx-2">{board.comments.length}</span>
              {/if}
          </td>
          <td>{ board.user ? board.user.username : "" }</td>
          <td>{moment(board.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>
        </tr>
        {/each}
        </tbody>
    </table>
    <!-- 글쓰기 버튼, 로그인 상태일 때만 보임 -->
    <!-- {#if $is_login} -->
    <div class="d-flex justify-content-end">
      <a use:link href="/board-create" class="btn btn-primary {$is_login ? '' : 'disabled'}">글쓰기</a>
    </div>
    <!--{/if}-->
    <!-- 페이징 컨트롤 -->
    <nav aria-label="Page navigation">
        <ul class="pagination justify-content-center">
          <!-- 처음 페이지로 이동 -->
          <li class="page-item">
            <button class="page-link" on:click={() => goToPage(0)}>&lt;&lt;</button>
          </li>
          <!-- 이전 페이지로 이동 -->
          {#if currentPage > 0}
          <li class="page-item">
            <button class="page-link" on:click={() => goToPage(currentPage - 1)}>&lt;</button>
          </li>
          {/if}
          <!-- 페이지 번호 -->
          {#each Array(totalPage) as _, i}
          {#if i >= currentPage - 5 && i <= currentPage + 5}
          <li class="page-item {i === currentPage ? 'active' : ''}">
            <button class="page-link" on:click={() => goToPage(i)}>{i + 1}</button>
          </li>
          {/if}
          {/each}
          <!-- 다음 페이지로 이동 -->
          {#if currentPage < totalPage - 1}
          <li class="page-item">
            <button class="page-link" on:click={() => goToPage(currentPage + 1)}>&gt;</button>
          </li>
          {/if}
          <!-- 마지막 페이지로 이동 -->
          <li class="page-item">
            <button class="page-link" on:click={() => goToPage(totalPage - 1)}>&gt;&gt;</button>
          </li>
        </ul>
      </nav>

  </div>