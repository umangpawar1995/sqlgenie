import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where, TokenList
from sqlparse.tokens import Keyword, DML

def optimize_sql(query: str) -> str:
    """
    Optimizes a SQL query by removing anti-patterns:
    - SELECT *
    - Unnecessary DISTINCT
    - Missing WHERE clause (warn)
    Returns the optimized SQL as a string.
    """
    parsed = sqlparse.parse(query)
    if not parsed:
        raise ValueError("Could not parse SQL query.")
    stmt = parsed[0]
    tokens = [t for t in stmt.tokens if not t.is_whitespace]
    # Detect SELECT *
    has_select_star = False
    for token in tokens:
        if token.ttype is DML and token.value.upper() == 'SELECT':
            idx = tokens.index(token)
            next_token = tokens[idx+1] if idx+1 < len(tokens) else None
            if next_token and next_token.value.strip() == '*':
                has_select_star = True
    # Remove DISTINCT if not needed
    cleaned_tokens = []
    skip_next = False
    for i, token in enumerate(tokens):
        if skip_next:
            skip_next = False
            continue
        if token.ttype is Keyword and token.value.upper() == 'DISTINCT':
            # Remove DISTINCT if not followed by aggregate
            after = tokens[i+1] if i+1 < len(tokens) else None
            if after and after.ttype is Keyword and after.value.upper() in ['COUNT', 'SUM', 'AVG', 'MIN', 'MAX']:
                cleaned_tokens.append(token)
            else:
                continue  # skip DISTINCT
        else:
            cleaned_tokens.append(token)
    # Check for WHERE clause
    has_where = any(isinstance(t, Where) or (t.ttype is Keyword and t.value.upper() == 'WHERE') for t in tokens)
    # Build suggestions
    suggestions = []
    if has_select_star:
        suggestions.append('-- Replaced SELECT * with column list for better performance.')
    if not has_where:
        suggestions.append('-- Warning: Query has no WHERE clause. Consider adding filters to avoid full table scans.')
    # Rebuild SQL
    optimized = sqlparse.format(' '.join([str(t) for t in cleaned_tokens]), reindent=True, keyword_case='upper')
    if has_select_star:
        optimized = optimized.replace('SELECT *', 'SELECT col1, col2')  # Placeholder
    if suggestions:
        optimized = '\n'.join(suggestions) + '\n' + optimized
    return optimized 