import pandas as pd


class OracleValidation:
    def __init__(self, project_name: str, sheet_name: str, result_path: str) -> None:
        self.df_oracle_results = pd.read_excel(
            result_path,  engine="openpyxl", sheet_name=sheet_name)
        self.df_oracle_results = self.df_oracle_results[self.df_oracle_results['Bad smell']
                                                        != "Refused Bequest"]
        self.df_bad_smells_detected = pd.read_csv(
            f'bad_smells_detected{project_name}.csv')
        self.project_name = project_name
        self.dictBadSmells = {
            'Data Class': 'data_class',
            'Feature Envy': 'feature_envy',
            'Large Class': 'large_class',
            'Long Method': 'long_method',
            'Refused Bequest': 'refused_bequest'
        }

    def validate(self) -> float:
        class_names = self.df_oracle_results['Classe']
        hits = 0
        for class_name in class_names:
            df_filter_class_oracle: pd.DataFrame = self.df_oracle_results[
                self.df_oracle_results['Classe'] == class_name]
            df_filter_class_detected: pd.DataFrame = self.df_bad_smells_detected[
                self.df_bad_smells_detected['class'] == class_name.replace(".java", "")]

            if(len(df_filter_class_detected) == 1):
                for i, row in df_filter_class_oracle.iterrows():
                    if(df_filter_class_detected[self.dictBadSmells[row['Bad smell']]].iloc[0] != 0):
                        hits += 1

        return hits/len(self.df_oracle_results)
