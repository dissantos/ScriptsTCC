import pandas as pd


class BadSmellDetectionMetrics:
    def __init__(self, project_name: str, path: str) -> None:
        self.project_name: str = project_name
        self.path: str = path
        self.class_code_metric: pd.DataFrame = pd.read_csv(
            self.path + "class_" + self.project_name + ".csv")
        self.method_code_metric: pd.DataFrame = pd.read_csv(
            self.path + "method_" + self.project_name + ".csv")
        self.df_bad_smells_detected: pd.DataFrame = pd.DataFrame(
            columns=['class', 'data_class', 'large_class', 'long_method', 'feature_envy', 'refused_bequest'],  index=['class'])

    def getDataClass(self, class_name: str) -> int:
        class_metric = self.class_code_metric[self.class_code_metric['class'] == class_name]

        if(class_metric['noc'].iloc[0] <= 8 and class_metric['dit'].iloc[0] <= 2 and class_metric['totalFieldsQty'].iloc[0] > 8):
            return 1
        else:
            return 0

    def getFeatureEnvy(self, class_name: str) -> int:
        class_metric = self.class_code_metric[self.class_code_metric['class'] == class_name]
        if class_metric['lcom*'].iloc[0] > 0.725:
            return 1
        else:
            return 0

    def getLargeClass(self, class_name: str) -> int:
        class_metric = self.class_code_metric[self.class_code_metric['class'] == class_name]

        if(class_metric['lcom*'].iloc[0] > 0.725 and class_metric['wmc'].iloc[0] > 34 and class_metric['totalFieldsQty'].iloc[0] > 8 and class_metric['totalMethodsQty'].iloc[0] > 14):
            return 1
        else:
            return 0

    def getLongMethod(self, class_name: str) -> int:
        methods_metric = self.method_code_metric[self.method_code_metric['class'] == class_name]
        cont_long_methods_class = 0

        for index, method in methods_metric.iterrows():
            if(method['loc'] > 30 and method['wmc'] > 4 and method['maxNestedBlocksQty'] > 3):
                cont_long_methods_class += 1

        return cont_long_methods_class

    def getRefusedBequest(self, class_name: str) -> int:
        # TODO
        return 0

    def detectBadSmells(self) -> None:
        class_names = self.class_code_metric['class']

        for class_name in class_names:
            data = {
                'class': class_name,
                'data_class': self.getDataClass(class_name),
                'large_class': self.getLargeClass(class_name),
                'long_method': self.getLongMethod(class_name),
                'feature_envy': self.getFeatureEnvy(class_name),
                'refused_bequest': self.getRefusedBequest(class_name),
            }

            row = pd.DataFrame(columns=['class', 'data_class', 'large_class',
                                        'long_method', 'feature_envy', 'refused_bequest'], data=data, index=['class'])

            self.df_bad_smells_detected = self.df_bad_smells_detected.append(
                row)

    def save_bad_smells(self, path):
        self.df_bad_smells_detected.to_csv(path+self.project_name+".csv")
