import requests
import pika
import json
from sqlalchemy.orm import Session
import database, models

def callback(ch, method, body):
    message = json.loads(body)
    print(f"Received message: {message}")

    try:
        action, book_id = message.split(": ")
        book_id = int(book_id)
    except ValueError:
        print("Error: Invalid message format")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    db: Session = database.SessionLocal()

    try:
        if action == "Book added":
            # Fetch book details from the Backend API
            backend_api_url = f"http://localhost:8081/books/{book_id}"
            response = requests.get(backend_api_url)

            if response.status_code == 200:
                book_data = response.json()
                # Add the book to the Frontend database
                new_book = models.Book(
                    id=book_data["id"],
                    title=book_data["title"],
                    author=book_data["author"],
                    publisher=book_data["publisher"],
                    category=book_data["category"],
                    is_available=True
                )
                db.add(new_book)
                db.commit()
                print(f"Book {book_id} added to the Frontend database.")
            else:
                print(f"Error fetching book details: {response.status_code}")

        elif action == "Book removed":
            # Remove the book from the Frontend database
            db.query(models.Book).filter(models.Book.id == book_id).delete()
            db.commit()
            print(f"Book {book_id} removed from the Frontend database.")

    except Exception as e:
        print(f"Error processing message: {e}")

    finally:
        db.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='book_updates', durable=True)
    channel.basic_consume(queue='book_updates', on_message_callback=callback)
    
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

