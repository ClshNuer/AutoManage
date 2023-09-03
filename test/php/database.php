<?php

// Load configuration file
require_once('config.php');
// define('DB_SERVER', '127.0.0.1');
// define('DB_USERNAME', 'root');
// define('DB_PASSWORD', '12345678');
// define('DB_NAME', 'userdb');

// Connect to database
function connect_to_database() {
    global $db_config;
    try {
        $link = new mysqli($db_config['server'], $db_config['username'], $db_config['password'], $db_config['dbname']);
        // $link = new mysqli($db_config['server'], $db_config['username'], $db_config['password']);
        if ($link->connect_error) {
            // Log error and return false
            error_log("Database connection failed: " . $link->connect_error);
            return false;
        }
        return $link;
    } catch (Exception $e) {
        // Log exception and return false
        error_log("Database connection failed: " . $e->getMessage());
        return false;
    }
}

// Close database connection
function close_database_connection($link) {
    $link->close();
}

// Create database
function create_database($link, $dbname) {
    $sql = "create database " . $dbname;
    if ($link->query($sql) === true) {
        echo "Database created successfully\n";
    } else {
        echo "Error creating database: " . $link->error . "\n";
    }
}

// Create table
function create_table($link, $dbname) {
    $sql = "create table users (
        id int(6) unsigned auto_increment primary key,
        firstname varchar(15),
        lastname varchar(15),
        email varchar(30)
        )";
    if ($link->query($sql) === true) {
        echo "Table created successfully\n";
    } else {
        echo "Error creating table: " . $link->error . "\n";
    }
}

// Insert data
function insert_data($link, $dbname, $firstname, $lastname, $email) {
    $sql = "insert into users (firstname, lastname, email)
        values ('$firstname', '$lastname', '$email')";
    if ($link->query($sql) === true) {
        echo "Insert data successfully\n";
    } else {
        echo "Error inserting data: " . $link->error . "\n";
    }
}

// Select data
function select_data($link, $dbname) {
    $sql = "select * from users";
    // $sql = "delete from users where firstname = 'Jesus Patel'";
    $result = $link->query($sql);
    if ($result->num_rows > 0) {
        // Output data of each row
        while ($row = $result->fetch_assoc()) {
            echo "id: " . $row["id"] . " - Name: " . $row["firstname"] . " " . $row["lastname"] . " - Email: " . $row["email"] . "\n";
        }
    } else {
        echo "0 results\n";
    }
}

// Main program
function main() {
    $link = connect_to_database(); // Connect to database
    if ($link) {
        echo "Database connection successful\n";
    } else {
        echo "Database connection failed\n";
    }

    create_database($link, DB_NAME); // Create database
    create_table($link, DB_NAME); // Create table
    insert_data($link, DB_NAME, "Jesus", "Patel", "example@gmail.com"); // Insert data

    close_database_connection($link); // Close database connection

}