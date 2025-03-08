import pandas as pd

def load_tsv(filename, usecols=None):
    print(f'Carregando {filename}...')
    return pd.read_csv(filename, sep='\t', usecols=usecols, dtype=str, na_values=['\\N']).fillna('')

def save_tsv(df, filename):
    print(f'Salvando {filename}...')
    df.to_csv(filename, sep='\t', index=False)

# Carregar um subconjunto do title.basics
print('Processando title.basics...')
title_basics = load_tsv('title.basics.tsv')
title_basics_sample = title_basics.sample(n=300, random_state=42)
save_tsv(title_basics_sample, 'filtered_title.basics.tsv')

# Obter os tconst filtrados
title_ids = set(title_basics_sample['tconst'])

def filter_by_title_id(filename, column_name):
    print(f'Filtrando {filename}...')
    df = load_tsv(filename)
    filtered_df = df[df[column_name].isin(title_ids)]
    save_tsv(filtered_df, f'filtered_{filename}')
    return filtered_df

# Filtrar e salvar os outros arquivos com base nos tconst
print('Filtrando title.crew...')
title_crew_filtered = filter_by_title_id('title.crew.tsv', 'tconst')

print('Filtrando title.principals...')
title_principals_filtered = filter_by_title_id('title.principals.tsv', 'tconst')

print('Filtrando title.ratings...')
title_ratings_filtered = filter_by_title_id('title.ratings.tsv', 'tconst')

# Filtrar name.basics apenas com os nomes que aparecem nos arquivos processados
print('Filtrando name.basics...')
people_ids = set(title_crew_filtered['directors']).union(
    set(title_crew_filtered['writers']),
    set(title_principals_filtered['nconst'])
)
name_basics = load_tsv('name.basics.tsv')
name_basics_filtered = name_basics[name_basics['nconst'].isin(people_ids)]
save_tsv(name_basics_filtered, 'filtered_name.basics.tsv')

print('Processamento concluído!')
