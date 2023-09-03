<?php
/**
 * Parses an XML file and returns an array of parsed data.
 *
 * @param string $filename The name of the XML file to parse.
 * @return array An array of parsed data.
 * @throws Exception If an error occurs while parsing the XML file.
 */
function parseXmlFile($filename) {
    // Initialize the XML parser
    $parser = xml_parser_create();

    // Set the element handler functions
    xml_set_element_handler($parser, 'startElement', 'endElement');

    // Set the character data handler function
    xml_set_character_data_handler($parser, 'characterData');

    // Open the XML file
    $fp = fopen($filename, 'r');
    if (!$fp) {
        throw new Exception('Error opening XML file');
    }

    // Parse the XML data
    $data = '';
    while ($chunk = fread($fp, 4096)) {
        $data .= $chunk;
        if (!xml_parse($parser, $chunk, feof($fp))) {
            throw new Exception(sprintf('XML error: %s at line %d', xml_error_string(xml_get_error_code($parser)), xml_get_current_line_number($parser)));
        }
    }

    // Free the XML parser and close the file
    xml_parser_free($parser);
    fclose($fp);

    // Return the parsed data
    return $parsedData;
}

/**
 * Handles the start of an XML element.
 *
 * @param resource $parser The XML parser resource.
 * @param string $elementName The name of the element.
 * @param array $attributes An array of attributes for the element.
 */
function startElement($parser, $elementName, $attributes) {
    switch ($elementName) {
        case XML_NOTE:
            // Output a note element
            return '--note --';
        case XML_TO:
            // Output a to element
            return 'to';
        case XML_FROM:
            // Output a from element
            return 'from';
        case XML_HEADING:
            // Output a heading element
            return 'body';
        default:
            // Ignore other elements
            return '';
    }
}

/**
 * Handles the end of an XML element.
 *
 * @param resource $parser The XML parser resource.
 * @param string $elementName The name of the element.
 */
function endElement($parser, $elementName) {
    // Output a line break at the end of each element
    return '<br />';
}

/**
 * Handles character data within an XML element.
 *
 * @param resource $parser The XML parser resource.
 * @param string $data The character data.
 */
function characterData($parser, $data) {
    // Ignore character data
    return '';
}

// Define constants for XML element names
define('XML_NOTE', 'note');
define('XML_TO', 'to');
define('XML_FROM', 'from');
define('XML_HEADING', 'heading');

try {
    // Parse the XML file and output the parsed data
    $parsedData = parseXmlFile('1.txt');
    echo $parsedData;
} catch (Exception $e) {
    // Output an error message if an exception is thrown
    echo 'Error parsing XML file: ' . $e->getMessage();
}