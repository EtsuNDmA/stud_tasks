from fid3 import *

if __name__ == '__main__':
    
    # Загрузим датасет, исключив 1 строку
    def class_coder(class_str, decode=False):
        codes = {
            b'Iris-setosa': 0,
            b'Iris-versicolor': 1,
            b'Iris-virginica': 2,
        }
        decodes = {
            0: 'Iris-setosa',
            1: 'Iris-versicolor',
            2: 'Iris-virginica',
        }
        if decode:
            # Имя по номеру
            return decodes[class_str]
        # Номер по имени
        return codes[class_str]
    dataset = np.loadtxt('iris.csv', delimiter=",", skiprows=1, converters={4:class_coder})
    X = dataset[:, :-1]
    y = dataset[:, -1].astype(int)
    
    # Создадим функции для вычисления нечтких аргументов
    # Аттрибуты датасета: Sepal Length , Sepal width, Petal Length , Petal Width 
    def sl_short(x):
        if x < 5.5:
            return 1.0
        elif x <= 6.5:
            return 6.5-x
        else:
            return 0.0

    def sl_long(x):
        if x < 5.5:
            return 0.0
        elif x <= 6.5:
            return x-5.5
        else:
            return 1.0

    def sw_short(x):
        if x < 2:
            return 1.0
        elif x <= 4:
            return 2 - 0.5*x
        else:
            return 0.0

    def sw_long(x):
        if x < 2:
            return 0.0
        elif x <= 4:
            return 0.5*x - 1
        else:
            return 1.0
            
    def pl_short(x):
        if x < 3:
            return 1.0
        elif x <= 5:
            return 2.5 - 0.5*x
        else:
            return 0.0

    def pl_long(x):
        if x < 3:
            return 0.0
        elif x <= 5:
            return 0.5*x - 1.5
        else:
            return 1.0

    def pw_short(x):
        if x < 0.5:
            return 1.0
        elif x <= 1.5:
            return 1.5 - x
        else:
            return 0.0

    def pw_long(x):
        if x < 0.5:
            return 0.0
        elif x <= 1.5:
            return x - 0.5
        else:
            return 1.0

    sl_short = np.vectorize(sl_short)
    sl_long = np.vectorize(sl_long)
    
    sw_short = np.vectorize(sw_short)
    sw_long = np.vectorize(sw_long)
    
    pl_short = np.vectorize(pl_short)
    pl_long = np.vectorize(pl_long)
    
    pw_short = np.vectorize(pw_short)
    pw_long = np.vectorize(pw_long)
    
    fuzzy_attributes = {
        'sepal_length': {
            'functions': [sl_short, sl_long],
            'names': ['short', 'long'],
            'column': 0,
        },                      
        'sepal_width': {
            'functions': [sw_short, sw_long],
            'names': ['short', 'long'],
            'column': 1,
        },
        'petal_length': {
            'functions': [pl_short, pl_long],
            'names': ['short', 'long'],
            'column': 2,
        },                      
        'petal_width': {
            'functions': [pw_short, pw_long],
            'names': ['short', 'long'],
            'column': 3,
        }, 
    }
    classes = [0, 1, 2]
    
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
        print("Class memberships for classes {}\n{}".format([class_coder(c, decode=True) for c in classes], c_memb), file=f)
        print("Test dataset contains {} members".format(X_test.shape[0]), file=f)
        print("X_test:\n{}".format(X_test), file=f)
        print("Prediction:\n{}\nTrue:\n{}".format(y_pred, y_test), file=f)
        print("Confusion matrix:\n{}".format(confusion_matrix), file=f)
        print("Correctly classified {:.0f}/{} samples".format(np.trace(confusion_matrix), X_test.shape[0]), file=f)
        print("Precision: ["+" ".join(['{:.2f}'.format(i) for i in precision])+"]", file=f)
        print("Recall: ["+" ".join(['{:.2f}'.format(i) for i in recall])+"]", file=f)