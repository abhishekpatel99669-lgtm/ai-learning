import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
text="Hey there! my name is abhishek patel"
tokens = enc.encode(text)
# Tokens: [25216, 1354, 0, 922, 1308, 382, 692, 38520, 53420, 2506, 296]
print("Tokens:", tokens)

decoded = enc.decode( [25216, 1354, 0, 922, 1308, 382, 692, 38520, 53420, 2506, 296,1243])

print("Decoded:", decoded)
