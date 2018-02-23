# Multi-Collection Manager

This is a set of methods to work with data contained in multiple collections. There are a few principal techniques and approaches for doing so.

## Link referencing / dereferencing

The main data model employed here is a graph. A graph edge can be a reference (a literal value that serves as an address or locator for the object) or a "live link" in memory that will go directly to the object. This toolkit provides a mechanism to freeze and thaw graph data.

## Object mapping

There are two ways of looking at objects between collections. One is a simple link from one collection to another. The other is to create a correspondence between collections and perhaps also transformations for matching the data in one to the data in another.