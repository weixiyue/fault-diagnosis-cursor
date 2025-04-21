import os
import re
import scipy.io as scio
import numpy as np
import pandas as pd
from datetime import datetime
import scipy.signal
from keras.models import Sequential, Model, load_model
from keras.optimizers import Adam
from sklearn.preprocessing import LabelBinarizer
from sklearn import preprocessing
from keras.layers import *
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.manifold import TSNE
import itertools
from sklearn.metrics import confusion_matrix
from keras.callbacks import ReduceLROnPlateau
from keras import backend as k
from keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import Callback
import tensorflow as tf
import tensorflow.keras as keras


raw_num = 240
col_num = 2000
num_classes = 10

x_train = []
y_train = []
x_valid = []
y_valid = []
x_test = []
y_test = []
history = ''
model = ''


# 自定义日志回调类
class TrainingLogger(Callback):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.start_time = None

    def on_train_begin(self, logs=None):
        self.start_time = datetime.now()
        self.logger.info(f"🟢 训练开始于 {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"🔧 模型架构：\n{self.model.summary()}")

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        self.logger.info(
            f"Epoch {epoch + 1}/{self.params['epochs']} - "
            f"loss: {logs.get('loss', 0):.4f} - "
            f"accuracy: {logs.get('accuracy', 0):.4f} - "
            f"val_loss: {logs.get('val_loss', 0):.4f} - "
            f"val_accuracy: {logs.get('val_accuracy', 0):.4f}"
        )

    def on_train_end(self, logs=None):
        end_time = datetime.now()
        duration = end_time - self.start_time
        self.logger.info(f"🔴 训练结束于 {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"⏱️ 总训练时长：{duration}")


class Data(object):

    def __init__(self):
        self.data = self.get_data()
        self.label = self.get_label()

    def file_list(self):
        return os.listdir('../backend/static/data/48k_Drive_End_3/')

    def get_data(self):
        file_list = self.file_list()
        for i in range(len(file_list)):
            file = scio.loadmat('../backend/static/data/48k_Drive_End_3/{}'.format(file_list[i]))
            for k in file.keys():
                file_matched = re.match('X\d{3}_DE_time',
                                        k)  # 'X\d{3}_DE_time'表示匹配的字符串必须以"X"开始，紧接着是三位数字，然后是"DE"，最后以"time"结束
                if file_matched:
                    key = file_matched.group()
            if i == 0:
                data = np.array(file[key][0:480000].reshape(raw_num, col_num))
            else:
                data = np.vstack((data, file[key][0:480000].reshape((raw_num, col_num))))
        return data

    def get_label(self):
        file_list = self.file_list()
        title = np.array([i.replace('.mat', '') for i in file_list])
        label = title[:, np.newaxis]
        label_copy = np.copy(label)
        for _ in range(raw_num - 1):
            label = np.hstack((label, label_copy))
        return label.flatten()


def prepare_data():
    raw_data = Data()
    data = raw_data.data
    label = raw_data.label
    lb = LabelBinarizer()
    y = lb.fit_transform(label)

    # Wiener filtering
    data_wiener = scipy.signal.wiener(data, mysize=3, noise=None)

    # down sampling
    index = np.arange(0, 2000, 8)
    data_samp = data_wiener[:, index]
    print(data_samp.shape)

    global x_train, y_train, x_valid, y_valid, x_test, y_test
    x_train, x_test, y_train, y_test = train_test_split(data_samp, y, test_size=0.3)


# t-sne初始可视化函数
def visualize_data():
    print("正在进行初始输入数据的可视化...")
    # x_train_tmp = tf.reshape(x_train, (len(x_train), 784))
    x_train_tmp = x_train
    y_train_tmp = y_train
    label_train = np.argmax(y_train, axis=1)
    X_tsne = TSNE().fit_transform(x_train)
    plt.figure(figsize=(10, 10))
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=label_train)
    plt.colorbar()
    plt.savefig("../diagnosis-system/src/assets/CNN_LSTM_sample.png", dpi=600)
    plt.show()


def built_model():
    input_seq = Input(shape=(250,))
    X = Reshape((1, 250))(input_seq)

    # encoder1
    ec1_layer1 = Conv1D(filters=50, kernel_size=20, strides=2,
                        padding='valid', activation='tanh',
                        data_format='channels_first')(X)
    ec1_layer2 = Conv1D(filters=30, kernel_size=10, strides=2,
                        padding='valid', activation='tanh',
                        data_format='channels_first')(ec1_layer1)
    ec1_outputs = MaxPooling1D(pool_size=2, strides=None, padding='valid',
                               data_format='channels_first')(ec1_layer2)

    # encoder2
    ec2_layer1 = Conv1D(filters=50, kernel_size=6, strides=1,
                        padding='valid', activation='tanh',
                        data_format='channels_first')(X)
    ec2_layer2 = Conv1D(filters=40, kernel_size=6, strides=1,
                        padding='valid', activation='tanh',
                        data_format='channels_first')(ec2_layer1)
    ec2_layer3 = MaxPooling1D(pool_size=2, strides=None, padding='valid',
                              data_format='channels_first')(ec2_layer2)
    ec2_layer4 = Conv1D(filters=30, kernel_size=6, strides=1,
                        padding='valid', activation='tanh',
                        data_format='channels_first')(ec2_layer3)
    ec2_layer5 = Conv1D(filters=30, kernel_size=6, strides=2,
                        padding='valid', activation='tanh',
                        data_format='channels_first')(ec2_layer4)
    ec2_outputs = MaxPooling1D(pool_size=2, strides=None, padding='valid',
                               data_format='channels_first')(ec2_layer5)

    encoder = multiply([ec1_outputs, ec2_outputs])

    dc_layer1 = LSTM(60, return_sequences=True)(encoder)
    dc_layer2 = LSTM(60)(dc_layer1)
    dc_layer3 = Dropout(0.5)(dc_layer2)
    dc_layer4 = Dense(10, activation='softmax')(dc_layer3)

    model = Model(input_seq, dc_layer4)

    return model


def plot_confusion_matrix(cm, classes, title='Confusion matrix', cmap=plt.cm.Blues, normalize=False):
    plt.imshow(cm , cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_mark = np.arange(len(classes))
    plt.xticks(tick_mark, classes, rotation=40)
    plt.yticks(tick_mark, classes)
    if normalize:
        cm = cm.astype('float')/cm.sum(axis=1)[:,np.newaxis]
        cm = '%.2f'%cm
    thresh = cm.max()/2.0
    for i,j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j,i,cm[i,j], horizontalalignment='center',color='black')
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predict label')
    plt.savefig("../diagnosis-system/src/assets/CNN_LSTM_confusion.png", dpi=600)
    plt.show()


def train_model(logger):
    # X_train, X_test, y_train, y_test = prepare_data()
    global model
    model = built_model()
    opt = Adam(lr=0.0006)
    model.compile(optimizer=opt, loss='mean_squared_error', metrics=['accuracy'])
    # 记录模型摘要
    logger.info("🔍 模型摘要：")
    buffer = []
    model.summary(print_fn=lambda x: buffer.append(x))
    logger.info("\n".join(buffer))

    # 数据预处理日志
    # logger.info("📊 数据预处理：")
    # logger.info(f"训练样本数: {x_train.shape[0]}")
    # logger.info(f"验证样本数: {x_valid.shape[0]}")
    # logger.info(f"测试样本数: {x_test.shape[0]}")
    logger.info(f"训练样本数: {len(x_train)}")
    # logger.info(f"验证样本数: {len(x_valid)}")
    logger.info(f"测试样本数: {len(x_test)}")

    checkpoint = ModelCheckpoint('best_cnn_lstm_model.h5', monitor='val_accuracy', save_best_only=True, mode='max')
    # 创建回调列表
    callbacks = [
        checkpoint,
        TrainingLogger(logger)  # 添加自定义日志回调
    ]

    global history
    # 开始训练
    logger.info("🚀 开始模型训练...")
    history = model.fit(x=x_train, y=y_train, batch_size=100, epochs=200,
                        verbose=2, validation_data=(x_test, y_test),
                        shuffle=True, initial_epoch=0, callbacks=callbacks)


def visualize_train():
    # 绘制acc和loss曲线
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
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
    plt.savefig("../diagnosis-system/src/assets/CNN_LSTM_accuracy.png", dpi=600)
    plt.figure()

    # 画loss曲线
    plt.plot(epochs, loss, 'r', linestyle='-.')
    plt.plot(epochs, val_loss, 'b', linestyle='dashdot')
    plt.title('Training and validation loss')
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend(["Loss", "Validation Loss"])
    plt.savefig("../diagnosis-system/src/assets/CNN_LSTM_loss.png", dpi=600)
    # plt.figure()
    plt.show()


def visualize_result():
    hidden_features = model.predict(x_test)
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
    plt.savefig("../diagnosis-system/src/assets/CNN_LSTM_result.png", dpi=600)
    plt.show()

    # predict result
    y_pre = model.predict(x_test)
    label_pre = np.argmax(y_pre, axis=1)
    label_true = np.argmax(y_test, axis=1)
    confusion_mat = confusion_matrix(label_true, label_pre)
    plot_confusion_matrix(confusion_mat, classes=range(10))


def run_Algorithm(logger):
    prepare_data()
    visualize_data()
    train_model(logger)
    visualize_train()
    visualize_result()

