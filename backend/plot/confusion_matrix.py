import numpy as np
import matplotlib.pyplot as plt
import itertools  # Often used for iterating through confusion matrix cells
from matplotlib import rcParams

# 设置中文字体（Windows系统通常使用SimHei，Mac使用PingFang SC）
rcParams['font.sans-serif'] = ['SimHei']  # Windows
# rcParams['font.sans-serif'] = ['PingFang SC']  # Mac
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    # print(cm) # Optional: Print the matrix values to console

    plt.figure(figsize=(7, 6))  # Adjust figure size as needed
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45, ha="right")  # Added rotation and alignment
    plt.yticks(tick_marks, classes)

    # Determine the threshold for text color (black/white)
    # This ensures text is readable on different background shades
    thresh = cm.max() / 2.
    # Add text annotations to each cell
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], 'd'),  # Use 'd' for integer format
                 horizontalalignment="center",
                 # Choose text color based on background darkness
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()  # Adjust layout to prevent labels overlapping
    plt.ylabel('真实标签')
    plt.xlabel('预测标签')  # Changed from 'Predicted label' to match image


# --- Data from your image ---
# Rows are True Labels, Columns are Predicted Labels
# cm_data = np.array([
#     [71,  0,  0,  0,  0,  0,  0,  0,  0,  0], # True label 0
#     [ 0, 78,  0,  0,  0,  0,  0,  0,  0,  0], # True label 1
#     [ 0,  0, 65,  1,  0,  0,  0,  0,  0,  0], # True label 2
#     [ 0,  0,  0, 75,  0,  0,  0,  0,  0,  0], # True label 3
#     [ 1,  0,  1,  0, 62,  0,  0,  0,  0,  0], # True label 4
#     [ 0,  0,  0,  0,  0, 64,  0,  0,  0,  0], # True label 5
#     [ 0,  0,  0,  0,  0,  0, 76,  0,  0,  0], # True label 6
#     [ 0,  0,  0,  0,  0,  0,  0, 78,  0,  0], # True label 7
#     [ 0,  0,  0,  0,  0,  0,  0,  0, 68,  0], # True label 8
#     [ 0,  0,  0,  0,  0,  0,  0,  0,  0, 80]  # True label 9
# ])

cm_data = np.array([
    [69, 1, 0, 0, 0, 0, 0, 0, 1, 0],  # True label 0
    [0, 66, 2, 0, 0, 0, 0, 0, 0, 0],  # True label 1
    [0, 2, 67, 0, 2, 0, 2, 0, 0, 0],  # True label 2
    [0, 0, 0, 75, 0, 0, 0, 0, 0, 0],  # True label 3
    [0, 2, 1, 0, 69, 0, 1, 0, 0, 0],  # True label 4
    [0, 0, 1, 0, 0, 81, 0, 0, 0, 0],  # True label 5
    [0, 0, 0, 0, 0, 0, 60, 0, 0, 0],  # True label 6
    [0, 0, 0, 0, 0, 0, 0, 79, 0, 0],  # True label 7
    [2, 0, 0, 0, 0, 0, 0, 0, 69, 0],  # True label 8
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 69]  # True label 9
])

# --- Define class labels ---
class_names = np.arange(10)  # Should be ['0', '1', ..., '9'] or similar

# --- Plot the confusion matrix ---
plot_confusion_matrix(cm_data, classes=class_names, title='混淆矩阵', cmap='Reds')

plt.savefig('confusion_matrix3.png', dpi=300, bbox_inches='tight')

# --- Display the plot ---
plt.show()

# def plot_confusion_matrix(cm, classes,
#                           normalize=False,
#                           title='Confusion matrix',
#                           cmap=plt.cm.Blues):  # Default is still Blues
#     """
#     This function prints and plots the confusion matrix.
#     Normalization can be applied by setting `normalize=True`.
#     """
#     if normalize:
#         cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
#         print("Normalized confusion matrix")
#     else:
#         print('Confusion matrix, without normalization')
#
#     plt.figure(figsize=(7, 6))
#     # Use the provided cmap in imshow
#     plt.imshow(cm, interpolation='nearest', cmap=cmap, vmin=0, vmax=80)  # Pass cmap here
#     plt.title(title)
#     plt.colorbar()  # Colorbar will now use the passed cmap
#     tick_marks = np.arange(len(classes))
#     plt.xticks(tick_marks, classes, rotation=45, ha="right")
#     plt.yticks(tick_marks, classes)
#
#     thresh = cm.max() / 2.  # Threshold for text color remains the same logic
#     for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
#         plt.text(j, i, format(cm[i, j], 'd'),
#                  horizontalalignment="center",
#                  # Text color logic might need slight adjustment for different cmaps,
#                  # but white/black based on threshold often works well.
#                  color="white" if cm[i, j] > thresh else "black")
#
#     # Explicitly set colorbar limits AFTER creating the plot elements
#     # Get the current image object to set clim on its colorbar
#     im = plt.gci()
#     plt.colorbar(im).set_clim(vmin=0, vmax=80)
#
#     plt.tight_layout()
#     plt.ylabel('真实标签')
#     plt.xlabel('预测标签')
#
#
# # --- Data from the SECOND image ---
# cm_data = np.array([
#     [69, 1, 0, 0, 0, 0, 0, 0, 1, 0],  # True label 0
#     [0, 66, 2, 0, 0, 0, 0, 0, 0, 0],  # True label 1
#     [0, 0, 67, 0, 1, 0, 0, 0, 0, 1],  # True label 2
#     [0, 0, 0, 75, 0, 0, 0, 0, 0, 0],  # True label 3
#     [0, 2, 2, 0, 69, 0, 2, 0, 0, 0],  # True label 4
#     [0, 0, 1, 0, 0, 81, 0, 0, 0, 0],  # True label 5
#     [0, 0, 0, 0, 0, 0, 60, 0, 0, 0],  # True label 6
#     [0, 0, 0, 0, 0, 0, 0, 79, 0, 0],  # True label 7
#     [2, 0, 0, 0, 0, 0, 0, 0, 69, 0],  # True label 8
#     [0, 0, 1, 0, 0, 0, 0, 0, 0, 69]  # True label 9
# ])
#
# # --- Define class labels ---
# class_names = np.arange(10)
#
# # --- Plot the confusion matrix with RED colormap ---
# # Pass cmap='Reds' (or plt.cm.Reds) when calling the function
# plot_confusion_matrix(cm_data, classes=class_names, title='混淆矩阵', cmap='Reds')
#
# plt.savefig('confusion_matrix2.png', dpi=300, bbox_inches='tight')
#
# # --- Display the plot ---
# plt.show()
