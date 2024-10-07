# n, m, p, c, d = 5,7,4,2,2
# rx, ry = 3,2
# santa = [[1,1,3],
#          [2,3,5],
#          [3,5,1],
#          [4,4,4]]
#
#
n, m, p, c, d = map(int, input().split())
rx, ry = map(int, input().split())
santa = [list(map(int, input().split())) for _ in range(p)]
board = [[0]*n for _ in range(n)]

# id : x, y, 점수, 기절, 탈락
santa = {sid:[x-1, y-1, 0, 0, False] for sid, x, y in santa}
santa = dict(sorted(santa.items()))

# 탈락한 산타
removal = []
# 루돌프: -1, 산타: 1-p, 빈칸: 0
rx -= 1
ry -= 1
board[rx][ry] = -1

#     상  우  하 좌 상좌 상우 하우 하좌
dx = [-1, 0, 1, 0, -1, -1, 1, 1]
dy = [0, 1, 0, -1, 1, -1, 1, -1]

def set_board_santa():
    for idx, (x, y, _, _, alive) in santa.items():
        if alive: continue
        # if not alive:
        board[x][y] = idx

set_board_santa()


def get_direct(rx, ry, sx, sy):
    # sx, sy = santa[idx][0], santa[idx][1]
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

def move_rudolf():
    global rx, ry

    # 1. 가장 가까운 산타 선택
    scandi = []
    for idx, info in santa.items():
        if info[4]: continue
        x, y = info[0], info[1]
        d = (rx - x)**2 + (ry - y)**2
        scandi.append([d, x, y, idx])
    scandi.sort(key= lambda x:(x[0], -x[1], -x[2]))
    select_santa = scandi[0]
    sx, sy = select_santa[1], select_santa[2]

    # 2. 이동 방향 선택
    di = get_direct(rx, ry, sx, sy)
    # print(f"루돌프 선택 산타:{select_santa[-1]}, 이동 방향: {di} {rx, ry} -> {rx +dx[di], ry + dy[di]}")

    # 3. 루돌프 공중으로 점프..
    board[rx][ry] = 0
    rx += dx[di]
    ry += dy[di]
    return di

def is_board(x, y):
    return 0 <= x < n and 0 <= y < n

from collections import deque
def crash(who, sid, di, sx, sy):
    global board

    # 1. 충돌 점수 획득
    score = d if who == 'santa' else c
    santa[sid][2] += score

    # 2. 기절 1턴 동안
    santa[sid][3] = 2

    # 3. score만큼 밀려남
    if who == 'santa':
        di = ((di + 4) -2) % 4  # 산타 반대방향

    q = deque()
    q.append([sx, sy, score, sid])

    while q:
        sx, sy, score, mid = q.popleft()
        nx = sx + dx[di]*score
        ny = sy + dy[di]*score
        # 격자 밖 -> 탈락
        if not is_board(nx, ny):
            santa[mid][4] = True
            removal.append(mid)
            break
        # 다른 산타 존재
        if board[nx][ny] > 0 and board[nx][ny] != mid:
            q.append([nx, ny, 1, board[nx][ny]])
            santa[mid][0], santa[mid][1] = nx, ny
        # 무사히 도착
        else:
            santa[mid][0], santa[mid][1] = nx, ny
            break
    board = [[0] * n for _ in range(n)]
    # 산타, 루돌프 보드 배치
    set_board_santa()

    board[rx][ry] = -1
    return

def move_santa(sid):
    # 루돌프와 가까워지는 방향 탐색
    # 가까워 질 수 없으면 움직이지 않음
    # 다른 산타 존재하면 움직이지 않음
    sx, sy = santa[sid][0], santa[sid][1]
    cur_dist = (rx - sx)**2 + (ry - sy)**2
    candi = []
    # 상 우 하 좌 -> 우선순위
    for dd in range(4):
        nx = sx + dx[dd]
        ny = sy + dy[dd]
        # 격자 밖 / 다른 산타 존재
        if not is_board(nx, ny) or board[nx][ny] > 0:   continue
        dist = (rx - nx)**2 + (ry - ny)**2
        if cur_dist > dist:
            cur_dist = dist
            candi.append([nx, ny, dd])
    # 가까워 지는 방향 없음 -> 이동 불가
    if len(candi) == 0: return

    nx, ny, di = candi.pop()
    # 루돌프 충돌
    if board[nx][ny] == -1:
    # if [rx, ry] == [nx, ny]:
        crash('santa', sid, di, nx, ny)
    else:
        santa[sid][0], santa[sid][1] = nx, ny
        board[sx][sy] = 0
        board[nx][ny] = sid

    return



# m개의 턴
for mm in range(m):
    # 모든 산타가 탈락 -> 즉시 종료
    if len(removal) == p:break
    # 산타 기절 턴 -1
    for id, info in santa.items():
        if info[3] > 0 and not info[4]:
            santa[id][3] -= 1

    # 1. 루돌프 이동
    di = move_rudolf()

    # 1.1 루돌프 충돌 -> 산타 밀고 착지
    if board[rx][ry] > 0:
        crash('rudolf', board[rx][ry], di, rx, ry)
        board[rx][ry] = -1
    # 1.2 충돌 없이 착지
    else:
        board[rx][ry] = -1

    # 2. 산타 이동
    for pp in range(1, p+1):
        # 탈락한 산타 이동 불가
        if santa[pp][4] or santa[pp][3] > 0:
            continue

        move_santa(pp)

    # 3. 살아남은 산타 점수 획득
    for idx, (_, _, _, _, alive) in santa.items():
        if alive: continue
        santa[idx][2] += 1


santa = [str(value[2]) for value in santa.values()]
print(' '.join(santa))