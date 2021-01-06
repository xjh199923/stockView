import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler  # 用里面的归一化库

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']


def predic_stock(df):
    # 查看总览信息，最大值最小值均值
    # panda加载csv文件
    return_data = []
    data = df
    data.describe()
    data_last = data
    data.info()

    # 打印出来大盘指数的变化趋势
    plt.plot(data['turnover'])

    # 将所有数据分成训练集和测试集
    data_train = data.iloc[:int(data.shape[0] * 0.8), :]
    data_test = data.iloc[int(data.shape[0] * 0.5):, :]
    print(data_train.shape, data_test.shape)
    print(data_train)

    # 进行归一化处理
    print(data_train)
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler.fit(data_train)
    data_train = scaler.transform(data_train)
    print(data_train)
    data_test = scaler.transform(data_test)
    # print(data_test)
    data_last = scaler.transform(data_last)
    # 将训练数据分出输入和输出
    X_train = data_train[:, 0:6]
    y_train = data_train[:, 6]
    # 将训练数据分出输入和输出
    X_test = data_test[:, 0:6]
    y_test = data_test[:, 6]

    # 全连接神经网络

    # 定义各层层数
    input_dim = X_train.shape[1]
    hidden1 = 1024
    hidden2 = 512
    hidden3 = 256
    hidden4 = 128
    output_dim = 1

    # 定义批的大小
    batch_size = 256
    # 定义跑多少轮
    epochs = 15

    # 重置计算图（为了安全）
    tf.reset_default_graph()

    # 定义输入层
    X = tf.placeholder(shape=[None, input_dim], dtype=tf.float32)
    Y = tf.placeholder(shape=[None], dtype=tf.float32)

    # 定义隐层变量
    W1 = tf.get_variable('W1', [input_dim, hidden1], initializer=tf.contrib.layers.xavier_initializer(seed=1))
    b1 = tf.get_variable('b1', [hidden1], initializer=tf.zeros_initializer())

    W2 = tf.get_variable('W2', [hidden1, hidden2], initializer=tf.contrib.layers.xavier_initializer(seed=1))
    b2 = tf.get_variable('b2', [hidden2], initializer=tf.zeros_initializer())

    W3 = tf.get_variable('W3', [hidden2, hidden3], initializer=tf.contrib.layers.xavier_initializer(seed=1))
    b3 = tf.get_variable('b3', [hidden3], initializer=tf.zeros_initializer())

    W4 = tf.get_variable('W4', [hidden3, hidden4], initializer=tf.contrib.layers.xavier_initializer(seed=1))
    b4 = tf.get_variable('b4', [hidden4], initializer=tf.zeros_initializer())

    W5 = tf.get_variable('W5', [hidden4, output_dim], initializer=tf.contrib.layers.xavier_initializer(seed=1))
    b5 = tf.get_variable('b5', [output_dim], initializer=tf.zeros_initializer())

    # 定义logits回归
    h1 = tf.nn.relu(tf.add(tf.matmul(X, W1), b1))
    h2 = tf.nn.relu(tf.add(tf.matmul(h1, W2), b2))
    h3 = tf.nn.relu(tf.add(tf.matmul(h2, W3), b3))
    h4 = tf.nn.relu(tf.add(tf.matmul(h3, W4), b4))
    out = tf.transpose(tf.add(tf.matmul(h4, W5), b5))

    # 定义损失
    cost = tf.reduce_mean(tf.squared_difference(out, Y))
    # 定义优化方式
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    # 开始图的运行阶段
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for e in range(epochs):
            # 所有这几万条数据的数据随机打乱。这样做主要是为了不让模型学习到位置信息
            shuffle_indices = np.random.permutation(np.arange(y_train.shape[0]))
            X_train = X_train[shuffle_indices]
            y_train = y_train[shuffle_indices]

            for i in range(y_train.shape[0] // batch_size):
                start = i * batch_size
                batch_x = X_train[start: start + batch_size]
                batch_y = y_train[start: start + batch_size]

                sess.run(optimizer, feed_dict={X: batch_x, Y: batch_y})

                # 到此处图的定义及图的运行已完毕
                # 看训练的过程
                if i % 10 == 0:
                    print("在训练集上的损失：", sess.run(cost, feed_dict={X: X_train, Y: y_train}))
                    print("在测试集上的损失：", sess.run(cost, feed_dict={X: X_test, Y: y_test}))
                    saver = tf.train.Saver()
                    saver.save(sess, "predict_dic/model.ckpt", meta_graph_suffix='meta', write_meta_graph=True)
                    tf.train.write_graph(sess.graph_def, "predict_dic/Model", "model.pb", False)
                    # 预测值
                    y_pred = sess.run(out, feed_dict={X: data_last[:, 0:6]})
                    y_pred = np.squeeze(y_pred)

    return_data.append(data_last[:, 6])
    print('xjh')
    print(data_last[:, 6])
    return_data.append(y_pred)
    return return_data

