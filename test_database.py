from database.db_manager import DatabaseManager

db = DatabaseManager()

generation_id = db.save_generation(
    task="Blog Writer",
    user_input="Write about Artificial Intelligence",
    generated_content="AI is transforming education.",
    tone="Professional",
    output_length="Short",
    latency=2.5,
    model="gemini-3.5-flash-lite"
)

print("Saved generation ID:", generation_id)

history = db.get_history()

for item in history:
    print(item["task"])
    print(item["generated_content"])