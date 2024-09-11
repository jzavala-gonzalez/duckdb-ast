# Using Mause's test cases from the AST repo,
# create a JSON file for each parse result

import os
import json

from duckdb_ast import parse_sql_to_json

query_list_path = 'outputs/query_list.txt'
query_json_dir = 'outputs/query_jsons'

sql_examples = [
        "select 1",
        "select * from range(0, 10)",
        "select * from duckdb_tables",
        "select frog from frogs",
        "select frog from frogs where height > 5 and leader = true",
        "select 1 * 1",
        "select frog.age from frogs",
        "select []::boolean[]",
        "select frog.* EXCLUDE age from frogs",
        """
SELECT *
EXCLUDE (timestamp_tz)
REPLACE (varchar.replace(chr(0), chr(10)) AS whatever)
FROM test_all_types()
        """,
        "select list_apply([1, 2, 3], x => x * 2)",
        "select 0::DECIMAL(15, 6)",
        "select 0::USER_TYPE",
        "select 0::STRUCT(a INT)",
        "select name from frogs GROUP BY age",
        "SELECT * FROM frogs USING SAMPLE 1% (BERNOULLI);",
        """
        select (select 1) as one
        """,
        """
        SELECT city, COUNT(*)
        FROM addresses
        GROUP BY city
        HAVING COUNT(*) >= 50;
        """,
        "SELECT 1 < 1, 1 <= 2",
        "SELECT '101010'::BIT",
        "SELECT 0::HUGEINT",
        "SELECT 0::UNION(num INT, str VARCHAR)",
        # r"SELECT '\xAA'::BLOB",
        "SELECT INTERVAL 1 YEAR",
        "SELECT NULL IS NULL",
        "SELECT DATE '1992-09-20'",
        "SELECT TIMESTAMP '1992-09-20 11:30:00'",
        "SELECT TIMESTAMPTZ '1992-09-20 11:30:00'",
        "SELECT i, CASE WHEN i>2 THEN 1 ELSE 0 END AS test FROM integers",
        "SELECT 'hello' COLLATE NOCASE",
        "SELECT 'Math' IN ('CS', 'Math'), X NOT IN ('CS', 'Math')",
        "SELECT a BETWEEN x AND y",
        "SELECT a NOT BETWEEN x AND y",
        "SELECT expression IS NOT NULL",
        "SELECT 2 IS DISTINCT FROM NULL, NULL IS NOT DISTINCT FROM NULL",
        "SELECT 2 < 3, 2 > 3, 2 <= 3, 4 >= NULL, NULL = NULL, 2 <> 2",
        "SELECT EXISTS(SELECT * FROM grades WHERE course='Math');",
        "SELECT 'Math' IN (SELECT course FROM grades);",
        """
        SELECT *
        FROM grades grades_parent
        WHERE grade=
            (SELECT MIN(grade)
             FROM grades
             WHERE grades.course=grades_parent.course);
        """,
        "SELECT MIN(COLUMNS(*)), COUNT(COLUMNS(*)) from numbers;",
        "SELECT a.* FROM (SELECT {'x':1, 'y':2, 'z':3} as a);",
        """
        WITH ranked_functions as (
            SELECT
                schema_name,
                function_name,
                row_number() over (partition by schema_name order by function_name) as function_rank
            FROM duckdb_functions()
        )
        SELECT
            *
        FROM ranked_functions
        WHERE
            function_rank < 3;
        """,
        """
        WITH RECURSIVE tag_hierarchy(id, source, path) AS (
  SELECT id, name, [name] AS path
  FROM tag
  WHERE subclassof IS NULL
UNION ALL
  SELECT tag.id, tag.name, list_prepend(tag.name, tag_hierarchy.path)
  FROM tag, tag_hierarchy
  WHERE tag.subclassof = tag_hierarchy.id
)
SELECT path
FROM tag_hierarchy
WHERE source = 'Oasis';
        """,
        """
        select
            thing[0],
            thing['hello'],
            thing[1:3],
            struct_pack(hello := 'world').hello,
        """,
        """
        SELECT * FROM range(10) t1 UNION ALL SELECT * FROM range(5) t2;
        """,
        """
        WITH RECURSIVE per_investor_amount AS (
            SELECT  0 AS investors_number,
                    0.00 AS investment_amount,
                    0.00 AS individual_amount
            UNION

            SELECT  investors_number + 1,
                    i.investment_amount,
                    i.investment_amount / (investors_number + 1)
            FROM investment i, per_investor_amount pia
            WHERE investors_number << 3
        )

        SELECT *
        FROM per_investor_amount
        ORDER BY  investment_amount, investors_number;
        """,
        "SELECT row_number() OVER () FROM sales;",
        "SELECT row_number() OVER (ORDER BY time) FROM sales;",
        "SELECT row_number() OVER (PARTITION BY region ORDER BY time) FROM sales;",
        """
        SELECT amount - lead(amount) OVER (ORDER BY time),
               amount - lag(amount) OVER (ORDER BY time),
               amount / SUM(amount) OVER (PARTITION BY region),
               FIRST(employee_name) OVER (ORDER BY salary DESC),
               LAST(employee_name)  OVER (ORDER BY salary DESC),
               NTH_VALUE(employee_name, 2) OVER (ORDER BY salary DESC)
        FROM basic_pays
        """,
        """
        SELECT Plant, Date,
    AVG(MWh) OVER (
        PARTITION BY Plant
        ORDER BY Date ASC
        RANGE BETWEEN INTERVAL 3 DAYS PRECEDING
                  AND INTERVAL 3 DAYS FOLLOWING)
        AS 'MWh 7-day Moving Average'
FROM 'Generation History'
ORDER BY 1, 2
        """,
        "SELECT #1, #2 FROM tbl",
        "SELECT $hello FROM tbl",
        "SELECT list_map(x -> x * 2)",
    ]

if os.path.isfile(query_list_path):
    os.remove(query_list_path)
if os.path.isdir(query_json_dir):
    files = os.listdir(query_json_dir)
    for file in files:
        os.remove(os.path.join(query_json_dir, file))
    os.rmdir(query_json_dir)
os.makedirs(query_json_dir)

f_query_list = open(query_list_path, 'a')
query_sep = '\n\n'
for i,sql in enumerate(sql_examples, start=1):
    # print(sql)
    f_query_list.write(f'Query #{i}\n{sql}{query_sep}')

    json_string = parse_sql_to_json(sql)
    json_data = json.loads(json_string)
    json_string_pretty = json.dumps(json_data, indent=2)
    json_path = os.path.join(query_json_dir, f'query_{i:02}.json')
    with open(json_path, 'w') as f:
        f.write(json_string_pretty)

    # break