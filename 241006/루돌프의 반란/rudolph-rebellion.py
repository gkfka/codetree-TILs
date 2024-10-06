n, m, p, c, d = map(int, input().split())
rx, ry = map(int, input().split())
# 0, 1: 산타 위치, 2: 점수, 3: 기절, 4:탈락
init_santa = [list(map(int, input().split())) for _ in range(p)]

# 인덱스 1,1로 시작 -> 0,0 조정
rx -= 1
ry -= 1

santa = {idx : [x-1, y-1, 0, False, False] for idx, x, y in init_santa}
board = [[0] * n for _ in range(n)]

# 탈락한 산타 번호 저장
removal = []
# 기절 산타: 2, 깨어남: 0
pass_out = [0]*(p+1)

# 0   1   2  3   4    5    6    7
# 상, 우, 하, 좌, 상우, 상좌, 하우, 하좌
dx = [-1, 0, 1, 0, -1, -1, 1, 1]
dy = [0, 1, 0, -1, 1, -1, 1, -1]
# def print_board(board):
#     for line in board:
#         print(line)
def get_direct(rx, ry, idx):
    sx, sy = santa[idx][0], santa[idx][1]
    if rx > sx:
        if ry > sy:     return 5    # 상좌
        elif ry < sy:   return 4    # 상우
        else:           return 0    # 상
    elif rx < sx:
        if ry > sy:     return 7    # 하좌
        elif ry < sy:   return 6    # 하우
        else:           return 2    # 하
    else:
        if ry > sy:     return 3    # 좌
        else:           return 1    # 우

# 탈락 산타 확인
def is_board(x, y):
    return 0 <= x < n and 0 <= y < n

from collections import deque
def crash(who, di, santa_id, x, y):
    global board
    score = c if who == 'rudolf' else d
    # 산타 -> 루돌프 충돌 : 방향 반대
    if who == 'santa':
        di = ((di + 4) - 2) % 4

    # 충돌한 산타 점수 + score
    santa[santa_id][2] += score

    # 연쇄반응을 위함
    q = deque()
    q.append([santa_id, x, y, di, score])

    while q:
        s_id, x, y, di, move = q.popleft()
        nx = x + dx[di] * move
        ny = y + dy[di] * move
        # 탈락 확인
        if not is_board(nx, ny):
            santa[santa_id][4] = True
            removal.append(santa_id)

            break
        # 기절 시키기
        santa[santa_id][3] = True
        pass_out[santa_id] += 2

        # 다른 산타 있음 -> 상호작용
        if board[nx][ny] > 0 and board[nx][ny] != santa_id:
            q.append([board[nx][ny], nx, ny, di, 1])
            santa[s_id][0], santa[s_id][1] = nx, ny
        else:
            santa[s_id][0], santa[s_id][1] = nx, ny
            break
    board = [[0]*n for _ in range(n)]
    # 산타 위치시키기
    for id, info in santa.items():
        if info[4]:continue
        x, y = info[0], info[1]
        board[x][y] = id

    # 루돌프 위치 시키기
    board[rx][ry] = -1
    # print('루돌프 이동 후 위치', rx, ry)

    return


def move_rudolf(rx, ry):
    # 가장 가까운 산타 선택
    candi_san = []
    for idx in range(1,p+1):
        # 탈락한 산타는 제외
        if santa[idx][4] :continue
        sx, sy = santa[idx][0], santa[idx][1]

        dist = (rx-sx)**2 + (ry-sy)**2
        candi_san.append([dist, sx, sy, idx])

    # 거리가 가장 작음, x가 큼, y가 큼
    candi_san.sort(key = lambda x:(x[0], -x[1], -x[2]))
    select_santa = candi_san[0][-1]     # 선택된 산타
    # 선택된 산타의 방향 선택
    di = get_direct(rx, ry, select_santa)


    # 루돌프 산타 방향 이동
    board[rx][ry] = 0
    rx += dx[di]
    ry += dy[di]

    if board[rx][ry] > 0:
        # 루돌프 충돌
        crash('rudolf', di, board[rx][ry], rx, ry)

    return rx, ry
def move_santa(s_id):
    x, y = santa[s_id][0], santa[s_id][1]
    candi = []
    # 루돌프와 가까워지는 방향 선택
    for d in range(4):
        nx = x + dx[d]
        ny = y + dy[d]
        dist = (rx - nx)**2 + (ry - ny)**2
        if is_board(nx, ny) and board[nx][ny] <= 0:
            candi.append([dist, d])
    candi.sort()
    di = candi[0][1]
    # 산타 이동
    nx = x + dx[di]
    ny = y + dy[di]
    # 산타 충돌
    if board[nx][ny] == -1:
        crash('santa', di, s_id, nx, ny)

        # def crash(who, di, santa_id, x, y):
    else:
        santa[s_id][0], santa[s_id][1] = nx, ny
        board[x][y] = 0
        board[nx][ny] = s_id
    return
# def set_santa():
#     for id, info in santa.items():

# m 턴동안 반복
for _ in range(m):
    # 모든 산타가 탈락 -> 게임 종료
    if len(removal) == p:
        break

    # 루돌프 이동
    rx, ry = move_rudolf(rx, ry)
    board[rx][ry] = -1
    # 산타 이동
    for pp in range(1,p+1):
        # 탈락한 산타
        if santa[pp][-1]:
            continue
        # 기절 산타
        if pass_out[pp] > 0:
            pass_out[pp] -= 1
            continue
        move_santa(pp)
    # 살아남은 산타 +1
    for id, info in santa.items():
        if info[4]:continue
        santa[id][2] += 1
    # print_board(board)
    # print(santa)
    # input()
score = [str(value[2]) for value in santa.values()]
print(' '.join(score))