<?php
// Define constants for the RSS feed URLs
define('GOOGLE_FEED_URL', 'http://news.google.com/news?ned=us&topic=h&output=rss');
define('MSNBC_FEED_URL', 'http://rss.msnbc.msn.com/id/3032091/device/rss/rss.xml');

// Get the selected feed from the query string
$selectedFeed = $_GET['q'];

// Define an array of valid feed options
$validFeeds = array(
    'google' => GOOGLE_FEED_URL,
    'msnbc' => MSNBC_FEED_URL
);

// Check if the selected feed is valid
if (!array_key_exists($selectedFeed, $validFeeds)) {
    echo 'Invalid feed selected';
    exit;
}

// Retrieve the XML data from the selected feed
try {
    $xmlData = file_get_contents($validFeeds[$selectedFeed]);
    $xmlDoc = new DOMDocument();
    if (!$xmlDoc->loadXML($xmlData)) {
        throw new Exception('Error parsing XML data');
    }
} catch (Exception $e) {
    echo 'Error retrieving or parsing XML data: ' . $e->getMessage();
    exit;
}

// Output the channel information
$channel = $xmlDoc->getElementsByTagName('channel')->item(0);
$channelTitle = $channel->getElementsByTagName('title')->item(0)->textContent;
$channelLink = $channel->getElementsByTagName('link')->item(0)->textContent;
$channelDesc = $channel->getElementsByTagName('description')->item(0)->textContent;

echo '<p><a href="' . $channelLink . '">' . $channelTitle . '</a></p>';
echo '<p>' . $channelDesc . '</p>';

// Output the item information
$items = $xmlDoc->getElementsByTagName('item');
$numItems = min($items->length, 3);
for ($i = 0; $i < $numItems; $i++) {
    $item = $items->item($i);
    $itemTitle = $item->getElementsByTagName('title')->item(0)->textContent;
    $itemLink = $item->getElementsByTagName('link')->item(0)->textContent;
    $itemDesc = $item->getElementsByTagName('description')->item(0)->textContent;

    echo '<p><a href="' . $itemLink . '">' . $itemTitle . '</a></p>';
    echo '<p>' . $itemDesc . '</p>';
}

/**
 * Retrieves the XML data from the specified URL and returns a DOMDocument object.
 *
 * @param string $url The URL of the XML data to retrieve.
 * @return DOMDocument The parsed XML data as a DOMDocument object.
 * @throws Exception If an error occurs while retrieving or parsing the XML data.
 */
function getXmlData($url) {
    $xmlData = file_get_contents($url);
    $xmlDoc = new DOMDocument();
    if (!$xmlDoc->loadXML($xmlData)) {
        throw new Exception('Error parsing XML data');
    }
    return $xmlDoc;
}