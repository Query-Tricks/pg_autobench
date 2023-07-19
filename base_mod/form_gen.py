def draw_table(data):
    edge        = ' '
    wall        = '|'
    line        = '='
    line_inside = ' '
    # Find the maximum width of the columns
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*data)]
    # Create a horizontal separator
    separator = f'{edge}'.join(f'{line}' * (width + 2) for width in col_widths)
    # Print the table
    print(f'{edge}' + separator + f'{edge}')
    for i, row in enumerate(data):
        print(f'{wall} ' + f' {wall} '.join(str(cell).ljust(width) for cell, width in zip(row, col_widths)) + f' {wall}')
        if i < len(data) - 1:
            if i == 0:
                print(f'{edge}' + separator + f'{edge}')
            else:
                print(f'{edge} ' + f' {edge} '.join(f'{line_inside}' * width for width in col_widths) + f' {edge}')
    print(f'{edge}' + separator + f'{edge}')

t = [
    ['hello', 'test','t'],
    ['hi','ttt','ttt'],
    ['by','111','123123'],
    ['','tfges','tes']
]

draw_table(t)
