# pricefinder
A nice selenium script to find price of a product through google and local search in webpages.


This scripts searches the HTML hierarchy from the point the name of the product was found and searches upward (goes to the parent element when not found) and terminates when it reaches the highest level (page level).
When a price tag is found, it is highlighted and a screenshot is saved as evidence.

