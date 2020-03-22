import csv

def pick_email(file):
    with open(file, 'r', encoding='utf-8') as f:
        file = list(csv.reader(f))
        lines = filter(lambda line: len(line)>1, file)
        return list(map(lambda e: e[:2], lines))

def write_rows(rows, new_file):
    with open(new_file, 'w', encoding='utf-8', newline='\n') as f:
        csv.writer(f).writerows(rows)
        #f.writelines(map(lambda r: r + '\n', rows))

if __name__ == '__main__':
    write_rows(pick_email('emails_fr.csv'), 'to_fr.csv')
    write_rows(pick_email('emails_foreign.csv'), 'to_foreign.csv')
