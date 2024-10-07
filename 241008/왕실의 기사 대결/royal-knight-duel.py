l, n, q = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(l)]
# r, c, h, w, k
sirs = [list(map(int, input().split())) for _ in range(n)]
# i, d
orders = [list(map(int, input().split()))for _ in range(q)]
#               x,   y,   크기, 체력, 받은 데미지, 탈락여부
sirs = {idx+1:[[x-1, y-1], [h, w],  k,      0,        False] for idx, (x, y, h, w, k) in enumerate(sirs)}
# 격자 내부 확인
def is_board(x, y):
    return 0 <= x < l and 0<= y < l

# 0:위, 1:오, 2:아, 3:왼
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

from collections import deque
def move_sir(id, di):
    # [x, y] = sirs[id][0]
    q = deque()
    q.append(id)

    check = set()
    # 이동이 완료 된 후, 데미지 적용하기 때문에 따로 저장
    demage = [0]* (n+1)
    # print(demage)
    while q:
        sid = q.popleft()
        # print('이동하는 기사:', sid)
        [x, y], [h, w] = sirs[sid][0], sirs[sid][1]

        nx = x + dx[di]
        ny = y + dy[di]
        # print(f"{x, y} ->{nx, ny} ")
        for i in range(nx, nx + h):
            for j in range(ny, ny + w):
                # print(i, j)
                # 벽이 발견되면 모두 취소
                if not is_board(i,j) or board[i][j] == 2:
                    # print('벽')
                    return
                # 함정이 있는 만큼 데미지
                if board[i][j] == 1:
                    demage[sid] += 1

        # 이동 했을때 밀리는 기사 확인
        for ss in sirs.keys():
            # 이미 이동하는 기사 넘어가기
            if ss in check or sirs[ss][-1]: continue
            [sx, sy], [sh, sw] = sirs[ss][0], sirs[ss][1]
            # 왼쪽 상단 모서리가 다른 격자 내부에 존재 / 오른쪽 하단 모서리가 다른 격자 내부에 존재
            if (nx <= sx + sh + -1 and ny <= sy + sw -1) and (sx <= nx + h-1 and sy <= ny + w -1):
                q.append(ss)
                check.add(ss)

    # 명령 받은 기사의 데미지 0으로
    demage[id] = 0
    # for key, value in sirs.items():
    for key in check:
        # print(f"{key}기사 {demage[key]}데미지")
        sirs[key][3] += demage[key]
        sirs[key][2] -= demage[key]
        # 받은 데미지가 체력보다 크면 탈락
        # if sirs[key][2] > sirs[key][3]:
        if sirs[key][2] < 0:
            sirs[key][4] = True
        else:
            [sx, sy] = sirs[key][0]
            sirs[key][0] = [sx + dx[di], sy + dy[di]]
    # print(sirs)




    # print(x, y)
# q 개의 명령을 수행
for id, di in orders:
    # print()
    # print(f"{id}기사가 {di}방향으로 이동")
    # 탈락한 기사 명령 수행 
    if sirs[id][4]:
        # print('탈락 기사 명령 무시')
        continue

    # 기사 이동
    move_sir(id, di)
    # print(sirs)

output = [value[3] for value in sirs.values() if not value[4]]
# print(output)
print(sum(output))