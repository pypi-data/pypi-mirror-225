# Importing Library
from scipy.stats import f_oneway


class annova:

    def __init__(self, data, predictor_list, target, alpha):
        self.data = data
        self.predictor_list = predictor_list
        self.target = target
        self.alpha = alpha

    def f_oneway_test(self):
        '''
        This function takes in a dataframe, a list of predictor, a target variable and a significance level
        and returns a list of predictor that are correlated with the target variable
        return: 

        Input: data: dataframe 
                predicator_list: list of predictor (Independent Features)
                target: target variable (Dependent Feature)
                alpha: significance level
        Output: 
            return selected columns in list
        '''
        selected_columns = []
        for predictor in self.predictor_list:
            cat_vs_num = self.data.groupby(predictor)[self.target].apply(list)
            f_statistic, p_value = f_oneway(*cat_vs_num)

            if (p_value < self.alpha):
                print(predictor, 'is correlated with',
                      self.target, '| P-Value:', p_value)
                selected_columns.append(predictor)
            else:
                print(predictor, 'is NOT correlated with',
                      self.target, '| P-Value:', p_value)
        print("--------------Selected Features------------")
        return selected_columns

# Function to perform f_oneway ANOVA test
