{% macro drop_view(view_name) %}
{% set sql %}
DROP VIEW IF EXISTS {{ view_name }} CASCADE;
{% endset %}
{{ run_query(sql) }}
{% endmacro %}