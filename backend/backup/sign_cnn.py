# -*- coding: gbk -*-
from time import sleep
from tensorflow import keras
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import random
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
from datetime import datetime
import numpy as np
import tensorflow as tf
from sklearn.manifold import TSNE
from backend.Algorithm import ovs_preprocess


# 如果是GPU，需要去掉注释，如果是CPU，则注释
# gpu = tf.config.experimental.list_physical_devices(device_type='GPU')
# assert len(gpu) == 1
# tf.config.experimental.set_memory_growth(gpu[0], True)

def subtime(date1, date2):
    return date2 - date1


length = 784  # 样本长度

# num_classes = 5    # 样本类别
# epochs=10           # 迭代次数
# number = 784        # 每类样本的数量
# rate = [0.8, 0.1, 0.1]  # 测试集验证集划分比例
# normal = True  # 是否标准化

num_classes = 10  # 样本类别
epochs = 10  # 迭代次数
number = 784  # 每类样本的数量
rate = [0.8, 0.1, 0.1]  # 测试集验证集划分比例
normal = True  # 是否标准化

# path = r'../../../static/data/1
path = r'../backend/static/data/1'

x_train = []
y_train = []
x_valid = []
y_valid = []
x_test = []
y_test = []
history = ''
model = ''


def main_Algoithm():
    global x_train, y_train, x_valid, y_valid, x_test, y_test
    x_train, y_train, x_valid, y_valid, x_test, y_test = ovs_preprocess.prepro(
        d_path=path,
        length=length,
        number=number,
        normal=normal,
        rate=rate,
        enc=False, enc_step=28)

    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_valid = np.array(x_valid)
    y_valid = np.array(y_valid)
    x_test = np.array(x_test)
    y_test = np.array(y_test)

    #
    # print(x_train.shape)
    # print(x_valid.shape)
    # print(x_test.shape)
    # print(y_train.shape)
    # print(y_valid.shape)
    # print(y_test.shape)

    y_train = [int(i) for i in y_train]
    y_valid = [int(i) for i in y_valid]
    y_test = [int(i) for i in y_test]

    # 打乱顺序
    index = [i for i in range(len(x_train))]
    random.seed(1)
    random.shuffle(index)
    x_train = np.array(x_train)[index]
    y_train = np.array(y_train)[index]

    index1 = [i for i in range(len(x_valid))]
    random.shuffle(index1)
    x_valid = np.array(x_valid)[index1]
    y_valid = np.array(y_valid)[index1]

    index2 = [i for i in range(len(x_test))]
    random.shuffle(index2)
    x_test = np.array(x_test)[index2]
    y_test = np.array(y_test)[index2]

    print('x_train的shape是：')
    print(x_train.shape)
    print('x_valid的shape是：')
    print(x_valid.shape)
    print('x_test的shape是：')
    print(x_test.shape)
    # print('y_train是：'+str(y_train))
    # print('y_valid是：'+str(y_valid))
    # print('y_test是：'+str(y_test))
    print("x_train的最大值和最小值：", x_train.max(), x_train.min())
    print("x_test的最大值和最小值：", x_test.max(), x_test.min())

    x_train = tf.reshape(x_train, (len(x_train), 784, 1))
    x_valid = tf.reshape(x_valid, (len(x_valid), 784, 1))
    x_test = tf.reshape(x_test, (len(x_test), 784, 1))


# 保存最佳模型
class CustomModelCheckpoint(keras.callbacks.Callback):
    def __init__(self, model, path):
        self.model = model
        self.path = path
        self.best_loss = np.inf

    def on_epoch_end(self, epoch, logs=None):
        val_loss = logs['val_loss']
        if val_loss < self.best_loss:
            print("\nValidation loss decreased from {} to {}, saving model".format(self.best_loss, val_loss))
            self.model.save_weights(self.path, overwrite=True)
            self.best_loss = val_loss


# t-sne初始可视化函数
def start_tsne():
    print("正在进行初始输入数据的可视化...")
    tf.compat.v1.disable_eager_execution()

    x_train1 = tf.compat.v1.reshape(x_train, (x_train.shape[0], 784))

    with tf.compat.v1.Session() as sess:
        x_train1 = sess.run(x_train1).astype(np.float32)  # 用 sess.run() 转换为 NumPy

    X_tsne = TSNE().fit_transform(x_train1)
    plt.figure(figsize=(10, 10))
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y_train)
    plt.colorbar()

    import os
    # 获取当前工作目录
    current_path = os.getcwd()

    # 打印当前工作目录
    print("当前路径:", current_path)

    # plt.savefig("../BackEnd/Algorithm/BackEnd/Algorithm/save_picture/CNN_sample.png",dpi=600)
    plt.savefig("../diagnosis-system/src/assets/CNN_sample.png", dpi=600)
    plt.show()


# sleep(600000)

# 模型定义
def mymodel():
    # padding——边缘填充
    # pooling——最大池化层通常用于对数据进行降采样，去除冗余信息、对特征进行压缩
    # flatten——展平层将输入中的每个批次展平为一维
    # Dropout——按照一定频率,随机地将输入的中的一些节点数值设置为0,可以防止过拟合
    # Dense——全连接层用于将一个特征空间线性变化到另一个特征空间，在整个神经网络中起到分类器的作用
    # filters——滤波器数目
    # kernal_size——算子尺寸
    # strides——步长
    inputs = keras.Input(shape=(x_train.shape[1], x_train.shape[2]))
    print("x_train.shape[1], x_train.shape[2]:")
    print(x_train.shape[1], x_train.shape[2])
    h1 = layers.Conv1D(filters=8, kernel_size=5, strides=1, padding='same', activation='relu')(inputs)
    h1 = layers.MaxPool1D(pool_size=2, strides=2, padding='same')(h1)

    h1 = layers.Conv1D(filters=16, kernel_size=3, strides=1, padding='same', activation='relu')(h1)
    h1 = layers.MaxPool1D(pool_size=2, strides=2, padding='same')(h1)

    h1 = layers.Flatten()(h1)
    h1 = layers.Dropout(0.6)(h1)
    h1 = layers.Dense(32, activation='relu')(h1)
    h1 = layers.Dense(10, activation='softmax')(h1)

    deep_model = keras.Model(inputs, h1, name="cnn")
    return deep_model


# 模型训练
def modeltrain():
    global model
    model = mymodel()

    model.summary()
    startdate = datetime.utcnow()  # 获取当前时间

    # 编译模型
    # 使用交叉熵损失函数
    model.compile(
        optimizer=keras.optimizers.Adam(),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])
    global history
    x_tmp = x_train
    with tf.compat.v1.Session() as sess:
        x_tmp = sess.run(x_tmp).astype(np.float32)
    x_tmp2 = x_valid
    with tf.compat.v1.Session() as sess:
        x_tmp2 = sess.run(x_tmp2).astype(np.float32)
    history = model.fit(x_tmp, y_train,
                        batch_size=256, epochs=epochs, verbose=1,
                        validation_data=(x_tmp2, y_valid),
                        callbacks=[CustomModelCheckpoint(
                            model, r'best_sign_cnn.h5')])

    # 加载模型
    # filepath = r'best_sign_cnn.h5'
    model.load_weights(filepath='best_sign_cnn.h5')
    # 编译模型
    model.compile(loss='sparse_categorical_crossentropy', optimizer=keras.optimizers.Adam(), metrics=['accuracy'])
    # 评估模型
    x_tmp3 = x_test
    with tf.compat.v1.Session() as sess:
        x_tmp3 = sess.run(x_tmp3).astype(np.float32)
    scores = model.evaluate(x_tmp3, y_test, verbose=1)
    print("评估完成")
    print('%s: %.2f%%' % (model.metrics_names[1], scores[1] * 100))

    y_predict = model.predict(x_tmp3)
    y_pred_int = np.argmax(y_predict, axis=1)
    print(y_pred_int[0:5])
    from sklearn.metrics import classification_report
    print(classification_report(y_test, y_pred_int, digits=4))


def acc_line():
    # 绘制acc和loss曲线
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(len(acc))  # Get number of epochs

    # 画accuracy曲线
    plt.plot(epochs, acc, 'r', linestyle='-.')
    plt.plot(epochs, val_acc, 'b', linestyle='dashdot')
    plt.title('Training and validation accuracy')
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend(["Accuracy", "Validation Accuracy"])
    plt.savefig("../diagnosis-system/src/assets/CNN_accuracy.png", dpi=600)
    plt.figure()

    # 画loss曲线
    plt.plot(epochs, loss, 'r', linestyle='-.')
    plt.plot(epochs, val_loss, 'b', linestyle='dashdot')
    plt.title('Training and validation loss')
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend(["Loss", "Validation Loss"])
    plt.savefig("../diagnosis-system/src/assets/CNN_loss.png", dpi=600)
    # plt.figure()
    plt.show()


# 绘制混淆矩阵
def confusion():
    x_tmp3 = x_test
    with tf.compat.v1.Session() as sess:
        x_tmp3 = sess.run(x_tmp3).astype(np.float32)
    y_pred_gailv = model.predict(x_tmp3, verbose=1)
    y_pred_int = np.argmax(y_pred_gailv, axis=1)
    print(len(y_pred_int))
    con_mat = confusion_matrix(y_test.astype(str), y_pred_int.astype(str))
    print(con_mat)
    classes = list(set(y_train))
    classes.sort()
    plt.imshow(con_mat, cmap=plt.cm.Blues)
    indices = range(len(con_mat))
    plt.xticks(indices, classes)
    plt.yticks(indices, classes)
    plt.colorbar()
    plt.xlabel('guess')
    plt.ylabel('true')
    for first_index in range(len(con_mat)):
        for second_index in range(len(con_mat[first_index])):
            plt.text(first_index, second_index, con_mat[second_index][first_index], va='center', ha='center')
    plt.savefig("../diagnosis-system/src/assets/CNN_confusion.png", dpi=600)
    plt.show()


def new_start_tsne():
    # pca = PCA(n_components=10)
    x_tmp3 = x_test
    with tf.compat.v1.Session() as sess:
        x_tmp3 = sess.run(x_tmp3).astype(np.float32)
    hidden_features = model.predict(x_tmp3)

    pca_result = hidden_features
    tsne = TSNE(n_components=2, verbose=1)
    tsne_results = tsne.fit_transform(pca_result[:])
    # -------------------------------可视化--------------------------------
    # y_test_cat = np_utils.to_categorical(y_test[:2400], num_classes=10)# 总的类别
    plt.figure(figsize=(5, 5))
    color_map = y_test[:]
    for cl in range(num_classes):  # 总的类别
        indices = np.where(color_map == cl)
        indices = indices[0]
        plt.scatter(tsne_results[indices, 0], tsne_results[indices, 1], label=None)
        # plt.scatter(tsne_results[indices, 0], tsne_results[indices, 1], label=cl)
    plt.tick_params(labelsize=18)
    plt.legend()
    # plt.savefig("./Algorithm/save_picture/result.png", dpi=600)
    plt.savefig("../diagnosis-system/src/assets/CNN_result.png", dpi=600)
    plt.show()


def run_Algorithm():
    main_Algoithm()
    start_tsne()
    modeltrain()
    acc_line()
    confusion()
    new_start_tsne()

# run_Algorithm()
