from sklearn.metrics import confusion_matrix
from tensorflow.keras.metrics import BinaryAccuracy, AUC

from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, auc
import matplotlib.pyplot as plt


def conf_matrix(y_true, y_pred):
    conf_matrix = confusion_matrix(y_true=y_true, y_pred=y_pred)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.matshow(conf_matrix, alpha=0.3)
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            ax.text(x=j, y=i, s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
    plt.xlabel('Predictions', fontsize=18)
    plt.ylabel('Actuals', fontsize=18)
    plt.title('Confusion Matrix', fontsize=18)
    plt.show()


def scores(truth, result):
    print('Precision: ', precision_score(truth, result))
    print('Recall: ', recall_score(truth, result))
    print('Accuracy: ', accuracy_score(truth, result))
    print('F1 Score: ', f1_score(truth, result))
    print('F1 Score: ', auc(truth, result))

    # source: https://rvprasad.medium.com/informedness-and-markedness-20e3f54d63bc
    #accuracy = TP/(total)
    #informedness   = TP/(RP) - FP/(RN)
    #               = TP/(TP+FN) - FP/(FP+TN)
    #               = recall - FP/(FP+TN)
    #markedness     = TP/(PP) - FN/(PN)
    #               = TP/(TP+FP) - FN/(FN+TN)
    #               = precision - FN/(FN+TN)
    # pf.plot_results_FFN(sample[:,0].reshape(4800), result, truth)

    auc_score = AUC()
    auc_score.update_state(truth, result)
    bin_acc = BinaryAccuracy()
    bin_acc.update_state(truth, result)
