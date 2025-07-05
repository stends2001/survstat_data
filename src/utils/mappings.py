from .germany_harm import harmfile_germany_geography

map_countynames_germany_de_eng = dict(zip(harmfile_germany_geography.df["kreis_name_de"], harmfile_germany_geography.df["kreis_name_eng"]))

map_countynames_germany_eng_de = dict(zip(harmfile_germany_geography.df["kreis_name_eng"], harmfile_germany_geography.df["kreis_name_de"]))

map_tokens_countynames_germany = dict(zip(harmfile_germany_geography.df["kreis_token"], harmfile_germany_geography.df["kreis_name_eng"]))

map_countynames_tokens_germany = dict(zip(harmfile_germany_geography.df["kreis_name_de"], harmfile_germany_geography.df["kreis_token"]))