BEGIN;
CREATE TABLE `books_publisher` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(30) NOT NULL,
    `address` varchar(50) NOT NULL,
    `city` varchar(60) NOT NULL,
    `state_province` varchar(30) NOT NULL,
    `country` varchar(50) NOT NULL,
    `website` varchar(200) NOT NULL
)
;
CREATE TABLE `books_author` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `first_name` varchar(30) NOT NULL,
    `last_name` varchar(40) NOT NULL,
    `email` varchar(75) NOT NULL
)
;
CREATE TABLE `books_book_authors` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `book_id` integer NOT NULL,
    `author_id` integer NOT NULL,
    UNIQUE (`book_id`, `author_id`)
)
;
ALTER TABLE `books_book_authors` ADD CONSTRAINT `author_id_refs_id_9e7e386` FOREIGN KEY (`author_id`) REFERENCES `books_author` (`id`);
CREATE TABLE `books_book` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `title` varchar(100) NOT NULL,
    `publisher_id` integer NOT NULL,
    `publication_date` date NOT NULL
)
;
ALTER TABLE `books_book` ADD CONSTRAINT `publisher_id_refs_id_c5b274bb` FOREIGN KEY (`publisher_id`) REFERENCES `books_publisher` (`id`);
ALTER TABLE `books_book_authors` ADD CONSTRAINT `book_id_refs_id_cfbcf262` FOREIGN KEY (`book_id`) REFERENCES `books_book` (`id`);
CREATE INDEX `books_book_22dd9c39` ON `books_book` (`publisher_id`);
COMMIT;
