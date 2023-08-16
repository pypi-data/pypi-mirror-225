from typing import Optional, Literal

def construct_url_with_filter(url: str, filter: dict, operator: Optional[Literal['and', 'or']] = 'and') -> str:
    filter_str = ''
    count = 0
    for field, requirement in filter.items():
        if requirement:
            if count == 0:
                filter_str = f'{field} {requirement}'
            else:
                filter_str = f'{filter_str} {operator} {field} {requirement}'

            count += 1
            
    return f'{url}?filter=({filter_str})' if filter_str != '' else url