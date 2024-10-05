# r, c, k = 6, 5, 6
# golem = [[2, 3],
#          [2, 0],
#          [4, 2],
#          [2, 0],
#          [2, 0],
#          [2, 2]]
r, c, k = map(int, input().split())
golem = [list(map(int, input().split())) for _ in range(k)]

# 주어진 좌표는 1-r, 1-c이기 때문에 인덱스 처리를 위해 1빼줌
for i in range(len(golem)):
    golem[i][0] -= 1
# rxc 격자 생성 -> 입장 하기 전을 위해 위에 세칸 더 생성
board = [[0] * c for _ in range(r+3)]
cnt = 1
result = 0  # 정렬의 최종 위치 행
#       북 동 남 서
# dirs = [0, 1, 2, 3]
# dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
def set_golem(x, y, dir_out):
    global cnt, exits
    board[x][y] = cnt
    board[x-1][y] = cnt
    board[x+1][y] = cnt
    board[x][y-1] = cnt
    board[x][y+1] = cnt
    cnt += 1
    exits.append([x + dx[dir_out], y + dy[dir_out]])

#  골렘 이동
def move_golem(in_y, dir_out):
    # 가운데 좌표 x, y
    x, y = 1, in_y # 가장 먼저 입장 하기 전의 x좌표 : 1(세칸 늘렸음)

    # 더이상 움직이지 못할 때까지 반복
    while True:
        # 남쪽 이동
        # 왼, 가, 오 아래가 비어있어야함
        if y >= 1 and y <= c and x<=r and  sum([board[x+1][y-1], board[x+2][y], board[x+1][y+1]]) == 0:
            x += 1
        # 서쪽 이동 -> 남쪽 이동, 출구 반시계
        # 왼위, 왼가, 왼아, 왼왼아, 왼아아 빈칸
        elif y >= 2 and x <= r and sum([board[x-1][y-1], board[x][y-2], board[x+1][y-1], board[x+1][y-2], board[x+2][y]]) == 0:
            x += 1  #남
            y -= 1  #서
            dir_out = (dir_out-1) % 4
        # 동쪽 이동 -> 남쪽 이동, 출구 시계
        # 오위, 오가, 오아, 오오아, 오아아 빈칸
        elif y >= 1 and y <= c-3 and x <= r and sum([board[x-1][y+1], board[x][y+2], board[x+1][y+1], board[x+1][y+2], board[x+2][y+1]]) == 0:
            x += 1  #남
            y += 1  #동
            dir_out = (dir_out+1) % 4


        # 어느 곳으로도 움직일 수 없음
        else:
            break

    return x, y, dir_out

from collections import deque
def move_soul(exits, x, y):
    # 인접 골렘이 있을 경우 -> 이동 / 아니라면 가장 남쪽으로 이동
    visited = [[0]*c for _ in range(r+3)]
    q = deque()
    q.append([x, y])
    visited[x][y] = 1
    max_x = 0

    while q:
        x, y = q.popleft()
        max_x = max(max_x, x)
        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d]
            # 격자 밖
            if not board_check(nx, ny): continue
            # 이미 방문함
            if visited[nx][ny] == 1:    continue
            # 골렘의 안 / 골렘의 출구 -> 다른 골렘
            if board[nx][ny] == board[x][y]  or (board[nx][ny] >= 1 and [x,y] in exits):
                q.append([nx, ny])
                visited[nx][ny] = 1

    return max_x -3 +1

def print_board(board):
    for line in board:
        print(line)

# 골렘의 가운데 좌표가 최소 격자 두칸 아래 와야함(격자의 첫번째 x: 3)
def is_board(x):
    return x < 3
def board_check(x, y):
    return  0<= x < r+3 and 0 <= y < c

exits = []               # 골렘 출구 좌표

# k개의 정령이 움직임
# 내려올 열, 출구 방향
for in_y, dir_out in golem:
    # 골렘 이동 -> 정령이동

    # 정렬 입장
    # 골렘이 가능한 경우로 모두 움직였는데도, 삐져나온 경우 -> 격자 지우고 턴 종료
    # 골렘의 출입구 저장 필요 -> 회전 할 때마다 회전
    # 남쪽이동 -> 서쪽이동 -> 동쪽이동 : 이동 우선순위
    # 서/동 쪽으로 이동 후, 방향을 남쪾으로 회전하고 이동
    # 정령 골렘 하차는 정해진 출구로 해야함
    # 정령 하차 할때, 인접한 골렘이 있다면 탑승 가능


    # 골렘 이동
    x, y, dir_out = move_golem(in_y, dir_out)

    # 튀어나온 좌표 있는지 확인 -> 만약 튀어나오면 좌표 클리어
    if is_board(x):
        board = [[0] * c for _ in range(r+3)]
        exits = []
        cnt = 1
        continue
    # 골렘 세팅
    set_golem(x, y, dir_out)
    # print(exits)
    # print_board(board)
    # print('---')

    # 정령이동
    value = move_soul(exits, x, y)
    # print(value)
    result += value
print(result)