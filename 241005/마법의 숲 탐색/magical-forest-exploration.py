from collections import deque
# rxc 격자, 정령의 수 k
# 골렘이 출발하는 열 ci, 골렘의 출구 정보 di
# 0북, 1동, 2남, 3서 : 골렘의 출구 정보
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
r, c, k = map(int, input().split())
golem = [list(map(int, input().split())) for _ in range(k)]

# r, c, k = 6, 5, 6
# golem = [[2, 3], [2, 0], [4, 2], [2, 0], [2, 0], [2, 2]]

# 골렘의 위치를 나타냄
golem_board = [[1] + [0] * c + [1] for _ in range(r+3)] + [[1]*(c+2)]
gol = 2
exit_list = set()
result = 0


# 격자의 가장 아래 : r, 격자 가장 위 : 1
# -> 격자밖 1로 둘러싸버린다, 빈칸 :0, 골렘 숫자 2부터
# golem = [[x-1, y] for (x, y) in golem]

# 골렘의 중앙이 ci열에 위치하도록 남쪽으로 내려감
# 우선순위 이동 -> 더이상 움직일 수 없을 때까지 반복
# 남쪽으로 이동 -> 서쪽으로 회전[출구 반시계이동, ] -> 동쪽으로 회전[출구 시계방향이동]

# 1. 골렘 이동 -> 골렘의 몸이 격자 밖이라면 격자 reset, 이때, 답 누적 하지 않음 ->2. 정령이동

# 골렘이동
def move_golem(golem_board, cy,di):
    cx= 1
    # 더이상 움직일 수 없을 때까지 이동
    while True:
        # 남쪽이동 # 세 칸이 빈 칸이면 이동가능
        # 왼, 가, 오
        if sum([golem_board[cx+1][cy-1] , golem_board[cx+2][cy] , golem_board[cx+1][cy+1]]) == 0:
            cx += 1
        # 서쪽이동, 출구 반시계
        # 위, 가, 아, 이동 후 왼, 이동 후, 아
        elif sum([golem_board[cx-1][cy-1] , golem_board[cx][cy-2] , golem_board[cx+1][cy-1] , golem_board[cx+1][cy-2] , golem_board[cx+2][cy-1]]) == 0:

            cy -=1
            cx += 1
            di = (di - 1) % 4
        # 동쪽이동, 출구 시계
        # 위, 가, 아, 이동후 오, 이동후 아
        elif sum([golem_board[cx-1][cy+1] , golem_board[cx][cy+2] , golem_board[cx+1][cy+1] , golem_board[cx+1][cy+2] , golem_board[cx+2][cy+1]]) == 0:
            cy += 1
            cx += 1
            di = (di + 1) % 4
        else:
            break
    return cx, cy, di


# 골렘의 가운데 x좌표가 범위 밖이면 True

def is_board(x):
    return x<4

def set_golem(x, y, di):
    global gol
    golem_board[cx][cy-1:cy+2] = [gol] * 3
    golem_board[cx-1][cy] = golem_board[cx + 1][cy] = gol
    gol += 1

    exit_list.add((x + dx[di], y + dy[di]))
    return gol
def move_elf(cx, cy):
    visited = [[0]*(c+2) for _ in range(r+4)]
    q = deque()
    q.append([cx, cy])
    visited[cx][cy] = 1

    max_x = 0

    while q:
        x, y = q.popleft()
        max_x = max(max_x, x)
        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d]
            # 이미 방문한 격자 넘어가기
            if visited[nx][ny] == 1:    continue
            # 같은 골렘 내부에서 움직이기 or 출구를 통해 다른 골렘으로 이동하기
            if golem_board[nx][ny] == golem_board[x][y] or  (golem_board[nx][ny] > 1 and (x,y) in exit_list):
                q.append([nx, ny])
                visited[nx][ny] = 1
    # 골렘이 입장하기 위해 만들어둔 좌표를 제외한 값을 출력
    return max_x - 2

# k 개의 정령이 이동
for idx, (ci,di) in enumerate(golem):

    # 골렘이동
    cx, cy, di = move_golem(golem_board, ci, di)
    # 격자 밖인지 확인
    if is_board(cx):

        golem_board = [[1] + [0] * c + [1] for _ in range(r + 3)] + [[1] * (c + 2)]
        exit_list = set()
        gol = 2
        continue

    # 골렘 배치
    gol = set_golem(cx, cy, di)

    # 정령이동
    # 마지막 값 누적
    result += move_elf(cx, cy)

print(result)