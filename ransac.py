import numpy as np
import random
import matplotlib.pyplot as plt
import math


# 1.获取样本数据sample、初始化inlier_num，模型的参数
# 2.输入模型所需要的最小点数n，根据最小点数，随机在sample中选择n个数
# 3.将n个数带入模型，计算当前条件下样本中的内点数量(比如拟合直线，则距离直线的垂直距离小于阈值的点为内点)
# 4.若该次迭代的内点数m大于inlier_num，则令inlier_num=n，并更新模型参数，并计算iter数并更新，iter = log(1-P)*log(1-（inlier_num/total_size）**2)
# 5.若inlier_num内点数满足内点数阈值，或迭代到最大数目，则停止，输出最优模型及参数
# 可实时更新迭代的次数：公式为iter = log(1-P)*log(1-（inlier_num/total_size）**2)， 其中P为期望得到正确模型的概率，log等价于ln

def f(x):
    y = x + 1
    return y


if __name__ == "__main__":
    data_size = 100
    x = np.linspace(0,10,data_size)
    y = f(x)
    # x,y添加一定随机偏差
    x = x + np.random.uniform(-1,1,x.shape[0])
    y = y + np.random.uniform(-1,1,y.shape[0])

    # 随机噪声点
    x_noise = np.random.random(data_size) * 20
    y_noise = np.random.random(data_size) * 20

    new_x = np.hstack((x_noise, x))
    new_y = np.hstack((y_noise, y))

    # 设置迭代次数
    iters = 2000
    # 数据和模型之间可接受的差值
    sigma = 1
    # 最好模型的参数估计和内点数目
    best_a = 0
    best_b = 0
    best_inlier_num = 0

    # 希望能得到正确模型的概率
    P = 0.99

    for i in range(math.floor(iters)):
        # 随机从数据中去选两个点去求模型
        sample_index = random.sample(range(2*data_size),2)
        x1 = new_x[sample_index[0]]
        y1 = new_y[sample_index[0]]

        x2 = new_x[sample_index[1]]
        y2 = new_y[sample_index[1]]

        # 构建该点的模型
        a = (y2 - y1) / (x2 - x1)
        b = y2 - a * x2

        inlier_num = 0
        for j in range(data_size * 2):
            x = new_x[j]
            y = new_y[j]

            # 求点到直线的距离
            y_estimate = a * x + b
            # error
            err = abs(y_estimate - y)
            if err <= sigma:
                inlier_num += 1

        if inlier_num > best_inlier_num:
            best_inlier_num = inlier_num
            # 重新计算迭代次数
            iters = math.log(1-P) / math.log(1-math.pow(inlier_num / (data_size * 2), 2))
            best_a = a
            best_b = b

        print(f"Epoch-->{i}, Update iters-->{iters}, best_inlier_num-->{best_inlier_num}")
        if inlier_num > data_size:
            print("break")
            break

    # 画图
    Y = best_a * new_x + best_b

    plt.title("ransac fitting")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.plot(new_x, new_y, "bo", label="Test Points")
    plt.plot(new_x, Y, "r-", label="Fitting line")
    plt.legend(loc="upper right")
    plt.savefig("./ransac_line_fitting.png", dpi=300)
    plt.show()
