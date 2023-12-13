# Сравнение хранилищ для доступа к структурированных данных

## Проблема
В моем рабочем проекте необходимо было выполнять множество запросов к матрицам (наборам структурированных данных, например, из csv файла) для поиска среди записей матриц таких, которые бы соответствовали фильтрам. Это было одним из узких мест программы. Хранение и поиск данных был организован с использованием SQLite. 
Необходимо было реализовать более быстрый доступ к записям матриц по фильтрам.
Сервис написан на Python 3.11.

### Формулировка требований
Прежде чем выбрать тестируемые хранилища, обозначим требования, которым хранилище должно удовлетворять:
- Поддержка фильтрации записей по операции эквивалентности, с условиями объединенными операцией конъюнкции (аналог `where col_1=val_1 and col_2=val_2 …` в sql);
- Поддержка сортировки (аналог `order by col1 asc col2 desc …` в sql);
- Поддержка операции выбора первой подходящей записи (аналог `limit 1` в sql).

### Установка ограничений для хранилища данных
Для выбора наиболее эффективного хранилища необходимо выделить некоторые ограничения работы программы:
- Поиск происходит по определенным колонкам;
- Сортировка происходит по определенным колонкам;
- Объем данных в формате csv не превышает 50 Мб.

Мы можем использовать эту информацию для создания индексов (п. 1) и/или предварительной сортировки данных (п. 2).

### Выбор хранилища
Так как нам необходима наибольшая скорость работы и объем данных, к которым должен выполняться запрос, не велик, то было принято решение использовать без серверное In-memory хранилище.  
Сравнивались:
- SQLite (реляционное хранилище);
- DuckDB (хранилище колоночного типа);
- Поиск по датафреймам Polars;
- Хеш-таблицы, созданные с помощью dict() в Python (DictDB).

#### Рассмотрим подробнее достоинства этих хранилищ при решении поставленной задачи (Таблица 1)

**Таблица 1 - Предварительное сравнение выбранных хранилищ**
| Хранилище | Индексация | Гибкость запросов | Сжатие данных |
|-----------|------------|-------------------|---------------|
| SQLite    | B-деревья, индексы вида UNIQUE, PRIMARY KEY, сложность поиска по индексу O(log n) | Высокая, поддержка SQL с расширенными функциями | Поддерживается в ограниченной степени |
| DuckDB    | Колоночные индексы, индекс построенный на основе столбцов, сложность поиска по индексу O(log n) | Высокая, оптимизировано для аналитических запросов, поддержка SQL | Эффективное сжатие, оптимизировано для колоночного хранения |
| Polars    | Не применимо, так как это библиотека обработки данных | Средняя, зависит от возможностей библиотеки Python для обработки данных | Не применимо, так как это библиотека обработки данных |
| Python dict() | Хеш-таблицы, прямой доступ по ключу, сложность получения данных O(1) | Ограниченная, основные операции поиска и обновления | Не применимо, но эффективное использование памяти благодаря хеш-таблицам |

Из таблицы 1 видим, что сложность O(1) на операции чтения данных в Python dict() ниже, чем сложность для той же операции в других, рассматриваемых хранилищах. Поэтому адаптированный под поставленную задачу словарь в Python должен позволить осуществлять доступ к данным за меньшее время.

### Описание DictDB
Для размещения данных в хеш-таблицах, созданных с помощью dict() в Python была реализована такая структура данных, в которой имя сущности (имя таблицы) ссылается на хеш-таблицу поисковых индексов (поле/поля, по которым планируется выполнять поиск сущностей. Поисковый индекс указывает на хеш-таблицу со значениями искомых полей. А значения искомых полей, в свою очередь, ссылаются на список сущностей (row_1, …, row_n), как показано на рисунке 1.

**Рисунок 1 - Структура хранения записей в DictDB**

### Тестирование хранилищ
Тестирование проводилось на хранилищах заполненных 1000 записями одной сущности при 10000 запросах на получение этих данных (на языка SQL эти запросы выглядели бы так: `SELECT * FROM TABLE_1 WHERE col_1 = val_1 and col_2 = val_2`). В тестах будем менять следующие параметры:
- Селективность запроса (будем загружать в хранилище одинаковые или случайные записи);
- Операция сортировки.

#### Проведем 4 теста:
1. Без использования сортировки и без высокой селективности данных;
2. Без использования сортировки и с высокой селективностью данных;
3. С использованием сортировки и без высокой селективности данных;
4. С использованием сортировки и с высокой селективностью данных.

**Результаты тестирования приведены в таблицах 2-3**

**Таблица 2 - Сравнения времени получения данных при 10000 запросах**
| Имя хранилища | Среднее время (Тест 1) | Среднее время (Тест 2) | Среднее время (Тест 3) | Среднее время (Тест 4) | Среднее время |
|---------------|------------------------|------------------------|------------------------|------------------------|---------------|
| dictdb        | 0.044815               | 0.046454               | 0.049994               | 0.049949               | 0.047803      |
| sqlite3       | 0.148322               | 0.098925               | 0.170734               | 0.117103               | 0.133771      |
| duckdb        | 3.601976               | 3.402912               | 5.392783               | 4.363182               | 4.190213      |
| polars        | 1.828073               | 1.242679               | 3.244541               | 1.674742               | 1.997509      |

### Таблица 3 - Сравнение выделения памяти при 10000 запросах
| Имя хранилища | Среднее выделение памяти (Тест 1) | Среднее выделение памяти (Тест 2) | Среднее выделение памяти (Тест 3) | Среднее выделение памяти (Тест 4) | Среднее выделение памяти |
|---------------|-----------------------------------|-----------------------------------|-----------------------------------|-----------------------------------|--------------------------|
| dictdb        | 1263.0                            | 436.0                             | 436.0                             | 436.0                             | 642.750                  |
| sqlite3       | 18586.5                           | 17256.5                           | 17670.5                           | 17488.5                           | 17750.500                |
| duckdb        | 1898.5                            | 626.0                             | 1425.5                            | 679.0                             | 1157.250                 |
| polars        | 4045.5                            | 2684.0                            | 3559.0                            | 2902.0                            | 3297.625                 |

На основании проведенных тестов можно сделать вывод о том, что DictDB превосходит сравниваемые хранилища по времени получения данных и по количеству выделенной памяти.

### Внедрение DictDB
После внедрения DictDB в проект наблюдались изменения следующих значимых для развертывания проекта параметров: RPS и RAM, представленных в таблице 4

### Таблица 4 - Результаты сравнения RPS и RAM в SQLite и DictDB
| Хранилище | RPS  | Память на старте (Mb) | Память после теста (Mb) | Относительный RPS (к SQLite) | Относительная память на старте (к SQLite) | Относительная память после теста (к SQLite) |
|-----------|------|-----------------------|-------------------------|-----------------------------|-------------------------------------------|---------------------------------------------|
| SQLite    | 200  | 460                   | 667                     | 1.0                         | 1.000000                                  | 1.000000                                    |
| DictDB    | 300  | 1350                  | 1600                    | 1.5                         | 2.934783                                  | 2.398801                                    |

В этой таблице представлены как абсолютные значения Requests Per Second (RPS) и использование памяти (в мегабайтах), так и их относительные значения по сравнению с SQLite. Например, DictDB имеет в 1.5 раза больше RPS и использует в ~2.93 раза больше памяти на старте и ~2.40 раза больше памяти после теста по сравнению с SQLite (Таблица 4).

### Выводы
Несмотря на высокие показатели роста RPS, такое решение, как DictDB не может быть внедрено в рабочий проект, так как целесообразнее будет поднять второй Pod с таким же контейнером с SQLite из-за высокого потребления оперативной памяти. Таким образом, для описанной мной задачи на Python лучшим, из сравниваемых хранилищ является SQLite.