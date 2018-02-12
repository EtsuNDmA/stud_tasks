from fid3 import *


def class_coder(classes, decode=False):
  codes = {cl.encode('utf-8'): i for i, cl in enumerate(classes)}
  decodes = {i: cl for i, cl in enumerate(classes)}

  def coder(class_):
    return codes[class_]

  def decoder(class_):
    return decodes[class_]

  if decode:
    # Имя по номеру
    return decoder
  # Номер по имени
  return coder


if __name__ == '__main__':
    # Загрузим параметры нечетких функций
    with open('iris_params.json', 'r') as fp:
      params = json.load(fp)

    verbose_classes = params['classes']
    class_coder_func = class_coder(verbose_classes)

    classes = [class_coder_func(c.encode('utf-8')) for c in verbose_classes]
    fuzzy_attributes = params['attributes']

    # Загрузим датасет, исключив 1 строку
    dataset = np.loadtxt('iris.csv', delimiter=",", skiprows=1, converters={4:class_coder_func})
    X = dataset[:, :-1]
    y = dataset[:, -1].astype(int)

    # Разделим датасет
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

    # Создадим и обучим классификатор
    clf = FuzzyID3Classifier(control_threshold=0.85, decision_threshold=0.02)
    clf.fit(X_train, y_train, fuzzy_attributes, classes)

    # Распечатаем дерево в файл
    with open('out_iris_tree.txt', 'w') as f:
        pprint(clf.tree, file=f)

    c_memb = clf.predict(X_test)
    y_pred = np.argmax(c_memb, axis=1)

    confusion_matrix = clf.confusion_matrix(y_pred, y_test)
    precision, recall = clf.score(y_pred, y_test)

    with open('out_iris_result.txt', 'w') as f:
        print("Class memberships for classes {}coded as {}\n{} ".format(verbose_classes, classes, c_memb), file=f)
        print("Test dataset contains {} members".format(X_test.shape[0]), file=f)
        print("X_test:\n{}".format(X_test), file=f)
        print("Prediction:\n{}\nTrue:\n{}".format(y_pred, y_test), file=f)
        print("Confusion matrix:\n{}".format(confusion_matrix), file=f)
        print("Correctly classified {:.0f}/{} samples".format(np.trace(confusion_matrix), X_test.shape[0]), file=f)
        print("Precision: ["+" ".join(['{:.2f}'.format(i) for i in precision])+"]", file=f)
        print("Recall: ["+" ".join(['{:.2f}'.format(i) for i in recall])+"]", file=f)
