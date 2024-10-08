# n, m, k = map(int, input().split())
# # 미로 정보
# board = [list(map(int, input().split())) for _ in range(n)]
#
# people = [list(map(int, input().split())) for _ in range(m)]
# ex, ey = map(int, input().split())

n, m, k = 5, 3, 8
board = [[0, 0, 0, 0, 1],
         [9, 2, 2, 0, 0],
         [0, 1, 0, 1, 0],
         [0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0]]
people = [[1, 3],
          [3, 1],
          [3, 5]]
ex, ey =  3,3


# x, y, 이동 거리, 탈출여부
people = {idx: [[x-1, y-1], 0, False] for idx,(x, y) in enumerate(people)}
ex -= 1
ey -= 1
# 탈출한 사람 저장
escape = []
# 상 하 -> 좌 우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def is_board(x, y):
    return 0<= x < n and 0<= y <n

def move_people(pid):
    [x, y] = people[pid][0]
    candi = []
    # 현재 거리
    cur_dist = abs(x-ex) + abs(y-ey)
    for d in range(4):
        nx = x + dx[d]
        ny = y + dy[d]

        # 격자 밖 / 벽
        if not is_board(nx, ny) or board[nx][ny] > 0:
            continue

        # 탈출 -> 이동거리 1 늘리고, 탈출 on
        if [nx, ny] == [ex, ey]:
            people[pid][1] += 1
            people[pid][2] = True
            escape.append(pid)
            return

        dist = abs(nx-ex) + abs(ny-ey)
        if cur_dist > dist:
            cur_dist = dist
            candi.append([nx, ny])
    # 움직일 수 없음
    if len(candi) == 0: return
    x, y = candi.pop()
    people[pid][0] = [x, y]
    people[pid][1] += 1

    return

def get_square():
    # 정사각형 찾기 -> 정사각형은 최소 2이상 n이하의 길이
    for ll in range(1, n+1):
        # 정사각형의 왼쪽 상단 좌표
        # r좌표가 작은 것이 우선 순위
        for x1 in range(0, n-ll + 1):
            # c좌표가 작은 것이 우선 순위
            for y1 in range(0, n-ll +1):
                # 정사각형의 오른쪽 하단 좌표
                x2 = x1 + ll
                y2 = y1 + ll
                # print(f"{x1, y1}, {x2, y2}")
                # 정사각형 내부 출구 여부
                if not (x1<= ex <= x2 and y1 <= ey <= y2):
                    # print('출구가 없음')
                    continue
                # 한명만 있어도 됨
                is_people = False
                # 정사각형 내부 참가자 여부
                for [x, y], _, alive in people.values():
                    # 탈출 제외
                    if alive: continue
                    if x1 <= x <= x2 and y1 <= y <= y2:
                        is_people = True
                        # print(x, y, '사람 있음')
                        break
                if is_people:
                    # print(x1, y1, x2, y2, ll)
                    return x1, y1, x2, y2, ll
def rotate(x1, y1, x2, y2, ll):

    new_board = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if x1<= i <= x2 and y1 <= j <= y2:
                # nx = j
                # ny = ll - i
                nx, ny = set_xy(i, j, x1, y1, ll)
                # print(f"{i, j} -> {nx, ny-1}")
                new_board[nx][ny] = board[i][j]
            else:
                new_board[i][j] = board[i][j]
    return new_board
def set_xy(x, y, x1, y1, ll):
    tempx, tempy = x - x1, y - y1
    # print(f"x: {x}, y:{y}, x1:{x1}, y1:{y1}, tempx: {tempx}, tempy : {tempy}")

    nx = tempy
    ny = ll - tempx
    return nx + x1, ny + y1
def maze_rotate():
    global board, ex, ey
    # 정사각형 찾기
    x1, y1, x2, y2, ll = get_square()
    # print(f"선택 사각형 왼위{x1, y1}, 길이 {ll}, ")
    # 선택된 죄표 내부 벽 내구도 -1
    for xx in range(x1, x2+1):
        for yy in range(y1, y2+1):
            # print('정사각형 내부 :',xx, yy)
            if board[xx][yy] > 0:
                board[xx][yy] -=1
    # for line in board:
    #     print(line)
    # print('내구도 -1 이후')

    # 정사각형 회전
    board = rotate(x1, y1, x2, y2, ll)
    # print(f"회전 후선택 사각형 왼위{x1, y1}, 길이 {ll}, ")

    # for line in board:
    #     print(line)
    # print('보드회전 완료')
    # 선택된 좌표 회전 -> 사람 좌표, 출구 좌표 조정
    for idx, ([x, y], _, alive) in people.items():
        if alive: continue  # 탈출 한 사람 제외
        if x1<= x <= x2 and y1 <= y <= y2:
            nx, ny = set_xy(x, y, x1, y1, ll)
            # print(f"{x, y} -> {nx, ny}")
            people[idx][0] = [nx, ny]
    # 출구 회전
    # temp = ex
    # ex = x1 + ey
    # ey = ll - temp + y1
    ex, ey = set_xy(ex, ey, x1, y1, ll)

# k초 동안 반복
for kk in range(k):
    # 모든 참가자가 탈출 -> 게임 종료
    if len(escape) == m:
        # print('모두 탈출')
        break

    # 모든 참가자 이동
    for pid in people.keys():
        # 탈출 한 경우
        if people[pid][2]:  continue
        move_people(pid)

    # print(people)
    # print('출구: ',ex, ey)
    # print('이동완료')

    # 미로 회전
    maze_rotate()
    # print('회전 완료')
    # for line in board:
    #     print(line)
    # print(people)
    # print('출구: ', ex, ey)
    # print(kk+1, '초 --')
    # input()
output = [value[1] for value in people.values()]
print(sum(output))
print(ex+1, ey+1)