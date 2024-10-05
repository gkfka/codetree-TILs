r, c, k = map(int, input().split())
golem = [list(map(int, input().split())) for _ in range(k)]

# 격자 밖으로 나가면 안됨 / 인덱스가 1로 시작 -> 격자 밖(y)을 벽으로 둘러쌈
# 골렘이 격자에 입장하기 전 밖에 있는 모습을 표현하기 위해 x값을 늘려줌 -> 3칸늘림
board = [[1] + [0]*c + [1] for _ in range(r+3)] + [[1]*(c+2)]

# 방향 -> 북동남서(시계)
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

def move_golem(in_y, di):
    x, y = 1, in_y  # 골렘이 입장 전 상태

    # 더이상 움직일 수 없을 때 까지
    while True:
        # 남쪽 이동
        # 왼아, 가아, 오아 빈칸
        if sum([board[x+1][y-1], board[x+2][y], board[x+1][y+1]]) == 0:
            x += 1  # 남쪽 이동

        # 서쪽 이동 -> 남쪽 이동
        # 왼위, 왼가, 왼아, 왼왼아, 왼아아 빈칸
        elif sum([board[x-1][y-1], board[x][y-2], board[x+1][y-1], board[x+1][y-2], board[x+2][y-1]]) == 0:
            y -= 1  # 서쪽 이동
            x += 1  # 남쪽 이동
            di = (di - 1) % 4   # 출구 반시계 이동

        # 동쪽 이동 -> 남쪽 이동
        # 오위, 오가, 오아, 오오아, 오아아 빈칸
        elif sum([board[x-1][y+1], board[x][y+2], board[x+1][y+1], board[x+1][y+2], board[x+2][y+1]]) == 0:
            y += 1  # 동쪽 이동
            x += 1  # 남쪽 이동
            di = (di + 1) % 4   # 출구 시계 이동

        # 더이상 이동 불가능
        else:
            break

    return x, y, di

# 골렘이 튀어나갔는지 확인
def is_board(x):
    # x를 늘린 것을 고려해야함 / 골렘의 가운데가 4에 와야 골렘이 모두 안에 위치
    return x < 4

# 골렘 격자에 위치 시키기
def set_golem(x, y, di):
    global cnt, exits

    board[x][y-1:y+2] = [cnt] * 3
    board[x-1][y] = board[x+1][y] = cnt


    cnt += 1    # 다음 골렘
    exits.append([x + dx[di], y + dy[di]])  # 골렘의 출구 저장

from collections import deque
# 정령 이동
def move_elf(x, y):
    visited = [[1] + [0]*c + [1] for _ in range(r+3)] + [[1]*(c+2)]

    q = deque()
    q.append([x, y])
    visited[x][y] = 1
    max_x = 0

    while  q:
        x, y = q.popleft()
        max_x = max(x, max_x)
        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d]

            # 이미 방문함
            if visited[nx][ny] == 1: continue
            # 골렘 안에서 가장 남쪽으로 움직임 / 골렘의 출구로 나가서 인접한 골렘으로 이동
            if (board[nx][ny] == board[x][y]) or (board[nx][ny] > 1 and [x, y] in exits):
                q.append([nx, ny])
                visited[nx][ny] = 1

    return max_x - 2    # 골렘 입장을 위해 늘린만큼 제거/격자 1로 시작

exits = []  # 골렘 출구를 저장
cnt = 2     # 0: 빈칸, 1: 벽, 2이상: 골렘
result = 0  # 누저 값

# k개의 정령 이동
for in_y, di in golem:
    # 골렘 이동
    x, y , di = move_golem(in_y, di)

    # 골렘이 밖으로 튀어 나갔는지 확인
    if is_board(x):
        # 격자를 초기화
        board = [[1] + [0]*c + [1] for _ in range(r+3)] + [[1]*(c+2)]
        cnt = 2     # 골렘 다 치우기
        exits = []  # 출구 비우기
        continue    # 다음 정령 탐색

    # 골렘 격자에 위치 시키기
    set_golem(x, y, di)

    # 정령 이동
    result += move_elf(x, y)
print(result)