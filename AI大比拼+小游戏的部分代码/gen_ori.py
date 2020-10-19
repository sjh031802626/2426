import os
from PIL import Image
import random
import copy


# 将图片填充为正方形
def fill_image(image):
    width, height = image.size
    # 选取长和宽中较大值作为新图片的
    new_image_length = width if width > height else height
    # 生成新图片[白底]
    new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
    # 将之前的图粘贴在新图上，居中
    if width > height:  # 原图宽大于高，则填充图片的竖直维度
        new_image.paste(image, (0, int((new_image_length - height) / 2)))  # (x,y)二元组表示粘贴上图相对下图的起始位置
    else:
        new_image.paste(image, (int((new_image_length - width) / 2), 0))
    return new_image


# 切图
def cut_image(image, n):
    width, height = image.size
    item_width = int(width / n)
    # box_list = []
    image_dict = {}  # 使用字典存储图片
    # (left, upper, right, lower)
    for i in range(0, n):
        for j in range(0, n):
            box = (j * item_width, i * item_width, (j + 1) * item_width, (i + 1) * item_width)
            image_dict[n*i+j] = image.crop(box)  # 切片
    return image_dict


# 归并函数，返回一趟归并的逆序对数
def merge(listA, tmpA, L, R, RightEnd):
    # L为待归并数组中，左半个数组的首元素下标；R为右半个数组的首元素下标
    # RightEnd为待归并数组最后一个元素的下标
    cnt = 0
    LeftEnd = R-1  # 左半个数组最后一个元素的下标
    tmp = L
    NumElements = RightEnd-L+1  # 待归并数组元素总数
    while (L <= LeftEnd) and (R <= RightEnd):
        if listA[L] <= listA[R]:
            tmpA[tmp] = listA[L]
            tmp += 1
            L += 1
        else:
            tmpA[tmp] = listA[R]
            tmp += 1
            R += 1
            cnt += LeftEnd-L+1
    while L <= LeftEnd:
        tmpA[tmp] = listA[L]
        tmp += 1
        L += 1
    while R <= RightEnd:
        tmpA[tmp] = listA[R]
        tmp += 1
        R += 1
    for i in range(NumElements):
        listA[RightEnd] = tmpA[RightEnd]
        RightEnd -= 1
    return cnt


# 循环进行归并排序，返回以len为步长进行归并排序得到的逆序对数
def merge_pass(listA, tmpA, N, len):
    # 一趟归并（采用循环方法，非递归）
    cnt = 0
    double_len = 2*len
    i = 0
    while i <= N-double_len:
        cnt += merge(listA, tmpA, i, i+len, i+double_len-1)
        i += double_len
    if i + len < N:
        cnt += merge(listA, tmpA, i, i+len, N-1)
    else:
        for j in range(i, N):
            tmpA[j] = listA[j]
    return cnt


# 基于归并排序求列表中逆序对的数目
def inverse_number(listA, N):
    # 使用非递归的方法实现基于归并排序的逆序对数目计数
    len = 1
    cnt = 0
    tmpA = [0]
    tmpA = tmpA*N
    while len < N:
        cnt += merge_pass(listA, tmpA, N, len)
        len *= 2
        cnt += merge_pass(tmpA, listA, N, len)
        len *= 2
    return cnt


# 判断列表中逆序对数的奇偶，若为偶，返回True
# 计算逆序对数时，不算空白块
def Judge_even(listA):
    n = len(listA)
    # inverse_number函数会进行归并排序，破坏原列表，故先拷贝一份
    tmp = copy.deepcopy(listA)
    for i in range(n):
        if tmp[i] < 0:
            del tmp[i]
            n -= 1
            break
    cnt = inverse_number(tmp, n)
    if (cnt % 2) == 0:
        return True
    else:
        return False


# 判断n阶数码问题是否可解，根据n的奇偶分类讨论
# 输入初态、初态白块位置、末态、阶数
def Judge_solvable(start, end, rank):
    length = len(end)
    judge_start = Judge_even(start)
    judge_end = True  # 末态的逆序对数必为0
    # 寻找初态中白块的位置blank_start
    for i in range(length):
        if start[i] < 0:
            blank_start = i
            break
    # 寻找末态中白块的位置blank_end
    for i in range(length):
        if end[i] < 0:
            blank_end = i
            break
    # k为初末状态白块所在行位置的差值，"//"表示整除向下取整
    k = abs(blank_start//rank - blank_end//rank)
    if rank % 2 == 1:
        # 若阶数为奇，则判断初末状态逆序对数是否同奇同偶
        # print("阶数为奇，同奇同偶")
        # print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
        if judge_start == judge_end:
            return True
    else:
        # 若阶数为偶，则还需要判断初末状态白块位置的关系
        # 若初末状态奇偶性相同，则白块所在行的差值k要为偶数才可解
        if judge_start == judge_end:
            if k % 2 == 0:
                # print("同奇同偶，k为偶，k: ", k, " judge_start: ", judge_start, " judge_end:  ", judge_end)
                # print(start)
                # print("+++++++++++++++++++++++++++++++++++++++++++")
                return True
        # 若初末状态奇偶性不同，则白块所在行的差值k要为奇数才可解
        else:
            if k % 2 == 1:
                # print("不同奇同偶，k为奇，k: ", k, " judge_start: ", judge_start, " judge_end:  ", judge_end)
                # print(start)
                # print("***********************************************")
                return True
    return False


# 将图片切成n*n个，存在字典中
# 随机选择一个切片作为白块，并记录编号,返回字典（切片编号以及对应的图片），列表（初态、白块编号、末态）
def gen_ori(img_path, n):
    start = []
    for i in range(n*n):
        start.append(i)
    image = Image.open(img_path)   # 打开图片
    image = fill_image(image)   # 将图片填充为方形
    image_dict = cut_image(image, n)    # 切割图片（n*n）,返回字典（数字0~8为键，切片image为值）
    blank = random.randint(0, n*n-1)  # 随机生成一个白块
    start[blank] = -1  # 将初态中对应的切片编号定为白块(-1)
    end = copy.deepcopy(start)  # 生成末态列表
    ok = False  # 判断生成的初态是否满足条件（可解，且不能太简单）
    length = len(start)
    while not ok:
        # print("now is not ok")
        random.shuffle(start)  # 随机打乱初态列表
        cnt = 0  # 计数初态有多少不在位数字
        if not Judge_solvable(start, end, n):
            # print(" not solvable emmmmmm", end=" ")
            # print(" start: ", Judge_even(start))
            # 若不可解，需要调整
            i = length-1
            j = i-1
            # 空白块不动
            if start[i] == -1:
                i = j-1
            if start[j] == -1:
                j = j-1
            # 交换列表除空白块外最后两个元素
            # print("before swap start: ", Judge_even(start))
            # print(start)
            start[i], start[j] = start[j], start[i]
            # print("after swap start : ", Judge_even(start))
            # print(start)
            ok = True
    # print("ok!")
    # 计算初态中白块位置
    for i in range(length):
        if start[i] < 0:
            blank = i
            break
    # 用字典返回切片列表（图片编号:图片）、初态、白块初始位置、末态
    resp = {'image_dict': image_dict, 'start': start, 'blank': blank, 'end': end}
    return resp


if __name__ == '__main__':
    img_path = "D:\\python_venv1\\game_project\\original_img\\a_.jpg"
    n = 6
    resp = gen_ori(img_path, n)  # img_path为图片路径，n表示阶数（n*n）
    print(resp['image_dict'])
    print(resp['start'])
    print(resp['blank'])
    print(resp['end'])

