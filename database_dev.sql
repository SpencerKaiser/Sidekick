CREATE DATABASE IF NOT EXISTS `sidekick_dev`;
CREATE USER 'sidekick'@'localhost' IDENTIFIED BY 'halpme';
GRANT ALL PRIVILEGES ON `sidekick_dev`. * TO 'sidekick'@'localhost';