from tokenizer import SQLPieceBPE
from datasets import load_from_disk
from tqdm import tqdm

s = SQLPieceBPE()
# s('select * from table where a = 1 and b = 2')
dataset = load_from_disk('/home/hj36wegi/scratch/data/dedup')
all_sql = []

for i,d in tqdm(enumerate(dataset)):
    batch_outputs = s(d['spans'],truncation=True,padding='max_length',max_length=512,return_tensors='pt')
    sql = s.convert_ids_to_tokens(batch_outputs['input_ids'].squeeze()[~batch_outputs['token_type_ids'].squeeze().bool()],skip_special_tokens=True)
    all_sql.append(sql)

    assert batch_outputs['input_ids'].shape[1] == batch_outputs['token_type_ids'].shape[1] == 512

    if i == 1000:
        break

flatten = lambda l: [item for sublist in l for item in sublist]

all_sql = [i.upper() for i in flatten(all_sql)]
print(set(all_sql).difference(s.sql_vocab))