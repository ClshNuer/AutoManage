<?php

/**
 * MySQL Database class for connecting to and interacting with the database.
 */
class MySQLDatabase {
    private $pdo;

    /**
     * Constructor for creating a new database connection.
     *
     * @param string $host The database host.
     * @param string $username The database username.
     * @param string $password The database password.
     * @param string $dbname The database name.
     */
    public function __construct($host, $username, $password, $dbname) {
        try {
            $dsn = "mysql:host=$host;dbname=$dbname";
            $this->pdo = new PDO($dsn, $username, $password);
            $this->pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch (PDOException $e) {
            error_log("MySQL Database connection failed: " . $e->getMessage());
            throw $e;
        }
    }

    /**
     * Executes a SQL query and returns the result set.
     *
     * @param string $sql The SQL query to execute.
     * @param array $params The parameters to bind to the query.
     * @return array The result set.
     */
    public function query($sql, $params = []) {
        try {
            $stmt = $this->pdo->prepare($sql);
            $stmt->execute($params);
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (PDOException $e) {
            error_log("Query failed: " . $e->getMessage());
            throw $e;
        }
    }

    /**
     * Creates the database and table if they do not exist.
     */
    public function createDatabaseAndTable() {
        $this->createDatabase();
        $this->createTable();
    }

    /**
     * Creates the database if it does not exist.
     */
    private function createDatabase() {
        $sql = "CREATE DATABASE IF NOT EXISTS " . DB_NAME;
        $this->pdo->exec($sql);
    }

    /**
     * Creates the users table if it does not exist.
     */
    private function createTable() {
        $sql = "CREATE TABLE IF NOT EXISTS users (
            id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            firstname VARCHAR(15),
            lastname VARCHAR(15),
            email VARCHAR(30)
        )";
        $this->pdo->exec($sql);
    }

    /**
     * Closes the database connection.
     */
    public function close() {
        $this->pdo = null;
    }
}

/**
 * Oracle Database class for connecting to and interacting with the database.
 */
 class ODBCDatabase {
    private $conn;

    /**
     * Constructor for creating a new database connection.
     *
     * @param string $host The database host.
     * @param string $username The database username.
     * @param string $password The database password.
     * @param string $dbname The database name.
     */
    public function __construct($host, $username, $password, $dbname) {
        try {
            $this->conn = odbc_connect($dbname, $username, $password);
        } catch (PDOException $e) {
            error_log("ODBC Database connection failed: " . $e->getMessage());
            throw $e;
        }
    }

    /**
     * Executes a SQL query and returns the result set.
     *
     * @param string $sql The SQL query to execute.
     * @param array $params The parameters to bind to the query.
     * @return array The result set.
     */
    public function query($sql, $params = []) {
        try {
            $stmt = odbc_prepare($this->conn, $sql);
            odbc_execute($stmt, $params);
            return odbc_fetch_array($stmt);
        } catch (PDOException $e) {
            error_log("Query failed: " . $e->getMessage());
            throw $e;
        }
    }

    /**
     * Creates the database and table if they do not exist.
     */
    public function createDatabaseAndTable() {
        $this->createDatabase();
        $this->createTable();
    }

    /**
     * Creates the database if it does not exist.
     */
    private function createDatabase() {
        $sql = "CREATE DATABASE IF NOT EXISTS " . DB_NAME;
        odbc_exec($this->conn, $sql);
    }

    /**
     * Creates the users table if it does not exist.
     */
    private function createTable() {
        $sql = "CREATE TABLE IF NOT EXISTS users (
            id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            firstname VARCHAR(15),
            lastname VARCHAR(15),
            email VARCHAR(30)
        )";
        odbc_exec($this->conn, $sql);
    }

    /**
     * Closes the database connection.
     */
    public function close() {
        odbc_close($this->conn);
    }
 }

// Load configuration file
require_once('config.php');

// Create new database connection
try {
    $db = new MySQLDatabase($db_config['server'], $db_config['username'], $db_config['password'], $db_config['dbname']);
    echo "MySQL Database connection successful\n";

    // Create database and table if they do not exist
    $db->createDatabaseAndTable();

    // Close database connection
    $db->close();
} catch (PDOException $e) {
    echo "MySQL Database connection failed\n";
}