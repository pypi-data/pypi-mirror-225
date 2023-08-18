from src.sqlpiece.SQLPieceBPE.tokenizer import SQLPieceBPE

text = "SELECT name FROM students WHERE age > 10"
s = SQLPieceBPE()

encoding = s(text)
print(encoding)