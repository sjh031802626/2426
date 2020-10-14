import pygame, sys, random, os, copy, win32ui, time
from pygame.locals import *
import puzzle_game as pg

# 初始化数据
windowSize = windowWidth, windowHeight = 640, 500
white = (255, 255, 255)
black = (0, 0, 0)
separation = 5
FPS = 30  # 游戏帧数

TILE_SIZE = int(windowHeight*0.6)
height = 250
width = 150
# 配置动作
UP = 'w'
DOWN = 's'
LEFT = 'a'
RIGHT = 'd'
pygame.init()
FPS_CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode(windowSize)  # 创建指定大小窗口
# 载入图片
gs = pygame.image.load("images/easy.png")  # 游戏开始
his = pygame.image.load("images/middle.png")  # 历史记录
bg = pygame.image.load("images/5.jpg")
bg2 = pygame.image.load("images/4.jpg")
update = pygame.image.load("images/update2.png")
ai = pygame.image.load("images/help1.png")
back = pygame.image.load("images/back2.png")
# 调整图片大小
iconScale = int(windowWidth*0.08), int(windowHeight * 0.1)
btnScale = int(windowWidth*0.4), int(windowHeight*0.1)
gs = pygame.transform.smoothscale(gs, btnScale)
his = pygame.transform.smoothscale(his, btnScale)
bg = pygame.transform.smoothscale(bg, (int(windowWidth), int(windowHeight)))
bg2 = pygame.transform.smoothscale(bg2, (int(windowWidth), int(windowHeight)))
update = pygame.transform.smoothscale(update, iconScale)
ai = pygame.transform.smoothscale(ai, iconScale)
back = pygame.transform.smoothscale(back, iconScale)


def main():
    size = 0
    steps = 0
    pygame.display.set_caption("滑动拼图")  # 设置窗口标题
    game_start = 0
    t0 = 0
    orig_list, current_list, target_list, rect, img_area, num_cells, seg_width, pic = 0, 0, 0, 0, 0, 0, 0, 0
    while True:
        if game_start == 0:
            game_before()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                size = GSBCheckMouse(mouse_x, mouse_y, size)
                game_start, size = GSCheckMouse(mouse_x, mouse_y, game_start, size)
                if size != 0 and game_start == 0:
                    '''
                    dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
                    dlg.SetOFNInitialDir('D:\pythonProject\img_match')  # 设置打开文件对话框中的初始显示目录
                    dlg.DoModal()
                    filename = dlg.GetPathName()  # 获取选择的文件名称
                    '''
                    orig_list, current_list, target_list, rect, img_area, num_cells, seg_width, pic = pic_disposal(
                        size)
                    game_start = 1
                    t0 = time.time()
                    Game(current_list, num_cells, pic, size, img_area, rect, seg_width, t0)
                    pygame.display.flip()
                # 判断滑块移动以及移动效果
                if is_valid_move(mouse_x, mouse_y, game_start):
                    blank_x, blank_y = get_blank_position(current_list, num_cells, size)
                    move_x, move_y, check, steps = check_direction(mouse_x, mouse_y, blank_x, blank_y,
                                                           current_list, img_area, rect, seg_width, size, pic, steps)
                    if check == 1:
                        current_list[blank_x + blank_y * size], current_list[move_x + move_y * size] = \
                        current_list[move_x + move_y * size], current_list[blank_x + blank_y * size]
                        Game(current_list, num_cells, pic, size, img_area, rect, seg_width, t0)
                    check_for_quit(current_list, target_list, t0)
                if game_start == 2:
                    slove(current_list, target_list,size, img_area, rect, seg_width, pic)
                    game_start = 1
                elif game_start == 3:
                    current_list = orig_list[:]
                    Game(current_list, num_cells, pic, size, img_area, rect, seg_width, t0)
                    game_start = 1
        pygame.display.flip()


# 开始游戏
def Game(current_list, num_cells, pic, size, img_area, rect, seg_width, t0):
    screen.blit(bg2, [0, 0])
    pic_display(current_list, num_cells, pic, size, img_area, rect, seg_width)
    screen.blit(update, [570, 0])
    if size == 3:
        screen.blit(ai, [500, 0])
    screen.blit(back, [10, 0])
    t1 = time.time()
    t = int(t1-t0)
    m = 0
    if t > 60:
        m = int(t//60)
        t = t % 60
    text = str(m)+":"+str(t)
    my_font = pygame.font.Font('arial', 20)
    img = my_font.render(text,True,(255,255,255))
    imga = img.get_rect()
    screen.blit(img, imga)


# 游戏图片处理
def pic_disposal(size):
    pic = pygame.image.load("a_.jpg")  # 载入图片
    pic = pygame.transform.smoothscale(pic, (int(windowHeight*0.6), int(windowHeight*0.6)))  #调整图片大小
    res = pg.gen_ori(size)
    orig_list = res['start']
    current_list = copy.deepcopy(orig_list)
    target_list = res['end']
    num_rows, num_cols = size, size # 拼图行列
    num_cells = size*size # 拼图共几个图块
    seg_width = int(windowHeight*0.6//size) # 每个拼图块大小
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
    if height < mouse_x < height+TILE_SIZE and width < mouse_y < width+TILE_SIZE and game_start==1:
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
    elif img_area[num][0] < mouse_x<img_area[num][0]+seg_width and \
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
    orig_pic = pic.copy()
    orig_pic = pygame.transform.smoothscale(orig_pic, (int(windowHeight * 0.3), int(windowHeight * 0.3)))
    screen.blit(orig_pic, [50, 100])
    for i in range(num_cells):
        if current_list[i] == -1:
            pygame.draw.rect(screen, white, (img_area[i], (seg_width, seg_width)))
            continue
        screen.blit(pic, img_area[i], rect[current_list[i]])
    for i in range(size+1):
        pygame.draw.line(screen, white, (i * seg_width+height, width), (i * seg_width+height, TILE_SIZE+width), 1)
        pygame.draw.line(screen, white, (0+height, i * seg_width+width), (TILE_SIZE+height, i * seg_width+width), 1)


# 检查游戏是否结束以及游戏结束发生事件
def check_for_quit(current_list, target_list, t0):
    if current_list == target_list:
        t1 = time.time()
        t = int(t1 - t0)
        print(t)


# 游戏开始前界面
def game_before():
    screen.blit(bg, [0, 0])
    # screen.blit(gs, [200, 100])
    # screen.blit(his, [200, 180])


#检查鼠标是否在游戏开始前的按钮上按下
def GSBCheckMouse(mouse_x, mouse_y, size):
    if 200 < mouse_x < 450 and 100 < mouse_y < 150 and size == 0 :
        size = 3
    elif 200 < mouse_x < 450 and 180 < mouse_y < 230 and size == 0:
        size = 4
    elif 200 < mouse_x < 450 and 260 < mouse_y < 310 and size == 0:
        size = 5
    return size


def GSCheckMouse(mouse_x, mouse_y, game_start, size):
    if 10 < mouse_x < iconScale[0]+10 and 0 < mouse_y < iconScale[1] and game_start ==1:
        game_start = 0
        size = 0
        game_before()
    elif 500 < mouse_x < iconScale[0]+500 and 0 < mouse_y < iconScale[1] and game_start == 1 and size == 3:
        game_start = 2
    elif 570 < mouse_x < iconScale[0]+570 and 0 < mouse_y < iconScale[1] and game_start == 1:
        game_start = 3

    return game_start, size


# 自动求解部分
def slove(current_list, target_list, size, img_area, rect, seg_width, pic):
    for i in range(size*size):
        if current_list[i] == -1:
            break
    blank_x, blank_y = i % size, int(i//size)
    num_cells = size*size
    get = pg.IDAstar(current_list, i, target_list, size)
    path = get.IDA()
    t0 = time.time()
    direction = None
    steps = 0
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
        Game(current_list, num_cells, pic, size, img_area, rect, seg_width, t0)
    check_for_quit(current_list, target_list, t0)

if __name__ == '__main__':
    main()