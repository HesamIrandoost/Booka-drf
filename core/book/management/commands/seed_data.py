import random

from faker import Faker

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from book.models import Author, Book, Genre, Review, Collection

fake = Faker()


class Command(BaseCommand):
    help = "Seed BookIMDb with realistic book data"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # ==========================================================
        # Clear old data
        # ==========================================================

        self.stdout.write("Clearing old data...")

        Review.objects.all().delete()
        Collection.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        Genre.objects.all().delete()

        User.objects.exclude(is_superuser=True).delete()

        # ==========================================================
        # Users
        # ==========================================================

        users = []

        for _ in range(20):
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                password="Test12345",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )

            users.append(user)

        self.stdout.write(self.style.SUCCESS("20 users created."))

        # ==========================================================
        # Genres
        # ==========================================================

        genre_data = [
            ("Fantasy", "Fantasy and magical stories."),
            ("Science Fiction", "Stories about science, technology and the future."),
            ("Mystery", "Stories centered around solving mysterious events."),
            ("Thriller", "Suspenseful and exciting stories."),
            ("Romance", "Stories focused on romantic relationships."),
            ("Historical Fiction", "Fictional stories set in historical periods."),
            ("Horror", "Stories designed to create fear and suspense."),
            ("Adventure", "Stories involving exploration and exciting journeys."),
            ("Classic", "Important and influential works of literature."),
            ("Dystopian", "Stories about oppressive or imagined future societies."),
            ("Philosophy", "Books dealing with philosophical questions and ideas."),
            (
                "Young Adult",
                "Literature primarily written for teenage and young adult readers.",
            ),
        ]

        genres = {}

        for name, description in genre_data:
            genre = Genre.objects.create(
                name=name,
                description=description,
            )

            genres[name] = genre

        self.stdout.write(self.style.SUCCESS(f"{len(genres)} genres created."))

        # ==========================================================
        # Books
        # ==========================================================

        books_data = [
            # ------------------------------------------------------
            # George Orwell
            # ------------------------------------------------------
            {
                "author": ("George", "Orwell", "1903-06-25", "Motihari, India"),
                "title": "1984",
                "publisher": "Secker & Warburg",
                "published_date": "1949-06-08",
                "pages": 328,
                "genres": ["Dystopian", "Classic"],
            },
            {
                "author": ("George", "Orwell", "1903-06-25", "Motihari, India"),
                "title": "Animal Farm",
                "publisher": "Secker & Warburg",
                "published_date": "1945-08-17",
                "pages": 112,
                "genres": ["Dystopian", "Classic"],
            },
            # ------------------------------------------------------
            # J.R.R. Tolkien
            # ------------------------------------------------------
            {
                "author": (
                    "J.R.R.",
                    "Tolkien",
                    "1892-01-03",
                    "Bloemfontein, South Africa",
                ),
                "title": "The Hobbit",
                "publisher": "George Allen & Unwin",
                "published_date": "1937-09-21",
                "pages": 310,
                "genres": ["Fantasy", "Adventure", "Classic"],
            },
            {
                "author": (
                    "J.R.R.",
                    "Tolkien",
                    "1892-01-03",
                    "Bloemfontein, South Africa",
                ),
                "title": "The Fellowship of the Ring",
                "publisher": "George Allen & Unwin",
                "published_date": "1954-07-29",
                "pages": 423,
                "genres": ["Fantasy", "Adventure", "Classic"],
            },
            {
                "author": (
                    "J.R.R.",
                    "Tolkien",
                    "1892-01-03",
                    "Bloemfontein, South Africa",
                ),
                "title": "The Two Towers",
                "publisher": "George Allen & Unwin",
                "published_date": "1954-11-11",
                "pages": 352,
                "genres": ["Fantasy", "Adventure"],
            },
            {
                "author": (
                    "J.R.R.",
                    "Tolkien",
                    "1892-01-03",
                    "Bloemfontein, South Africa",
                ),
                "title": "The Return of the King",
                "publisher": "George Allen & Unwin",
                "published_date": "1955-10-20",
                "pages": 416,
                "genres": ["Fantasy", "Adventure", "Classic"],
            },
            # ------------------------------------------------------
            # Frank Herbert
            # ------------------------------------------------------
            {
                "author": ("Frank", "Herbert", "1920-10-08", "Tacoma, Washington, USA"),
                "title": "Dune",
                "publisher": "Chilton Company",
                "published_date": "1965-08-01",
                "pages": 412,
                "genres": ["Science Fiction", "Adventure", "Classic"],
            },
            {
                "author": ("Frank", "Herbert", "1920-10-08", "Tacoma, Washington, USA"),
                "title": "Dune Messiah",
                "publisher": "Putnam",
                "published_date": "1969-05-01",
                "pages": 256,
                "genres": ["Science Fiction", "Adventure"],
            },
            # ------------------------------------------------------
            # Jane Austen
            # ------------------------------------------------------
            {
                "author": (
                    "Jane",
                    "Austen",
                    "1775-12-16",
                    "Steventon, Hampshire, England",
                ),
                "title": "Pride and Prejudice",
                "publisher": "T. Egerton",
                "published_date": "1813-01-28",
                "pages": 432,
                "genres": ["Romance", "Classic"],
            },
            {
                "author": (
                    "Jane",
                    "Austen",
                    "1775-12-16",
                    "Steventon, Hampshire, England",
                ),
                "title": "Sense and Sensibility",
                "publisher": "Thomas Egerton",
                "published_date": "1811-10-30",
                "pages": 409,
                "genres": ["Romance", "Classic"],
            },
            # ------------------------------------------------------
            # F. Scott Fitzgerald
            # ------------------------------------------------------
            {
                "author": (
                    "F. Scott",
                    "Fitzgerald",
                    "1896-09-24",
                    "St. Paul, Minnesota, USA",
                ),
                "title": "The Great Gatsby",
                "publisher": "Charles Scribner's Sons",
                "published_date": "1925-04-10",
                "pages": 180,
                "genres": ["Classic", "Romance"],
            },
            # ------------------------------------------------------
            # J.K. Rowling
            # ------------------------------------------------------
            {
                "author": (
                    "J.K.",
                    "Rowling",
                    "1965-07-31",
                    "Yate, Gloucestershire, England",
                ),
                "title": "Harry Potter and the Philosopher's Stone",
                "publisher": "Bloomsbury",
                "published_date": "1997-06-26",
                "pages": 223,
                "genres": ["Fantasy", "Adventure", "Young Adult"],
            },
            {
                "author": (
                    "J.K.",
                    "Rowling",
                    "1965-07-31",
                    "Yate, Gloucestershire, England",
                ),
                "title": "Harry Potter and the Chamber of Secrets",
                "publisher": "Bloomsbury",
                "published_date": "1998-07-02",
                "pages": 251,
                "genres": ["Fantasy", "Adventure", "Young Adult"],
            },
            {
                "author": (
                    "J.K.",
                    "Rowling",
                    "1965-07-31",
                    "Yate, Gloucestershire, England",
                ),
                "title": "Harry Potter and the Prisoner of Azkaban",
                "publisher": "Bloomsbury",
                "published_date": "1999-07-08",
                "pages": 317,
                "genres": ["Fantasy", "Adventure", "Young Adult"],
            },
            {
                "author": (
                    "J.K.",
                    "Rowling",
                    "1965-07-31",
                    "Yate, Gloucestershire, England",
                ),
                "title": "Harry Potter and the Goblet of Fire",
                "publisher": "Bloomsbury",
                "published_date": "2000-07-08",
                "pages": 636,
                "genres": ["Fantasy", "Adventure", "Young Adult"],
            },
            # ------------------------------------------------------
            # Harper Lee
            # ------------------------------------------------------
            {
                "author": ("Harper", "Lee", "1926-04-28", "Monroeville, Alabama, USA"),
                "title": "To Kill a Mockingbird",
                "publisher": "J.B. Lippincott & Co.",
                "published_date": "1960-07-11",
                "pages": 281,
                "genres": ["Classic", "Historical Fiction"],
            },
            # ------------------------------------------------------
            # Leo Tolstoy
            # ------------------------------------------------------
            {
                "author": ("Leo", "Tolstoy", "1828-09-09", "Yasnaya Polyana, Russia"),
                "title": "War and Peace",
                "publisher": "The Russian Messenger",
                "published_date": "1869-01-01",
                "pages": 1225,
                "genres": ["Classic", "Historical Fiction", "Romance"],
            },
            {
                "author": ("Leo", "Tolstoy", "1828-09-09", "Yasnaya Polyana, Russia"),
                "title": "Anna Karenina",
                "publisher": "The Russian Messenger",
                "published_date": "1878-01-01",
                "pages": 864,
                "genres": ["Classic", "Romance"],
            },
            # ------------------------------------------------------
            # Fyodor Dostoevsky
            # ------------------------------------------------------
            {
                "author": ("Fyodor", "Dostoevsky", "1821-11-11", "Moscow, Russia"),
                "title": "Crime and Punishment",
                "publisher": "The Russian Messenger",
                "published_date": "1866-01-01",
                "pages": 671,
                "genres": ["Classic", "Philosophy", "Mystery"],
            },
            {
                "author": ("Fyodor", "Dostoevsky", "1821-11-11", "Moscow, Russia"),
                "title": "The Brothers Karamazov",
                "publisher": "The Russian Messenger",
                "published_date": "1880-01-01",
                "pages": 796,
                "genres": ["Classic", "Philosophy"],
            },
            {
                "author": ("Fyodor", "Dostoevsky", "1821-11-11", "Moscow, Russia"),
                "title": "Notes from Underground",
                "publisher": "Epoch",
                "published_date": "1864-01-01",
                "pages": 136,
                "genres": ["Philosophy", "Classic"],
            },
            # ------------------------------------------------------
            # Aldous Huxley
            # ------------------------------------------------------
            {
                "author": (
                    "Aldous",
                    "Huxley",
                    "1894-07-26",
                    "Godalming, Surrey, England",
                ),
                "title": "Brave New World",
                "publisher": "Chatto & Windus",
                "published_date": "1932-01-01",
                "pages": 311,
                "genres": ["Dystopian", "Science Fiction", "Classic"],
            },
            # ------------------------------------------------------
            # Mary Shelley
            # ------------------------------------------------------
            {
                "author": ("Mary", "Shelley", "1797-08-30", "London, England"),
                "title": "Frankenstein",
                "publisher": "Lackington, Hughes",
                "published_date": "1818-01-01",
                "pages": 280,
                "genres": ["Horror", "Science Fiction", "Classic"],
            },
            # ------------------------------------------------------
            # Bram Stoker
            # ------------------------------------------------------
            {
                "author": ("Bram", "Stoker", "1847-11-08", "Clontarf, Dublin, Ireland"),
                "title": "Dracula",
                "publisher": "Archibald Constable",
                "published_date": "1897-05-26",
                "pages": 418,
                "genres": ["Horror", "Classic", "Mystery"],
            },
            # ------------------------------------------------------
            # Gabriel García Márquez
            # ------------------------------------------------------
            {
                "author": (
                    "Gabriel García",
                    "Márquez",
                    "1927-03-06",
                    "Aracataca, Colombia",
                ),
                "title": "One Hundred Years of Solitude",
                "publisher": "Harper & Row",
                "published_date": "1967-05-30",
                "pages": 417,
                "genres": ["Classic", "Historical Fiction"],
            },
            {
                "author": (
                    "Gabriel García",
                    "Márquez",
                    "1927-03-06",
                    "Aracataca, Colombia",
                ),
                "title": "Love in the Time of Cholera",
                "publisher": "Penguin",
                "published_date": "1985-01-01",
                "pages": 368,
                "genres": ["Romance", "Classic"],
            },
            # ------------------------------------------------------
            # Paulo Coelho
            # ------------------------------------------------------
            {
                "author": ("Paulo", "Coelho", "1947-08-24", "Rio de Janeiro, Brazil"),
                "title": "The Alchemist",
                "publisher": "HarperCollins",
                "published_date": "1988-01-01",
                "pages": 208,
                "genres": ["Adventure", "Philosophy"],
            },
            # ------------------------------------------------------
            # Hermann Hesse
            # ------------------------------------------------------
            {
                "author": ("Hermann", "Hesse", "1877-07-02", "Calw, Germany"),
                "title": "Siddhartha",
                "publisher": "S. Fischer Verlag",
                "published_date": "1922-01-01",
                "pages": 152,
                "genres": ["Philosophy", "Classic"],
            },
            {
                "author": ("Hermann", "Hesse", "1877-07-02", "Calw, Germany"),
                "title": "Steppenwolf",
                "publisher": "S. Fischer Verlag",
                "published_date": "1927-01-01",
                "pages": 237,
                "genres": ["Philosophy", "Classic"],
            },
            # ------------------------------------------------------
            # Victor Hugo
            # ------------------------------------------------------
            {
                "author": ("Victor", "Hugo", "1802-02-26", "Besançon, France"),
                "title": "Les Misérables",
                "publisher": "A. Lacroix",
                "published_date": "1862-01-01",
                "pages": 1463,
                "genres": ["Classic", "Historical Fiction", "Romance"],
            },
            # ------------------------------------------------------
            # Charles Dickens
            # ------------------------------------------------------
            {
                "author": ("Charles", "Dickens", "1812-02-07", "Portsmouth, England"),
                "title": "Oliver Twist",
                "publisher": "Richard Bentley",
                "published_date": "1838-01-01",
                "pages": 608,
                "genres": ["Classic", "Historical Fiction"],
            },
            {
                "author": ("Charles", "Dickens", "1812-02-07", "Portsmouth, England"),
                "title": "A Christmas Carol",
                "publisher": "Chapman & Hall",
                "published_date": "1843-12-19",
                "pages": 104,
                "genres": ["Classic"],
            },
            # ------------------------------------------------------
            # Mark Twain
            # ------------------------------------------------------
            {
                "author": ("Mark", "Twain", "1835-11-30", "Florida, Missouri, USA"),
                "title": "The Adventures of Tom Sawyer",
                "publisher": "American Publishing Company",
                "published_date": "1876-01-01",
                "pages": 274,
                "genres": ["Adventure", "Classic"],
            },
            {
                "author": ("Mark", "Twain", "1835-11-30", "Florida, Missouri, USA"),
                "title": "Adventures of Huckleberry Finn",
                "publisher": "Charles L. Webster",
                "published_date": "1884-12-10",
                "pages": 366,
                "genres": ["Adventure", "Classic"],
            },
            # ------------------------------------------------------
            # William Shakespeare
            # ------------------------------------------------------
            {
                "author": (
                    "William",
                    "Shakespeare",
                    "1564-04-26",
                    "Stratford-upon-Avon, England",
                ),
                "title": "Hamlet",
                "publisher": "Various",
                "published_date": "1603-01-01",
                "pages": 342,
                "genres": ["Classic", "Romance"],
            },
            {
                "author": (
                    "William",
                    "Shakespeare",
                    "1564-04-26",
                    "Stratford-upon-Avon, England",
                ),
                "title": "Romeo and Juliet",
                "publisher": "Various",
                "published_date": "1597-01-01",
                "pages": 288,
                "genres": ["Romance", "Classic"],
            },
            {
                "author": (
                    "William",
                    "Shakespeare",
                    "1564-04-26",
                    "Stratford-upon-Avon, England",
                ),
                "title": "Macbeth",
                "publisher": "Various",
                "published_date": "1623-01-01",
                "pages": 249,
                "genres": ["Classic", "Mystery"],
            },
            # ------------------------------------------------------
            # Albert Camus
            # ------------------------------------------------------
            {
                "author": ("Albert", "Camus", "1913-11-07", "Dréan, Algeria"),
                "title": "The Stranger",
                "publisher": "Gallimard",
                "published_date": "1942-01-01",
                "pages": 123,
                "genres": ["Philosophy", "Classic"],
            },
            {
                "author": ("Albert", "Camus", "1913-11-07", "Dréan, Algeria"),
                "title": "The Plague",
                "publisher": "Gallimard",
                "published_date": "1947-01-01",
                "pages": 308,
                "genres": ["Philosophy", "Classic"],
            },
            # ------------------------------------------------------
            # Franz Kafka
            # ------------------------------------------------------
            {
                "author": ("Franz", "Kafka", "1883-07-03", "Prague, Czech Republic"),
                "title": "The Metamorphosis",
                "publisher": "Kurt Wolff Verlag",
                "published_date": "1915-01-01",
                "pages": 96,
                "genres": ["Classic", "Philosophy"],
            },
            {
                "author": ("Franz", "Kafka", "1883-07-03", "Prague, Czech Republic"),
                "title": "The Trial",
                "publisher": "Verlag Die Schmiede",
                "published_date": "1925-01-01",
                "pages": 255,
                "genres": ["Mystery", "Philosophy", "Classic"],
            },
            # ------------------------------------------------------
            # Oscar Wilde
            # ------------------------------------------------------
            {
                "author": ("Oscar", "Wilde", "1854-10-16", "Dublin, Ireland"),
                "title": "The Picture of Dorian Gray",
                "publisher": "Ward Lock",
                "published_date": "1890-06-20",
                "pages": 254,
                "genres": ["Classic", "Horror", "Philosophy"],
            },
            # ------------------------------------------------------
            # Bram Stoker / Horror
            # ------------------------------------------------------
            {
                "author": (
                    "H.P.",
                    "Lovecraft",
                    "1890-08-20",
                    "Providence, Rhode Island, USA",
                ),
                "title": "The Call of Cthulhu",
                "publisher": "Weird Tales",
                "published_date": "1928-02-01",
                "pages": 38,
                "genres": ["Horror", "Mystery"],
            },
            # ------------------------------------------------------
            # Ray Bradbury
            # ------------------------------------------------------
            {
                "author": ("Ray", "Bradbury", "1920-08-22", "Waukegan, Illinois, USA"),
                "title": "Fahrenheit 451",
                "publisher": "Ballantine Books",
                "published_date": "1953-10-19",
                "pages": 249,
                "genres": ["Dystopian", "Science Fiction", "Classic"],
            },
            # ------------------------------------------------------
            # Margaret Atwood
            # ------------------------------------------------------
            {
                "author": ("Margaret", "Atwood", "1939-11-18", "Ottawa, Canada"),
                "title": "The Handmaid's Tale",
                "publisher": "McClelland and Stewart",
                "published_date": "1985-01-01",
                "pages": 311,
                "genres": ["Dystopian", "Science Fiction"],
            },
            # ------------------------------------------------------
            # Suzanne Collins
            # ------------------------------------------------------
            {
                "author": (
                    "Suzanne",
                    "Collins",
                    "1962-08-10",
                    "Hartford, Connecticut, USA",
                ),
                "title": "The Hunger Games",
                "publisher": "Scholastic",
                "published_date": "2008-09-14",
                "pages": 374,
                "genres": ["Dystopian", "Young Adult", "Adventure"],
            },
            {
                "author": (
                    "Suzanne",
                    "Collins",
                    "1962-08-10",
                    "Hartford, Connecticut, USA",
                ),
                "title": "Catching Fire",
                "publisher": "Scholastic",
                "published_date": "2009-09-01",
                "pages": 391,
                "genres": ["Dystopian", "Young Adult", "Adventure"],
            },
            # ------------------------------------------------------
            # Dan Brown
            # ------------------------------------------------------
            {
                "author": ("Dan", "Brown", "1964-06-22", "Exeter, New Hampshire, USA"),
                "title": "The Da Vinci Code",
                "publisher": "Doubleday",
                "published_date": "2003-03-18",
                "pages": 489,
                "genres": ["Mystery", "Thriller", "Adventure"],
            },
            # ------------------------------------------------------
            # Stephen King
            # ------------------------------------------------------
            {
                "author": ("Stephen", "King", "1947-09-21", "Portland, Maine, USA"),
                "title": "The Shining",
                "publisher": "Doubleday",
                "published_date": "1977-01-28",
                "pages": 447,
                "genres": ["Horror", "Thriller"],
            },
            {
                "author": ("Stephen", "King", "1947-09-21", "Portland, Maine, USA"),
                "title": "It",
                "publisher": "Viking",
                "published_date": "1986-09-15",
                "pages": 1138,
                "genres": ["Horror", "Thriller"],
            },
            # ------------------------------------------------------
            # John Steinbeck
            # ------------------------------------------------------
            {
                "author": (
                    "John",
                    "Steinbeck",
                    "1902-02-27",
                    "Salinas, California, USA",
                ),
                "title": "The Grapes of Wrath",
                "publisher": "The Viking Press",
                "published_date": "1939-04-14",
                "pages": 464,
                "genres": ["Classic", "Historical Fiction"],
            },
            {
                "author": (
                    "John",
                    "Steinbeck",
                    "1902-02-27",
                    "Salinas, California, USA",
                ),
                "title": "Of Mice and Men",
                "publisher": "Covici Friede",
                "published_date": "1937-02-06",
                "pages": 107,
                "genres": ["Classic", "Historical Fiction"],
            },
            # ------------------------------------------------------
            # Ernest Hemingway
            # ------------------------------------------------------
            {
                "author": (
                    "Ernest",
                    "Hemingway",
                    "1899-07-21",
                    "Oak Park, Illinois, USA",
                ),
                "title": "The Old Man and the Sea",
                "publisher": "Charles Scribner's Sons",
                "published_date": "1952-09-01",
                "pages": 127,
                "genres": ["Classic", "Adventure"],
            },
            # ------------------------------------------------------
            # Miguel de Cervantes
            # ------------------------------------------------------
            {
                "author": (
                    "Miguel de Cervantes",
                    "Saavedra",
                    "1547-09-29",
                    "Alcalá de Henares, Spain",
                ),
                "title": "Don Quixote",
                "publisher": "Francisco de Robles",
                "published_date": "1605-01-16",
                "pages": 863,
                "genres": ["Adventure", "Classic"],
            },
        ]

        # ==========================================================
        # Create Authors + Books
        # ==========================================================

        authors = {}
        books = []

        for data in books_data:

            first_name, last_name, date_born, place_born = data["author"]

            author_key = (first_name, last_name)

            if author_key not in authors:

                author = Author.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    biography=fake.paragraph(nb_sentences=10),
                    date_born=date_born,
                    place_born=place_born,
                    website=f"https://{fake.domain_name()}",
                )

                authors[author_key] = author

            else:
                author = authors[author_key]

            book = Book.objects.create(
                author=author,
                title=data["title"],
                about=fake.paragraph(nb_sentences=5),
                summary=fake.paragraph(nb_sentences=8),
                pages=data["pages"],
                publisher=data["publisher"],
                published_date=data["published_date"],
            )

            book.genres.set(genres[genre_name] for genre_name in data["genres"])

            books.append(book)

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(authors)} authors and {len(books)} books created."
            )
        )

        # ==========================================================
        # Reviews
        # ==========================================================

        review_subjects = [
            "Absolutely loved it",
            "A memorable reading experience",
            "One of my favorite books",
            "Really interesting",
            "Worth reading",
            "A powerful story",
            "Beautifully written",
            "Not what I expected",
            "A fascinating book",
            "Highly recommended",
            "A book I will remember",
            "Surprisingly good",
            "An unforgettable story",
            "Definitely worth reading",
        ]

        review_texts = [
            "The story was engaging from beginning to end.",
            "I really enjoyed the characters and the writing style.",
            "This book gave me a lot to think about.",
            "The world building was impressive and memorable.",
            "Some parts were slow, but overall I enjoyed the experience.",
            "The themes of this book are still relevant today.",
            "I would definitely recommend this book to other readers.",
            "The characters felt surprisingly realistic.",
            "The writing style made the story very immersive.",
            "The ending stayed in my mind for a long time.",
            "I enjoyed the atmosphere and the development of the story.",
            "There were some weak parts, but the overall experience was great.",
        ]

        reviews = []

        # 300 root reviews

        for _ in range(300):

            user = random.choice(users)
            book = random.choice(books)

            review = Review.objects.create(
                user=user,
                book=book,
                subject=random.choice(review_subjects),
                text=random.choice(review_texts),
                likes=random.randint(0, 150),
                star=random.randint(1, 5),
                status=True,
            )

            reviews.append(review)

        # ==========================================================
        # Replies
        # ==========================================================

        reply_texts = [
            "I completely agree with you.",
            "I had a similar experience.",
            "Interesting point!",
            "I actually felt the opposite.",
            "This is exactly what I thought.",
            "Thanks for sharing your opinion.",
            "I might give this book another try.",
            "The ending was my favorite part too.",
            "I noticed the same thing.",
            "That's an interesting interpretation.",
        ]

        replies = []

        # Around 40% of reviews receive a reply

        reply_count = int(len(reviews) * 0.4)

        for review in random.sample(reviews, k=reply_count):

            reply = Review.objects.create(
                user=random.choice(users),
                book=review.book,
                subject="Reply",
                text=random.choice(reply_texts),
                likes=random.randint(0, 50),
                parent=review,
                star=0,
                status=True,
            )

            replies.append(reply)

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(reviews)} reviews and {len(replies)} replies created."
            )
        )

        # ==========================================================
        # Update Book ratings
        # ==========================================================

            # for book in books:
            #     book.update_star()

            # self.stdout.write(self.style.SUCCESS("Book ratings calculated."))

        # ==========================================================
        # Collections
        # ==========================================================

        collection_names = [
            "My Favorite Books",
            "Books I Want to Read",
            "Best Classics",
            "My Favorite Fantasy Books",
            "Books Everyone Should Read",
            "My Weekend Reading",
            "Books That Changed My Perspective",
            "My All-Time Favorites",
            "Books Worth Recommending",
            "My Personal Library",
        ]

        collections = []

        for user in users:

            for _ in range(random.randint(2, 4)):

                collection = Collection.objects.create(
                    user=user,
                    title=random.choice(collection_names),
                    description=fake.paragraph(nb_sentences=3),
                    is_public=random.choice([True, True, True, False]),
                )

                collection.books.set(
                    random.sample(
                        books,
                        random.randint(3, min(10, len(books))),
                    )
                )

                collections.append(collection)

        self.stdout.write(
            self.style.SUCCESS(f"{len(collections)} collections created.")
        )

        # ==========================================================
        # Done
        # ==========================================================

        self.stdout.write(
            self.style.SUCCESS("\nBookIMDb database seeded successfully!")
        )
