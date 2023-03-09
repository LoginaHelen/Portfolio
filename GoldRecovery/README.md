# Восстановление золота из руды

## Описание проекта

Необходимо подготовить модель машинного обучения, предсказывающую коэффициент восстановления золота из золотосодержащей руды. Модель поможет оптимизировать производство, чтобы не запускать предприятие с убыточными характеристиками.

## Навыки и инструменты

- pandas
- numpy
- seaborn
- matplotlib
- math
- sklearn.metrics.make_scorer
- sklearn.metrics.mean_absolute_error
- sklearn.model_selection.cross_val_score
- sklearn.tree.DecisionTreeRegressor
- sklearn.ensemble.RandomForestRegressor
- sklearn.linear_model.LinearRegression
- sklearn.model_selection.GridSearchCV
- sklearn.dummy.DummyRegressor

## Общий вывод

Было проведено обучение выбранных моделей для стадий грубой и тонкой очистки, проведена проверка выбранных обученных моделей на тестовом наборе и выбрана одна для запуска в производство.