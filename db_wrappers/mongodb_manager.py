import time
from db_wrappers.flat_file_manager import FlatFileManager

def main():
    print("Welcome to Chai!")
    user_id = input("Please enter your user ID to begin: ")

    db_manager = FlatFileManager(storage_dir="data")

    threads = db_manager.list_user_threads(user_id)

    if threads:
        print("Existing threads:")
        for i, t in enumerate(threads, start=1):
            print(f"{i}. {t}")
        print(f"{len(threads)+1}. Start a new thread")

        choice = input("Select a thread number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(threads):
            conversation_id = threads[int(choice) - 1]
        else:
            conversation_id = input("Enter a name for your new thread: ")
    else:
        conversation_id = input("No threads found. Enter a name for your new thread: ")

    run_chat(db_manager, user_id, conversation_id)


def run_chat(db_manager: FlatFileManager, user_id: str, conversation_id: str):
    start_time = time.time()
    messages = db_manager.get_conversation(conversation_id)
    end_time = time.time()
    duration = end_time - start_time

    if messages:
        print("Previous conversation:")
        for msg in messages:
            print(f"{msg['role'].capitalize()}: {msg['content']}")
        print(f"(Load time: {duration:.4f} seconds)")

    print(f"Conversation: '{conversation_id}'. Type 'exit' to quit.")

    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        start_time = time.perf_counter()

        messages.append({"role": "user", "content": user_input})

        ai_response = "This is a mock response from the AI."
        messages.append({"role": "assistant", "content": ai_response})

        relative_filepath = f"{user_id}_{conversation_id}.json"
        db_manager.save_conversation(f"{user_id}_{conversation_id}", relative_filepath, messages)

        end_time = time.perf_counter()
        duration = end_time - start_time

        print(f"AI: {ai_response}")
        print(f"(Operation took {duration:.4f} seconds)\n")


if __name__ == "__main__":
    main()
