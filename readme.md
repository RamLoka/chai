# Project: Chai (Chat + AI)

This repository contains the source code for the "Chai" command-line AI chat application, developed as part of the DBT230 course.

## Author

**Name:** [Tretin Brundige]

## Lab 1: Flat-File Persistence

This lab focuses on building the foundational persistence layer using a simple flat-file (JSON) system. The goal is to establish a performance baseline for file I/O operations, which will serve as a benchmark for subsequent labs involving more advanced database technologies.

# Questions

1. What are two different designs you contemplated for your multiple conversations implementation?
A- A single JSON file per user including all threads within.
A- A single JSON file per thread that included name by user and thread.

2. A vibe coder wants to make a quick MVP (minimum viable product) over the weekend that handles chat threads with AI models. Do you recommend using JSON files for persistence? Why?
A- Yes as its simple and quick to implement at the cost of its lack of scalability 

3. You are interviewing at OpenAI. The interviewer asks if you would use raw JSON files to store user chats or if you would use a database or other form of persistence and to explain your choice. How would you reply?
A- I would use a database to promote concurrency and performance. JSON is great as a prototype but do to its lack of scalability, JSON proves to be far slower when handling large amounts of data.

4. What did you notice about performance using this file storage method?
A- JSON can handle small conversations well but begins to slow down as messages grow to full read/write

# Questions

1. As conversations get longer, adding new messages to a flat file gets slower because the program has to rewrite the entire JSON file each time, so append times grow steadily. With MongoDB, adding messages is much faster since it can just update the existing document in place, keeping append times almost the same no matter how long the conversation is. Reading the full conversation shows a similar trend, flat files take longer as they grow, while MongoDB can quickly retrieve the document in its efficient binary format. These differences come down to how the two systems store dataflat files rewrite everything, whereas MongoDB manages data more intelligently with in-place updates and optimized storage.

2. In MongoDB, using $push to add a message is atomic, this means multiple messages can be added at the same time without  overwriting each other. This is  important in a chat app, where messages come in rapidly, as this maintains accurate conversations and keep them in the right order.

3. If your chat app suddenly went viral, with a million users each having 10 threads of 500 messages, the difference between FlatFileManager and MongoDBManager would be huge. FlatFileManager would have to dig through countless JSON files for every thread, which would slow things down as more users join, and managing millions of files could even hit system limits. Loading a conversation would take longer, especially if lots of users are chatting at the same time. MongoDBManager, on the other hand, can quickly find all threads for a user and pull up entire conversations thanks to its indexed queries. Its database handles storage efficiently and scales much better, making it a far smoother choice for a fast-growing, real-time chat app.

4. Embedded messages design:
Keeping all messages in one document makes it super fast to load a full conversation. Perfect for chat apps where users usually want to see the whole thread in one go.

Separate message documents design:
Saving each message individually makes it easier to handle really long conversations or to search and filter messages. It also prevents problems if a conversation grows too big.

When to use separate messages:
If your app has huge conversations, tons of messages, or you need to do things like search across all messages or analyze user activity, storing messages separately scales better and keeps everything manageable.
