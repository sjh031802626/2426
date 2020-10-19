import pygame, sys, random, os, copy, win32ui, time
from pygame.locals import *
import puzzle_game as pg

# 初始化数据
windowSize = windowWidth, windowHeight = 640, 500
white = (255, 255, 255)
font_color = (255, 255, 255)
black = (0, 0, 0)
digital_road_color = (139,69,19)
separation = 5
FPS = 30  # 游戏帧数
list = []
TILE_SIZE = int(windowHeight*0.6)
height = 250
width = 150
# 配置动作
UP = 'w'
DOWN = 's'
LEFT = 'a'
RIGHT = 'd'
pygame.init()
pygame.font.init()
FPS_CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode(windowSize)  # 创建指定大小窗口
# 载入图片
gs = pygame.image.load("images/easy.png")  # 游戏开始
his = pygame.image.load("images/middle.png")  # 历史记录
bg = pygame.image.load("images/3.jpg")
bg2 = pygame.image.load("images/3.jpg")
con = pygame.image.load("images/e.jpg")
# 调整图片大小
iconScale = int(windowWidth*0.08), int(windowHeight * 0.1)
btnScale = int(windowWidth*0.4), int(windowHeight*0.1)
gs = pygame.transform.smoothscale(gs, btnScale)
his = pygame.transform.smoothscale(his, btnScale)
bg = pygame.transform.smoothscale(bg, (int(windowWidth), int(windowHeight)))
bg2 = pygame.transform.smoothscale(bg2, (int(windowWidth), int(windowHeight)))

his_position = []
for j in range(3):
    for i in range(5):
        his_position.append([j*200+30, 200+50*i])
        his_position.append([70+j*200, 200+50*i])
        his_position.append([160+j*200, 200+50*i])


def main():
    size = 0
    steps = 0
    pygame.display.set_caption("滑动拼图")  # 设置窗口标题
    game_start = 0
    t0,t1 = 0, 0
    flag = 0
    orig_list, current_list, target_list, rect, img_area, num_cells, seg_width, pic = 0, 0, 0, 0, 0, 0, 0, 0
    while True:
        if game_start == 0:
            game_before()
        if game_start == -2:
            if flag == 0:
                t1 = time.time()
                flag = 1
            congratulation(t0, steps, t1)
        if game_start != 0 and game_start != -1 and game_start != -2 and game_start != -3:
            t1 = time.time()
            t = int(t1 - t0)
            m = 0
            if t > 60:
                m = int(t // 60)
                t = t % 60
            text = str("%02d"%m) + " : " + str("%02d"%t)
            my_font = pygame.font.Font('3.ttf', 30)
            img = my_font.render(text, True, (255, 255, 255))
            time_rect = (50, 300, 20, 20)
            Game(current_list, num_cells, pic, size, img_area, rect, seg_width, steps, game_start)
            screen.blit(img, time_rect)
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                game_start = history_click(game_start, mouse_x, mouse_y)
                size, game_start = GSBCheckMouse(mouse_x, mouse_y, size, game_start)
                game_start, size, steps, t0 = GSCheckMouse(mouse_x, mouse_y, game_start, size, steps, t0)
                if size != 0 and game_start == 0:
                    '''
                    dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
                    dlg.SetOFNInitialDir('D:\pythonProject\img_match')  # 设置打开文件对话框中的初始显示目录
                    dlg.DoModal()
                    filename = dlg.GetPathName()  # 获取选择的文件名称
                    '''
                    orig_list, current_list, target_list, rect, img_area, num_cells, seg_width, pic = pic_disposal(
                        size, game_start)
                    game_start = 1
                    t0 = time.time()
                    Game(current_list, num_cells, pic, size, img_area, rect, seg_width, steps, game_start)
                    pygame.display.flip()
                #print(game_start)
                game_start = congratulation_click(game_start, mouse_x, mouse_y)
                # 判断滑块移动以及移动效果
                if is_valid_move(mouse_x, mouse_y, game_start):
                    blank_x, blank_y = get_blank_position(current_list, num_cells, size)
                    move_x, move_y, check, steps = check_direction(mouse_x, mouse_y, blank_x, blank_y,
                                                           current_list, img_area, rect, seg_width, size, pic, steps)
                    if check == 1:
                        current_list[blank_x + blank_y * size], current_list[move_x + move_y * size] = \
                            current_list[move_x + move_y * size], current_list[blank_x + blank_y * size]
                        Game(current_list, num_cells, pic, size, img_area, rect, seg_width, steps, game_start)
                    game_start = check_for_quit(current_list, target_list, t0, steps, size, game_start)
                if game_start == 2 or game_start == 6:
                    steps = solve(current_list, target_list, size, img_area, rect, seg_width, pic, steps, game_start)
                    if game_start == 6:
                        game_start = 5
                    else:
                        game_start = 1
                elif game_start == 4 or game_start == 8:
                    steps = next_step(current_list, target_list, size, img_area, rect, seg_width, pic, steps, game_start)
                    if game_start == 8:
                        game_start = 5
                    else:
                        game_start = 1
                elif game_start == 3 or game_start == 7:
                    current_list = orig_list[:]
                    Game(current_list, num_cells, pic, size, img_area, rect, seg_width, steps, game_start)
                    if game_start == 7:
                        game_start = 5
                    else:
                        game_start = 1
                    steps = 0
                elif game_start == -1:
                    history_display()
                elif game_start == -3:
                    screen.blit(bg2, [0, 0])
                    my_font = pygame.font.Font('3.ttf', 35)
                    img = my_font.render("请在键盘上输入3-9中任一数字", True, font_color)
                    screen.blit(img, [80, 200])
                    img = my_font.render("进入n阶游戏", True, font_color)
                    screen.blit(img, [200, 240])
            elif event.type == KEYDOWN:
                key_num = event.key
                if game_start == -3:
                    size, game_start = get_size(key_num, game_start)
                    game_start = 5
                    orig_list, current_list, target_list, rect, img_area, num_cells, seg_width, pic = pic_disposal(
                        size, game_start)
                    t0 = time.time()
                    Game(current_list, num_cells, pic, size, img_area, rect, seg_width, steps, game_start)
                    pygame.display.flip()
        pygame.display.flip()


# 开始游戏
def Game(current_list, num_cells, pic, size, img_area, rect, seg_width, steps, game_start):
    screen.blit(bg2, [0, 0])
    if game_start >= 5:
        digital_road_display(current_list, num_cells, pic, size, img_area, rect, seg_width)
    else:
        pic_display(current_list, num_cells, pic, size, img_area, rect, seg_width)
    my_font = pygame.font.Font('3.ttf', 40)
    img = my_font.render("重玩", True, font_color)
    screen.blit(img, [550, 5])
    # screen.blit(update, [570, 0])
    if size == 3:
        img = my_font.render("帮助", True, font_color)
        screen.blit(img, [450, 5])
        img = my_font.render("下一步", True, font_color)
        screen.blit(img, [300, 5])
    img = my_font.render("返回", True, font_color)
    screen.blit(img, [10, 5])
    # screen.blit(back, [10, 0])
    steps = str(steps)
    step_rect = (50, 330, 20, 20)
    my_font = pygame.font.Font('3.ttf', 30)
    img = my_font.render("steps: "+steps, True, (255, 255, 255))
    screen.blit(img, step_rect)


def digital_road_display(current_list, num_cells, pic, size, img_area, rect, seg_width):
    for i in range(num_cells):
        if current_list[i] == -1:
            pygame.draw.rect(screen, white, (img_area[i], (seg_width, seg_width)))
            continue
        screen.blit(pic, img_area[i], rect[current_list[i]])
        my_font = pygame.font.Font('3.ttf', int(200//size))
        img = my_font.render(str(current_list[i]+1), True, digital_road_color)

        if current_list[i] >= 10:
            screen.blit(img, [int(img_area[i][0] + seg_width // 5), int(img_area[i][1] + seg_width // 5)])
        else:
            screen.blit(img, [int(img_area[i][0] + seg_width // 3), int(img_area[i][1] + seg_width // 5)])
    for i in range(size + 1):
        pygame.draw.line(screen, white, (i * seg_width + height, width), (i * seg_width + height, seg_width * size + width), 1)
        pygame.draw.line(screen, white, (0 + height, i * seg_width + width),
                         (seg_width * size + height, i * seg_width + width), 1)


# 游戏图片处理
def pic_disposal(size, game_start):
    pic = pygame.image.load("images/a.jpg")
    if size == 3 and game_start == 0:
        pic = pygame.image.load("images/a.jpg")
    elif size == 4 and game_start == 0:
        pic = pygame.image.load("images/b.jpg")
    elif size == 5 and game_start == 0:
        pic = pygame.image.load("images/c.jpg")  # 载入图片
    elif game_start == 5:
        pic = pygame.image.load("images/d.jpg")
    pic = pygame.transform.smoothscale(pic, (int(windowHeight*0.6), int(windowHeight*0.6)))   # 调整图片大小
    res = pg.gen_ori(size)
    orig_list = res['start']
    current_list = copy.deepcopy(orig_list)
    target_list = res['end']
    num_rows, num_cols = size, size  # 拼图行列
    num_cells = size*size  # 拼图共几个图块
    seg_width = int(windowHeight*0.6//size)  # 每个拼图块大小
    rect = []
    img_area = []
    for i in range(num_cells):
        y_pos = int(i//num_cols)
        x_pos = i % num_cols
        rect.append(pygame.Rect(x_pos*seg_width, y_pos*seg_width, seg_width, seg_width))  # 图片切片的图
        img_area.append([int(x_pos*seg_width+height), int(y_pos*seg_width+width)])  # 九个图片位置
    return orig_list, current_list, target_list, rect, img_area, num_cells, seg_width, pic


# 是否为有效移动
def is_valid_move(mouse_x, mouse_y, game_start):
    if height < mouse_x < height+TILE_SIZE and width < mouse_y < width+TILE_SIZE and (game_start == 1 or game_start == 5):
        return True
    return False


# 滑块移动方向
def check_direction(mouse_x, mouse_y, blank_x, blank_y, current_list, img_area, rect, seg_width, size, pic, steps):
    direction = None
    num = blank_x + blank_y*size
    if img_area[num][0]+seg_width < mouse_x < img_area[num][0]+seg_width*2 and \
            img_area[num][1] < mouse_y < img_area[num][1]+seg_width:
        direction = RIGHT
    elif img_area[num][0]-seg_width < mouse_x < img_area[num][0] and \
            img_area[num][1] < mouse_y < img_area[num][1]+seg_width:
        direction = LEFT
    elif img_area[num][0] < mouse_x < img_area[num][0]+seg_width and \
            img_area[num][1]-seg_width < mouse_y < img_area[num][1]:
        direction = UP
    elif img_area[num][0] < mouse_x < img_area[num][0]+seg_width and \
            img_area[num][1]+seg_width < mouse_y < img_area[num][1]+seg_width*2:
        direction = DOWN
    move_x, move_y, check, steps = slide_animation(blank_x, blank_y, current_list, direction,
                                                   img_area, rect, seg_width, size, pic, steps)
    return move_x, move_y, check, steps


# 滑动动画
def slide_animation(blank_x, blank_y, current_list, direction, img_area, rect, seg_width, size, pic, steps):
    move_x, move_y, check = 0, 0, 0
    if direction == UP:
        move_x, move_y, check = blank_x, blank_y-1, 1
    elif direction == DOWN:
        move_x, move_y, check = blank_x, blank_y+1, 1
    elif direction == LEFT:
        move_x, move_y, check = blank_x-1, blank_y, 1
    elif direction == RIGHT:
        move_x, move_y, check = blank_x+1, blank_y, 1
    if check == 0:
        return move_x, move_y, check, steps
    base_surf = screen.copy() # 复制一个新的窗口对象
    # 绘制空白区(这时候有2块空白区域)
    num2 = move_x+move_y*size
    steps = steps+1
    pygame.draw.rect(base_surf, white, (img_area[num2], (seg_width, seg_width)))
    base_surf = base_surf.copy()
    my_font = pygame.font.Font('3.ttf', int(200 // size))
    # 绘制滑动效果
    for i in range(0, seg_width, 15):  # animation_speed步长偏移速度,每次循环后方块的位置向指定方向移动
        screen.blit(base_surf, (0, 0))
        if direction == UP:
            screen.blit(pic, (img_area[num2][0], img_area[num2][1]+i), rect[current_list[num2]]) #x不动,y轴向上偏移
        if direction == DOWN:
            screen.blit(pic, (img_area[num2][0], img_area[num2][1]-i), rect[current_list[num2]])  # x不动,y轴向下偏移
        if direction == LEFT:
            screen.blit(pic, (img_area[num2][0]+i, img_area[num2][1]), rect[current_list[num2]]) # y不动,x轴向右偏移
        if direction == RIGHT:
            screen.blit(pic, (img_area[num2][0]-i, img_area[num2][1]), rect[current_list[num2]]) # y不动,x轴向左偏移
        pygame.display.update()
        pygame.time.delay(FPS)
    return move_x, move_y, check, steps


# 白块位置
def get_blank_position(current_list, num_cells, size):
    for i in range(num_cells):
        if current_list[i] == -1:
            return i % size, int(i//size)


# 图片显示
def pic_display(current_list, num_cells, pic, size, img_area, rect, seg_width):
    orig_pic = pygame.transform.smoothscale(pic, [int(windowHeight * 0.3), int(windowHeight * 0.3)])
    screen.blit(orig_pic, [50, 100])
    for i in range(2):
        pygame.draw.line(screen, white, (i * int(windowHeight * 0.3)+50, 100),
                         (i * int(windowHeight * 0.3)+50, int(windowHeight * 0.3)+100), 1)
        pygame.draw.line(screen, white, (50, i * int(windowHeight * 0.3)+100),
                         (int(windowHeight * 0.3)+50, i * int(windowHeight * 0.3)+100), 1)
    for i in range(num_cells):
        if current_list[i] == -1:
            pygame.draw.rect(screen, white, (img_area[i], (seg_width, seg_width)))
            continue
        screen.blit(pic, img_area[i], rect[current_list[i]])
    for i in range(size+1):
        pygame.draw.line(screen, white, (i * seg_width+height, width), (i * seg_width+height, TILE_SIZE+width), 1)
        pygame.draw.line(screen, white, (0+height, i * seg_width+width), (TILE_SIZE+height, i * seg_width+width), 1)


# 检查游戏是否结束以及游戏结束发生事件
def check_for_quit(current_list, target_list, t0, steps, size, game_start):
    if current_list == target_list:
        t1 = time.time()
        t = int(t1 - t0)
        m = 0
        if t > 60:
            m = int(t // 60)
            t = t % 60
        text = str("%2d" % m) + " : " + str("%2d" % t)
        change_history(size, m, t, steps)
        my_font = pygame.font.Font(pygame.font.match_font('2.ttf'), 30)
        img = my_font.render(text, True, (255, 255, 255))
        time_rect = (50, 300, 20, 20)
        screen.blit(img, time_rect)
        pygame.display.update()
        steps = str(steps)
        step_rect = (50, 330, 20, 20)
        my_font = pygame.font.Font(pygame.font.match_font('2.ttf'), 30)
        img = my_font.render(steps, True, (255, 255, 255))
        screen.blit(img, step_rect)
        game_start = -2
    return game_start

# 游戏开始前界面
def game_before():
    screen.blit(bg, [0, 0])
    my_font = pygame.font.Font('25.ttf', 50)
    img = my_font.render("4×4", True, font_color)
    screen.blit(img, [250, 160])
    img = my_font.render("5×5", True, font_color)
    screen.blit(img, [250, 220])
    img = my_font.render("3×3", True, font_color)
    screen.blit(img, [250, 100])
    img = my_font.render("数字华容道", True, font_color)
    screen.blit(img, [190, 280])
    img = my_font.render("往次得分", True, font_color)
    screen.blit(img, [210, 340])
    # screen.blit(gs, [200, 100])
    # screen.blit(his, [200, 180])


# 检查鼠标是否在游戏开始前的按钮上按下
def GSBCheckMouse(mouse_x, mouse_y, size, game_start):
    if 250 < mouse_x < 450 and 100 < mouse_y < 140 and size == 0 and game_start == 0:
        size = 3
    elif 250 < mouse_x < 450 and 160 < mouse_y < 200 and size == 0 and game_start == 0:
        size = 4
    elif 250 < mouse_x < 450 and 220 < mouse_y < 260 and size == 0 and game_start == 0:
        size = 5
    elif 210 < mouse_x < 450 and 280 < mouse_y < 320 and size == 0 and game_start == 0:
        game_start = -3
    elif 210 < mouse_x < 450 and 340 < mouse_y < 400 and size == 0 and game_start == 0:
        game_start = -1
    return size, game_start


def GSCheckMouse(mouse_x, mouse_y, game_start, size, steps, t0):
    if 0 < mouse_x < 85 and 0 < mouse_y < 40 and (game_start == 1 or game_start == 5):
        game_start = 0
        size = 0
        steps = 0
        game_before()
    elif 450 < mouse_x < 540 and 5 < mouse_y < 50 and (game_start == 1 or game_start == 5) and size == 3:
        if game_start == 5:
            game_start = 6
        else:
            game_start = 2
    elif 550 < mouse_x < 640 and 5 < mouse_y < 50 and (game_start == 1 or game_start == 5):
        if game_start == 5:
            game_start = 7
        else:
            game_start = 3
        t0 = time.time()
    elif 350 < mouse_x < 440 and 5 < mouse_y < 50 and (game_start == 1 or game_start == 5) and size == 3:
        if game_start == 5:
            game_start = 8
        else:
            game_start = 4
    '''elif game_start == -2:
        game_start = 0
        steps = 0'''
    return game_start, size, steps, t0


# 自动求解部分
def solve(current_list, target_list, size, img_area, rect, seg_width, pic, steps, game_start):
    for i in range(size*size):
        if current_list[i] == -1:
            break
    blank_x, blank_y = i % size, int(i//size)
    num_cells = size*size
    get = pg.IDAstar(current_list, i, target_list, size)
    path = get.IDA()
    t0 = time.time()
    direction = None
    for i in path:
        if i == 'w':
            direction = UP
        elif i == 'a':
            direction = LEFT
        elif i == 's':
            direction = DOWN
        elif i == 'd':
            direction = RIGHT
        move_x, move_y, check, steps = slide_animation(blank_x, blank_y, current_list, direction, img_area, rect, seg_width, size, pic,steps)
        current_list[blank_x + blank_y * size], current_list[move_x + move_y * size] = \
            current_list[move_x + move_y * size], current_list[blank_x + blank_y * size]
        blank_x, blank_y = move_x, move_y
        Game(current_list, num_cells, pic, size, img_area, rect, seg_width, steps, game_start)
        game_start = check_for_quit(current_list, target_list, t0, steps, size, game_start)
    return steps


def next_step(current_list, target_list, size, img_area, rect, seg_width, pic, steps, game_start):
    for i in range(size*size):
        if current_list[i] == -1:
            break
    blank_x, blank_y = i % size, int(i//size)
    num_cells = size*size
    get = pg.IDAstar(current_list, i, target_list, size)
    path = get.IDA()
    t0 = time.time()
    direction = None
    if path[0] == 'w':
        direction = UP
    elif path[0] == 'a':
        direction = LEFT
    elif path[0] == 's':
        direction = DOWN
    elif path[0] == 'd':
        direction = RIGHT
    move_x, move_y, check, steps = slide_animation(blank_x, blank_y, current_list, direction, img_area, rect, seg_width,
                                                   size, pic, steps)
    current_list[blank_x + blank_y * size], current_list[move_x + move_y * size] = \
        current_list[move_x + move_y * size], current_list[blank_x + blank_y * size]
    blank_x, blank_y = move_x, move_y
    Game(current_list, num_cells, pic, size, img_area, rect, seg_width, steps, game_start)
    return steps


def get_history():
    f1 = open('history.txt', "r+", encoding='UTF-8')
    temp = []
    list = []
    a = []
    txt = f1.read()
    temp.append(txt)
    f1.close()
    for words in temp:
        for word in words:
            if word == ' ' or word == 'a' or word == ':':
                list.append(a.copy())
                a.clear()
                continue
            a.append(word)
    return list


def change_history(size, m, t, steps):
    list = get_history()
    lehgth = 15
    position = 0
    if size == 3:
        position = 1
    elif size == 4:
        position = 2
    elif size == 5:
        position = 3
    del list[position * lehgth-1]
    del list[position * lehgth-2]
    del list[position * lehgth-3]
    list.insert(position*lehgth-lehgth, str( "%02d"%m ))
    list.insert(position*lehgth+1-lehgth, str("%02d"%t))
    if steps>99:
        list.insert(position * lehgth + 2 - lehgth, str("%d" % steps))
    else:
        list.insert(position*lehgth+2-lehgth, str("%02d"%steps))
    f2 = open('history.txt', "w+", encoding='UTF-8')
    for word in list:
        for j in word:
            f2.write(j)
        f2.write(' ')
    f2.close()


def history_click(game_start, mouse_x, mouse_y):
    if game_start == -1 and 0 < mouse_x < 80 and 0 < mouse_y < 40:
        game_start = 0
    return game_start


def congratulation_click(game_start, mouse_x, mouse_y):
    if game_start == -2 and 0 < mouse_x < 80 and 0 < mouse_y < 40:
        game_start = 0
    return game_start


# 历史记录展示
def history_display():
    list = get_history()
    screen.blit(bg2, [0, 0])
    my_font = pygame.font.Font('3.ttf', 60)
    img = my_font.render("往次得分", True, font_color)
    screen.blit(img, [180, 40])

    my_font = pygame.font.Font('3.ttf', 35)

    img = my_font.render("返回", True, font_color)
    screen.blit(img, [5, 5])
    pygame.draw.rect(screen, white, [17, 120, 185, 320])
    pygame.draw.rect(screen, white, [217, 120, 185, 320])
    pygame.draw.rect(screen, white, [417, 120, 185, 320])
    my_font = pygame.font.Font('2.ttf', 25)
    img = my_font.render("4×4", True, black)
    screen.blit(img, [280, 120])
    img = my_font.render("5×5", True, black)
    screen.blit(img, [480, 120])
    img = my_font.render("3×3", True, black)
    screen.blit(img, [80, 120])
    img = my_font.render("序号 时间   步数", True, black)
    screen.blit(img, [15, 160])
    screen.blit(img, [215, 160])
    screen.blit(img, [415, 160])
    for i in range(15):
        txt = str(list[i*3][0])+str(list[i*3][1]) +":"+ str(list[i*3+1][0])+str(list[i*3+1][1])
        j = i % 5 + 1
        img = my_font.render(str(j), True, black)
        time_rect = his_position[i * 3]
        screen.blit(img, time_rect)
        img = my_font.render(txt, True, black)
        time_rect = his_position[i*3+1]
        screen.blit(img, time_rect)
        if str(list[i*3+2][0]) == 'a':
            step = str(list[i*3+2][1])+str(list[i*3+2][2])+str(list[i*3+2][3])
        else:
            step = str(list[i*3+2][0])+str(list[i*3+2][1])
        img = my_font.render(step, True, black)
        time_rect = his_position[i*3+2]
        screen.blit(img, time_rect)


def get_size(key_num,game_start):
    size = 0
    if 51 <= key_num <= 57:
        size = key_num - 48
    else:
        game_start = 0
    return size, game_start


def congratulation(t0, steps, t1):
    screen.blit(bg2, [0, 0])
    my_font = pygame.font.Font('25.ttf', 30)
    t = int(t1 - t0)
    m = 0
    if t > 60:
        m = int(t // 60)
        t = t % 60
    txt = "哇！你只花了"+str(steps)+"步就完成了拼图!"
    img = my_font.render(txt, True, font_color)
    screen.blit(img, [100, 60])
    txt = "用时"+str("%02d" % m) + "分" + str("%02d" % t)+"秒"
    img = my_font.render(txt, True, font_color)
    screen.blit(img, [200, 90])
    screen.blit(con, [150, 130, 80, 80])
    my_font = pygame.font.Font('3.ttf', 35)
    img = my_font.render("返回", True, font_color)
    screen.blit(img, [5, 5])


if __name__ == '__main__':
    main()