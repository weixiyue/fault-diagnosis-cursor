# -*- coding: gbk -*-
from time import sleep
from tensorflow import keras
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import random
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
from tensorflow.keras.callbacks import Callback
from datetime import datetime
import numpy as np
import tensorflow as tf
from sklearn.manifold import TSNE
from backend.Algorithm import ovs_preprocess


# �����GPU����Ҫȥ��ע�ͣ������CPU����ע��
# gpu = tf.config.experimental.list_physical_devices(device_type='GPU')
# assert len(gpu) == 1
# tf.config.experimental.set_memory_growth(gpu[0], True)


def subtime(date1, date2):
    return date2 - date1


length = 784  # ��������

num_classes = 10  # �������
epochs = 10  # ��������
number = 784  # ÿ������������
rate = [0.8, 0.1, 0.1]  # ���Լ���֤�����ֱ���
normal = True  # �Ƿ��׼��

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


# �Զ�����־�ص���
class TrainingLogger(Callback):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.start_time = None

    def on_train_begin(self, logs=None):
        self.start_time = datetime.now()
        self.logger.info(f"? ѵ����ʼ�� {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"? ģ�ͼܹ���\n{self.model.summary()}")

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        self.logger.info(
            f"Epoch {epoch + 1}/{self.params['epochs']} - "
            f"loss: {logs.get('loss', 0):.4f} - "
            f"accuracy: {logs.get('acc', 0):.4f} - "
            f"val_loss: {logs.get('val_loss', 0):.4f} - "
            f"val_accuracy: {logs.get('val_acc', 0):.4f}"
        )

    def on_train_end(self, logs=None):
        end_time = datetime.now()
        duration = end_time - self.start_time
        self.logger.info(f"? ѵ�������� {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"?? ��ѵ��ʱ����{duration}")


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

    # ����˳��
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

    print('x_train��shape�ǣ�')
    print(x_train.shape)
    print('x_valid��shape�ǣ�')
    print(x_valid.shape)
    print('x_test��shape�ǣ�')
    print(x_test.shape)
    # print('y_train�ǣ�'+str(y_train))
    # print('y_valid�ǣ�'+str(y_valid))
    # print('y_test�ǣ�'+str(y_test))
    print("x_train�����ֵ����Сֵ��", x_train.max(), x_train.min())
    print("x_test�����ֵ����Сֵ��", x_test.max(), x_test.min())

    x_train = tf.reshape(x_train, (len(x_train), 784, 1))
    x_valid = tf.reshape(x_valid, (len(x_valid), 784, 1))
    x_test = tf.reshape(x_test, (len(x_test), 784, 1))


# �������ģ��
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


# t-sne��ʼ���ӻ�����
def start_tsne():
    print("���ڽ��г�ʼ�������ݵĿ��ӻ�...")
    tf.compat.v1.disable_eager_execution()

    x_train_tmp = x_train
    y_train_tmp = y_train

    x_train1 = tf.compat.v1.reshape(x_train, (x_train.shape[0], 784))

    with tf.compat.v1.Session() as sess:
        x_train1 = sess.run(x_train1).astype(np.float32)  # �� sess.run() ת��Ϊ NumPy

    X_tsne = TSNE().fit_transform(x_train1)
    plt.figure(figsize=(10, 10))
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y_train)
    plt.colorbar()

    import os
    # ��ȡ��ǰ����Ŀ¼
    current_path = os.getcwd()

    # ��ӡ��ǰ����Ŀ¼
    print("��ǰ·��:", current_path)

    # plt.savefig("../BackEnd/Algorithm/BackEnd/Algorithm/save_picture/CNN_sample.png",dpi=600)
    plt.savefig("../diagnosis-system/src/assets/CNN_sample.png", dpi=600)
    plt.show()


# sleep(600000)

# ģ�Ͷ���
def mymodel():
    # padding������Ե���
    # pooling�������ػ���ͨ�����ڶ����ݽ��н�������ȥ��������Ϣ������������ѹ��
    # flatten����չƽ�㽫�����е�ÿ������չƽΪһά
    # Dropout��������һ��Ƶ��,����ؽ�������е�һЩ�ڵ���ֵ����Ϊ0,���Է�ֹ�����
    # Dense����ȫ���Ӳ����ڽ�һ�������ռ����Ա仯����һ�������ռ䣬���������������𵽷�����������
    # filters�����˲�����Ŀ
    # kernal_size�������ӳߴ�
    # strides��������
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


# ģ��ѵ��
def modeltrain(logger):
    try:
        global model
        model = mymodel()

        model.summary()
        startdate = datetime.utcnow()  # ��ȡ��ǰʱ��

        # ��¼ģ��ժҪ
        logger.info("? ģ��ժҪ��")
        buffer = []
        model.summary(print_fn=lambda x: buffer.append(x))
        logger.info("\n".join(buffer))

        # ����ģ��
        # ʹ�ý�������ʧ����
        model.compile(
            optimizer=keras.optimizers.Adam(),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])

        # ����Ԥ������־
        logger.info("? ����Ԥ����")
        logger.info(f"ѵ��������: {x_train.shape[0]}")
        logger.info(f"��֤������: {x_valid.shape[0]}")
        logger.info(f"����������: {x_test.shape[0]}")
        # logger.info(f"ѵ��������: {len(x_train)}")
        # logger.info(f"��֤������: {len(x_valid)}")
        # logger.info(f"����������: {len(x_test)}")

        # �����ص��б�
        callbacks = [
            CustomModelCheckpoint(model, 'best_sign_cnn.h5'),
            TrainingLogger(logger)  # ����Զ�����־�ص�
        ]

        global history
        x_tmp = x_train
        with tf.compat.v1.Session() as sess:
            x_tmp = sess.run(x_tmp).astype(np.float32)
        x_tmp2 = x_valid
        with tf.compat.v1.Session() as sess:
            x_tmp2 = sess.run(x_tmp2).astype(np.float32)

        # ��ʼѵ��
        logger.info("? ��ʼģ��ѵ��...")
        # history = model.fit(x_tmp, y_train,
        #                     batch_size=256, epochs=epochs, verbose=1,
        #                     validation_data=(x_tmp2, y_valid),
        #                     callbacks=[CustomModelCheckpoint(
        #                         model, r'best_sign_cnn.h5')])
        history = model.fit(x_tmp, y_train,
                            batch_size=256, epochs=epochs, verbose=1,
                            validation_data=(x_tmp2, y_valid),
                            callbacks=callbacks)

        # ����ģ��
        # filepath = r'best_sign_cnn.h5'
        model.load_weights(filepath='best_sign_cnn.h5')
        # ����ģ��
        model.compile(loss='sparse_categorical_crossentropy', optimizer=keras.optimizers.Adam(), metrics=['accuracy'])

        # ģ������
        logger.info("? ģ��������")
        x_tmp3 = x_test
        with tf.compat.v1.Session() as sess:
            x_tmp3 = sess.run(x_tmp3).astype(np.float32)
        scores = model.evaluate(x_tmp3, y_test, verbose=1)
        print("�������")
        print('%s: %.2f%%' % (model.metrics_names[1], scores[1] * 100))

        logger.info(f"����׼ȷ��: {scores[1] * 100:.2f}%")

        y_predict = model.predict(x_tmp3)
        y_pred_int = np.argmax(y_predict, axis=1)
        print(y_pred_int[0:5])

        # Ԥ������־
        logger.info("? Ԥ��������ǰ5������")
        logger.info(f"��ʵ��ǩ: {y_test[:5]}")
        logger.info(f"Ԥ���ǩ: {y_pred_int[:5]}")

        from sklearn.metrics import classification_report
        print(classification_report(y_test, y_pred_int, digits=4))

        # ���౨��
        report = classification_report(y_test, y_pred_int, digits=4)
        logger.info("? ���౨�棺\n" + report)

    except Exception as e:
        logger.error(f"? ѵ�������з�������: {str(e)}", exc_info=True)
        raise


def acc_line():
    # ����acc��loss����
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(len(acc))  # Get number of epochs

    # ��accuracy����
    plt.plot(epochs, acc, 'r', linestyle='-.')
    plt.plot(epochs, val_acc, 'b', linestyle='dashdot')
    plt.title('Training and validation accuracy')
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend(["Accuracy", "Validation Accuracy"])
    plt.savefig("../diagnosis-system/src/assets/CNN_accuracy.png", dpi=600)
    plt.figure()

    # ��loss����
    plt.plot(epochs, loss, 'r', linestyle='-.')
    plt.plot(epochs, val_loss, 'b', linestyle='dashdot')
    plt.title('Training and validation loss')
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend(["Loss", "Validation Loss"])
    plt.savefig("../diagnosis-system/src/assets/CNN_loss.png", dpi=600)
    # plt.figure()
    plt.show()


# ���ƻ�������
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
    # -------------------------------���ӻ�--------------------------------
    # y_test_cat = np_utils.to_categorical(y_test[:2400], num_classes=10)# �ܵ����
    plt.figure(figsize=(5, 5))
    color_map = y_test[:]
    for cl in range(num_classes):  # �ܵ����
        indices = np.where(color_map == cl)
        indices = indices[0]
        plt.scatter(tsne_results[indices, 0], tsne_results[indices, 1], label=None)
        # plt.scatter(tsne_results[indices, 0], tsne_results[indices, 1], label=cl)
    plt.tick_params(labelsize=18)
    plt.legend()
    # plt.savefig("./Algorithm/save_picture/result.png", dpi=600)
    plt.savefig("../diagnosis-system/src/assets/CNN_result.png", dpi=600)
    plt.show()


def run_Algorithm(logger):
    main_Algoithm()
    start_tsne()
    modeltrain(logger)
    acc_line()
    confusion()
    new_start_tsne()

# run_Algorithm()
