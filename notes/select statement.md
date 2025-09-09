# Select statement

The collection of expressions which may be "selected" in a SQL statement fall under the `ParsedExpressionSubclasses` type. This is a union of the following expression types:

FunctionExpression
ColumnRefExpression
StarExpression
ConstantExpression
CastExpression
ComparisonExpression
ConjunctionExpression
LambdaExpression
ParameterExpression
PositionalReferenceExpression
SubqueryExpression
OperatorExpression
CaseExpression
CollateExpression
BetweenExpression
WindowExpression

Here are examples of each one.

## FunctionExpression
```sql
select range(0, 10)
```
## ColumnRefExpression
```sql
select a_column
```
## StarExpression
```sql
select *
```
## ConstantExpression
```sql
select 2
```
## CastExpression
```sql
select 2::FLOAT,
       CAST(2 AS FLOAT),
```
## ComparisonExpression
```sql
select a_column > 2
```
## ConjunctionExpression
```sql
select (condition_a AND condition_b)
```
## LambdaExpression
```sql
select x -> 2*x
```
## ParameterExpression
(prepared statements)
```sql
select $1
```
## PositionalReferenceExpression
```sql
select #1, #2
```
## SubqueryExpression
```sql
select (select 2 as two)
```
## OperatorExpression
```sql
select col is NULL
```
## CaseExpression
```sql
select case when a > 2 then true else false end
```
## CollateExpression
```sql
select 'hello' COLLATE NOCASE = 'hElLO'
```
## BetweenExpression
```sql
select col between 1 and 2
```
## WindowExpression
```sql
select row_number() over ()
```